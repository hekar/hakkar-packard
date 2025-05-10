import sqlite3
from typing import Dict, List, Any
from datetime import datetime
from .sink import MetricSink
import json

class SqliteMetricSink(MetricSink):
    """SQLite-based metric sink that stores metrics in a local SQLite database."""
    
    def __init__(self, db_path: str):
        """Initialize the SQLite sink.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self) -> None:
        """Create the necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Create metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_labels TEXT
            )
        """)
        
        self.conn.commit()
    
    def write(self, metrics: List[Dict[str, Any]], timestamp: datetime) -> None:
        """Store metrics in the SQLite database.
        
        Args:
            metrics: List of metric dictionaries to store
            timestamp: Timestamp when the metrics were collected
        """
        cursor = self.conn.cursor()
        
        for metric in metrics:
            # Convert metric labels to JSON string
            labels = json.dumps(metric.get('labels', {}))
            
            cursor.execute("""
                INSERT INTO metrics (timestamp, metric_name, metric_value, metric_labels)
                VALUES (?, ?, ?, ?)
            """, (
                timestamp.isoformat(),
                metric.get('name', ''),
                metric.get('value'),
                labels
            ))
        
        self.conn.commit()
    
    def close(self) -> None:
        """Close the SQLite connection."""
        self.conn.close() 