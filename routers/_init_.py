"""
Routers package - exposes all route modules.
"""

from .url_scanner import router as url_scanner_router
from .file_scanner import router as file_scanner_router
from .email_scanner import router as email_scanner_router

__all__ = [
    "url_scanner_router",
    "file_scanner_router",
    "email_scanner_router",
]
