from fastapi import APIRouter
import logging
from typing import Dict, Any

from services.health_service import get_health_status
from models.health import HealthStatus

# Use uvicorn's logger for consistent formatting
logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.get("", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint. Returns the status of various components.
    Uses the health service to perform checks and aggregate results.
    """
    logger.info("Health endpoint: Processing health check request")
    
    # Use the health service function to get overall health status
    health_status = get_health_status()
    
    logger.info(f"Health endpoint: Completed health check. Status: {health_status.status}")
    return health_status
