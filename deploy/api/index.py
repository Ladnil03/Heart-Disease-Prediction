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
    logger.warning("MONGO_URI not found. Database features will be disabled.")
    MONGO_URI = None

# App Initialization 
app = FastAPI(title="Heart Disease Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model with error handling
model = None
try:
    # Try to load from current directory first (Vercel deployment)
    model_path = "heart_model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        logger.info(f"Model loaded successfully from {model_path}")
    else:
        raise FileNotFoundError("Model file not found")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    # Don't raise exception here, handle it in the endpoint

# MongoDB connection with context manager
@contextmanager
def get_db_connection():
    client = None
    try:
        if MONGO_URI:
            client = MongoClient(MONGO_URI)
            db = client["heart_disease_db"]
            yield db
        else:
            yield None
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        yield None
    finally:
        if client:
            client.close()

# Request Schema with validation
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

# API Key Validation
def verify_api_key(api_key: str):
    if api_key != API_KEY_VALUE:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API", "status": "running"}

@app.post("/predict")
def predict(data: HeartInput, api_key: str = Header(..., alias="api-key")):
    verify_api_key(api_key)

    if model is None:
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        # Prepare input for model
        X = np.array([[
            data.age, data.sex, data.cp, data.trestbps, data.chol,
            data.fbs, data.restecg, data.thalach, data.exang,
            data.oldpeak, data.slope, data.ca, data.thal
        ]])

        # Model prediction
        risk_prob = model.predict_proba(X)[0][1]

        # Determine risk level
        if risk_prob < 0.3:
            risk_level = "Low"
        elif risk_prob < 0.6:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        # Save to MongoDB if available
        try:
            with get_db_connection() as db:
                if db is not None:
                    predictions_col = db["predictions"]
                    prediction_data = {
                        **data.dict(),
                        "risk_probability": float(risk_prob),
                        "risk_level": risk_level
                    }
                    predictions_col.insert_one(prediction_data)
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            # Continue without failing

        return {
            "risk_probability": round(float(risk_prob), 2),
            "risk_level": risk_level
        }
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction service error")

# Vercel handler function
def handler(request):
    from mangum import Mangum
    asgi_handler = Mangum(app)
    return asgi_handler(request)