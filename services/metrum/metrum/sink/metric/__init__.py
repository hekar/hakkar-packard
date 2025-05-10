from typing import Optional
from .sink import MetricSink
from .http_sink import HttpMetricSink
from .debug_sink import DebugMetricSink
from .sqlite_sink import SqliteMetricSink

def create_metric_sink(
    sink_type: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    db_path: Optional[str] = None,
    pretty: bool = True
) -> MetricSink:
    """Create a metric sink based on the specified type.
    
    Args:
        sink_type: Type of sink to create ('http', 'debug', or 'sqlite')
        endpoint: For HTTP sink, the endpoint URL
        api_key: For HTTP sink, optional API key
        db_path: For SQLite sink, path to database file
        pretty: For debug sink, whether to pretty-print output
    
    Returns:
        An instance of the requested metric sink
    
    Raises:
        ValueError: If sink_type is invalid or required parameters are missing
    """
    if sink_type == 'http':
        if not endpoint:
            raise ValueError("endpoint is required for HTTP sink")
        return HttpMetricSink(endpoint, api_key)
    
    elif sink_type == 'debug':
        return DebugMetricSink(pretty)
    
    elif sink_type == 'sqlite':
        if not db_path:
            raise ValueError("db_path is required for SQLite sink")
        return SqliteMetricSink(db_path)
    
    else:
        raise ValueError(f"Invalid sink type: {sink_type}")

__all__ = [
    'MetricSink',
    'HttpMetricSink',
    'DebugMetricSink',
    'SqliteMetricSink',
    'create_metric_sink'
] 