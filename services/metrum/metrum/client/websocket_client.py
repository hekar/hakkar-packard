from typing import AsyncGenerator, Optional

import websockets
from websockets.client import WebSocketClientProtocol

from ..settings import settings
from ..common.logger import logger


class WebSocketClient:
    """WebSocket client for real-time communication."""
    
    def __init__(self, url: Optional[str] = None):
        self.url = url or settings.ws_url
        self.ws: Optional[WebSocketClientProtocol] = None
        logger.debug("websocket_client_initialized", url=self.url)
    
    async def connect(self):
        """Connect to WebSocket server."""
        if not self.url:
            logger.error("websocket_url_not_configured", error="No URL provided")
            raise ValueError("WebSocket URL not configured")
        
        logger.debug("websocket_connect_attempt", url=self.url)
        try:
            self.ws = await websockets.connect(self.url)
            logger.info("websocket_connected", url=self.url)
        except Exception as e:
            logger.error("websocket_connect_failed", 
                        url=self.url,
                        error=str(e),
                        error_type=type(e).__name__)
            raise
    
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        if self.ws:
            logger.debug("websocket_disconnect_attempt", url=self.url)
            try:
                await self.ws.close()
                self.ws = None
                logger.info("websocket_disconnected", url=self.url)
            except Exception as e:
                logger.error("websocket_disconnect_failed",
                            url=self.url,
                            error=str(e),
                            error_type=type(e).__name__)
                raise
        else:
            logger.debug("websocket_disconnect_skipped", reason="no_active_connection")
    
    async def send(self, message: str):
        """Send message to WebSocket server."""
        if not self.ws:
            logger.error("websocket_send_failed", 
                        error="No active connection",
                        url=self.url)
            raise RuntimeError("WebSocket not connected")
        
        logger.debug("websocket_send_attempt", 
                    url=self.url,
                    message_length=len(message))
        try:
            await self.ws.send(message)
            logger.debug("websocket_message_sent",
                        url=self.url,
                        message_length=len(message))
        except Exception as e:
            logger.error("websocket_send_failed",
                        url=self.url,
                        error=str(e),
                        error_type=type(e).__name__,
                        message_length=len(message))
            raise
    
    async def receive(self) -> AsyncGenerator[str, None]:
        """Receive messages from WebSocket server."""
        if not self.ws:
            logger.error("websocket_receive_failed",
                        error="No active connection",
                        url=self.url)
            raise RuntimeError("WebSocket not connected")
        
        logger.debug("websocket_receive_start", url=self.url)
        try:
            while True:
                message = await self.ws.recv()
                logger.debug("websocket_message_received",
                            url=self.url,
                            message_length=len(message))
                yield message
        except websockets.exceptions.ConnectionClosed as e:
            logger.info("websocket_connection_closed",
                       url=self.url,
                       code=e.code,
                       reason=e.reason)
            return
        except Exception as e:
            logger.error("websocket_receive_failed",
                        url=self.url,
                        error=str(e),
                        error_type=type(e).__name__)
            raise 