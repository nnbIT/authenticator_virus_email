import pandas as pd
from pathlib import Path
from ml.feature_extraction import extract_features

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw" / "processed"/ "data.xlsx"
PROCESSED_DATA = BASE_DIR / "data" / "raw" / "processed" / "data_processed.csv"

def process_dataset():
    print(f"Loading dataset from: {RAW_DATA}")

    # Load raw csv (must contain: url,label)
    df = pd.read_excel(RAW_DATA)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("❌ data.csv must contain 'url' and 'label' columns")

    print("Extracting features…")

    processed_rows = []

    for _, row in df.iterrows():
        url = row["url"]
        label = row["label"]

        features = extract_features(url)
        features["label"] = label  # add label at the end

        processed_rows.append(features)

    # Convert to DataFrame
    processed_df = pd.DataFrame(processed_rows)

    # Save
    processed_df.to_csv(PROCESSED_DATA, index=False)
    print(f"✅ Processing complete! Saved to:\n{PROCESSED_DATA}")

if __name__ == "__main__":
    process_dataset()
