from typing import Dict, List
from .base import BaseMetricsCollector

class DatabaseMetrics(BaseMetricsCollector):
    """Collects metrics from pg_stat_database."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_database"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "datid",
                "description": "OID of a database"
            },
            {
                "name": "datname",
                "description": "Name of the database"
            },
            {
                "name": "numbackends",
                "description": "Number of backends currently connected to this database"
            },
            {
                "name": "xact_commit",
                "description": "Number of transactions in this database that have been committed"
            },
            {
                "name": "xact_rollback",
                "description": "Number of transactions in this database that have been rolled back"
            },
            {
                "name": "blks_read",
                "description": "Number of disk blocks read in this database"
            },
            {
                "name": "blks_hit",
                "description": "Number of times disk blocks were found already in the buffer cache"
            },
            {
                "name": "tup_returned",
                "description": "Number of rows returned by queries in this database"
            },
            {
                "name": "tup_fetched",
                "description": "Number of rows fetched by queries in this database"
            },
            {
                "name": "tup_inserted",
                "description": "Number of rows inserted by queries in this database"
            },
            {
                "name": "tup_updated",
                "description": "Number of rows updated by queries in this database"
            },
            {
                "name": "tup_deleted",
                "description": "Number of rows deleted by queries in this database"
            },
            {
                "name": "conflicts",
                "description": "Number of queries canceled due to conflicts with recovery in this database"
            },
            {
                "name": "temp_files",
                "description": "Number of temporary files created by queries in this database"
            },
            {
                "name": "temp_bytes",
                "description": "Total amount of data written to temporary files by queries in this database"
            },
            {
                "name": "deadlocks",
                "description": "Number of deadlocks detected in this database"
            },
            {
                "name": "checksum_failures",
                "description": "Number of data page checksum failures detected in this database"
            },
            {
                "name": "blk_read_time",
                "description": "Time spent reading data file blocks by backends in this database, in milliseconds"
            },
            {
                "name": "blk_write_time",
                "description": "Time spent writing data file blocks by backends in this database, in milliseconds"
            },
            {
                "name": "stats_reset",
                "description": "Time at which these statistics were last reset"
            }
        ]
    
    def collect(self) -> List[Dict]:
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
            WHERE datname = current_database()
        """
        return self._execute_query(query) 