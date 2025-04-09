def sentiment_summary(tweets, analyzer):
    result = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for tweet in tweets:
        sentiment = analyzer(tweet)
        result[sentiment] += 1
    return result
