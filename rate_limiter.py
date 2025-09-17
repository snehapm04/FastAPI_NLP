# rate_limiter.py
import time
from fastapi import HTTPException

# Store last request timestamp per query
last_request_time = {}

# Set minimum interval between requests per query (in seconds)
MIN_INTERVAL = 60

def check_rate_limit(query: str):
    """
    Raises HTTPException if query is requested too soon.
    """
    now = time.time()
    last_time = last_request_time.get(query)

    if last_time:
        elapsed = now - last_time
        if elapsed < MIN_INTERVAL:
            wait = int(MIN_INTERVAL - elapsed)
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit: please wait {wait} seconds before retrying this query."
            )
    
    # Update last request time
    last_request_time[query] = now
