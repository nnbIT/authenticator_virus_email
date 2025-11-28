import re
import math
from urllib.parse import urlparse, parse_qs

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]


IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy - optimized version"""
    if not text:
        return 0.0


    text_length = len(text)
    if text_length == 0:
        return 0.0

    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1

    entropy = 0.0
    for count in char_counts.values():
        probability = count / text_length
        entropy -= probability * math.log(probability, 2)

    return entropy

def extract_features(url: str) -> dict:
    """Extracts ML features from a URL - OPTIMIZED VERSION ⚡"""
    parsed = urlparse(url.lower())
    domain = parsed.netloc
    path = parsed.path


    domain_parts = domain.split(".")
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""


    has_ip = 1 if IP_PATTERN.match(domain) else 0


    url_lower = url.lower()
    contains_keywords = sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in url_lower)


    features = {
        "url": url,
        "domain": domain,
        "tld": tld,
        "has_ip": has_ip,
        "num_subdomains": domain.count("."),
        "url_length": len(url),
        "num_params": len(parse_qs(parsed.query)),
        "contains_keywords": contains_keywords,
        "entropy": shannon_entropy(url),
        "path_length": len([p for p in path.split("/") if p]),
        "special_chars": sum(url.count(c) for c in "@%="),
        "is_https": 1 if parsed.scheme == "https" else 0,
    }

    return features
