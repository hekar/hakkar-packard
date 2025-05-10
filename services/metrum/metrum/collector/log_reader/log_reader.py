from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, Optional

class LogReader(ABC):
    """Interface for reading PostgreSQL logs from various sources."""
    
    @abstractmethod
    def get_log_files(self) -> list[Path]:
        pass

    @abstractmethod
    def tail(self, file: Path) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    def read_logs(
        self,
        follow: bool = False,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> AsyncGenerator[str, None]:
        """Read logs from the configured source.
        
        Args:
            follow: Whether to continuously follow logs for new entries
            start_time: Only return logs after this time
            end_time: Only return logs before this time
        
        Yields:
            Log lines matching the criteria
        """
        pass 
