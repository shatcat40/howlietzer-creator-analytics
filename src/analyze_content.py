import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "howlietzer_analytics.db"


def main():
    with sqlite3.connect(DB_PATH) as conn:

        # Load table into pandas
        df = pd.read_sql_query(
            "SELECT * FROM content_inventory",
            conn
        )

    print("\nCONTENT OVERVIEW")
    print(df.head())

    # Total views by category
    category_views = (
        df.groupby("category")["views"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTOTAL VIEWS BY CATEGORY")
    print(category_views)

    # Average clicks by content type
    avg_clicks = (
        df.groupby("content_type")["clicks"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\nAVERAGE CLICKS BY CONTENT TYPE")
    print(avg_clicks)

    # Engagement score
    df["engagement_score"] = (
        df["clicks"]
        + df["comments"] * 2
        + df["shares"] * 3
    )

    top_posts = (
        df[[
            "title",
            "category",
            "engagement_score"
        ]]
        .sort_values(
            by="engagement_score",
            ascending=False
        )
    )

    print("\nTOP PERFORMING POSTS")
    print(top_posts.head(10))


if __name__ == "__main__":
    main()