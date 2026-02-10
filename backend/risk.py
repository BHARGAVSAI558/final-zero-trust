def calculate_risk(ueba):
    weights = {
        "ODD_LOGIN_TIME": 15,
        "FAILED_LOGIN": 25,
        "MULTIPLE_LOGIN_ATTEMPTS": 30,
        "EXTERNAL_NETWORK": 25,
        "UNKNOWN_DEVICE_ID": 35,
        "HOTSPOT_NETWORK": 20,
        "UNTRUSTED_DEVICE": 30,
        "DEVICE_CHANGE_DETECTED": 35,
        "SENSITIVE_FILE_ACCESS": 40,
        "GEOLOCATION_ANOMALY": 45,
        "MULTIPLE_IP_ADDRESSES": 30,
        "FILE_DELETION": 35,
        "EXCESSIVE_FILE_ACCESS": 40,
    }

    risk = {}
    for user, signals in ueba.items():
        score = sum(weights.get(s, 0) for s in signals)
        risk[user] = {
            "score": min(score, 100),
            "events": signals,
            "level": get_risk_level(score)
        }
    return risk

def get_risk_level(score: int) -> str:
    if score >= 90:
        return "CRITICAL"
    elif score >= 70:
        return "HIGH"
    elif score >= 50:
        return "MEDIUM"
    elif score >= 30:
        return "LOW"
    return "MINIMAL"
