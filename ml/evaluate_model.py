import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "raw" / "processed" / "data_processed.csv"
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


def evaluate_model():
    print(f"📌 Loading dataset from: {PROCESSED_DATA}")
    df = pd.read_csv(PROCESSED_DATA)

    if "label" not in df.columns:
        raise ValueError("❌ 'label' column missing in processed dataset")

    # Same cleanup as training
    X = df.drop(columns=["label", "url", "domain", "tld"])
    y = df["label"]

    print(f"📌 Loading trained model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    print("📌 Making predictions…")
    y_pred = model.predict(X)

    accuracy = accuracy_score(y, y_pred)
    print(f"✅ Accuracy: {accuracy:.4f}\n")

    print("📌 Classification Report:")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    evaluate_model()
