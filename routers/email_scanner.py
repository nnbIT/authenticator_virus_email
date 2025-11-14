from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl
import re

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


@router.post("/")
async def scan_url(data: URLInput):
    url_str = str(data.url)  # ensure string conversion
    risk = calculate_risk(url_str)

    return {
        "url": url_str,
        "risk_percent": risk,
        "result": "⚠️ Suspicious" if risk > 50 else "😊 Probably safe"
    }
