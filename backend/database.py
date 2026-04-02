"""
Database module for MongoDB connection management.

Provides a module-level singleton connection pool and a context manager
for safe, reusable database connections. Also seeds initial API key data.
"""
# Fixes: FIX-7 (connection pool singleton)

from contextlib import contextmanager
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, API_KEYS_COLLECTION, API_KEY_VALUE, logger

# ------------------------------------
# Module-level singleton client
# ------------------------------------
_client: MongoClient | None = None


def get_client() -> MongoClient | None:
    """Return (and lazily create) the shared MongoClient connection pool."""
    global _client
    if _client is None and MONGO_URI:
        _client = MongoClient(
            MONGO_URI,
            maxPoolSize=10,
            serverSelectionTimeoutMS=5000,
        )
        logger.info("MongoDB connection pool created")
    return _client


def close_client() -> None:
    """Close the shared MongoClient (called on FastAPI shutdown)."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        logger.info("MongoDB connection pool closed")


@contextmanager
def get_db_connection():
    """Yield a MongoDB database handle from the shared pool."""
    client = get_client()
    if client is None:
        raise RuntimeError("No MongoDB URI configured")
    try:
        yield client[DB_NAME]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise


def init_api_key():
    """Ensure the default API key exists in the database."""
    if not MONGO_URI:
        return

    try:
        with get_db_connection() as db:
            api_keys_col = db[API_KEYS_COLLECTION]
            # amazonq-ignore-next-line
            if api_keys_col.count_documents({"api_key": API_KEY_VALUE}) == 0:
                api_keys_col.insert_one({"api_key": API_KEY_VALUE})
                logger.info("API key initialized in database")
    except Exception as e:
        logger.warning(f"Could not initialize API key: {str(e)}")
