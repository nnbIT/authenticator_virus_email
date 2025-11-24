import pandas as pd
from pathlib import Path
from ml.feature_extraction import extract_features

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw" / "processed" / "data.xlsx"
PROCESSED_DATA = BASE_DIR / "data" / "raw" / "processed" / "data_processed.csv"

def process_dataset():
    print(f"Loading dataset from: {RAW_DATA}")

    # Load dataset (Excel or CSV)
    df = pd.read_excel(RAW_DATA)

    # Ensure required columns exist
    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("❌ data.xlsx must contain 'url' and 'label' columns")

    print("Extracting features…")

    processed_rows = []

    for i, row in df.iterrows():
        url = row["url"]
        label = row["label"]

        # Skip missing or invalid URLs
        if not isinstance(url, str) or url.strip() == "" or pd.isna(url):
            print(f"Skipping invalid URL at row {i}: {url}")
            continue

        try:
            features = extract_features(url)
            features["label"] = label
            processed_rows.append(features)

        except Exception as e:
            print(f"⚠️ Error processing row {i}: {e}")
            continue

    # Convert to DataFrame
    processed_df = pd.DataFrame(processed_rows)

    # Save processed output
    processed_df.to_csv(PROCESSED_DATA, index=False)
    print(f"✅ Processing complete! Saved to:\n{PROCESSED_DATA}")

if __name__ == "__main__":
    process_dataset()
