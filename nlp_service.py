from collections import Counter
from config import HAZARD_KEYWORDS
from transformers import pipeline
from functools import lru_cache

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Exclusion phrases (non-disaster flood context, etc.)
NEGATIVE_CONTEXT = [
    "flooded with emails",
    "flood of emotions",
    "flood of offers",
    "data flood",
    "flood of memories",
]

# Candidate labels for zero-shot classification
CANDIDATE_LABELS = ["natural disaster", "unrelated"]


def is_relevant_context(text: str) -> bool:
    """
    Step 1: Rule-based context check (quick filter).
    """
    text_lower = text.lower()

    for phrase in NEGATIVE_CONTEXT:
        if phrase in text_lower:
            return False

    return True


@lru_cache(maxsize=10000)  # cache up to 10k unique texts
def classify_hazard(text: str) -> str:
    """
    Hybrid hazard classification with caching.
    1. Rule-based filter
    2. Zero-shot classifier
    3. Keyword match for specific hazard type
    """

    text_lower = text.lower()

    # Step 1: quick rule-based filter
    if not is_relevant_context(text_lower):
        return "not_hazard"

    # Step 2: zero-shot classification
    result = classifier(text, candidate_labels=CANDIDATE_LABELS)
    top_label = result["labels"][0]
    score = result["scores"][0]

    if top_label == "unrelated" and score > 0.7:
        return "not_hazard"

    # Step 3: hazard-specific classification by keyword
    for keyword in HAZARD_KEYWORDS:
        if keyword in text_lower:
            return keyword

    return "unknown"


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
