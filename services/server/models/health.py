from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Simple health status of the application"""
    status: str  # "healthy" or "unhealthy"
    server: bool  # true if server is healthy, false otherwise
    database: bool  # true if database is healthy, false otherwise