from datetime import datetime, timedelta, timezone

def get_start_time(hours: int = 2) -> str:
    """
    Returns ISO8601 formatted start_time for Twitter API.
    Example: "2025-09-18T06:00:00Z"
    """
    start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    return start_time.isoformat(timespec="seconds").replace("+00:00", "Z")

# Example hazard_contexts (can be expanded as before)
hazard_contexts = {
    "flood": ["flood", "flooding", "flooded", "water level", "inundation"],
    "cyclone": ["cyclone", "hurricane", "typhoon", "storm", "wind speed"],
    "tsunami": ["tsunami", "tidal wave", "seismic wave", "earthquake"],
    "storm surge": ["storm surge", "coastal flooding", "surge"],
    "landslide": ["landslide", "mudslide", "rock fall", "slope failure"],
    "heavy rain": ["heavy rain", "downpour", "torrential", "rainfall"],
    "high waves": ["high waves", "rough seas", "wave height"],
    "swell surge": ["swell surge", "long period swell", "sea swell"],
    "ocean hazard": ["ocean hazard", "marine hazard", "sea condition"]
}


def build_query(hazard: str = None, location: str = None) -> str:
    """
    Build a safe query with hazard and location filters.
    Expands hazard to include synonyms from hazard_contexts.
    """
    query_parts = []

    if hazard and hazard in hazard_contexts:
        # Expand to all synonyms for the chosen hazard
        synonyms = hazard_contexts[hazard]
        query_parts.append("(" + " OR ".join([f'"{kw}"' for kw in synonyms]) + ")")
    else:
        # fallback: use all hazard categories
        all_hazards = [kw for synonyms in hazard_contexts.values() for kw in synonyms]
        query_parts.append("(" + " OR ".join([f'"{kw}"' for kw in all_hazards]) + ")")

    if location:
        query_parts.append(f'("{location}")')

    # Always enforce language and exclude retweets
    query_parts.append("lang:en -is:retweet")

    return " ".join(query_parts)
