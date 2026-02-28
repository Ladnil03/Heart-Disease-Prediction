"""
API key authentication helper.

Verifies an incoming API key against the database (or falls back
to a simple env-var comparison when MongoDB is unavailable).
"""

from fastapi import HTTPException
from database import get_db_connection
from config import MONGO_URI, API_KEY_VALUE, API_KEYS_COLLECTION, logger


def verify_api_key(api_key: str) -> None:
    """Raise HTTPException(401) if the provided key is invalid."""

    if not MONGO_URI:
        # Fallback: compare against the env-var value directly
        if api_key != API_KEY_VALUE:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        return

    try:
        with get_db_connection() as db:
            api_keys_col = db[API_KEYS_COLLECTION]
            if not api_keys_col.find_one({"api_key": api_key}):
                raise HTTPException(status_code=401, detail="Invalid API Key")
    # amazonq-ignore-next-line
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying API key: {str(e)}")
        raise HTTPException(status_code=503, detail="Authentication service unavailable")
