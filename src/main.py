import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "content_inventory.csv"
DB_PATH = BASE_DIR / "database" / "howlietzer_analytics.db"


def extract_data(csv_path: Path) -> pd.DataFrame:
    """Load raw content inventory CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    return pd.read_csv(csv_path)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare content inventory data."""
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower()

    if "publish_date" in df.columns:
        df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    if "word_count" in df.columns:
        df["word_count"] = pd.to_numeric(df["word_count"], errors="coerce").fillna(0).astype(int)

    return df


def load_data(df: pd.DataFrame, db_path: Path) -> None:
    """Load transformed data into SQLite."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql("content_inventory", conn, if_exists="replace", index=False)


def main():
    print("Starting Howlietzer content analytics ETL...")

    raw_df = extract_data(CSV_PATH)
    clean_df = transform_data(raw_df)
    load_data(clean_df, DB_PATH)

    print(f"Loaded {len(clean_df)} rows into {DB_PATH}")
    print("ETL complete.")


if __name__ == "__main__":
    main()