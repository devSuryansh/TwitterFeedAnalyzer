import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
