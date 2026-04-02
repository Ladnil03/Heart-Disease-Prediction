"""
Application entry point.

This file is intentionally kept slim — it wires together middleware,
routes, and startup tasks. All business logic lives in /services,
all route handlers in /routes, and all config in config.py.
"""
# Fixes: FIX-1 (GET /api/token endpoint), FIX-3 (CORS origins from config),
#        FIX-7 (DB shutdown handler), FIX-8 (critical startup error + sys.exit)

import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from config import APP_TITLE, CORS_ORIGINS, logger
from database import init_api_key, close_client
from services.model_service import load_model
from routes import health, predict, report
from auth import create_signed_token, check_token_rate_limit

# ------------------------------------
# App Initialization
# ------------------------------------
app = FastAPI(title=APP_TITLE)

# CORS
# Wildcard "*" is only present in CORS_ORIGINS when ALLOW_ALL_ORIGINS=true
# (see config.py). It is disabled by default in production. (FIX-3)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Startup: load model & seed data (FIX-8)
# ------------------------------------
try:
    model = load_model()
except (FileNotFoundError, RuntimeError) as e:
    logger.critical(f"STARTUP FAILED — could not load model: {e}")
    sys.exit(1)

predict.set_model(model)
init_api_key()

# ------------------------------------
# Register routers
# ------------------------------------
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(report.router)


# ------------------------------------
# Token endpoint (FIX-1)
# ------------------------------------
@app.get("/api/token", tags=["Auth"])
async def get_token(request: Request):
    """
    Issue a short-lived signed token for browser clients.
    Rate-limited to prevent abuse (in-memory TTL dict, no extra deps).
    """
    client_ip = request.client.host if request.client else "unknown"
    check_token_rate_limit(client_ip)
    token = create_signed_token()
    return {"token": token}


# ------------------------------------
# Shutdown: close DB pool (FIX-7)
# ------------------------------------
@app.on_event("shutdown")
def shutdown_db():
    close_client()