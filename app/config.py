import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('FCH_SECRET_KEY', 'dev-secret')
    MONGO_URI = os.environ.get('FCH_MONGO_URI', '')
    JWT_SECRET_KEY = os.environ.get('FCH_JWT_SECRET_KEY', 'dev-jwt-secret')
