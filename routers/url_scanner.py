from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
import re
from urllib.parse import urlparse

router = APIRouter(prefix="/url", tags=["URL Scanner"])

class URLInput(BaseModel):
    url: HttpUrl


def calculate_risk(url: str) -> float:
    url = str(url).lower()  # double guarantee it's a string
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

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]

BAD_TLDS = ["ru", "cn", "tk", "ml", "ga", "cf", "gq"]  # cheap domains often used in attacks

def heuristic_risk_score(url: str) -> dict:
    url = url.lower()
    parsed = urlparse(url)

    score = 0
    reasons = []

    # 1️⃣ IP-only URLs (very suspicious)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", parsed.netloc):
        score += 35
        reasons.append("URL uses raw IP address")

    # 2️⃣ TLD reputation
    tld = parsed.netloc.split(".")[-1]
    if tld in BAD_TLDS:
        score += 20
        reasons.append(f"Suspicious TLD: .{tld}")

    # 3️⃣ Suspicious keywords
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url:
            score += 10
            reasons.append(f"Keyword detected: {keyword}")

    # 4️⃣ Too many parameters
    if url.count("=") > 3:
        score += 15
        reasons.append("Too many URL parameters")

    # 5️⃣ URL too long
    if len(url) > 120:
        score += 15
        reasons.append("URL length suspicious (>120 chars)")

    # 6️⃣ % encoding indicates obfuscation
    if "%2f" in url or "%3d" in url:
        score += 10
        reasons.append("Obfuscated URL encoding detected")

    # 7️⃣ Multiple subdomains (phishing trick)
    if parsed.netloc.count(".") >= 3:
        score += 15
        reasons.append("Multiple nested subdomains")

    # Finalize score
    score = min(score, 100)

    return {
        "risk": score,
        "classification": "⚠️ Suspicious" if score >= 50 else "🟢 Probably safe",
        "reasons": reasons
    }

@router.post("/")
async def scan_url(data: URLInput):
    url_str = str(data.url).lower()  # ensure string conversion

    simple_risk = calculate_risk(url_str)
    advanced_risk = heuristic_risk_score(url_str)

    return {
        "url": url_str,
        "simple_filter": {
            "risk_percent": simple_risk,
            "result": "⚠️ Suspicious" if simple_risk > 50 else "😊 Probably safe"
        },
        "advanced_filter": advanced_risk
    }
