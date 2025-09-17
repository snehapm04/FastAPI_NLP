from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from twitter_client import search_tweets
from nlp_service import analyze_disaster_label, analyze_sentiment, extract_keywords, analyze_engagement, get_tweet_count

router = APIRouter()

class FetchNLPRequest(BaseModel):
    city: str
    disaster: str
    max_results: int = 30

@router.post("/nlp/fetch_tweets")
async def nlp_fetch_tweets(payload: FetchNLPRequest):
    query = f"{payload.disaster} {payload.city}"
    tweets = await search_tweets(query=query, max_results=payload.max_results)

    analyzed = []
    for tweet in tweets:
        analyzed.append({
            "tweet_id": tweet["id"],
            "text": tweet["text"],
            "created_at": tweet["created_at"],
            **analyze_disaster_label(tweet["text"], payload.disaster),
            **analyze_sentiment(tweet["text"]),
            "keywords": extract_keywords(tweet["text"]),
            "engagement": analyze_engagement(tweet),
        })

    return {
        "city": payload.city,
        "disaster": payload.disaster,
        "count": len(analyzed),
        "date": datetime.utcnow().date().isoformat(),
        "time": datetime.utcnow().time().isoformat(),
        "tweets": analyzed
    }

@router.get("/nlp/counts")
def nlp_counts(city: str, disaster: str, start_date: str, end_date: str):
    count = get_tweet_count(city, disaster, start_date, end_date)
    return {
        "city": city,
        "disaster": disaster,
        "start_date": start_date,
        "end_date": end_date,
        "count": count
    }
