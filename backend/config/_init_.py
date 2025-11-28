"""
Configuration package.
Loads global project settings.
"""

from .settings import (
    BASE_DIR,
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    MODEL_PATH,
    DEFAULT_MODEL_NAME,
    BAD_TLDS,
    SUSPICIOUS_KEYWORDS,
    API_VERSION,
    PROJECT_NAME,
)

__all__ = [
    "BASE_DIR",
    "DATA_RAW_DIR",
    "DATA_PROCESSED_DIR",
    "MODEL_PATH",
    "DEFAULT_MODEL_NAME",
    "BAD_TLDS",
    "SUSPICIOUS_KEYWORDS",
    "API_VERSION",
    "PROJECT_NAME",
]
