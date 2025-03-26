import logging
from typing import Optional, Callable

from models.health import HealthStatus
from repositories import health

logger = logging.getLogger("uvicorn")

def is_server_healthy() -> bool:
    """
    Check if the server is healthy.
    
    In a real-world scenario, this could check for:
    - Available memory
    - CPU load
    - Disk space
    - Other critical dependencies
    
    Returns:
        True, since if this code is executing, the server is running
    """
    # If this code is executing, the server is running
    # In a real implementation, you could add more checks here
    return True

def get_health_status(
    server_health_fn: Optional[Callable[[], bool]] = None,
    db_health_fn: Optional[Callable[[], bool]] = None
) -> HealthStatus:
    """
    Get the overall health status of the application.
    
    Args:
        server_health_fn: Optional override for server health check function (for testing)
        db_health_fn: Optional override for database health check function (for testing)
        
    Returns:
        A HealthStatus object with simple health information
    """
    logger.info("Health service: Checking system health")
    
    # Use provided functions or defaults
    server_fn = server_health_fn or is_server_healthy
    db_fn = db_health_fn or health.is_database_healthy
    
    # Check server and database health
    server_healthy = server_fn()
    db_healthy = db_fn()
    
    # Overall status is healthy only if both server and database are healthy
    status = "healthy" if (server_healthy and db_healthy) else "unhealthy"
    
    # Build the simple health status response
    health_status = HealthStatus(
        status=status,
        server=server_healthy,
        database=db_healthy
    )
    
    logger.info(f"Health service: Health check complete. Status: {status}")
    return health_status