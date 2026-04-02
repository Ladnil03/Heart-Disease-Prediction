"""
ML Model service.

Handles loading the trained model from disk and running predictions.
Keeping model I/O isolated here makes it easy to swap models or
add versioning later.
"""
# Fixes: FIX-8 (corrupted model handling), FIX-9 (NaN/Inf guard in prepare_input)

import os
import pickle
import joblib
import numpy as np
from config import MODEL_PATH, RISK_THRESHOLDS, FEATURE_NAMES, logger


def load_model():
    """
    Load the pickled ML model.

    Raises
    ------
    FileNotFoundError
        When the model file does not exist on disk.
    RuntimeError
        When the file exists but is corrupted / incompatible, or when the
        loaded object is not a valid scikit-learn classifier.
    """
    path = MODEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file '{path}' not found. Run model/preprocessing_training.py first."
        )
    try:
        # amazonq-ignore-next-line
        model = joblib.load(path)
    except (pickle.UnpicklingError, EOFError, ValueError) as e:
        raise RuntimeError(
            f"Model file '{path}' is corrupted or incompatible: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading model: {e}") from e

    # Smoke-test: confirm the model has predict_proba
    if not hasattr(model, "predict_proba"):
        raise RuntimeError(
            f"Loaded object from '{path}' is not a valid classifier "
            "(missing predict_proba)."
        )
    logger.info(f"Model loaded successfully from '{path}'")
    return model


def prepare_input(data) -> np.ndarray:
    """Convert a HeartInput schema instance into a numpy array for the model."""
    arr = np.array([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang,
        data.oldpeak, data.slope, data.ca, data.thal,
    ]], dtype=np.float64)
    if not np.all(np.isfinite(arr)):
        raise ValueError("Input contains NaN or Inf values after conversion")
    return arr


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
