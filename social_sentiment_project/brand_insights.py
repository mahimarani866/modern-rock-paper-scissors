import pandas as pd


def main():
    # Load the brand-level sentiment summary created earlier
    summary_path = "data/brand_sentiment_summary.csv"
    df = pd.read_csv(summary_path)

    print("=== Brand Sentiment Summary ===")
    print(df)

    # Find brand with highest positive %
    best_brand = df.sort_values("positive_pct", ascending=False).iloc[0]
    worst_brand = df.sort_values("negative_pct", ascending=False).iloc[0]

    print("\n=== Simple Insights ===")
    print(
        f"- Best overall sentiment: {best_brand['brand']} "
        f"({best_brand['positive_pct']*100:.1f}% positive, "
        f"{best_brand['negative_pct']*100:.1f}% negative)"
    )
    print(
        f"- Most negative sentiment: {worst_brand['brand']} "
        f"({worst_brand['negative_pct']*100:.1f}% negative)"
    )

    # If you want, you can add thresholds
    print("\nTip: These insights can be used for brand monitoring dashboards.")


if __name__ == "__main__":
    main()
