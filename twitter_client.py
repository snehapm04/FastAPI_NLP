import httpx
import asyncio
import time
from config import TWITTER_BEARER_TOKEN, SEARCH_RECENT_URL
HEADERS = {
    "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
}


async def safe_get(url: str, params: dict, retries: int = 5):
    """
    Make a safe GET request with retry & exponential backoff for rate limits (429).
    """
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            response = await client.get(url, headers=HEADERS, params=params)

            if response.status_code == 429:
                reset_after = response.headers.get("x-rate-limit-reset")
                if reset_after:
                    # Twitter gives a Unix timestamp (UTC seconds)
                    reset_at = int(reset_after)
                    now = int(time.time())
                    wait_time = reset_at - now
                else:
                    wait_time = 60 * (attempt + 1)  # fallback exponential

                wait_time = max(wait_time, 15)  # always wait at least 15s

                print(f"⚠️ Rate limited (429). Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
                continue

            try:
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e}")
                await asyncio.sleep(5)

    raise Exception("❌ Failed after retries (429 or other errors)")
async def search_tweets(query: str, max_results: int = 10):
    params = {
        "query": query,
        "max_results": str(max_results),
        "tweet.fields": "author_id,conversation_id,created_at,public_metrics"
    }
    data = await safe_get(SEARCH_RECENT_URL, params=params)
    return data.get("data", [])


async def get_direct_replies(conversation_id: str, author_id: str, max_results: int = 5):
    query = f"conversation_id:{conversation_id} in_reply_to_user_id:{author_id}"
    params = {
        "query": query,
        "max_results": str(max_results),
        "tweet.fields": "author_id,conversation_id,created_at,public_metrics"
    }
    data = await safe_get(SEARCH_RECENT_URL, params=params)
    return data.get("data", [])