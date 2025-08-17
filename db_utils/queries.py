# query_examples.py
import sqlite3
import pandas as pd
from math import radians, sin, cos, asin, sqrt

DB = "listings.db"
TABLE = "listings"

def haversine_km(lat1, lon1, lat2, lon2):
    # returns distance
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 6371.0 * 2 * asin(sqrt(a))

def get_listing_by_id(listing_id):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE} WHERE id = ?", conn, params=(listing_id,))
    conn.close()
    return df

def get_price_range(min_p, max_p, limit=50):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE} WHERE price BETWEEN ? AND ? ORDER BY price LIMIT ?;", conn, params=(min_p, max_p, limit))
    conn.close()
    return df

def get_nearby(lat, lon, radius_km=5.0):
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * abs(cos(radians(lat))) if abs(cos(radians(lat)))>0.01 else 1)
    lat_min, lat_max = lat - lat_delta, lat + lat_delta
    lon_min, lon_max = lon - lon_delta, lon + lon_delta
    conn = sqlite3.connect(DB)
    query = f"SELECT * FROM {TABLE} WHERE latitude BETWEEN ? AND ? AND longitude BETWEEN ? AND ?;"
    df = pd.read_sql_query(query, conn, params=(lat_min, lat_max, lon_min, lon_max))
    conn.close()
    if df.empty:
        return df
    df['distance_km'] = df.apply(lambda r: haversine_km(lat, lon, r['latitude'], r['longitude']), axis=1)
    return df[df['distance_km'] <= radius_km].sort_values('distance_km').reset_index(drop=True)

if __name__ == "__main__":
    print("Pick one sample id from DB:")
    conn = sqlite3.connect(DB)
    cur = conn.execute("SELECT id, title, price, latitude, longitude FROM listings LIMIT 5;")
    for row in cur.fetchall():
        print(row)
    conn.close()

    example_df = get_price_range(100, 200)
    print(f"\nFound {len(example_df)} listings between $100 and $200. Sample:")
    print(example_df[['id','title','price']].head())

    # Nearby example (pick coordinates near stored sample)
    lat_sample, lon_sample = 37.77, -122.41
    near = get_nearby(lat_sample, lon_sample, radius_km=3.0)
    print(f"\nNearby listings within 3km of ({lat_sample},{lon_sample}): {len(near)}")
    print(near[['id','title','price','distance_km']].head())
