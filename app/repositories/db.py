import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from pymongo.server_api import ServerApi

from app.config import Config


_client = None
_db_name = os.environ.get('FCH_DB_NAME', 'freelance_clienthub')


def get_client():
    global _client
    if _client is None:
        if not Config.MONGO_URI:
            raise ConnectionFailure("MONGO_URI not set. Please configure MongoDB connection in .env file.")
        try:
            # Use ServerApi for MongoDB Atlas connections
            if Config.MONGO_URI and 'mongodb+srv://' in Config.MONGO_URI:
                # For Atlas, use ServerApi and handle SSL certificate issues
                _client = MongoClient(
                    Config.MONGO_URI, 
                    server_api=ServerApi('1'),
                    serverSelectionTimeoutMS=10000,
                    tlsAllowInvalidCertificates=True
                )
            else:
                _client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            _client.admin.command('ping')
        except (ConnectionFailure, ConfigurationError, Exception) as e:
            print(f"MongoDB connection error: {e}")
            raise ConnectionFailure(f"Failed to connect to MongoDB: {e}")
    return _client


def get_db():
    if not Config.MONGO_URI:
        raise ConnectionFailure("MONGO_URI not set. Please configure MongoDB connection in .env file.")
    
    client = get_client()
    if client is None:
        raise ConnectionFailure("MongoDB client is None. Please check your connection settings.")
    
    return client[_db_name]

