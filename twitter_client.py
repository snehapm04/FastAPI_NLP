import httpx
from config import TWITTER_BEARER_TOKEN, DEFAULT_MAX_RESULTS, TIME_WINDOW_HOURS
from utils import get_start_time, build_query

TWITTER_API_URL = "https://api.twitter.com/2/tweets/search/recent"

headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

async def fetch_tweets(hazard: str = None, location: str = None, max_results: int = DEFAULT_MAX_RESULTS):
    """
    Fetch tweets from Twitter API with hazard and location filters.
    """
    query = build_query(hazard, location)
    start_time = get_start_time(TIME_WINDOW_HOURS)

    params = {
        "query": query,
        "tweet.fields": "id,text,author_id,created_at,conversation_id,public_metrics",
        "max_results": min(max_results, 50),  # enforce Twitter safe limit
        "start_time": start_time
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(TWITTER_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Twitter API error: {response.status_code} {response.text}")

    return query, start_time, response.json()

