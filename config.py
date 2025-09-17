import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
SEARCH_RECENT_URL = "https://api.twitter.com/2/tweets/search/recent"
TWEET_FIELDS = "tweet.fields=author_id,conversation_id,created_at,public_metrics"