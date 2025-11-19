import re
import math
from urllib.parse import urlparse, parse_qs

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]

def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy used to detect randomness/obfuscation."""
    if not text:
        return 0.0

    probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = - sum([p * math.log(p, 2) for p in probabilities])

    return entropy


def extract_features(url: str) -> dict:
    """Extracts ML features from a URL."""
    parsed = urlparse(url.lower())

    domain = parsed.netloc
    path = parsed.path

    # Features
    tld = domain.split(".")[-1] if "." in domain else ""
    has_ip = 1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) else 0
    num_subdomains = domain.count(".")
    url_length = len(url)
    query = parse_qs(parsed.query)
    num_params = len(query)
    contains_keywords = sum(1 for k in SUSPICIOUS_KEYWORDS if k in url)
    entropy_score = shannon_entropy(url)
    path_parts = [p for p in path.split("/") if p]
    path_length = len(path_parts)
    special_chars = sum(url.count(c) for c in "@%=")
    is_https = 1 if parsed.scheme == "https" else 0

    return {
        "url": url,
        "domain": domain,
        "tld": tld,
        "has_ip": has_ip,
        "num_subdomains": num_subdomains,
        "url_length": url_length,
        "num_params": num_params,
        "contains_keywords": contains_keywords,
        "entropy": entropy_score,
        "path_length": path_length,
        "special_chars": special_chars,
        "is_https": is_https,
    }


