import os
import sys
import pytest
from unittest.mock import patch

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Mark this module's tests as unit tests
pytestmark = pytest.mark.unit

from utils.env import EnvConfig, get_bool_env_variable, get_env_variable, get_int_env_variable


def test_env_initialization():
    """
    Test that the Environment configuration initializes correctly.
    """
    with patch.dict(os.environ, {}, clear=True):
        # Create a new environment configuration
        env_instance = EnvConfig()
        
        # Default values should be set
        assert isinstance(env_instance.port, int)
        assert env_instance.database_url.startswith("postgresql://")
        assert isinstance(env_instance.debug, bool)


def test_env_from_environment_variables():
    """
    Test that environment variables are correctly loaded.
    """
    # Set environment variables
    with patch.dict(os.environ, {
        "PORT": "5000",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test",
        "DEBUG": "true"
    }):
        # Create a new environment configuration
        env_instance = EnvConfig()
        
        # Values should be loaded from environment variables
        assert env_instance.port == 5000
        assert env_instance.database_url == "postgresql://test:test@localhost:5432/test"
        assert env_instance.debug is True


def test_env_boolean_parsing():
    """
    Test that boolean environment variables are correctly parsed.
    """
    # Test truthy values
    assert get_bool_env_variable("TEST_BOOL", default=False) is False
    
    # Test with different truthy values
    with patch.dict(os.environ, {"TEST_BOOL": "true"}):
        assert get_bool_env_variable("TEST_BOOL", default=False) is True
    
    with patch.dict(os.environ, {"TEST_BOOL": "false"}):
        assert get_bool_env_variable("TEST_BOOL", default=True) is False


def test_env_int_parsing():
    """
    Test that integer environment variables are correctly parsed.
    """
    # Test with a valid integer
    with patch.dict(os.environ, {"TEST_INT": "5000"}):
        result = get_int_env_variable("TEST_INT", default=8000)
        assert result == 5000
        assert isinstance(result, int)
    
    # Test with default value
    assert get_int_env_variable("TEST_INT", default=8000) == 8000


def test_env_config_has_required_fields():
    """
    Test that the EnvConfig has all the required fields.
    """
    # Check that the EnvConfig model has these important fields
    env_instance = EnvConfig()
    assert hasattr(env_instance, "port")
    assert hasattr(env_instance, "host")
    assert hasattr(env_instance, "debug")
    assert hasattr(env_instance, "database_url")
    assert hasattr(env_instance, "cors_origins")