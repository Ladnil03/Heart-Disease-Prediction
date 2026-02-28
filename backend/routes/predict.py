"""
Prediction route.

Accepts patient data, runs the ML model, computes SHAP explanations,
and optionally persists the prediction to MongoDB.
"""

from fastapi import APIRouter, Header, HTTPException
from schemas import HeartInput
from auth import verify_api_key
from services.model_service import predict
from services.shap_service import compute_shap
from database import get_db_connection
from config import MONGO_URI, PREDICTIONS_COLLECTION, logger

router = APIRouter(prefix="/api", tags=["Prediction"])

# The loaded model instance is injected via app state (see main.py)
_model = None


def set_model(model):
    """Called once at startup to inject the loaded model."""
    global _model
    _model = model


@router.post("/predict")
def predict_endpoint(data: HeartInput, api_key: str = Header(..., alias="api-key")):
    # amazonq-ignore-next-line
    verify_api_key(api_key)

    try:
        # 1. Model prediction
        result = predict(_model, data)

        # 2. SHAP explainability
        shap_result = compute_shap(_model, result["X"])

        # 3. Persist to MongoDB (non-blocking — failures don't stop the response)
        if MONGO_URI:
            try:
                with get_db_connection() as db:
                    predictions_col = db[PREDICTIONS_COLLECTION]
                    prediction_data = {
                        **data.dict(),
                        "risk_probability": result["risk_probability"],
                        "risk_level": result["risk_level"],
                    }
                    predictions_col.insert_one(prediction_data)
            except Exception as e:
                logger.error(f"Error saving prediction to database: {str(e)}")

        # 4. Build response
        return {
            "risk_probability": result["risk_probability"],
            "risk_level": result["risk_level"],
            **shap_result,
        }

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction service error")
