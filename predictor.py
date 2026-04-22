from model.train import train_models
from textblob import TextBlob

vectorizer, dept_model, priority_model = train_models()

def predict(text):
    text_lower = text.lower()
    X = vectorizer.transform([text])

    dept = dept_model.predict(X)[0]
    priority = priority_model.predict(X)[0]

    # Confidence score
    probs = dept_model.predict_proba(X)
    confidence = max(probs[0])

    # Rule-based override
    if "fraud" in text_lower or "unauthorized" in text_lower:
        return "Fraud & Security", "High", confidence

    # Sentiment boost
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment < -0.5:
        priority = "High"

    return dept, priority, confidence