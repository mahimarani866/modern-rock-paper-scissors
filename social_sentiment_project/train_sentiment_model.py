import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
import joblib


def main():
    # 1. Load data
    df = pd.read_csv("data/social_posts_raw.csv")
    print("Loaded data:", df.shape)
    print(df.head())

    X = df["text"]
    y = df["sentiment"]

    # 2. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 3. Build NLP pipeline: TF-IDF + Logistic Regression
    text_clf = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=5,
                    max_df=0.9,
                    stop_words="english",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    multi_class="multinomial",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # 4. Train model
    print("\nTraining model...")
    text_clf.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = text_clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print("\n===== Model Performance =====")
    print("Accuracy:", round(acc, 4))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=3))

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred, labels=["Positive", "Negative", "Neutral"]))

    # 6. Retrain on full data and save the model
    print("\nRetraining on full dataset...")
    text_clf.fit(X, y)

    os.makedirs("models", exist_ok=True)
    model_path = "models/sentiment_pipeline.joblib"
    joblib.dump(text_clf, model_path)
    print(f"✅ Saved trained pipeline to {model_path}")

    # 7. Brand-level sentiment summary (for dashboards / insights)
    brand_sent = (
        df.groupby(["brand", "sentiment"])["post_id"]
        .count()
        .unstack(fill_value=0)
        .reset_index()
    )

    # ensure columns exist
    for label in ["Positive", "Negative", "Neutral"]:
        if label not in brand_sent.columns:
            brand_sent[label] = 0

    brand_sent["total_posts"] = (
        brand_sent["Positive"] + brand_sent["Negative"] + brand_sent["Neutral"]
    )

    brand_sent["positive_pct"] = (brand_sent["Positive"] / brand_sent["total_posts"]).round(3)
    brand_sent["negative_pct"] = (brand_sent["Negative"] / brand_sent["total_posts"]).round(3)
    brand_sent["neutral_pct"] = (brand_sent["Neutral"] / brand_sent["total_posts"]).round(3)

    summary_path = "data/brand_sentiment_summary.csv"
    brand_sent.to_csv(summary_path, index=False)

    print(f"\n✅ Saved brand sentiment summary to {summary_path}")
    print(brand_sent)


if __name__ == "__main__":
    main()
