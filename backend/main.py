from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
import joblib
import numpy as np
import os
from dotenv import load_dotenv
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
API_KEY_VALUE = os.getenv("API_KEY", "Heart_disease_api")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

# App Initialization 
app = FastAPI(title="Heart Disease Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model with error handling
try:
    # amazonq-ignore-next-line
    model = joblib.load("heart_model.pkl")
    logger.info("Model loaded successfully")
# amazonq-ignore-next-line
except FileNotFoundError:
    logger.error("Model file 'heart_model.pkl' not found")
    raise FileNotFoundError("Model file 'heart_model.pkl' not found. Please ensure the model is trained and saved.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise Exception(f"Error loading model: {str(e)}")

# MongoDB connection with context manager
@contextmanager
def get_db_connection():
    client = None
    try:
        client = MongoClient(MONGO_URI)
        db = client["heart_disease_db"]
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=503, detail="Database service unavailable")
    finally:
        if client:
            client.close()

# Initialize API key in database
try:
    with get_db_connection() as db:
        api_keys_col = db["api_keys"]
        # amazonq-ignore-next-line
        if api_keys_col.count_documents({"api_key": API_KEY_VALUE}) == 0:
            api_keys_col.insert_one({"api_key": API_KEY_VALUE})
            logger.info("API key initialized in database")
except Exception as e:
    logger.warning(f"Could not initialize API key: {str(e)}")

# ----------------------------------
# Request Schema with validation
# ----------------------------------
class HeartInput(BaseModel):
    age: int = Field(ge=1, le=150, description="Age must be between 1 and 150")
    sex: int = Field(ge=0, le=1, description="Sex: 0=Female, 1=Male")
    cp: int = Field(ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: int = Field(ge=50, le=300, description="Resting blood pressure (50-300)")
    chol: int = Field(ge=100, le=600, description="Serum cholesterol (100-600)")
    fbs: int = Field(ge=0, le=1, description="Fasting blood sugar > 120 mg/dl (0 or 1)")
    restecg: int = Field(ge=0, le=2, description="Resting ECG results (0-2)")
    thalach: int = Field(ge=60, le=250, description="Maximum heart rate (60-250)")
    exang: int = Field(ge=0, le=1, description="Exercise induced angina (0 or 1)")
    oldpeak: float = Field(ge=0.0, le=10.0, description="ST depression (0.0-10.0)")
    slope: int = Field(ge=0, le=2, description="Slope of peak exercise ST segment (0-2)")
    ca: int = Field(ge=0, le=3, description="Number of major vessels (0-3)")
    thal: int = Field(ge=1, le=3, description="Thalassemia (1-3)")

# ----------------------------------
# API Key Validation with error handling
# ----------------------------------
def verify_api_key(api_key: str):
    try:
        with get_db_connection() as db:
            api_keys_col = db["api_keys"]
            if not api_keys_col.find_one({"api_key": api_key}):
                raise HTTPException(status_code=401, detail="Invalid API Key")
    # amazonq-ignore-next-line
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}")
        raise HTTPException(status_code=503, detail="Authentication service unavailable")

# ----------------------------------
# Prediction Endpoint with comprehensive error handling
# ----------------------------------
@app.post("/predict")
def predict(data: HeartInput, api_key: str = Header(..., alias="api-key")):
    # amazonq-ignore-next-line
    verify_api_key(api_key)

    try:
        # Prepare input for model (all 13 features)
        X = np.array([[
            data.age, data.sex, data.cp, data.trestbps, data.chol,
            data.fbs, data.restecg, data.thalach, data.exang,
            data.oldpeak, data.slope, data.ca, data.thal
        ]])

        # Model prediction with error handling
        risk_prob = model.predict_proba(X)[0][1]

        # Determine risk level
        if risk_prob < 0.3:
            risk_level = "Low"
        elif risk_prob < 0.6:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        # Save to MongoDB Atlas using context manager and improved data mapping
        try:
            with get_db_connection() as db:
                predictions_col = db["predictions"]
                prediction_data = {
                    **data.dict(),
                    "risk_probability": float(risk_prob),
                    "risk_level": risk_level
                }
                predictions_col.insert_one(prediction_data)
        except Exception as e:
            logger.error(f"Error saving prediction to database: {str(e)}")
            # Continue execution even if database save fails

        return {
            "risk_probability": round(float(risk_prob), 2),
            "risk_level": risk_level
        }
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction service error")