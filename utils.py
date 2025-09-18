from datetime import datetime, timedelta, timezone

def get_start_time(hours: int = 2) -> str:
    """
    Returns ISO8601 formatted start_time for Twitter API.
    Example: "2025-09-18T06:00:00Z"
    """
    start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    return start_time.isoformat(timespec="seconds").replace("+00:00", "Z")

def build_query(hazard: str = None, location: str = None) -> str:
    """
    Build a safe query with hazard and location filters.
    """
    query_parts = []

    if hazard:
        query_parts.append(f'("{hazard}")')
    else:
        # fallback: use all hazards
        query_parts.append("(" + " OR ".join([f'"{kw}"' for kw in [
            "ocean hazard", "tsunami", "cyclone", "flood", 
            "storm surge", "landslide", "heavy rain", "high waves", "swell surge"
        ]]) + ")")

    if location:
        query_parts.append(f'("{location}")')

    # Always enforce language and no-retweets
    query_parts.append("lang:en -is:retweet")

    return " ".join(query_parts)
