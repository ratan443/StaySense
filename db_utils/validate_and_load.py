# Read the CSV
# Validate columns
# Save Parquet (Parquet stores columnar data efficiently. Faster to read only needed columns and better for large files)
# Write to SQLite

import pandas as pd
import sqlite3
import os

CSV = "listings.csv"
PARQUET = "listings.parquet"
DB = "listings.db"
TABLE = "listings"

REQUIRED_COLUMNS = ["id","title","description","price","currency","latitude","longitude","rating","num_reviews","tags","image_urls","top_reviews","category","last_updated"]

def validate_columns(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    assert not missing, f"Missing columns: {missing}"

def validate_ids(df):
    dup = df['id'].duplicated().sum()
    assert dup == 0, f"Duplicate ids: {dup}"

def validate_lat_long(df):
    assert df['latitude'].between(-90, 90).all(), "Latitude out of range"
    assert df['longitude'].between(-180, 180).all(), "Longitude out of range"

def validate_price(df):
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    assert df['price'].notnull().all(), "Price is not numeric"
    assert (df['price'] > 0).all(), "Price <= 0 found"

def validate_rating(df):
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    assert df['rating'].between(0,5).all(), "Rating out of range"

def validator(df: pd.DataFrame):
    validate_columns(df)
    validate_ids(df)
    validate_lat_long(df)
    validate_price(df)
    validate_rating(df)

    return df

def main():
    assert os.path.exists(CSV), f"{CSV} not found. Run generator first."
    df = pd.read_csv(CSV)
    df = validator(df)

    # Save Parquet
    df.to_parquet(PARQUET, index=False)
    print(f"Saved Parquet: {PARQUET}")

    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    df.to_sql(TABLE, conn, index=False)

    # Create indexes (Why indices? Speed)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_price ON listings(price);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_rating ON listings(rating);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lat ON listings(latitude);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lon ON listings(longitude);")
    conn.commit()
    conn.close()
    print(f"Saved SQLite DB: {DB}")

if __name__ == "__main__":
    main()
