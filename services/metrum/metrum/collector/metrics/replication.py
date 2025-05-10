from typing import Dict, List
from datetime import datetime
from .base import BaseMetricsCollector

class ReplicationMetricsCollector(BaseMetricsCollector):
    """Collector for PostgreSQL replication statistics."""
    
    @property
    def table_name(self) -> str:
        return "pg_stat_replication"
    
    @property
    def columns(self) -> List[Dict[str, str]]:
        return [
            {"name": "pid", "description": "Process ID of the WAL sender process"},
            {"name": "usesysid", "description": "OID of the user logged into this WAL sender process"},
            {"name": "usename", "description": "Name of the user logged into this WAL sender process"},
            {"name": "application_name", "description": "Name of the application that is connected to this WAL sender"},
            {"name": "client_addr", "description": "IP address of the client connected to this WAL sender"},
            {"name": "client_hostname", "description": "Host name of the connected client"},
            {"name": "client_port", "description": "TCP port number that the client is using for communication"},
            {"name": "backend_start", "description": "Time when this process was started"},
            {"name": "backend_xmin", "description": "This standby's xmin horizon if hot_standby_feedback is enabled"},
            {"name": "state", "description": "Current WAL sender state"},
            {"name": "sent_lsn", "description": "Last transaction log position sent on this connection"},
            {"name": "write_lsn", "description": "Last transaction log position written to disk by this standby server"},
            {"name": "flush_lsn", "description": "Last transaction log position flushed to disk by this standby server"},
            {"name": "replay_lsn", "description": "Last transaction log position replayed into the database on this standby server"},
            {"name": "write_lag", "description": "Time elapsed between flushing recent WAL locally and receiving notification that this standby server has written it"},
            {"name": "flush_lag", "description": "Time elapsed between flushing recent WAL locally and receiving notification that this standby server has flushed it"},
            {"name": "replay_lag", "description": "Time elapsed between flushing recent WAL locally and receiving notification that this standby server has applied it"},
            {"name": "sync_priority", "description": "Priority of this standby server for being chosen as the synchronous standby"},
            {"name": "sync_state", "description": "Synchronous state of this standby server"},
            {"name": "reply_time", "description": "Time of last reply message received from standby server"}
        ]
    
    def collect(self) -> List[Dict]:
        """Collect replication statistics from pg_stat_replication."""
        query = f"""
            SELECT {', '.join(self.get_column_names())}
            FROM {self.table_name}
        """
        return self._execute_query(query) 