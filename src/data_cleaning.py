
import pandas as pd
import os

# Project data folder
DATA_FOLDER = "data"

def load_datasets():
    """Load all five loyalty datasets."""

    files = {
        "customers": "customers.csv",
        "transactions": "transactions.csv",
        "earned": "points_earned.csv",
        "redeemed": "points_redeemed.csv",
        "expired": "points_expired.csv"
    }

    datasets = {}

    for name, filename in files.items():
        path = os.path.join(DATA_FOLDER, filename)

        if os.path.exists(path):
            datasets[name] = pd.read_csv(path)
            print(f"{filename} loaded successfully!")
        else:
            raise FileNotFoundError(f"Missing file: {path}")

    return datasets


def clean_datasets(datasets):
    """Clean missing and duplicate records."""

    cleaned = {}

    for name, df in datasets.items():

        original_count = len(df)

        # Remove duplicate records
        df = df.drop_duplicates()

        # Remove rows with missing required values
        df = df.dropna()

        cleaned[name] = df

        print(f"\n{name.upper()}")
        print("Original records:", original_count)
        print("Clean records:", len(df))

    return cleaned


if __name__ == "__main__":

    print("LOYALTYIQ DATA CLEANING PIPELINE")
    print("--------------------------------")

    datasets = load_datasets()

    cleaned_data = clean_datasets(datasets)

    print("\nAll datasets processed successfully!")
