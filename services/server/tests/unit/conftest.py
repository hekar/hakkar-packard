import pytest
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Mark all tests in this directory as unit tests
pytestmark = pytest.mark.unit

@pytest.fixture
def mock_dependencies():
    """
    Return a dictionary of mocked dependencies for service testing.
    
    This provides a central place to define mocks for all dependencies
    that services rely on, making it easier to update or extend mocks.
    """
    return {}