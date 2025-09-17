from datetime import datetime
import random

# Simple mock implementations

def analyze_disaster_label(text, disaster):
    return {
        "disaster_label": disaster,
        "label_score": round(random.uniform(0.7, 1.0), 2)
    }

def analyze_sentiment(text):
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    return {
        "sentiment": random.choice(sentiments),
        "sentiment_score": round(random.uniform(0.5, 1.0), 2)
    }

def extract_keywords(text):
    words = text.lower().split()
    return list(set(words))[:3]

def analyze_engagement(tweet):
    return {
        "retweet_count": tweet["public_metrics"]["retweet_count"],
        "reply_count": tweet["public_metrics"]["reply_count"],
        "like_count": tweet["public_metrics"]["like_count"]
    }

# For counts endpoint (mock)
def get_tweet_count(city, disaster, start_date, end_date):
    return random.randint(50, 200)
