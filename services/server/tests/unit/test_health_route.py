import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Mark this module's tests as unit tests
pytestmark = pytest.mark.unit

from models.health import HealthStatus
import services.health_service


def test_health_status_model():
    """
    Test that the HealthStatus model works correctly.
    """
    # Create a health status
    status = HealthStatus(
        status="healthy",
        server=True,
        database=True
    )
    
    # Verify the properties
    assert status.status == "healthy"
    assert status.server is True
    assert status.database is True
    
    # Create an unhealthy status
    status = HealthStatus(
        status="unhealthy",
        server=False,
        database=True
    )
    
    # Verify the properties
    assert status.status == "unhealthy"
    assert status.server is False
    assert status.database is True


@patch("services.health_service.health.is_database_healthy")
def test_health_service_with_healthy_db(mock_db_health):
    """
    Test that the health service returns healthy status when database is healthy.
    """
    # Set up database health check to return True
    mock_db_health.return_value = True
    
    # Call the health service
    result = services.health_service.get_health_status()
    
    # Verify the result
    assert result.status == "healthy"
    assert result.server is True
    assert result.database is True


@patch("services.health_service.health.is_database_healthy")
def test_health_service_with_unhealthy_db(mock_db_health):
    """
    Test that the health service returns unhealthy status when database is unhealthy.
    """
    # Set up database health check to return False
    mock_db_health.return_value = False
    
    # Call the health service
    result = services.health_service.get_health_status()
    
    # Verify the result
    assert result.status == "unhealthy"
    assert result.server is True
    assert result.database is False