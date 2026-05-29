from ml.feature_extraction import extract_features

url = "http://example.com"
features = extract_features(url)
print("Entropy value:", features['entropy'])
print("Type of entropy:", type(features['entropy']))
