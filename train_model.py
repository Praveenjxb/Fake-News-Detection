"""
train_model.py

Loads the Fake/Real news dataset, cleans the text, converts it to TF-IDF
features, trains a Logistic Regression classifier, and saves the trained
model + vectorizer to disk (model.pkl / vectorizer.pkl) using joblib.

Run this once before starting the Flask app:
    python train_model.py
"""

import re
import string

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def clean_text(text: str) -> str:
    """Lowercase, strip URLs/punctuation/extra whitespace from a news text."""
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)   # remove URLs
    text = re.sub(r"<.*?>", " ", text)                    # remove HTML tags
    text = re.sub(r"[%s]" % re.escape(string.punctuation), " ", text)
    text = re.sub(r"\d+", " ", text)                      # remove digits
    text = re.sub(r"\s+", " ", text).strip()               # collapse whitespace
    return text


def load_dataset() -> pd.DataFrame:
    fake_df = pd.read_csv("dataset/Fake.csv")
    real_df = pd.read_csv("dataset/True.csv")

    fake_df["label"] = 0   # 0 = FAKE
    real_df["label"] = 1   # 1 = REAL

    df = pd.concat([fake_df, real_df], ignore_index=True)
    df = df.dropna(subset=["text"])
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle
    return df


def main():
    print("Loading dataset...")
    df = load_dataset()
    print(f"Total rows: {len(df)}  (fake={sum(df.label == 0)}, real={sum(df.label == 1)})")

    print("Cleaning text...")
    df["clean_text"] = df["text"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    print("Vectorizing with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc * 100:.2f}%\n")
    print(classification_report(y_test, y_pred, target_names=["FAKE", "REAL"]))

    print("Saving model.pkl and vectorizer.pkl ...")
    joblib.dump(model, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    print("Done.")


if __name__ == "__main__":
    main()
