
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = "MyDB"
MONGO_URI = "mongodb+srv://notyourbeast10:qwerty123@cluster0.52ms49f.mongodb.net/?appName=Cluster0"


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
