import os
import sys
import pytest
from typing import Generator
from fastapi.testclient import TestClient

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import app's main modules
from main import app

# Mark all tests in this directory as integration tests
pytestmark = pytest.mark.integration

@pytest.fixture(scope="function")
def test_client() -> Generator[TestClient, None, None]:
    """
    Fixture to create a FastAPI test client for testing endpoints.
    
    This is a simplified approach that doesn't require a real database,
    as we'll mock any database calls at the service layer.
    """
    with TestClient(app) as client:
        yield client