"""
app.py

Flask backend for the Fake News Detection System.

Routes:
    GET  /            -> Home page (input form)
    GET  /about       -> About page
    POST /predict     -> JSON API: { "text": "..." } -> { "prediction": "...", "confidence": ... }
    GET  /health      -> Health check for the ML model

Run with:
    python app.py
"""

import os
import re
import string

import joblib
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests (useful if templates are ever served separately)

MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

model = None
vectorizer = None
model_load_error = None

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    else:
        model_load_error = (
            "model.pkl / vectorizer.pkl not found. "
            "Run 'python train_model.py' first."
        )
except Exception as exc:  # pragma: no cover
    model_load_error = f"Failed to load model: {exc}"


def clean_text(text: str) -> str:
    """Same cleaning logic used during training — must stay in sync."""
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/health")
def health():
    if model is None or vectorizer is None:
        return jsonify({"status": "error", "message": model_load_error}), 503
    return jsonify({"status": "ok", "message": "Model loaded and ready."})


@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return jsonify({"error": model_load_error or "Model not loaded."}), 503

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please provide non-empty 'text' in the request body."}), 400

    if len(text) < 10:
        return jsonify({"error": "Please enter a longer piece of text (at least 10 characters)."}), 400

    cleaned = clean_text(text)
    features = vectorizer.transform([cleaned])

    prediction = model.predict(features)[0]              # 0 = FAKE, 1 = REAL
    probabilities = model.predict_proba(features)[0]      # [P(fake), P(real)]
    confidence = round(float(max(probabilities)) * 100, 2)

    label = "REAL" if prediction == 1 else "FAKE"

    return jsonify({
        "prediction": label,
        "confidence": confidence,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
