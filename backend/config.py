"""
Configuration module for the Heart Disease Prediction API.

Centralizes all environment variables, constants, and configuration values
so they are defined in one place and easily adjustable.
"""

import os
import logging
from dotenv import load_dotenv

# ------------------------------------
# Logging Configuration
# ------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------
# Environment Variables
# ------------------------------------
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
API_KEY_VALUE = os.getenv("API_KEY", "Heart_disease_api")

# ------------------------------------
# Application Settings
# ------------------------------------
APP_TITLE = "Heart Disease Prediction API"

# Model path (relative to the backend directory)
MODEL_PATH = "heart_model.pkl"

# Database names / collections
DB_NAME = "heart_disease_db"
PREDICTIONS_COLLECTION = "predictions"
API_KEYS_COLLECTION = "api_keys"

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://heart-disease-prediction-zj5z.vercel.app",
    "*",
]

# Risk level thresholds
RISK_THRESHOLDS = {
    "low": 0.3,
    "moderate": 0.6,
}

# Feature names used by the ML model (ordered)
FEATURE_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

# Human-readable feature labels (for reports & frontend)
FEATURE_LABELS = {
    "age": "Your Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Cholesterol Level",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG",
    "thalach": "Maximum Heart Rate",
    "exang": "Exercise Induced Angina",
    "oldpeak": "ST Depression",
    "slope": "ST Segment Slope",
    "ca": "Major Vessels",
    "thal": "Thalassemia",
}

# Clinical interpretations for each feature
FEATURE_INTERPRETATIONS = {
    "age": "Older age increases risk.",
    "sex": "Male sex increases risk.",
    "cp": "Certain chest pain types increase risk.",
    "trestbps": "Higher resting blood pressure increases risk.",
    "chol": "Higher cholesterol increases risk.",
    "fbs": "High fasting blood sugar increases risk.",
    "restecg": "Abnormal ECG increases risk.",
    "thalach": "Lower maximum heart rate increases risk.",
    "exang": "Exercise-induced angina increases risk.",
    "oldpeak": "Greater ST depression increases risk.",
    "slope": "Flat or downsloping ST segment increases risk.",
    "ca": "More major vessels increases risk.",
    "thal": "Certain thalassemia types increase risk.",
}

# Risk level colour mapping (hex) for PDF reports
RISK_COLORS = {
    "Low": "#27ae60",
    "Moderate": "#f39c12",
    "High": "#e74c3c",
}

# ------------------------------------
# Startup diagnostics
# ------------------------------------
logger.info(f"MONGO_URI loaded: {'Yes' if MONGO_URI else 'No'}")
logger.info(f"API_KEY loaded: {'Yes' if API_KEY_VALUE else 'No'}")
