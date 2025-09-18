
# INCOIS Hazard NLP Engine Backend

## Overview

This FastAPI backend ingests hazard-related posts from **X (Twitter)** and processes them using a **hybrid NLP engine** to classify hazards, extract keywords, and summarize engagement metrics.

It is designed to support **INCOIS** for early warning and disaster risk monitoring along India’s coasts.

---

## Features

* Fetch **hazard-related posts** from Twitter using **filters**:

  * Keywords: cyclone, flood, tsunami, storm surge, landslide, ocean hazard, etc.
  * Language: English only
  * Exclude retweets
  * Time window: last 2 hours
* **Hazard classification**:

  * Rule-based context filtering
  * Hugging Face zero-shot classification (`facebook/bart-large-mnli`)
  * Keyword-based hazard labeling
* **Keyword extraction** per post and aggregated summary
* **Engagement metrics** (likes, retweets, replies, quotes)
* Optional fetching of **direct replies**
* **Caching** to prevent repeated heavy NLP computations
* **Location and hazard filtering** for precise search
* **Modular architecture** for easy integration

---

## Project Structure

```
incois_backend/
│── config.py          # API keys, hazard keywords, defaults
│── twitter_client.py  # Fetch posts/replies from Twitter API
│── nlp_engine.py      # Hazard classification + keyword extraction
│── utils.py           # Helpers (time formatting, query building)
│── schemas.py         # Pydantic models for request/response
│── main.py            # FastAPI application with endpoints
│── requirements.txt   # Dependencies
│── README.md
```

---

## 1️⃣ Setup & Configuration

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd incois_backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt example:**

```
fastapi
uvicorn
httpx
pydantic
python-dotenv
transformers
torch
```

### 4. Configure API keys

Create a `.env` file in the root folder:

```
TWITTER_BEARER_TOKEN=YOUR_TWITTER_BEARER_TOKEN
```

In `config.py` you can adjust:

```python
HAZARD_KEYWORDS = ["ocean hazard","tsunami","cyclone","flood","storm surge","landslide","heavy rain"]
DEFAULT_MAX_RESULTS = 20
TIME_WINDOW_HOURS = 2
```

---

## 2️⃣ Running the Server

```bash
uvicorn main:app --reload
```

* Server runs at: `http://127.0.0.1:8000`
* Interactive docs: `http://127.0.0.1:8000/docs`

---

## 3️⃣ API Endpoint

### **Fetch Hazard Posts**

```
GET /fetch_posts
```

**Query Parameters:**

| Parameter    | Type | Description                                                        |
| ------------ | ---- | ------------------------------------------------------------------ |
| hazard       | str  | Filter by hazard type (e.g., cyclone, flood)                       |
| location     | str  | Filter posts mentioning a location (e.g., Chennai, Andhra Pradesh) |
| max\_results | int  | Max number of posts to fetch (default 20, max 50)                  |

---

### **Example Request**

```
GET http://127.0.0.1:8000/fetch_posts?hazard=flood&location=Chennai&max_results=10
```

---

### **Sample JSON Response**

```json
{
  "query": "(flood) (Chennai) lang:en -is:retweet",
  "time_window": "last_2h",
  "hazard_filter": "flood",
  "location_filter": "Chennai",
  "posts": [
    {
      "id": "1701456789012345",
      "text": "Flood waters rising near Chennai due to heavy rain",
      "created_at": "2025-09-18T07:40:00Z",
      "author_id": "112233",
      "conversation_id": "1701456789012345",
      "hazard_classification": "flood",
      "engagement": {
        "retweet_count": 15,
        "reply_count": 6,
        "like_count": 55,
        "quote_count": 2
      },
      "keyword_frequency": {
        "flood": 1,
        "rain": 1
      },
      "direct_replies": []
    }
  ],
  "keyword_summary": {
    "flood": 1,
    "rain": 1
  }
}
```

---

### ⚡ Response Fields

* `query`: Actual Twitter API query used.
* `time_window`: Always last 2 hours.
* `hazard_filter`, `location_filter`: Echo of applied filters.
* `posts`: List of main posts with metadata:

  * `hazard_classification` → hazard type or `not_hazard`
  * `keyword_frequency` → frequency of hazard-related keywords
  * `engagement` → likes, retweets, replies, quotes
  * `direct_replies` → optional list of replies
* `keyword_summary`: Aggregated keyword counts across all posts.

---

