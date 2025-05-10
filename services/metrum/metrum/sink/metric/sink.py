from abc import ABC, abstractmethod
from typing import Dict, List, Any
from datetime import datetime

class MetricSink(ABC):
    """Interface for metric sinks that handle metric storage and forwarding."""
    
    @abstractmethod
    def write(self, metrics: List[Dict[str, Any]], timestamp: datetime) -> None:
        """Write metrics to the sink.
        
        Args:
            metrics: List of metric dictionaries to write
            timestamp: Timestamp when the metrics were collected
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the sink and release any resources."""
        pass 