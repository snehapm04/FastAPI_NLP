from fastapi import FastAPI
from routers import router as tweet_router
from nlp_routes import router as nlp_router

app = FastAPI(title="Disaster Tweets API")

app.include_router(tweet_router)
app.include_router(nlp_router)
