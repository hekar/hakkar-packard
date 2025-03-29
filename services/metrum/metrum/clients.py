import asyncio
from typing import AsyncGenerator, Optional

import httpx
import websockets
from websockets.client import WebSocketClientProtocol

from .settings import settings


class HTTPClient:
    """HTTP client for making requests."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.base_url,
            timeout=settings.http_timeout
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def get(self, url: str, **kwargs):
        """Make GET request."""
        return await self.client.get(url, **kwargs)
    
    async def post(self, url: str, **kwargs):
        """Make POST request."""
        return await self.client.post(url, **kwargs)


class WebSocketClient:
    """WebSocket client for real-time communication."""
    
    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.ws_url
        self.ws: Optional[WebSocketClientProtocol] = None
    
    async def connect(self):
        """Connect to WebSocket server."""
        if not self.url:
            raise ValueError("WebSocket URL not configured")
        self.ws = await websockets.connect(self.url)
    
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        if self.ws:
            await self.ws.close()
            self.ws = None
    
    async def send(self, message: str):
        """Send message to WebSocket server."""
        if not self.ws:
            raise RuntimeError("WebSocket not connected")
        await self.ws.send(message)
    
    async def receive(self) -> AsyncGenerator[str, None]:
        """Receive messages from WebSocket server."""
        if not self.ws:
            raise RuntimeError("WebSocket not connected")
        try:
            while True:
                message = await self.ws.recv()
                yield message
        except websockets.exceptions.ConnectionClosed:
            return 