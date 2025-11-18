"""
Global configuration settings for the project.
You can store paths, constants, environment variables, and ML model settings here.
"""

import os
from pathlib import Path

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# DATA PATHS
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODEL_PATH = BASE_DIR / "data" / "model.pkl"

# -----------------------------
# MACHINE LEARNING SETTINGS
DEFAULT_MODEL_NAME = "url_malware_classifier"

# -----------------------------
# HEURISTICS SETTINGS
BAD_TLDS = ["ru", "cn", "tk", "ml", "ga", "cf", "gq"]
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]

# -----------------------------
# SERVER / API SETTINGS
API_VERSION = "1.0.0"
PROJECT_NAME = "Cybersecurity Analyzer API"
