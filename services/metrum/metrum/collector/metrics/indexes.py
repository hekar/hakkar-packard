from typing import Dict, List
from .base import BaseMetricsCollector

class IndexMetrics(BaseMetricsCollector):
    """Collects metrics from pg_stat_user_indexes."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_user_indexes"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "relid",
                "description": "OID of the table for this index"
            },
            {
                "name": "indexrelid",
                "description": "OID of this index"
            },
            {
                "name": "schemaname",
                "description": "Name of the schema containing this index"
            },
            {
                "name": "relname",
                "description": "Name of the table for this index"
            },
            {
                "name": "indexrelname",
                "description": "Name of this index"
            },
            {
                "name": "idx_scan",
                "description": "Number of index scans initiated on this index"
            },
            {
                "name": "idx_tup_read",
                "description": "Number of index entries returned by scans on this index"
            },
            {
                "name": "idx_tup_fetch",
                "description": "Number of live table rows fetched by simple index scans using this index"
            }
        ]
    
    def collect(self) -> List[Dict]:
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
            ORDER BY idx_scan DESC
        """
        return self._execute_query(query) 