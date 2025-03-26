import pytest
from fastapi.testclient import TestClient
import unittest.mock as mock
import sys
import os

# Add the server directory to the Python path if needed (for clean imports)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from routes.v1 import health
from services.health_service import get_health_status

# Mark tests in this file as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture
def patch_health_service(monkeypatch):
    """
    Patch the health service to avoid database connection attempts during testing.
    This allows testing the API contract without requiring external services.
    """
    mock_status = mock.MagicMock()
    mock_status.status = "healthy"
    mock_status.server = True
    mock_status.database = True
    
    monkeypatch.setattr(health, "get_health_status", lambda: mock_status)
    return mock_status


def test_health_endpoint_success(test_client: TestClient, patch_health_service):
    """
    Test that the health endpoint returns a 200 status code with correct format when healthy.
    This test focuses on the API contract, not the actual implementation.
    """
    # Send a GET request to the health endpoint
    response = test_client.get("/api/v1/health")
    
    # Assert response status code is 200
    assert response.status_code == 200
    
    # Assert the response JSON has the correct format
    data = response.json()
    assert "status" in data
    assert "server" in data
    assert "database" in data
    
    # Verify the values are correct types
    assert isinstance(data["status"], str)
    assert isinstance(data["server"], bool)
    assert isinstance(data["database"], bool)
    
    # The values should match our mock
    assert data["status"] == "healthy"
    assert data["server"] is True
    assert data["database"] is True


def test_health_endpoint_unhealthy(test_client: TestClient, patch_health_service):
    """
    Test that the health endpoint properly reflects an unhealthy status.
    """
    # Configure our mock to return unhealthy status
    patch_health_service.status = "unhealthy"
    patch_health_service.server = True
    patch_health_service.database = False
    
    # Send a GET request to the health endpoint
    response = test_client.get("/api/v1/health")
    
    # Assert response status code is still 200 (health endpoint should return 200 even when unhealthy)
    assert response.status_code == 200
    
    # Assert the response JSON has the correct values
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["server"] is True
    assert data["database"] is False