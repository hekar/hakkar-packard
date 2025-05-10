import json
from typing import Dict, List, Any
from datetime import datetime
from .sink import MetricSink

class DebugMetricSink(MetricSink):
    """Debug metric sink that prints metrics to stdout."""
    
    def __init__(self, pretty: bool = True):
        """Initialize the debug sink.
        
        Args:
            pretty: Whether to pretty-print the JSON output
        """
        self.pretty = pretty
    
    def write(self, metrics: List[Dict[str, Any]], timestamp: datetime) -> None:
        """Print metrics to stdout.
        
        Args:
            metrics: List of metric dictionaries to print
            timestamp: Timestamp when the metrics were collected
        """
        output = {
            'timestamp': timestamp.isoformat(),
            'metrics': metrics
        }
        
        if self.pretty:
            print(json.dumps(output, indent=2))
        else:
            print(json.dumps(output))
    
    def close(self) -> None:
        """No resources to close for debug sink."""
        pass 