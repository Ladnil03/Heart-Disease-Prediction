"""
API key authentication helper.

Verifies an incoming API key against the database (or falls back
to a simple env-var comparison when MongoDB is unavailable).
Also accepts short-lived signed tokens issued by GET /api/token.
"""
# Fixes: FIX-1 (accept signed browser tokens in verify_api_key)

import hmac
import time
from fastapi import HTTPException
from database import get_db_connection
from config import MONGO_URI, API_KEY_VALUE, API_KEYS_COLLECTION, TOKEN_SECRET, TOKEN_TTL, logger


# ---------------------------------------------------------------------------
# Token helpers (FIX-1)
# ---------------------------------------------------------------------------

def _sign(payload: str) -> str:
    """Return an HMAC-SHA256 hex digest of *payload* using TOKEN_SECRET."""
    return hmac.new(TOKEN_SECRET.encode(), payload.encode(), "sha256").hexdigest()


def create_signed_token() -> str:
    """
    Create a short-lived signed token:  <expiry_unix_int>.<hmac>
    The token is valid for TOKEN_TTL seconds.
    """
    expiry = int(time.time()) + TOKEN_TTL
    payload = str(expiry)
    sig = _sign(payload)
    return f"{expiry}.{sig}"


def _verify_signed_token(token: str) -> bool:
    """Return True if *token* is a valid, unexpired signed token."""
    try:
        expiry_str, sig = token.split(".", 1)
        expiry = int(expiry_str)
    except (ValueError, AttributeError):
        return False

    if int(time.time()) > expiry:
        return False                     # expired

    expected = _sign(expiry_str)
    return hmac.compare_digest(expected, sig)


# ---------------------------------------------------------------------------
# Rate-limit store (simple in-memory TTL dict — no extra deps)
# ---------------------------------------------------------------------------
_rate_store: dict[str, list[float]] = {}
_RATE_WINDOW = 60          # seconds
_RATE_MAX_CALLS = 10       # max token-fetch calls per IP per window


def check_token_rate_limit(client_ip: str) -> None:
    """Raise 429 if *client_ip* has exceeded the token-fetch rate limit."""
    now = time.time()
    calls = _rate_store.get(client_ip, [])
    calls = [t for t in calls if now - t < _RATE_WINDOW]   # prune old
    if len(calls) >= _RATE_MAX_CALLS:
        raise HTTPException(status_code=429, detail="Too many token requests. Retry later.")
    calls.append(now)
    _rate_store[client_ip] = calls


# ---------------------------------------------------------------------------
# Main auth function
# ---------------------------------------------------------------------------

def verify_api_key(api_key: str) -> None:
    """
    Raise HTTPException(401) if the provided key is invalid.

    Accepts:
      1. A valid short-lived signed token (issued by GET /api/token).
      2. The raw env-var API key (server-to-server / fallback).
      3. A key stored in MongoDB (when MONGO_URI is configured and key is not the env key).
    """
    # 1. Accept valid signed browser tokens
    if _verify_signed_token(api_key):
        return

    # 2. Raw env-var key — accepted immediately regardless of DB state.
    #    This keeps server-to-server calls working even when MongoDB is unreachable.
    if api_key == API_KEY_VALUE:
        return

    # 3. No MONGO_URI configured — reject anything else outright
    if not MONGO_URI:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 4. MongoDB lookup (for keys provisioned directly in the DB)
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
