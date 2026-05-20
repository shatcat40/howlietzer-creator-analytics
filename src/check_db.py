import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "howlietzer_analytics.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in database:")
    print(tables)

    cursor.execute("SELECT * FROM content_inventory LIMIT 5;")
    rows = cursor.fetchall()

    print("\nFirst 5 rows:")
    for row in rows:
        print(row)