import os


class Config:
    SECRET_KEY = os.environ.get('FCH_SECRET_KEY', 'dev-secret')
    MONGO_URI = os.environ.get('FCH_MONGO_URI', '')
