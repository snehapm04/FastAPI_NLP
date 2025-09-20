
# INCOIS Hazard NLP Engine

## Overview

This FastAPI backend ingests hazard-related posts from **X (Twitter)** and processes them using a **hybrid NLP engine** to classify hazards, extract keywords, and summarize engagement metrics.

It is designed to support **INCOIS** (Indian National Centre for Ocean Information Services) for early warning and disaster risk monitoring along India's coasts.

---

## Features

* **Real-time Twitter Data Fetching**:
  * Hazard-specific keyword filtering (cyclone, flood, tsunami, storm surge, landslide, etc.)
  * Location-based filtering (e.g., Chennai, Andhra Pradesh)
  * English language posts only
  * Excludes retweets for original content
  * Configurable time window (default: last 2 hours)

* **Advanced Hazard Classification**:
  * **LLM-based context analysis** using `facebook/bart-large-mnli` zero-shot classification
  * **Multi-step classification pipeline**:
    1. Context analysis to determine if content is hazard-related
    2. Specific hazard type identification using keyword matching
    3. Confidence-based filtering to reduce false positives
  * **Caching** with LRU cache to optimize performance
  * **Hazard categories**: flood, cyclone, tsunami, storm surge, landslide, heavy rain, high waves, ocean hazard

* **Keyword Analysis**:
  * Per-post keyword frequency extraction
  * Aggregated keyword summary across all posts
  * Hazard-specific keyword tracking

* **Engagement Metrics**:
  * Retweet count, reply count, like count, quote count
  * Social media impact assessment

* **API Features**:
  * RESTful API with FastAPI
  * Interactive API documentation (Swagger UI)
  * Pydantic models for request/response validation
  * Error handling and rate limiting considerations

---

## Project Structure

```
FastAPI_NLP-main/
├── main.py              # FastAPI application with endpoints
├── nlp_service.py       # Hazard classification + keyword extraction
├── twitter_client.py    # Twitter API integration
├── schemas.py           # Pydantic models for request/response
├── utils.py             # Helper functions (time formatting, query building)
├── config.py            # Configuration (API keys, hazard keywords, defaults)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── genai/              # Virtual environment (if using venv)
```

---

## 1️⃣ Setup & Configuration

### Prerequisites

- Python 3.8 or higher
- Twitter API Bearer Token (for accessing Twitter API v2)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd FastAPI_NLP-main
```

### 2. Set up virtual environment

```bash
# Create virtual environment
python -m venv genai

# Activate virtual environment
# On Windows:
genai\Scripts\activate
# On Linux/macOS:
source genai/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Dependencies included:**
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server for running FastAPI
- `httpx` - HTTP client for async requests
- `pydantic` - Data validation using Python type annotations
- `python-dotenv` - Load environment variables from .env file
- `transformers` - Hugging Face transformers library for NLP models
- `torch` - PyTorch for deep learning models

### 4. Configure API keys

Create a `.env` file in the root directory:

```env
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

**To get a Twitter Bearer Token:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app or use an existing one
3. Generate a Bearer Token in the "Keys and Tokens" section

### 5. Configuration options

In `config.py`, you can customize:

```python
# Hazard-related keywords for filtering
HAZARD_KEYWORDS = [
    "ocean hazard", "tsunami", "cyclone", "flood", "storm surge",
    "landslide", "heavy rain", "high waves", "swell surge"
]

# Default settings
DEFAULT_MAX_RESULTS = 20  # Maximum tweets to fetch per request
TIME_WINDOW_HOURS = 2     # Time window for tweet search (last 2 hours)
```

---

## 2️⃣ Running the Server

### Start the development server

```bash
# Make sure your virtual environment is activated
# Then run:
python main.py
```

Or alternatively:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the application

- **API Server**: `http://127.0.0.1:8000`
- **Interactive API Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://127.0.0.1:8000/redoc`

### Production deployment

For production deployment, use:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 3️⃣ NLP Models & Classification

### Hazard Classification Pipeline

The system uses a sophisticated multi-step approach for hazard classification:

1. **Context Analysis**: Uses `facebook/bart-large-mnli` for zero-shot classification to determine if content is hazard-related
2. **Specific Hazard Identification**: Keyword-based matching for specific hazard types
3. **Confidence Filtering**: Only returns classifications with sufficient confidence (>0.6)

### Supported Hazard Types

- `flood` - Flooding, water level rise, inundation
- `cyclone` - Cyclones, hurricanes, typhoons, storms
- `tsunami` - Tsunamis, tidal waves, seismic waves
- `storm surge` - Storm surges, coastal flooding
- `landslide` - Landslides, mudslides, rock falls
- `heavy rain` - Heavy rainfall, downpours, torrential rain
- `high waves` - High waves, rough seas, wave height
- `ocean hazard` - General ocean hazards, marine hazards
- `not_hazard` - Content not related to hazards
- `unknown` - Hazard-related but type unclear


## 4️⃣ API Endpoint

### **Fetch Hazard Posts**

```
GET /fetch_posts
```

**Query Parameters:**

| Parameter    | Type | Description                                                        |
| ------------ | ---- | ------------------------------------------------------------------ |
| hazard       | str  | Filter by hazard type (e.g., cyclone, flood)                       |
| location     | str  | Filter posts mentioning a location (e.g., Chennai, Andhra Pradesh) |
| max\_results | int  | Max number of posts to fetch (default 5, max 50)                  |

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

## 5️⃣ Usage Examples

### Example 1: Search for flood-related posts in Chennai

```bash
curl "http://127.0.0.1:8000/fetch_posts?hazard=flood&location=Chennai&max_results=5"
```

### Example 2: Search for cyclone posts without location filter

```bash
curl "http://127.0.0.1:8000/fetch_posts?hazard=cyclone&max_results=10"
```

### Example 3: Search for any hazard-related posts in Andhra Pradesh

```bash
curl "http://127.0.0.1:8000/fetch_posts?location=Andhra%20Pradesh&max_results=15"
```
