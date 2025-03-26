import logging
from typing import Dict, Any, Optional, Iterator, TypeVar, Callable
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from psycopg.connection import Connection
from psycopg.cursor import Cursor

from utils.env import env

# Set up logging
logger = logging.getLogger("uvicorn")

# Create a singleton connection pool
_pool: Optional[ConnectionPool] = None

def get_pool() -> ConnectionPool:
    """
    Get or create the database connection pool.
    
    Returns:
        A PostgreSQL connection pool.
    """
    global _pool
    if _pool is None:
        connection_url = env.database_url
        _pool = ConnectionPool(connection_url, min_size=1, max_size=10)
        logger.info(f"Initialized PostgreSQL connection pool (min=1, max=10)")
    return _pool

@contextmanager
def get_connection() -> Iterator[Connection]:
    """
    Context manager to get a database connection from the pool.
    
    Yields:
        A PostgreSQL connection.
    """
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

@contextmanager
def get_cursor(commit: bool = False) -> Iterator[Cursor]:
    """
    Context manager to get a database cursor.
    
    Args:
        commit: Whether to commit the transaction after the context manager exits.
    
    Yields:
        A PostgreSQL cursor with dict row factory.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            try:
                yield cur
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Database error: {e}")
                raise

T = TypeVar('T')
def with_cursor(func: Callable[[Cursor, ...], T]) -> Callable[..., T]:
    """
    Decorator to use a database cursor with a function.
    
    Args:
        func: The function to decorate.
    
    Returns:
        A decorated function that will be called with a cursor.
    """
    def wrapper(*args, **kwargs):
        with get_cursor() as cursor:
            return func(cursor, *args, **kwargs)
    return wrapper

def with_transaction(func: Callable[[Cursor, ...], T]) -> Callable[..., T]:
    """
    Decorator to use a database cursor with automatic transaction commit.
    
    Args:
        func: The function to decorate.
    
    Returns:
        A decorated function that will be called with a cursor in a transaction.
    """
    def wrapper(*args, **kwargs):
        with get_cursor(commit=True) as cursor:
            return func(cursor, *args, **kwargs)
    return wrapper