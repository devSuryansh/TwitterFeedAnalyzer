from pymongo import MongoClient
from config.config import MONGO_URI
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client["twitter_feed"]
users = db["users"]
searches = db["searches"]

def insert_user(username, password):
    users.insert_one({"username": username, "password": password})

def get_user(username):
    return users.find_one({"username": username})

def save_search(username, keyword, tweets):
    searches.insert_one({
        "username": username,
        "keyword": keyword,
        "tweets": tweets,
        "timestamp": datetime.utcnow()
    })

def get_user_searches(username):
    return list(searches.find({"username": username}))
