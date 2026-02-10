# access.py
def decide_access(score: int) -> str:
    """
    Zero Trust access decision engine
    """
    if score >= 90:
        return "DENY"
    elif score >= 50:
        return "RESTRICT"
    return "ALLOW"
