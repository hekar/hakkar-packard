import json
import requests
from typing import Dict, List, Any
from datetime import datetime
from .sink import MetricSink

class HttpMetricSink(MetricSink):
    """HTTP-based metric sink that sends metrics to a remote endpoint."""
    
    def __init__(self, endpoint: str, api_key: str = None):
        """Initialize the HTTP sink.
        
        Args:
            endpoint: URL of the metrics endpoint
            api_key: Optional API key for authentication
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def write(self, metrics: List[Dict[str, Any]], timestamp: datetime) -> None:
        """Send metrics to the HTTP endpoint.
        
        Args:
            metrics: List of metric dictionaries to send
            timestamp: Timestamp when the metrics were collected
        """
        payload = {
            'timestamp': timestamp.isoformat(),
            'metrics': metrics
        }
        
        try:
            response = self.session.post(
                self.endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # TODO: Add proper error handling and logging
            raise RuntimeError(f"Failed to send metrics to {self.endpoint}: {str(e)}")
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close() 