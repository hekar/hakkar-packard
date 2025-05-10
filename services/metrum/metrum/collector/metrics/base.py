from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import text
from metrum.db.base import get_connection

class BaseMetricsCollector(ABC):
    """Base class for all metrics collectors."""
    
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.last_collection_time: Optional[datetime] = None
    
    @property
    @abstractmethod
    def table_name(self) -> str:
        """Name of the PostgreSQL statistics table."""
        pass
    
    @property
    @abstractmethod
    def columns(self) -> List[Dict[str, str]]:
        """List of column definitions with names and descriptions."""
        pass
    
    @abstractmethod
    def collect(self) -> List[Dict]:
        """Collect metrics from the database."""
        pass
    
    def _execute_query(self, query: str) -> List[Dict]:
        """Execute a query and return results as a list of dictionaries."""
        with get_connection(self.db_name) as conn:
            result = conn.execute(text(query))
            return [dict(zip(result.keys(), row)) for row in result.fetchall()]
    
    def get_column_names(self) -> List[str]:
        """Get list of column names."""
        return [col['name'] for col in self.columns]
    
    def get_column_descriptions(self) -> Dict[str, str]:
        """Get dictionary mapping column names to descriptions."""
        return {col['name']: col['description'] for col in self.columns} 
