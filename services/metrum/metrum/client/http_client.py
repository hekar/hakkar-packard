import httpx

from ..settings import settings


class HttpClient:
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