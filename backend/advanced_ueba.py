from datetime import datetime, timedelta

def calculate_advanced_risk(username, db):
    cursor = db.cursor(dictionary=True)
    risk = 0
    signals = []
    
    cursor.execute("SELECT COUNT(*) as c FROM login_logs WHERE user_id=%s AND (HOUR(login_time) >= 20 OR HOUR(login_time) < 6) AND login_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 0:
        risk += c * 8
        signals.append(f"ODD_HOUR_LOGIN({c})")
    
    cursor.execute("SELECT COUNT(*) as c FROM login_logs WHERE user_id=%s AND success=0 AND login_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 3:
        risk += 20
        signals.append(f"FAILED_LOGIN({c})")
    
    cursor.execute("SELECT COUNT(DISTINCT ip_address) as c FROM login_logs WHERE user_id=%s AND login_time > DATE_SUB(NOW(), INTERVAL 2 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 2:
        risk += 15
        signals.append(f"MULTIPLE_IPS({c})")
    
    cursor.close()
    risk = min(risk, 100)
    
    if risk <= 30:
        level, decision, zone = "LOW", "ALLOW", "CRITICAL"
    elif risk <= 50:
        level, decision, zone = "MEDIUM", "RESTRICT", "SENSITIVE"
    elif risk <= 70:
        level, decision, zone = "HIGH", "RESTRICT", "INTERNAL"
    else:
        level, decision, zone = "CRITICAL", "DENY", "PUBLIC"
    
    return {"risk_score": risk, "risk_level": level, "decision": decision, "zone": zone, "signals": signals}
