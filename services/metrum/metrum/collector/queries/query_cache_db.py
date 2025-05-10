from typing import List, Optional

from metrum.db.base import Base, get_db, engine
from metrum.collector.queries.query import MetrumQuery, QueryType
from metrum.collector.queries.query_cache import MetrumQueryCache


class MetrumQueryCacheDb:
    """
    Class for interacting with the MetrumQueryCache database.
    
    This class provides methods for storing, retrieving, and updating query cache information.
    """
    
    @staticmethod
    def create_tables():
        """Create the necessary tables in the database."""
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def add_query(query: MetrumQuery, sent_to_server: bool = False) -> MetrumQueryCache:
        """
        Add a query to the cache.
        
        Args:
            query: MetrumQuery instance to cache
            sent_to_server: Whether the query was sent to the server
            
        Returns:
            The created MetrumQueryCache instance
        """
        db = next(get_db())
        try:
            cache_entry = MetrumQueryCache(
                query_hash=query.query_hash,
                query=query.query,
                query_type=query.query_type.value,
                sent_to_server=sent_to_server
            )
            db.add(cache_entry)
            db.commit()
            db.refresh(cache_entry)
            return cache_entry
        finally:
            db.close()
    
    @staticmethod
    def get_query_by_hash(query_hash: str) -> Optional[MetrumQueryCache]:
        """
        Get a query from the cache by its hash.
        
        Args:
            query_hash: Hash of the query to retrieve
            
        Returns:
            MetrumQueryCache instance if found, None otherwise
        """
        db = next(get_db())
        try:
            return db.query(MetrumQueryCache).filter(MetrumQueryCache.query_hash == query_hash).first()
        finally:
            db.close()
    
    @staticmethod
    def update_sent_to_server(query_hash: str, sent_to_server: bool = True) -> Optional[MetrumQueryCache]:
        """
        Update the sent_to_server flag for a query.
        
        Args:
            query_hash: Hash of the query to update
            sent_to_server: New value for the sent_to_server flag
            
        Returns:
            Updated MetrumQueryCache instance if found, None otherwise
        """
        db = next(get_db())
        try:
            cache_entry = db.query(MetrumQueryCache).filter(MetrumQueryCache.query_hash == query_hash).first()
            if cache_entry:
                cache_entry.sent_to_server = sent_to_server
                db.commit()
                db.refresh(cache_entry)
            return cache_entry
        finally:
            db.close()
    
    @staticmethod
    def get_all_queries(limit: int = 100, offset: int = 0) -> List[MetrumQueryCache]:
        """
        Get all queries from the cache with pagination.
        
        Args:
            limit: Maximum number of queries to return
            offset: Number of queries to skip
            
        Returns:
            List of MetrumQueryCache instances
        """
        db = next(get_db())
        try:
            return db.query(MetrumQueryCache).order_by(MetrumQueryCache.created_at.desc()).offset(offset).limit(limit).all()
        finally:
            db.close()
    
    @staticmethod
    def get_queries_by_type(query_type: QueryType, limit: int = 100, offset: int = 0) -> List[MetrumQueryCache]:
        """
        Get queries of a specific type from the cache with pagination.
        
        Args:
            query_type: Type of queries to retrieve
            limit: Maximum number of queries to return
            offset: Number of queries to skip
            
        Returns:
            List of MetrumQueryCache instances
        """
        db = next(get_db())
        try:
            return db.query(MetrumQueryCache).filter(
                MetrumQueryCache.query_type == query_type.value
            ).order_by(MetrumQueryCache.created_at.desc()).offset(offset).limit(limit).all()
        finally:
            db.close()
    
    @staticmethod
    def delete_query(query_hash: str) -> bool:
        """
        Delete a query from the cache.
        
        Args:
            query_hash: Hash of the query to delete
            
        Returns:
            True if the query was deleted, False otherwise
        """
        db = next(get_db())
        try:
            result = db.query(MetrumQueryCache).filter(MetrumQueryCache.query_hash == query_hash).delete()
            db.commit()
            return result > 0
        finally:
            db.close() 