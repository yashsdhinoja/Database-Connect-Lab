import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Username and Password from Atlas
MONGO_USER = quote_plus("y8698881_db_user")
MONGO_PASS = quote_plus("God@eyes&890&")  # Auto-encodes @ and & safely

# Your exact cluster domain
REAL_CLUSTER_HOST = "m0.fzsomkl.mongodb.net"

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{REAL_CLUSTER_HOST}/?retryWrites=true&w=majority"

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["UserAnalyticsDB"]

activity_collection = mongo_db["user_activities"]
screen_time_collection = mongo_db["screen_time_logs"]
mood_history_collection = mongo_db["mood_logs"]