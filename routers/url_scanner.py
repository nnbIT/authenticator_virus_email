from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
import re

router = APIRouter(prefix="/url", tags=["URL Scanner"])

class URLInput(BaseModel):
    url: HttpUrl


def calculate_risk(url: str) -> float:
    """
    Very simple heuristic-based risk calculator.
    Later we will upgrade it with real threat intelligence APIs.
    """

    risk = 0

    # Suspicious patterns
    patterns = [
        r"\.ru", r"\.cn", r"login-", r"verify-", r"secure-", r"paypal-", r"bank",
        r"free-", r"-gift", r"-bonus"
    ]

    for p in patterns:
        if re.search(p, url.lower()):
            risk += 10

    # URL too long
    if len(url) > 120:
        risk += 20

    # Has many parameters
    if url.count("=") > 3:
        risk += 15

    return min(risk, 100)


@router.post("/")
async def scan_url(data: URLInput):
    url = data.url
    risk = calculate_risk(url)

    return {
        "url": url,
        "risk_percent": risk,
        "result": "⚠️ Suspicious" if risk > 50 else "😊 Probably safe"
    }
