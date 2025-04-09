import requests
from config.config import TWITTER_BEARER_TOKEN

def fetch_tweets(keyword, count=20):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={count}&tweet.fields=text"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return [tweet["text"] for tweet in response.json().get("data", [])]
