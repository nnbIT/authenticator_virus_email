import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"

model = joblib.load(MODEL_PATH)

def get_model():
    return model
