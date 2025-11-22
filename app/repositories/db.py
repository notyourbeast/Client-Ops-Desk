import os
from pymongo import MongoClient

from app.config import Config


_client = None
_use_mock = os.environ.get('FCH_USE_MOCK_DB', 'false').lower() == 'true'


def get_client():
    global _client
    if _use_mock:
        return None
    if _client is None:
        try:
            _client = MongoClient(Config.MONGO_URI) if Config.MONGO_URI else None
        except Exception:
            _client = None
    return _client


def get_db():
    if _use_mock or not Config.MONGO_URI or get_client() is None:
        from app.repositories.mock_db import get_mock_db
        return get_mock_db()
    client = get_client()
    return client["freelance_clienthub"]

