def normalize_score(value, max_value):
    """Scale a score to 0–1 range"""
    return value / max_value if max_value else 0
