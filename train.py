
import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------
# TEXT CLEANING FUNCTION
# -------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# -------------------------
# TRAIN MODELS
# -------------------------
def train_models():
    df = pd.read_csv("data/dataset.csv")

    # Clean text
    df["text"] = df["text"].apply(clean_text)

    # TF-IDF with semantic improvement (n-grams)
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),   # BIG upgrade (captures phrases)
        max_features=5000
    )

    X = vectorizer.fit_transform(df["text"])

    # Department model
    dept_model = LogisticRegression(max_iter=200)
    dept_model.fit(X, df["label"])

    # Priority model
    priority_model = LogisticRegression(max_iter=200)
    priority_model.fit(X, df["priority"])

    # SAVE MODELS
    pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))
    pickle.dump(dept_model, open("model/dept_model.pkl", "wb"))
    pickle.dump(priority_model, open("model/priority_model.pkl", "wb"))

    print("✅ Models trained and saved!")

    return vectorizer, dept_model, priority_model


# Run once to train
if __name__ == "__main__":
    train_models()

