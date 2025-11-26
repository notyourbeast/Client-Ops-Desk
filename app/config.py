import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('FCH_SECRET_KEY', 'dev-secret')
    MONGO_URI = os.environ.get('FCH_MONGO_URI', '')
    JWT_SECRET_KEY = os.environ.get('FCH_JWT_SECRET_KEY', 'dev-jwt-secret')
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('FCH_GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('FCH_GOOGLE_CLIENT_SECRET', '')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    
    # Flask URL configuration for OAuth redirects
    SERVER_NAME = os.environ.get('FCH_SERVER_NAME', None)  # e.g., 'localhost:5000'
    PREFERRED_URL_SCHEME = os.environ.get('FCH_URL_SCHEME', 'http')