import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('FCH_SECRET_KEY', 'dev-secret')
    MONGO_URI = os.environ.get('FCH_MONGO_URI', '')
    JWT_SECRET_KEY = os.environ.get('FCH_JWT_SECRET_KEY', 'dev-jwt-secret')



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://notyourbeast10:<db_password>@cluster0.52ms49f.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)