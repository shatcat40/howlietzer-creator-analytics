import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "howlietzer_analytics.db"
REPORTS_DIR = BASE_DIR / "reports"

REPORT_PATH = REPORTS_DIR / "monthly_creator_report.md"


def load_data() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            "SELECT * FROM content_inventory",
            conn
        )


def calculate_metrics(df: pd.DataFrame) -> dict:

    df = df.copy()

    df["engagement_score"] = (
        df["clicks"]
        + df["comments"] * 2
        + df["shares"] * 3
    )

    top_post = df.sort_values(
        "engagement_score",
        ascending=False
    ).iloc[0]

    metrics = {
        "total_views": int(df["views"].sum()),
        "total_clicks": int(df["clicks"].sum()),
        "total_comments": int(df["comments"].sum()),
        "total_shares": int(df["shares"].sum()),
        "average_engagement": round(df["engagement_score"].mean(), 2),
        "top_post_title": top_post["title"],
        "top_post_score": int(top_post["engagement_score"]),
        "best_category": (
            df.groupby("category")["views"]
            .sum()
            .idxmax()
        ),
        "best_content_type": (
            df.groupby("content_type")["clicks"]
            .mean()
            .idxmax()
        ),
    }

    return metrics


def generate_report(metrics: dict) -> str:

    report_date = datetime.now().strftime("%B %Y")

    report = f"""
# Howlietzer Monthly Creator Intelligence Report

## Reporting Period
{report_date}

## Executive Summary
This report summarizes creator analytics performance for Howlietzer Media Network.

## Top Performing Content
- Best post: {metrics['top_post_title']}
- Highest engagement score: {metrics['top_post_score']}
- Best category: {metrics['best_category']}
- Best content type: {metrics['best_content_type']}

## Key Metrics
- Total views: {metrics['total_views']}
- Total clicks: {metrics['total_clicks']}
- Total comments: {metrics['total_comments']}
- Total shares: {metrics['total_shares']}
- Average engagement score: {metrics['average_engagement']}

## Insights
1. The strongest category this month was {metrics['best_category']}.
2. The top-performing content type was {metrics['best_content_type']}.
3. {metrics['top_post_title']} generated the highest audience engagement.

## Recommended Creative Actions
1. Increase content production in the strongest-performing category.
2. Continue experimenting with high-engagement content types.
3. Monitor engagement trends month-over-month.

## Charts
See reports/figures for generated visualizations.

## Next Month Strategy
Focus on scaling high-performing content while testing new creative concepts.
"""

    return report


def save_report(report_text: str) -> None:

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(report_text)


def main():

    print("Generating monthly creator intelligence report...")

    df = load_data()

    metrics = calculate_metrics(df)

    report_text = generate_report(metrics)

    save_report(report_text)

    print(f"Report saved to: {REPORT_PATH}")
    print("Report generation complete.")


if __name__ == "__main__":
    main()