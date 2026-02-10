from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
import psycopg2.extras
from auth import router
from ueba import analyze_ueba
from risk import calculate_risk
from access import decide_access
from blockchain import audit_chain
from microsegmentation import check_segment_access, get_accessible_resources
from models import HeartbeatPayload
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Zero Trust Security Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

def safe_dt(dt):
    return dt.isoformat() if isinstance(dt, datetime) else None

@app.get("/security/analyze/admin")
def admin_view():
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM login_logs")
    logins = cursor.fetchall()

    cursor.execute("SELECT * FROM device_logs")
    devices = cursor.fetchall()

    cursor.execute("SELECT * FROM file_access_logs")
    files = cursor.fetchall()

    ueba = analyze_ueba(logins, devices, files)
    risk = calculate_risk(ueba)

    cursor.execute("""
        SELECT user_id,
               COUNT(*) AS total_logins,
               MAX(login_time) AS last_login
        FROM login_logs
        GROUP BY user_id
    """)
    metrics = cursor.fetchall()
    metrics_map = {m["user_id"]: m for m in metrics}

    latest_device = {}
    for d in devices:
        if not d["first_seen"]:
            continue
        u = d["user_id"]
        if u not in latest_device or d["first_seen"] > latest_device[u]["first_seen"]:
            latest_device[u] = d

    output = []
    for user, r in risk.items():
        dev = latest_device.get(user, {})
        
        # Get latest login location
        user_logins = [l for l in logins if l["user_id"] == user]
        latest_login = user_logins[-1] if user_logins else {}

        output.append({
            "user": user,
            "risk_score": r["score"],
            "risk_level": r["level"],
            "decision": decide_access(r["score"]),
            "signals": r["events"],
            "total_logins": metrics_map.get(user, {}).get("total_logins", 0),
            "last_login": safe_dt(metrics_map.get(user, {}).get("last_login")),
            "ip_address": dev.get("ip_address"),
            "mac_address": dev.get("mac_address"),
            "wifi_ssid": dev.get("wifi_ssid"),
            "hostname": dev.get("hostname"),
            "os": dev.get("os"),
            "last_seen": safe_dt(dev.get("first_seen")),
            "country": latest_login.get("country", "Unknown"),
            "city": latest_login.get("city", "Unknown"),
            "accessible_resources": get_accessible_resources(r["score"])
        })

    cursor.close()
    db.close()

    audit_chain.add_event({
        "timestamp": datetime.utcnow().isoformat(),
        "type": "ADMIN_ANALYSIS",
        "user": "admin",
        "data": {"users_analyzed": len(output)}
    })

    return output

@app.get("/security/analyze/user/{username}")
def user_view(username: str):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT * FROM login_logs WHERE user_id=%s ORDER BY login_time DESC", (username,))
    logins = cursor.fetchall()

    cursor.execute("SELECT * FROM device_logs WHERE user_id=%s ORDER BY first_seen DESC", (username,))
    devices = cursor.fetchall()

    cursor.execute("SELECT * FROM file_access_logs WHERE user_id=%s", (username,))
    files = cursor.fetchall()

    cursor.close()
    db.close()

    if not logins and not devices:
        return None

    ueba = analyze_ueba(logins, devices, files)
    risk = calculate_risk(ueba)

    score = risk.get(username, {}).get("score", 0)
    signals = risk.get(username, {}).get("events", [])
    level = risk.get(username, {}).get("level", "MINIMAL")
    
    # Get latest device info
    latest_device = devices[0] if devices else {}
    latest_login = logins[0] if logins else {}

    return {
        "user": username,
        "risk_score": score,
        "risk_level": level,
        "decision": decide_access(score),
        "signals": signals,
        "total_logins": len(logins),
        "last_login": safe_dt(logins[0]["login_time"]) if logins else None,
        "accessible_resources": get_accessible_resources(score),
        "ip_address": latest_device.get("ip_address") or latest_login.get("ip_address"),
        "mac_address": latest_device.get("mac_address"),
        "wifi_ssid": latest_device.get("wifi_ssid"),
        "hostname": latest_device.get("hostname"),
        "os": latest_device.get("os"),
        "country": latest_login.get("country", "Unknown"),
        "city": latest_login.get("city", "Unknown")
    }

@app.get("/admin/file-access")
def file_access_admin():
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("""
        SELECT user_id, file_name, action, ip_address, access_time
        FROM file_access_logs
        ORDER BY access_time DESC
        LIMIT 100
    """)
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    for r in rows:
        r["access_time"] = safe_dt(r["access_time"])

    return rows

@app.get("/audit/chain")
def view_audit_chain():
    return [
        {
            "index": b.index,
            "timestamp": b.timestamp,
            "hash": b.hash,
            "prev_hash": b.prev_hash,
            "data": b.data
        }
        for b in audit_chain.chain
    ]

@app.post("/agent/heartbeat")
def agent_heartbeat(payload: HeartbeatPayload):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO device_logs
        (user_id, device_id, mac_address, os, trusted, first_seen, wifi_ssid, hostname, ip_address)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            payload.user,
            payload.fingerprint,
            payload.mac_address,
            payload.os,
            False,
            datetime.now(),
            payload.wifi_ssid,
            payload.hostname,
            payload.ip_address,
        )
    )

    db.commit()
    cursor.close()
    db.close()
    return {"status": "SUCCESS"}

@app.get("/microsegment/check/{resource}")
def check_resource_access(resource: str, username: str):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("SELECT * FROM login_logs WHERE user_id=%s", (username,))
    logins = cursor.fetchall()
    cursor.execute("SELECT * FROM device_logs WHERE user_id=%s", (username,))
    devices = cursor.fetchall()
    cursor.execute("SELECT * FROM file_access_logs WHERE user_id=%s", (username,))
    files = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    ueba = analyze_ueba(logins, devices, files)
    risk = calculate_risk(ueba)
    score = risk.get(username, {}).get("score", 0)
    
    return check_segment_access(resource, score)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Zero Trust Platform"}

class LocationUpdate(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    city: str
    country: str

@app.post("/update-location")
def update_location(loc: LocationUpdate):
    db = get_db()
    cursor = db.cursor()
    
    # Update latest login with accurate GPS location
    cursor.execute("""
        UPDATE login_logs 
        SET city = %s, country = %s
        WHERE user_id = %s 
        ORDER BY login_time DESC 
        LIMIT 1
    """, (f"{loc.city} ({loc.latitude:.4f}, {loc.longitude:.4f})", loc.country, loc.user_id))
    
    db.commit()
    cursor.close()
    db.close()
    
    return {"status": "SUCCESS"}

class FileAccessRequest(BaseModel):
    user_id: str
    file_name: str
    action: str

@app.post("/files/access")
def file_access(req: FileAccessRequest, request: Request):
    db = get_db()
    cursor = db.cursor()
    
    ip = request.client.host
    
    cursor.execute("""
        INSERT INTO file_access_logs (user_id, file_name, action, ip_address, access_time)
        VALUES (%s, %s, %s, %s, %s)
    """, (req.user_id, req.file_name, req.action, ip, datetime.now()))
    
    db.commit()
    cursor.close()
    db.close()
    
    audit_chain.add_event({
        "timestamp": datetime.utcnow().isoformat(),
        "type": "FILE_ACCESS",
        "user": req.user_id,
        "file": req.file_name,
        "action": req.action,
        "ip": ip
    })
    
    return {"status": "SUCCESS", "message": f"{req.action} {req.file_name}"}

@app.get("/files/list/{username}")
def list_user_files(username: str):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("""
        SELECT file_name, action, ip_address, access_time
        FROM file_access_logs
        WHERE user_id = %s
        ORDER BY access_time DESC
        LIMIT 50
    """, (username,))
    
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    
    for r in rows:
        r["access_time"] = safe_dt(r["access_time"])
    
    return rows
