"""
Health-check route.

A lightweight endpoint to verify the API is running —
used by monitoring, load balancers, and the frontend connection test.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API", "status": "running"}
