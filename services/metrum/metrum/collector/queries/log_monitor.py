from metrum.common.logger import logger
from metrum.collector.log_reader import LogMonitor, create_log_reader
from metrum.settings import settings
from metrum.collector.queries import PatternLoader

class LogMonitorService:
    """Service for monitoring PostgreSQL logs and processing patterns."""
    
    def __init__(self, from_beginning: bool = False):
        self.from_beginning = from_beginning
        self.logs_directory = settings.logs_dir
        self.reader = create_log_reader(logs_dir=self.logs_directory)
        self.pattern_loader = PatternLoader()
    
    async def run(self):
        """Run the log monitoring service."""
        logger.info("starting_log_monitor_service")
        logger.debug("using_logs_directory", directory=str(self.logs_directory))
        
        log_files = self.reader.get_log_files()
        if not log_files:
            error_msg = f"Error: No log files found in {self.logs_directory}"
            logger.error("no_log_files_found", directory=str(self.logs_directory))
            raise RuntimeError(error_msg)
        
        pattern_config = self.pattern_loader.load_patterns()
        logger.debug("loaded_patterns", 
                    pattern_count=len(pattern_config.patterns),
                    patterns=list(pattern_config.patterns.keys()))
        
        if self.from_beginning:
            await self._process_all_logs(log_files, pattern_config)
        else:
            await self._process_latest_log(log_files, pattern_config)
    
    async def _process_all_logs(self, log_files, pattern_config):
        """Process all log files from the beginning."""
        logger.info("processing_all_log_files", count=len(log_files))
        
        for log_file in log_files:
            logger.info("processing_log_file", file=str(log_file))
            
            monitor = LogMonitor(
                log_file_path=str(log_file),
                patterns=pattern_config.patterns,
                http_endpoint=settings.http_endpoint,
                db_url=settings.database_url,
                poll_interval=settings.poll_interval,
            )
            
            try:
                await monitor.run()
            except Exception as e:
                logger.error("file_processing_error", file=str(log_file), error=str(e), exc_info=True)
                raise
    
    async def _process_latest_log(self, log_files, pattern_config):
        """Process only the latest log file."""
        latest_log = log_files[-1]
        logger.info("monitoring_log_file", file=str(latest_log))
        
        monitor = LogMonitor(
            log_file_path=str(latest_log),
            patterns=pattern_config.patterns,
            http_endpoint=settings.http_endpoint,
            db_url=settings.database_url,
            poll_interval=settings.poll_interval,
        )
        
        try:
            await monitor.run()
        except Exception as e:
            logger.error("service_error", error=str(e), exc_info=True)
            raise 