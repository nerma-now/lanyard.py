import logging

logger = logging.getLogger("lanyard.client")
aiohttp_logger = logging.getLogger("lanyard.http.aiohttp")
httpx_logger = logging.getLogger("lanyard.http.httpx")

__all__ = ["aiohttp_logger", "httpx_logger", "logger"]
