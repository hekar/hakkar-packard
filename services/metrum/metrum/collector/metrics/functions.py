from typing import Dict, List
from .base import BaseMetricsCollector

class FunctionMetrics(BaseMetricsCollector):
    """Collects metrics from pg_stat_user_functions."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_user_functions"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "funcid",
                "description": "OID of a function"
            },
            {
                "name": "schemaname",
                "description": "Name of the schema containing this function"
            },
            {
                "name": "funcname",
                "description": "Name of this function"
            },
            {
                "name": "calls",
                "description": "Number of times this function has been called"
            },
            {
                "name": "total_time",
                "description": "Total time spent in this function and all other functions called by it, in milliseconds"
            },
            {
                "name": "self_time",
                "description": "Total time spent in this function itself, not including other functions called by it, in milliseconds"
            }
        ]
    
    def collect(self) -> List[Dict]:
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
            ORDER BY total_time DESC
        """
        return self._execute_query(query) 