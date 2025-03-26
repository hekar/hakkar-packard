from fastapi import APIRouter, FastAPI
from typing import List, Dict, Any, Optional
from routes.v1.v1 import router as v1_router

class RouteHandler:
    """Handler for managing and including API routes"""
    
    def __init__(self):
        """Initialize an empty list of routers"""
        self.routers: List[Dict[str, Any]] = []
    
    def add_router(self, router: APIRouter, prefix: str, tags: Optional[List[str]] = None):
        """
        Add a router with prefix and optional tags.
        
        Args:
            router: The APIRouter to add
            prefix: URL prefix for the router
            tags: Optional list of tags for documentation
        """
        self.routers.append({
            "router": router,
            "prefix": prefix,
            "tags": tags or []
        })
    
    def include_routers(self, app: FastAPI):
        """
        Include all registered routers in the FastAPI app.
        
        Args:
            app: The FastAPI application
        """
        for router_info in self.routers:
            app.include_router(
                router_info["router"],
                prefix=router_info["prefix"],
                tags=router_info["tags"]
            )


# For backward compatibility with existing code
router = APIRouter()
router.include_router(v1_router, prefix="/v1")
