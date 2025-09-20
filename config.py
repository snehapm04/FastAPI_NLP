import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Twitter API credentials
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Hazard-related keywords
HAZARD_KEYWORDS = [
    # Tsunami-related
    "tsunami", "tidal wave", "sea earthquake", "underwater quake", 
    "seismic sea waves", "aftershock waves",

    # Storm Surge / Cyclones
    "storm surge", "cyclone", "hurricane", "typhoon", "gale winds", 
    "landfall", "severe storm", "coastal flooding", "wind damage", "gusts",

    # High Waves / Swell Surges
    "high tide", "rough sea", "high waves", "giant waves", 
    "rogue wave", "swells", "swell surge", "freak wave", "abnormal waves",

    # Coastal Currents & Abnormal Sea Behaviour
    "rip current", "strong current", "abnormal tide", "unusual tide", 
    "sudden flooding", "sea water rise", "backwash", "beach erosion", 
    "fast-moving water", "undertow",

    # Flooding / Coastal Damage
    "sea flooding", "seawater intrusion", "coastal inundation", 
    "storm damage", "sea level rise", "shoreline erosion", 
    "property damage", "washed away", "boats capsized",

    # Emergency & Risk Signals
    "evacuation", "alert", "warning", "red alert", "danger", 
    "emergency", "rescue", "stranded", "missing fishermen", "port closed"
]


# Default configuration
DEFAULT_MAX_RESULTS = 20  # Safe number to avoid rate limits
TIME_WINDOW_HOURS = 2   # Only fetch last 2 hours
