import os
import sys
import pytest
from fastapi import APIRouter

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from routes.route_handler import RouteHandler

# Mark this module's tests as unit tests
pytestmark = pytest.mark.unit


def test_route_handler_creation():
    """
    Test that the RouteHandler class initializes correctly.
    """
    # Create a new RouteHandler instance
    handler = RouteHandler()
    
    # Should have an empty router list
    assert len(handler.routers) == 0


def test_add_router():
    """
    Test adding a router to the RouteHandler.
    """
    # Create a new RouteHandler instance
    handler = RouteHandler()
    
    # Create a router to add
    router = APIRouter()
    
    # Add the router with a prefix
    handler.add_router(router, "/test")
    
    # Should have one router in the list
    assert len(handler.routers) == 1
    assert handler.routers[0]["router"] == router
    assert handler.routers[0]["prefix"] == "/test"
    assert handler.routers[0]["tags"] == []


def test_add_router_with_tags():
    """
    Test adding a router with tags to the RouteHandler.
    """
    # Create a new RouteHandler instance
    handler = RouteHandler()
    
    # Create a router to add
    router = APIRouter()
    
    # Add the router with a prefix and tags
    handler.add_router(router, "/test", ["test-tag"])
    
    # Should have one router in the list
    assert len(handler.routers) == 1
    assert handler.routers[0]["router"] == router
    assert handler.routers[0]["prefix"] == "/test"
    assert handler.routers[0]["tags"] == ["test-tag"]


def test_include_routers():
    """
    Test including routers in an app.
    """
    # Create a new RouteHandler instance
    handler = RouteHandler()
    
    # Create routers to add
    router1 = APIRouter()
    router2 = APIRouter()
    
    # Add the routers
    handler.add_router(router1, "/test1", ["test1"])
    handler.add_router(router2, "/test2", ["test2"])
    
    # Create a mock app
    class MockApp:
        def __init__(self):
            self.included_routers = []
        
        def include_router(self, router, prefix, tags):
            self.included_routers.append({
                "router": router,
                "prefix": prefix,
                "tags": tags
            })
    
    mock_app = MockApp()
    
    # Include the routers in the mock app
    handler.include_routers(mock_app)
    
    # Should have included both routers
    assert len(mock_app.included_routers) == 2
    assert mock_app.included_routers[0]["router"] == router1
    assert mock_app.included_routers[0]["prefix"] == "/test1"
    assert mock_app.included_routers[0]["tags"] == ["test1"]
    assert mock_app.included_routers[1]["router"] == router2
    assert mock_app.included_routers[1]["prefix"] == "/test2"
    assert mock_app.included_routers[1]["tags"] == ["test2"]