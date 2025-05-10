from pathlib import Path
from typing import Optional
from metrum.settings import settings
from .log_reader import LogReader
from .file_log_reader import FileLogReader

def create_log_reader(
    logs_dir: Optional[Path] = None,
    pattern: Optional[str] = None
) -> LogReader:
    """Create a LogReader implementation based on settings.
    
    Args:
        logs_dir: Optional override for logs directory
        pattern: Optional override for log file pattern
        
    Returns:
        A LogReader implementation appropriate for the configured log mode
        
    Raises:
        ValueError: If the configured log mode is not supported
    """
    if settings.log_mode == "file":
        return FileLogReader(logs_dir=logs_dir, pattern=pattern)
    else:
        raise ValueError(f"Unsupported log mode: {settings.log_mode}") 