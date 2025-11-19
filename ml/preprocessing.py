from ml.feature_extraction import extract_features

url = "https://paypal-login-secure-confirm-update.com/login?session=123&auth=true"

features = extract_features(url)
print(features)
