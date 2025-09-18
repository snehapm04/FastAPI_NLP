from typing import Optional, List, Dict
from pydantic import BaseModel

class Engagement(BaseModel):
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

class Reply(BaseModel):
    id: str
    text: str
    created_at: str
    author_id: str
    hazard_classification: str
    engagement: Engagement
    keyword_frequency: Dict[str, int]

class Post(BaseModel):
    id: str
    text: str
    created_at: str
    author_id: str
    conversation_id: str
    hazard_classification: str
    engagement: Engagement
    keyword_frequency: Dict[str, int]
    direct_replies: Optional[List[Reply]] = []

class FetchResponse(BaseModel):
    query: str
    time_window: str
    hazard_filter: Optional[str]
    location_filter: Optional[str]
    posts: List[Post]
    keyword_summary: Dict[str, int]
