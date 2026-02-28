"""
Application entry point.

This file is intentionally kept slim — it wires together middleware,
routes, and startup tasks. All business logic lives in /services,
all route handlers in /routes, and all config in config.py.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_TITLE, CORS_ORIGINS
from database import init_api_key
from services.model_service import load_model
from routes import health, predict, report

# ------------------------------------
# App Initialization
# ------------------------------------
app = FastAPI(title=APP_TITLE)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Startup: load model & seed data
# ------------------------------------
model = load_model()
predict.set_model(model)
init_api_key()

# ------------------------------------
# Register routers
# ------------------------------------
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(report.router)