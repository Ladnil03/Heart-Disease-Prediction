"""
Pydantic request/response schemas.

Defines the data shapes accepted and returned by each endpoint,
with field-level validation constraints.
"""

from pydantic import BaseModel, Field


class HeartInput(BaseModel):
    """Input schema for the /api/predict endpoint."""

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


class ReportRequest(BaseModel):
    """Input schema for the /api/report endpoint."""

    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    risk_probability: float
    risk_level: str
    shap_values: dict
    top_risk_factors: list
    base_value: float
