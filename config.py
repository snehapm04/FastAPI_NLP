import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twitter API credentials
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Hazard-related keywords
HAZARD_KEYWORDS = [
    "ocean hazard", "tsunami", "cyclone", "flood", "storm surge",
    "landslide", "heavy rain", "high waves", "swell surge"
]

# Default configuration
DEFAULT_MAX_RESULTS = 20  # Safe number to avoid rate limits
TIME_WINDOW_HOURS = 2   # Only fetch last 2 hours
