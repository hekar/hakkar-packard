import asyncio
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, Optional
from metrum.common.logger import logger
from metrum.settings import settings
from .log_reader import LogReader

class FileLogReader(LogReader):
    """PostgreSQL log reader for filesystem-based logs."""

    def __init__(self, logs_dir: Optional[Path] = None, pattern: Optional[str] = None):
        """Initialize the log reader.
        
        Args:
            logs_dir: Directory containing log files. Defaults to settings.logs_dir
            pattern: Log file pattern. Defaults to settings.log_pattern
        """
        self.logs_dir = (logs_dir or settings.logs_dir).absolute()
        self.pattern = pattern or settings.log_pattern
        logger.debug("initialized_log_reader", 
                    logs_dir=str(self.logs_dir),
                    pattern=self.pattern)

    def get_log_files(self) -> list[Path]:
        """Get all matching log files in the logs directory."""
        log_files = sorted(self.logs_dir.glob(self.pattern))
        logger.debug("found_log_files",
                    count=len(log_files),
                    files=[str(f) for f in log_files])
        return log_files

    async def tail(self, file: Path) -> AsyncGenerator[str, None]:
        """Tail a log file and yield new lines.
        
        Args:
            file: Path to the log file to tail
        
        Yields:
            New lines from the log file
        """
        logger.debug("starting_file_tail", file=str(file))
        with file.open() as f:
            # Seek to end of file
            f.seek(0, 2)
            current_position = f.tell()
            logger.debug("tail_initial_position", position=current_position)
            
            while True:
                line = f.readline()
                if not line:
                    await asyncio.sleep(0.1)  # Avoid busy waiting
                    continue
                logger.debug("tail_new_line", 
                           file=str(file),
                           line_length=len(line))
                yield line.rstrip()

    async def read_logs(
        self,
        follow: bool = False,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> AsyncGenerator[str, None]:
        """Read logs from all matching files.
        
        Args:
            follow: Whether to continuously follow log files for new entries
            start_time: Only return logs after this time
            end_time: Only return logs before this time
        
        Yields:
            Log lines matching the criteria
        """
        logger.debug("starting_log_read",
                    follow=follow,
                    start_time=start_time.isoformat() if start_time else None,
                    end_time=end_time.isoformat() if end_time else None)

        log_files = self.get_log_files()
        if not log_files:
            error_msg = f"No log files found matching {self.pattern} in {self.logs_dir}"
            logger.error("no_log_files_found", 
                        pattern=self.pattern,
                        directory=str(self.logs_dir))
            raise FileNotFoundError(error_msg)

        if follow:
            # When following, only tail the most recent log file
            latest_log = log_files[-1]
            logger.info("following_latest_log", file=str(latest_log))
            async for line in self.tail(latest_log):
                yield line
        else:
            # Read all matching files
            for log_file in log_files:
                logger.debug("reading_log_file", file=str(log_file))
                with log_file.open() as f:
                    for line in f:
                        # TODO: Parse timestamp and filter by start_time/end_time
                        logger.debug("read_line", 
                                   file=str(log_file),
                                   line_length=len(line))
                        yield line.rstrip() 