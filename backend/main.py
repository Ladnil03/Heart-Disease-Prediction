from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import joblib
import numpy as np
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# App Initialization 
app = FastAPI(title="Heart Disease Prediction API")

# Load ML Model
model = joblib.load("heart_model.pkl")

# MongoDB Atlas connection
client = MongoClient(MONGO_URI)
db = client["heart_disease_db"]

api_keys_col = db["api_keys"]
predictions_col = db["predictions"]

# Insert API key (Run once)
API_KEY_VALUE = "Heart_disease_api"

if api_keys_col.count_documents({"api_key": API_KEY_VALUE}) == 0:
    api_keys_col.insert_one({"api_key": API_KEY_VALUE})

# ----------------------------------
# Request Schema (13 features)
# ----------------------------------
class HeartInput(BaseModel):
    age: int
    sex: int
    cp: int              # chest pain type
    trestbps: int        # resting blood pressure
    chol: int            # serum cholesterol
    fbs: int             # fasting blood sugar > 120 mg/dl
    restecg: int         # resting electrocardiographic results
    thalach: int         # maximum heart rate achieved
    exang: int           # exercise induced angina
    oldpeak: float       # ST depression induced by exercise relative to rest
    slope: int           # slope of the peak exercise ST segment
    ca: int              # number of major vessels colored by fluoroscopy
    thal: int            # thalassemia (3 = normal; 6 = fixed defect; 7 = reversible defect)

# ----------------------------------
# API Key Validation
# ----------------------------------
def verify_api_key(api_key: str):
    if not api_keys_col.find_one({"api_key": api_key}):
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ----------------------------------
# Prediction Endpoint
# ----------------------------------
@app.post("/predict")
def predict(data: HeartInput, api_key: str = Header(...)):
    verify_api_key(api_key)

    # Prepare input for model (all 13 features)
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

    # Save to MongoDB Atlas
    predictions_col.insert_one({
        "age": data.age,
        "sex": data.sex,
        "cp": data.cp,
        "trestbps": data.trestbps,
        "chol": data.chol,
        "fbs": data.fbs,
        "restecg": data.restecg,
        "thalach": data.thalach,
        "exang": data.exang,
        "oldpeak": data.oldpeak,
        "slope": data.slope,
        "ca": data.ca,
        "thal": data.thal,
        "risk_probability": float(risk_prob),
        "risk_level": risk_level,
    })

    return {
        "risk_probability": round(float(risk_prob), 2),
        "risk_level": risk_level
    }
