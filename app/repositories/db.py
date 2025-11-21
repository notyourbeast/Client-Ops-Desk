from pymongo import MongoClient

from app.config import Config


_client = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(Config.MONGO_URI)
    return _client


def get_db():
    client = get_client()
    return client["freelance_clienthub"]

