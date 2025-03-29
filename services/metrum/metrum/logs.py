import asyncio
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, Optional

from .settings import settings


class LogReader:
    """PostgreSQL log reader for filesystem-based logs."""

    def __init__(self, logs_dir: Optional[Path] = None, pattern: Optional[str] = None):
        """Initialize the log reader.
        
        Args:
            logs_dir: Directory containing log files. Defaults to settings.logs_dir
            pattern: Log file pattern. Defaults to settings.log_pattern
        """
        self.logs_dir = logs_dir or settings.logs_dir
        self.pattern = pattern or settings.log_pattern

    def get_log_files(self) -> list[Path]:
        """Get all matching log files in the logs directory."""
        return sorted(self.logs_dir.glob(self.pattern))

    async def tail(self, file: Path) -> AsyncGenerator[str, None]:
        """Tail a log file and yield new lines.
        
        Args:
            file: Path to the log file to tail
        
        Yields:
            New lines from the log file
        """
        with file.open() as f:
            # Seek to end of file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    await asyncio.sleep(0.1)  # Avoid busy waiting
                    continue
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
        if settings.log_mode != "filesystem":
            raise ValueError(f"Log mode {settings.log_mode} not supported")

        log_files = self.get_log_files()
        if not log_files:
            raise FileNotFoundError(
                f"No log files found matching {self.pattern} in {self.logs_dir}"
            )

        if follow:
            # When following, only tail the most recent log file
            latest_log = log_files[-1]
            async for line in self.tail(latest_log):
                yield line
        else:
            # Read all matching files
            for log_file in log_files:
                with log_file.open() as f:
                    for line in f:
                        # TODO: Parse timestamp and filter by start_time/end_time
                        yield line.rstrip() 