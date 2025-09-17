# routes.py
from fastapi import APIRouter, Query
from rate_limiter import check_rate_limit
from service import search_tweets, get_direct_replies

router = APIRouter()

@router.get("/tweets")
async def fetch_tweets(query: str = Query(...), post_limit: int = 5, reply_limit: int = 5):
    # Check rate limit for this query
    check_rate_limit(query)

    # Fetch main posts
    main_posts = await search_tweets(query, max_results=post_limit)

    result = {}
    for post in main_posts:
        # Fetch direct replies
        replies = await get_direct_replies(post["conversation_id"], post["author_id"], max_results=reply_limit)
        comments = [r["text"] for r in replies]
        result[post["text"]] = comments

    return result
