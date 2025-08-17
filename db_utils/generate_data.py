# Creates a small listings CSV for test data
# Synthetic data for building pipelines without needing production access. Uses SF city coordinates

import csv
import random
import uuid
from datetime import datetime, timedelta

LAT_MIN, LAT_MAX = 37.70, 37.82
LON_MIN, LON_MAX = -122.52, -122.36

TITLES = ["Cozy Cabin", "Sunny Loft", "Quiet Bungalow", "Beachside Studio", "Downtown 1BR"]
TAGS = [["kid-friendly", "family"], ["beach", "romantic"], ["work-friendly", "fast-wifi"], ["pet-friendly"], ["budget"]]
CATEGORIES = ["cabin", "apartment", "house", "studio"]

def get_random_location():
    return round(random.uniform(LAT_MIN, LAT_MAX), 6), round(random.uniform(LON_MIN, LON_MAX), 6)

def get_random_price():
    return round(random.uniform(50, 350), 2)

def get_random_rating():
    return round(random.uniform(3.0, 5.0), 2)

def get_random_reviews():
    random_int = random.randint(0, 500)
    snippets = []
    for i in range(min(3, random_int)):
        snippets.append(f"Review {i+1}: Great stay - {random.choice(['clean', 'cozy', 'convenient'])}.")
    return " ; ".join(snippets)

def create_listing(i):
    lat, long = get_random_location()
    title = random.choice(TITLES)
    tags = ";".join(random.choice(TAGS))
    category = random.choice(CATEGORIES)
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": f"Description about {title}. This is listing #{i}.",
        "price": get_random_price(),
        "currency": "USD",
        "latitude": lat,
        "longitude": long,
        "rating": get_random_rating(),
        "num_reviews": random.randint(0, 500),
        "tags": tags,
        "image_urls": f"https://example.com/{i}.jpg",
        "top_reviews": get_random_reviews(),
        "category": category,
        "last_updated": (datetime.utcnow() - timedelta(days=random.randint(0, 365))).date().isoformat()
    }

def main(count=500):
    out_csv = "data/listings.csv"
    keys = ["id", "title", "description", "price", "currency", "latitude", "longitude", "rating", "num_reviews", "tags", "image_urls", "top_reviews", "category", "last_updated"]
    with open(out_csv, "w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for i in range(count):
            writer.writerow(create_listing(i))

if __name__ == "__main__":
    main()