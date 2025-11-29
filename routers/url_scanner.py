from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
from urllib.parse import urlparse
import re
import joblib
import pandas as pd
from pathlib import Path

from ml.feature_extraction import extract_features

# ✅ FIX: Remove trailing slash from prefix
router = APIRouter(prefix="/url", tags=["URL Scanner"])

# Load ML model once at startup with error handling
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "model.pkl"
try:
    ml_model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded successfully")
except Exception as e:
    ml_model = None
    print(f"❌ Failed to load ML model: {e}")

class URLInput(BaseModel):
    url: HttpUrl

# -----------------------------
# SIMPLE HEURISTIC FILTER
# -----------------------------
def calculate_risk(url: str) -> float:
    url = str(url).lower()
    risk = 0

    patterns = [
        r"\.ru", r"\.cn", r"login-", r"verify-", r"secure-", r"paypal-", r"bank",
        r"free-", r"-gift", r"-bonus"
    ]

    for p in patterns:
        if re.search(p, url):
            risk += 10

    if len(url) > 120:
        risk += 20

    if url.count("=") > 3:
        risk += 15

    return min(risk, 100)

# -----------------------------
# ADVANCED HEURISTIC FILTER
# -----------------------------
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]

BAD_TLDS = ["ru", "cn", "tk", "ml", "ga", "cf", "gq"]

def heuristic_risk_score(url: str) -> dict:
    url = url.lower()
    parsed = urlparse(url)

    score = 0
    reasons = []

    # IP-based URL
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.netloc):
        score += 35
        reasons.append("URL uses raw IP address")

    # TLD
    tld = parsed.netloc.split(".")[-1]
    if tld in BAD_TLDS:
        score += 20
        reasons.append(f"Suspicious TLD: .{tld}")

    # Suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url:
            score += 10
            reasons.append(f"Keyword detected: {keyword}")

    # URL parameters
    if url.count("=") > 3:
        score += 15
        reasons.append("Too many URL parameters")

    # URL length
    if len(url) > 120:
        score += 15
        reasons.append("URL too long (>120 characters)")

    # Obfuscated encoding
    if "%2f" in url or "%3d" in url:
        score += 10
        reasons.append("URL encoding obfuscation detected")

    # Subdomains trick
    if parsed.netloc.count(".") >= 3:
        score += 15
        reasons.append("Multiple nested subdomains")

    score = min(score, 100)

    return {
        "risk": score,
        "classification": "⚠️ Suspicious" if score >= 50 else "🟢 Probably safe",
        "reasons": reasons
    }

# -----------------------------
# MACHINE LEARNING FILTER
# -----------------------------
def ml_predict(url: str) -> dict:
    """
    Convert URL → features → ML prediction with error handling
    """
    try:
        if ml_model is None:
            return {
                "prediction": -1,
                "probability": 0.0,
                "classification": "❌ ML Model Not Available",
                "error": "ML model failed to load"
            }

        features = extract_features(url)
        df = pd.DataFrame([features])

        if "url" in df.columns:
            df = df.drop(columns=["url", "domain", "tld"], errors="ignore")

        prediction = ml_model.predict(df)[0]
        probability = ml_model.predict_proba(df)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "classification": "⚠️ Malicious (ML)" if prediction == 1 else "🟢 Safe (ML)"
        }

    except Exception as e:
        return {
            "prediction": -1,
            "probability": 0.0,
            "classification": f"❌ ML Error: {str(e)}",
            "error": True
        }

# -----------------------------
# FINAL ROUTE: RETURN ALL FILTERS TOGETHER
# -----------------------------
@router.post("/")
async def scan_url(data: URLInput):
    url_str = str(data.url).lower()

    # 1) Basic filter
    simple_risk = calculate_risk(url_str)

    # 2) Advanced heuristic
    advanced_risk = heuristic_risk_score(url_str)

    # 3) ML classifier
    ml_result = ml_predict(url_str)

    return {
        "url": url_str,
        "filters": {
            "simple_heuristic": {
                "risk_percent": simple_risk,
                "result": "⚠️ Suspicious" if simple_risk > 50 else "😊 Safe"
            },
            "advanced_heuristic": advanced_risk,
            "machine_learning": ml_result
        }
    }

# ✅ ADD: Test endpoint to verify the API is working
@router.get("/test")
async def test_endpoint():
    return {
        "status": "✅ URL Scanner is working!",
        "endpoint": "POST /scan/url",
        "ml_model_loaded": ml_model is not None
    }
