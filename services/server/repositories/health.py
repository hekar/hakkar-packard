import logging

from . import db

logger = logging.getLogger("uvicorn")

@db.with_cursor
def is_database_healthy(cursor) -> bool:
    """
    Check if the database is healthy.
    
    Args:
        cursor: Database cursor provided by the with_cursor decorator.
        
    Returns:
        True if the database is healthy, False otherwise.
    """
    try:
        # Simple query to check database connectivity
        cursor.execute("SELECT 1;")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False