from typing import Dict, List
from .base import BaseMetricsCollector

class TableMetrics(BaseMetricsCollector):
    """Collects metrics from pg_stat_user_tables."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_user_tables"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {
                "name": "relid",
                "description": "OID of a table"
            },
            {
                "name": "schemaname",
                "description": "Name of the schema containing this table"
            },
            {
                "name": "relname",
                "description": "Name of this table"
            },
            {
                "name": "seq_scan",
                "description": "Number of sequential scans initiated on this table"
            },
            {
                "name": "seq_tup_read",
                "description": "Number of live rows fetched by sequential scans"
            },
            {
                "name": "idx_scan",
                "description": "Number of index scans initiated on this table"
            },
            {
                "name": "idx_tup_fetch",
                "description": "Number of live rows fetched by index scans"
            },
            {
                "name": "n_tup_ins",
                "description": "Number of rows inserted"
            },
            {
                "name": "n_tup_upd",
                "description": "Number of rows updated"
            },
            {
                "name": "n_tup_del",
                "description": "Number of rows deleted"
            },
            {
                "name": "n_tup_hot_upd",
                "description": "Number of rows HOT updated (i.e., with no separate index update required)"
            },
            {
                "name": "n_live_tup",
                "description": "Estimated number of live rows"
            },
            {
                "name": "n_dead_tup",
                "description": "Estimated number of dead rows"
            },
            {
                "name": "n_mod_since_analyze",
                "description": "Estimated number of rows modified since this table was last analyzed"
            },
            {
                "name": "last_vacuum",
                "description": "Last time at which this table was manually vacuumed (not counting VACUUM FULL)"
            },
            {
                "name": "last_autovacuum",
                "description": "Last time at which this table was vacuumed by the autovacuum daemon"
            },
            {
                "name": "last_analyze",
                "description": "Last time at which this table was manually analyzed"
            },
            {
                "name": "last_autoanalyze",
                "description": "Last time at which this table was analyzed by the autovacuum daemon"
            },
            {
                "name": "vacuum_count",
                "description": "Number of times this table has been manually vacuumed (not counting VACUUM FULL)"
            },
            {
                "name": "autovacuum_count",
                "description": "Number of times this table has been vacuumed by the autovacuum daemon"
            },
            {
                "name": "analyze_count",
                "description": "Number of times this table has been manually analyzed"
            },
            {
                "name": "autoanalyze_count",
                "description": "Number of times this table has been analyzed by the autovacuum daemon"
            }
        ]
    
    def collect(self) -> List[Dict]:
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
            ORDER BY n_live_tup DESC
        """
        return self._execute_query(query) 