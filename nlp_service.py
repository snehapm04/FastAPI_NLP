from collections import Counter
from config import HAZARD_KEYWORDS
from transformers import pipeline
from functools import lru_cache
import json

# Initialize LLM-based classifier for better context understanding
classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-emotion")

# Hazard-specific classification pipeline
hazard_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Comprehensive hazard categories for LLM classification
HAZARD_CATEGORIES = [
    # Ocean & Coastal Hazards
    "flood",
    "cyclone",
    "tsunami",
    "storm surge",
    "landslide",
    "heavy rain",
    "high waves",
    "ocean hazard",
    "swell surge",
    "coastal erosion",
    "rip current",
    "strong currents",
    "abnormal tides",
    "sea level rise",
    "rogue wave",
    "seawater intrusion",
    "coastal inundation",
    "boat capsized",
    "shipwreck",
    "fishermen missing",
    "port closure",
    "oil spill",
    "maritime accident",
    "algal bloom",
    "fish kill",
    "marine pollution",
    "debris hazard",
    "saltwater intrusion",
    "not_hazard",
    "unknown"
]



def analyze_context_with_llm(text: str) -> dict:
    """
    Use LLM to analyze the context and determine if it's hazard-related.
    Returns confidence scores for different hazard types.
    """
    try:
        # Use zero-shot classification for hazard detection
        result = hazard_classifier(
            text, 
            candidate_labels=["natural disaster", "weather emergency", "not_hazard"]
        )
        
        # Get the top classification
        top_label = result["labels"][0]
        confidence = result["scores"][0]
        
        return {
            "category": top_label,
            "confidence": confidence,
            "is_hazard": top_label in ["natural disaster", "weather emergency"] and confidence > 0.6
        }
    except Exception as e:
        print(f"LLM classification error: {e}")
        return {"category": "unknown", "confidence": 0.0, "is_hazard": False}


def identify_specific_hazard(text: str) -> str:
    """
    Identify the specific type of hazard using keyword matching and context.
    """
    text_lower = text.lower()
    
    # Check for specific hazard keywords with context validation
hazard_contexts = {
    "flood": [
        "flood", "flooding", "flooded", "water level", "inundation",
        "sea flooding", "coastal inundation", "submerged"
    ],
    "cyclone": [
        "cyclone", "hurricane", "typhoon", "tropical storm", "windstorm",
        "gale winds", "landfall", "severe storm", "super cyclone"
    ],
    "tsunami": [
        "tsunami", "tidal wave", "seismic wave", "earthquake wave",
        "underwater quake", "seaquake", "aftershock waves"
    ],
    "storm surge": [
        "storm surge", "coastal flooding", "sea water rise",
        "wave surge", "ocean surge", "cyclone surge"
    ],
    "heavy rain": [
        "heavy rain", "downpour", "torrential rain", "rainfall",
        "cloudburst", "monsoon rain"
    ],
    "high waves": [
        "high waves", "rough seas", "wave height", "giant waves",
        "rogue wave", "freak wave", "swells", "abnormal waves"
    ],
    "swell surge": [
        "swell surge", "long period swell", "sea swell",
        "wave swell", "dangerous swell"
    ],
    "coastal erosion": [
        "coastal erosion", "shoreline erosion", "beach erosion",
        "sand loss", "coastal retreat"
    ],
    "rip current": [
        "rip current", "strong current", "undertow", "backwash",
        "dangerous current"
    ],
    "sea level rise": [
        "sea level rise", "rising sea", "ocean rise", "coastal submergence"
    ],
    "boat capsized": [
        "boat capsized", "boat overturned", "capsize", "fishing boat sunk"
    ],
    "shipwreck": [
        "shipwreck", "vessel sunk", "ship grounded", "maritime accident"
    ],
    "fishermen missing": [
        "fishermen missing", "missing fishermen", "lost at sea", "crew missing"
    ],
    "port closure": [
        "port closure", "harbor closed", "fishing ban", "shipping stopped"
    ],
    "oil spill": [
        "oil spill", "oil leakage", "tanker spill", "marine oil pollution"
    ],
    "algal bloom": [
        "algal bloom", "red tide", "green tide", "toxic algae"
    ],
    "fish kill": [
        "fish kill", "dead fish", "mass fish death", "floating fish"
    ],
    "marine pollution": [
        "marine pollution", "sea pollution", "plastic waste", "chemical spill",
        "ocean pollution", "marine debris"
    ],
    "not_hazard": [
        "normal", "clear sky", "safe", "no risk", "good weather"
    ],
    "unknown": [
        "uncertain", "not sure", "unknown", "unidentified", "other"
    ]
}

    
    for hazard_type, keywords in hazard_contexts.items():
        for keyword in keywords:
            if keyword in text_lower:
                return hazard_type
    
    return "unknown"


@lru_cache(maxsize=10000)  # cache up to 10k unique texts
def classify_hazard(text: str) -> str:
    """
    Advanced LLM-based hazard classification with context understanding.
    1. LLM context analysis
    2. Specific hazard identification
    3. Confidence-based filtering
    """
    
    # Step 1: LLM-based context analysis
    context_analysis = analyze_context_with_llm(text)
    
    # Step 2: If not hazard-related, return early
    if not context_analysis["is_hazard"]:
        return "not_hazard"
    
    # Step 3: Identify specific hazard type
    specific_hazard = identify_specific_hazard(text)
    
    # Step 4: Return classification based on confidence and specificity
    if specific_hazard != "unknown":
        return specific_hazard
    elif context_analysis["confidence"] > 0.7:
        return "unknown"  # Hazard-related but type unclear
    else:
        return "not_hazard"


def extract_keywords(text: str) -> dict:
    """
    Extract frequency of hazard keywords from text.
    """
    text_lower = text.lower()
    freq = {}
    for keyword in HAZARD_KEYWORDS:
        count = text_lower.count(keyword)
        if count > 0:
            freq[keyword] = count
    return freq


def summarize_keywords(posts: list) -> dict:
    """
    Aggregate keyword frequencies across all posts.
    """
    counter = Counter()
    for post in posts:
        counter.update(post.get("keyword_frequency", {}))
    return dict(counter)
