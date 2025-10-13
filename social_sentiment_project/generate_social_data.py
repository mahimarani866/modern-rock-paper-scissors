import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)


def generate_social_posts(n_posts: int = 12000) -> pd.DataFrame:
    """
    Generate a synthetic social media dataset with sentiment labels.

    Each row is one post with:
    - platform
    - brand
    - created_at
    - text
    - sentiment (Positive / Negative / Neutral)
    """

    brands = ["NovaPhone", "SkyWear", "FreshFizz", "QuickEats"]
    platforms = ["Twitter", "Instagram", "Reddit", "YouTube", "LinkedIn"]

    positive_templates = [
        "Absolutely love {brand}! {feature} 😍",
        "{brand} just nailed it again. {feature} #happycustomer",
        "Honestly, {brand} has the best {feature}. Totally worth it.",
        "So impressed with {brand} right now – {feature} made my day.",
        "Shoutout to {brand} for amazing {feature}! ⭐⭐⭐⭐⭐",
    ]

    negative_templates = [
        "Really disappointed with {brand}. {feature} was a mess. 😡",
        "{brand} seriously needs to fix their {feature}.",
        "Worst experience with {brand} so far – {feature} is terrible.",
        "I regret choosing {brand}. {feature} completely failed.",
        "How can {brand} ship such bad {feature}? Never again.",
    ]

    neutral_templates = [
        "Tried {brand} today, still forming an opinion about their {feature}.",
        "Saw a new update from {brand} about {feature}. Interesting.",
        "Anyone else using {brand} for {feature}? Curious about your thoughts.",
        "{brand} just launched something around {feature}.",
        "Reading mixed reviews about {brand}'s {feature}.",
    ]

    brand_features = {
        "NovaPhone": ["battery life", "camera quality", "5G performance", "design"],
        "SkyWear": ["delivery speed", "fabric quality", "return policy", "sizing"],
        "FreshFizz": ["flavour options", "pricing", "sugar content", "packaging"],
        "QuickEats": ["delivery time", "order accuracy", "customer support", "offers"],
    }

    rows = []
    start_date = datetime(2025, 1, 1)

    for i in range(n_posts):
        brand = np.random.choice(brands)
        platform = np.random.choice(platforms)

        # random date within 90 days
        offset_days = np.random.randint(0, 90)
        offset_minutes = np.random.randint(0, 24 * 60)
        created_at = start_date + timedelta(days=int(offset_days), minutes=int(offset_minutes))

        # choose sentiment with some imbalance
        sentiment = np.random.choice(
            ["Positive", "Negative", "Neutral"],
            p=[0.5, 0.25, 0.25],
        )

        if sentiment == "Positive":
            template = np.random.choice(positive_templates)
        elif sentiment == "Negative":
            template = np.random.choice(negative_templates)
        else:
            template = np.random.choice(neutral_templates)

        feature = np.random.choice(brand_features[brand])

        text = template.format(brand=brand, feature=feature)

        # add a few hashtags / emojis randomly
        extras = [
            "",
            " #"+brand.lower(),
            " #"+feature.replace(" ", ""),
            " 😊",
            " 😬",
        ]
        text = text + np.random.choice(extras)

        rows.append(
            {
                "post_id": f"POST_{i+1:05d}",
                "platform": platform,
                "brand": brand,
                "created_at": created_at.isoformat(timespec="seconds"),
                "text": text,
                "sentiment": sentiment,
            }
        )

    df = pd.DataFrame(rows)
    return df


def main():
    os.makedirs("data", exist_ok=True)
    df_posts = generate_social_posts(n_posts=12000)
    output_path = "data/social_posts_raw.csv"
    df_posts.to_csv(output_path, index=False)

    print(f"✅ Saved dataset to {output_path}")
    print("First 5 rows:\n", df_posts.head())
    print("\nSentiment distribution:")
    print(df_posts["sentiment"].value_counts(normalize=True).round(3))


if __name__ == "__main__":
    main()
