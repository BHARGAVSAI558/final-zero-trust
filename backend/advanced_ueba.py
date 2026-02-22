from datetime import datetime, timedelta

def calculate_advanced_risk(username, db):
    cursor = db.cursor(dictionary=True)
    risk = 0
    signals = []
    
    # Critical file READ (low risk)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND (file_name LIKE %s OR file_name LIKE %s OR file_name LIKE %s) AND action='READ' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username, '%secret%', '%credential%', '%salary%'))
    c = cursor.fetchone()['c']
    if c > 0:
        risk += c * 5
        signals.append(f"CRITICAL_FILE_READ({c})")
    
    # Critical file EDIT (very high risk - most dangerous)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND (file_name LIKE %s OR file_name LIKE %s OR file_name LIKE %s) AND action='WRITE' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username, '%secret%', '%credential%', '%salary%'))
    c = cursor.fetchone()['c']
    if c > 0:
        risk += c * 20
        signals.append(f"CRITICAL_FILE_EDIT({c})")
    
    # Critical file DOWNLOAD (high risk)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND (file_name LIKE %s OR file_name LIKE %s OR file_name LIKE %s) AND action='DOWNLOAD' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username, '%secret%', '%credential%', '%salary%'))
    c = cursor.fetchone()['c']
    if c > 0:
        risk += c * 12
        signals.append(f"CRITICAL_FILE_DOWNLOAD({c})")
    
    # Any file deletion (high risk)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND action='DELETE' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 0:
        risk += c * 15
        signals.append(f"FILE_DELETION({c})")
    
    # Regular file editing (low-medium risk)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND action='WRITE' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 1:
        risk += c * 3
        signals.append(f"FILE_EDIT({c})")
    
    # Regular file download (low risk)
    cursor.execute("SELECT COUNT(*) as c FROM file_access_logs WHERE user_id=%s AND action='DOWNLOAD' AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)", (username,))
    c = cursor.fetchone()['c']
    if c > 3:
        risk += c * 2
        signals.append(f"FILE_DOWNLOAD({c})")
    
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
