import joblib
import pandas as pd
from ml.feature_extraction import extract_features

# Load model
model = joblib.load('ml/model.pkl')

# Test LinkedIn URL
test_urls = [
    "http://linkedin.com/feed/",
    "https://google.com",
    "http://login-verify-secure.com"
]

for url in test_urls:
    features = extract_features(url)
    df = pd.DataFrame([features])

    # Identify non-numeric columns
    print(f"\nURL: {url}")
    print("Features:", list(features.keys()))
    print("Non-numeric:", [k for k, v in features.items() if not isinstance(v, (int, float))])

    # Predict
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    print(f"Prediction: {'Malicious' if pred==1 else 'Safe'} ({prob:.1%})")
