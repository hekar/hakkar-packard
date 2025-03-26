import unittest.mock as mock
import pytest

from services.health_service import get_health_status

# Mark this module's tests as unit tests
pytestmark = pytest.mark.unit


def test_all_healthy():
    """Test that the service returns healthy status when both server and database are healthy"""
    # Arrange
    mock_server_fn = mock.MagicMock(return_value=True)
    mock_db_fn = mock.MagicMock(return_value=True)
    
    # Act
    result = get_health_status(server_health_fn=mock_server_fn, db_health_fn=mock_db_fn)
    
    # Assert
    assert result.status == "healthy"
    assert result.server is True
    assert result.database is True
    mock_server_fn.assert_called_once()
    mock_db_fn.assert_called_once()


def test_server_unhealthy():
    """Test that the service returns unhealthy status when server is unhealthy"""
    # Arrange
    mock_server_fn = mock.MagicMock(return_value=False)
    mock_db_fn = mock.MagicMock(return_value=True)
    
    # Act
    result = get_health_status(server_health_fn=mock_server_fn, db_health_fn=mock_db_fn)
    
    # Assert
    assert result.status == "unhealthy"
    assert result.server is False
    assert result.database is True
    mock_server_fn.assert_called_once()
    mock_db_fn.assert_called_once()


def test_db_unhealthy():
    """Test that the service returns unhealthy status when database is unhealthy"""
    # Arrange
    mock_server_fn = mock.MagicMock(return_value=True)
    mock_db_fn = mock.MagicMock(return_value=False)
    
    # Act
    result = get_health_status(server_health_fn=mock_server_fn, db_health_fn=mock_db_fn)
    
    # Assert
    assert result.status == "unhealthy"
    assert result.server is True
    assert result.database is False
    mock_server_fn.assert_called_once()
    mock_db_fn.assert_called_once()