from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from pydantic import BaseModel

from metrum.db.base import Base


class MetrumQueryCache(Base):
    """
    SQLAlchemy model for storing query cache information in SQLite.
    
    Attributes:
        id: Primary key
        query_hash: Hash of the query for identification
        query: The original SQL query string
        query_type: Type of query (SELECT, UPDATE, DELETE, MERGE)
        sent_to_server: Whether the query was sent to the server
        created_at: When the cache entry was created
        updated_at: When the cache entry was last updated
    """
    __tablename__ = "metrum_query_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String, unique=True, index=True, nullable=False)
    query = Column(String, nullable=False)
    query_type = Column(String, nullable=False)
    sent_to_server = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 