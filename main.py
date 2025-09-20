from fastapi import FastAPI, Query
from twitter_client import fetch_tweets
from nlp_service import classify_hazard, extract_keywords, summarize_keywords
from schemas import FetchResponse, Post, Engagement
import uvicorn

app = FastAPI(title="INCOIS Hazard NLP Engine", version="1.0")

@app.get("/fetch_posts", response_model=FetchResponse)
async def fetch_posts(
    hazard: str = Query(None, description="Hazard filter (e.g., cyclone, flood)"),
    location: str = Query(None, description="Location filter (e.g., Andhra Pradesh, Chennai)"),
    max_results: int = Query(10, le=50, description="Max results (10-50)")
):
    query, start_time, raw = await fetch_tweets(hazard, location, max_results)

    posts = []
    for tweet in raw.get("data", []):
        text = tweet["text"]

        classification = classify_hazard(text)
        
        # Skip posts with "unknown" or "not_hazard" classifications
        if classification in ["unknown", "not_hazard"]:
            continue
            
        keyword_freq = extract_keywords(text)
        metrics = tweet["public_metrics"]

        post = Post(
            id=tweet["id"],
            text=text,
            created_at=tweet["created_at"],
            author_id=tweet["author_id"],
            conversation_id=tweet["conversation_id"],
            hazard_classification=classification,
            engagement=Engagement(
                retweet_count=metrics.get("retweet_count", 0),
                reply_count=metrics.get("reply_count", 0),
                like_count=metrics.get("like_count", 0),
                quote_count=metrics.get("quote_count", 0),
            ),
            keyword_frequency=keyword_freq,
            direct_replies=[]  # extension: can be filled by another call
        )
        posts.append(post.dict())

    keyword_summary = summarize_keywords(posts)

    return {
        "query": query,
        "time_window": "last_2h",
        "hazard_filter": hazard,
        "location_filter": location,
        "posts": posts,
        "keyword_summary": keyword_summary
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


