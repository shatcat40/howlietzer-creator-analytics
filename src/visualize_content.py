import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "howlietzer_analytics.db"
FIGURES_DIR = BASE_DIR / "reports" / "figures"


def load_data() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM content_inventory", conn)


def save_views_by_category(df: pd.DataFrame) -> None:
    category_views = df.groupby("category")["views"].sum().sort_values(ascending=False)

    plt.figure()
    category_views.plot(kind="bar")
    plt.title("Views by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Views")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "views_by_category.png")
    plt.close()


def save_avg_clicks_by_content_type(df: pd.DataFrame) -> None:
    avg_clicks = df.groupby("content_type")["clicks"].mean().sort_values(ascending=False)

    plt.figure()
    avg_clicks.plot(kind="bar")
    plt.title("Average Clicks by Content Type")
    plt.xlabel("Content Type")
    plt.ylabel("Average Clicks")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "avg_clicks_by_content_type.png")
    plt.close()


def save_top_posts_by_engagement(df: pd.DataFrame) -> None:
    df = df.copy()
    df["engagement_score"] = df["clicks"] + df["comments"] * 2 + df["shares"] * 3

    top_posts = df.sort_values("engagement_score", ascending=False).head(10)

    plt.figure()
    plt.barh(top_posts["title"], top_posts["engagement_score"])
    plt.title("Top Posts by Engagement Score")
    plt.xlabel("Engagement Score")
    plt.ylabel("Title")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_posts_by_engagement.png")
    plt.close()


def save_views_vs_word_count(df: pd.DataFrame) -> None:
    plt.figure()
    plt.scatter(df["word_count"], df["views"])
    plt.title("Views vs. Word Count")
    plt.xlabel("Word Count")
    plt.ylabel("Views")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "views_vs_word_count.png")
    plt.close()


def main():
    print("Generating Howlietzer content analytics charts...")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    save_views_by_category(df)
    save_avg_clicks_by_content_type(df)
    save_top_posts_by_engagement(df)
    save_views_vs_word_count(df)

    print(f"Charts saved to: {FIGURES_DIR}")
    print("Visualization complete.")


if __name__ == "__main__":
    main()