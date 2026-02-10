from typing import List, Dict

class MicroSegment:
    def __init__(self, name: str, resources: List[str], max_risk_score: int):
        self.name = name
        self.resources = resources
        self.max_risk_score = max_risk_score

SEGMENTS = {
    "public": MicroSegment("Public", ["dashboard", "profile"], 100),
    "internal": MicroSegment("Internal", ["reports", "analytics"], 50),
    "sensitive": MicroSegment("Sensitive", ["admin", "config", "credentials"], 30),
    "critical": MicroSegment("Critical", ["database", "secrets", "keys"], 10),
}

def check_segment_access(resource: str, risk_score: int) -> Dict:
    for segment_name, segment in SEGMENTS.items():
        if resource in segment.resources:
            allowed = risk_score <= segment.max_risk_score
            return {
                "segment": segment_name,
                "allowed": allowed,
                "max_risk": segment.max_risk_score,
                "current_risk": risk_score,
                "reason": "Access granted" if allowed else f"Risk score {risk_score} exceeds limit {segment.max_risk_score}"
            }
    
    return {
        "segment": "unknown",
        "allowed": False,
        "reason": "Resource not found in any segment"
    }

def get_accessible_resources(risk_score: int) -> List[str]:
    accessible = []
    for segment in SEGMENTS.values():
        if risk_score <= segment.max_risk_score:
            accessible.extend(segment.resources)
    return accessible
