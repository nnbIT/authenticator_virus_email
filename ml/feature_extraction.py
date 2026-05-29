import re
import math
from urllib.parse import urlparse, parse_qs

# Existing constants
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account",
    "paypal", "bank", "confirm", "free", "gift", "bonus"
]

# Safe TLDs (commonly used by legitimate websites)
SAFE_TLDS = {"com", "org", "net", "edu", "gov", "io", "co", "uk", "de", "fr", "ca", "au", "in", "br", "mx", "jp", "kr", "nl", "se", "pl", "it", "es", "ch", "be", "no", "dk", "fi", "nz", "sg", "my", "ph", "pk", "tr", "il", "za", "ng", "ae", "sa", "cl", "ar", "co", "ve", "pe"}

# List of well‑known brands for typosquatting detection (top 20)
KNOWN_BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple", "facebook",
    "instagram", "netflix", "spotify", "linkedin", "twitter", "whatsapp",
    "yahoo", "ebay", "dropbox", "github", "stackoverflow", "adobe", "salesforce"
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

def levenshtein_distance(s1: str, s2: str) -> int:
    """Simple Levenshtein distance for typosquatting detection"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def brand_similarity_score(domain: str) -> int:
    """
    Returns 1 if domain is a likely typosquat of a known brand,
    otherwise 0.
    """
    domain_clean = re.sub(r'[^a-z]', '', domain.lower())  # keep only letters
    for brand in KNOWN_BRANDS:
        # Direct brand match? That's not a typo – it's the real thing (but might be safe)
        if domain_clean == brand:
            return 0
        # Check if domain contains brand with small distance
        if len(domain_clean) >= 3 and len(brand) >= 3:
            # Sliding window: brand could be part of longer domain
            for i in range(len(domain_clean) - len(brand) + 1):
                sub = domain_clean[i:i+len(brand)]
                if levenshtein_distance(sub, brand) <= 2:
                    return 1
    return 0

def extract_features(url: str) -> dict:
    """Extracts ML features from a URL - HYBRID VERSION (11 + 4 new)"""
    parsed = urlparse(url.lower())
    domain = parsed.netloc
    path = parsed.path

    domain_parts = domain.split(".")
    tld = domain_parts[-1] if len(domain_parts) > 1 else ""

    has_ip = 1 if IP_PATTERN.match(domain) else 0

    url_lower = url.lower()
    contains_keywords = sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in url_lower)

    # --- NEW FEATURES ---
    # digit_ratio: proportion of digits in domain (excluding TLD)
    domain_no_tld = ".".join(domain_parts[:-1]) if len(domain_parts) > 1 else domain
    digit_count = sum(c.isdigit() for c in domain_no_tld)
    digit_ratio = digit_count / len(domain_no_tld) if len(domain_no_tld) > 0 else 0.0

    # hyphen_count: number of hyphens in domain
    hyphen_count = domain.count('-')

    # tld_risk: 1 if TLD is in high-risk list
    tld_risk = 0 if tld in SAFE_TLDS else 1

    # brand_similarity: 1 if domain looks like a known brand with typos
    brand_similarity = brand_similarity_score(domain_no_tld)

    # Build feature dictionary (keep existing + new)
    features = {
        "url": url,
        "domain": domain,
        "tld": tld,
        "has_ip": has_ip,
        "num_subdomains": len(domain.split(".")) - 2 if len(domain.split(".")) > 2 else 0,
        "url_length": len(url),
        "num_params": len(parse_qs(parsed.query)),
        "contains_keywords": contains_keywords,
        "entropy": shannon_entropy(url),
        "path_length": len([p for p in path.split("/") if p]),
        "special_chars": sum(url.count(c) for c in "@%="),
        "is_https": 1 if parsed.scheme == "https" else 0,
        # NEW FEATURES (numeric)
        "digit_ratio": digit_ratio,
        "hyphen_count": hyphen_count,
        "tld_risk": tld_risk,
        "brand_similarity": brand_similarity,
    }
    return features
