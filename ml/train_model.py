import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "raw" / "processed" / "data_processed.csv"
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


def train_model():
    print(f"📌 Loading processed dataset from: {PROCESSED_DATA}")

    df = pd.read_csv(PROCESSED_DATA)

    if "label" not in df.columns:
        raise ValueError("❌ 'label' column missing in processed dataset")

    # Only numeric columns
    df_numeric = df.select_dtypes(include=['number'])

    # Split features and labels
    X = df_numeric.drop(columns=["label"])
    y = df_numeric["label"]

    print("📌 Splitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("📌 Training RandomForest model...")
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )

    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"✅ Model trained! Test Accuracy: {accuracy:.4f}")

    print(f"📌 Saving model to: {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)

    print("🎉 Training pipeline complete!")


if __name__ == "__main__":
    train_model()
