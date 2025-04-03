import asyncio
import click
from metrum.common.logger import logger
from metrum.logs import LogMonitor, LogReader
from metrum.settings import settings
from metrum.queries import PatternLoader
from pathlib import Path

@click.command()
@click.option('--from-beginning', is_flag=True, help='Process all log files from the beginning instead of just the latest one')
def run(from_beginning):
    """Run the Metrum service."""
    logger.info("starting_metrum_service")

    logs_directory = settings.logs_dir
    logger.debug("using_logs_directory", directory=str(logs_directory))
    
    reader = LogReader(logs_dir=logs_directory)
    log_files = reader.get_log_files()
    if not log_files:
        error_msg = f"Error: No log files found in {logs_directory}"
        logger.error("no_log_files_found", directory=str(logs_directory))
        click.echo(error_msg, err=True)
        return
    
    if from_beginning:
        # Process all log files from the beginning
        logger.info("processing_all_log_files", count=len(log_files))
        click.echo(f"Processing all log files ({len(log_files)} files)")
        
        pattern_loader = PatternLoader()
        pattern_config = pattern_loader.load_patterns()
        logger.debug("loaded_patterns", 
                    pattern_count=len(pattern_config.patterns),
                    patterns=list(pattern_config.patterns.keys()))
        
        for log_file in log_files:
            logger.info("processing_log_file", file=str(log_file))
            click.echo(f"Processing log file: {log_file}")
            
            monitor = LogMonitor(
                log_file_path=str(log_file),
                patterns=pattern_config.patterns,
                http_endpoint=settings.http_endpoint,
                db_url=settings.database_url,
                poll_interval=settings.poll_interval,
            )
            
            try:
                asyncio.run(monitor.run())
            except Exception as e:
                logger.error("file_processing_error", file=str(log_file), error=str(e), exc_info=True)
                click.echo(f"Error processing {log_file}: {e}", err=True)
    else:
        # Process only the latest log file (default behavior)
        latest_log = log_files[-1]
        logger.info("monitoring_log_file", file=str(latest_log))
        click.echo(f"Monitoring latest log file: {latest_log}")
        
        pattern_loader = PatternLoader()
        pattern_config = pattern_loader.load_patterns()
        logger.debug("loaded_patterns", 
                    pattern_count=len(pattern_config.patterns),
                    patterns=list(pattern_config.patterns.keys()))
        
        monitor = LogMonitor(
            log_file_path=str(latest_log),
            patterns=pattern_config.patterns,
            http_endpoint=settings.http_endpoint,
            db_url=settings.database_url,
            poll_interval=settings.poll_interval,
        )
        
        try:
            asyncio.run(monitor.run())
        except KeyboardInterrupt:
            logger.info("service_stopped_by_user")
        except Exception as e:
            logger.error("service_error", error=str(e), exc_info=True)
            raise 