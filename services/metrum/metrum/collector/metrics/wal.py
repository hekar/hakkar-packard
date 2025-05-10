from typing import Dict, List
from datetime import datetime
from .base import BaseMetricsCollector

class WALMetricsCollector(BaseMetricsCollector):
    """Collector for PostgreSQL WAL (Write-Ahead Logging) statistics."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_wal"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {"name": "wal_records", "description": "Total number of WAL records generated"},
            {"name": "wal_fpi", "description": "Total number of WAL full page images generated"},
            {"name": "wal_bytes", "description": "Total amount of WAL generated in bytes"},
            {"name": "wal_buffers_full", "description": "Number of times WAL data was written to disk because WAL buffers became full"},
            {"name": "wal_write", "description": "Number of times WAL buffers were written to disk via XLogWrite request"},
            {"name": "wal_sync", "description": "Number of times WAL files were synced to disk via issue_xlog_fsync request"},
            {"name": "wal_write_time", "description": "Total amount of time spent writing WAL buffers to disk, in milliseconds"},
            {"name": "wal_sync_time", "description": "Total amount of time spent syncing WAL files to disk, in milliseconds"},
            {"name": "stats_reset", "description": "Time at which these statistics were last reset"}
        ]
    
    def collect(self) -> List[Dict]:
        """Collect WAL statistics from pg_stat_wal."""
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
        """
        return self._execute_query(query) 