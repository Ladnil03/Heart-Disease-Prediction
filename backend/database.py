"""
Database module for MongoDB connection management.

Provides a context manager for safe, reusable database connections
and a helper to initialise seed data (e.g. API keys) on startup.
"""

from contextlib import contextmanager
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, API_KEYS_COLLECTION, API_KEY_VALUE, logger


@contextmanager
def get_db_connection():
    """Yield a MongoDB database handle, ensuring the client is closed afterwards."""
    client = None
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
    finally:
        if client:
            client.close()


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
