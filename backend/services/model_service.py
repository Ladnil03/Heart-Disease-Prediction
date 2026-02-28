"""
ML Model service.

Handles loading the trained model from disk and running predictions.
Keeping model I/O isolated here makes it easy to swap models or
add versioning later.
"""

import joblib
import numpy as np
from config import MODEL_PATH, RISK_THRESHOLDS, FEATURE_NAMES, logger


def load_model():
    """Load the pickled ML model. Raises on failure so the app refuses to start."""
    try:
        # amazonq-ignore-next-line
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully")
        return model
    except FileNotFoundError:
        logger.error(f"Model file '{MODEL_PATH}' not found")
        raise FileNotFoundError(
            f"Model file '{MODEL_PATH}' not found. "
            "Please ensure the model is trained and saved."
        )
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def prepare_input(data) -> np.ndarray:
    """Convert a HeartInput schema instance into a numpy array for the model."""
    return np.array([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal,
    ]])


def classify_risk(probability: float) -> str:
    """Map a probability to a human-readable risk level string."""
    if probability < RISK_THRESHOLDS["low"]:
        return "Low"
    elif probability < RISK_THRESHOLDS["moderate"]:
        return "Moderate"
    return "High"


def predict(model, data) -> dict:
    """
    Run a full prediction pipeline:
    1. Prepare input features.
    2. Get class probability from the model.
    3. Classify into Low / Moderate / High.

    Returns a dict with risk_probability and risk_level.
    """
    X = prepare_input(data)
    risk_prob = float(model.predict_proba(X)[0][1])
    risk_level = classify_risk(risk_prob)

    return {
        "X": X,
        "risk_probability": round(risk_prob, 2),
        "risk_level": risk_level,
    }
