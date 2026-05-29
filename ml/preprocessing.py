import pandas as pd
from pathlib import Path
from feature_extraction import extract_features

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR /"backend" / "data" / "raw" / "processed" / "data1.csv"
PROCESSED_DATA = BASE_DIR /"backend" / "data" / "raw" / "processed" / "data_processed.csv"

def process_dataset():
    print(f"Loading dataset from: {RAW_DATA}")
    df = pd.read_csv(RAW_DATA)

    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("❌ data.xlsx must contain 'url' and 'label' columns")

    print("Extracting features…")
    processed_rows = []

    for i, row in df.iterrows():
        url = row["url"]
        label = row["label"]

        if not isinstance(url, str) or url.strip() == "" or pd.isna(url):
            print(f"Skipping invalid URL at row {i}: {url}")
            continue

        try:
            features = extract_features(url)
            # Validate entropy type
            if not isinstance(features.get('entropy'), float):
                print(f"⚠️ Warning: entropy is {type(features['entropy'])} for {url}")
                features['entropy'] = float(features['entropy'])  # force conversion
            features["label"] = label
            processed_rows.append(features)
        except Exception as e:
            print(f"⚠️ Error processing row {i}: {e}")
            continue

    processed_df = pd.DataFrame(processed_rows)

    # Save with explicit comma separator and fixed float format
    processed_df.to_csv(PROCESSED_DATA, index=False, sep=',', float_format='%.6f')
    print(f"✅ Processing complete! Saved to:\n{PROCESSED_DATA}")

if __name__ == "__main__":
    process_dataset()
