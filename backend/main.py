from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import os
import requests
import hashlib
import json
from websocket_manager import manager
from advanced_ueba import calculate_advanced_risk

def get_db():
    import mysql.connector
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="zerotrust"
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Zero Trust Security Platform", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_geolocation(ip):
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5).json()
        if not geo.get('error'):
            return {
                "country": geo.get("country_name", "Unknown"),
                "city": geo.get("city", "Unknown"),
                "region": geo.get("region", "Unknown"),
                "latitude": geo.get("latitude", 0),
                "longitude": geo.get("longitude", 0),
                "timezone": geo.get("timezone", "Unknown"),
                "isp": geo.get("org", "Unknown"),
                "ip": geo.get("ip", ip),
                "postal": geo.get("postal", "Unknown")
            }
    except:
        pass
    return {"country": "Unknown", "city": "Unknown", "region": "Unknown", "latitude": 0, "longitude": 0, "timezone": "Unknown", "isp": "Unknown", "ip": ip, "postal": "Unknown"}

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 'timestamp': str(datetime.now()), 'proof': proof, 'previous_hash': previous_hash, 'data': []}
        self.chain.append(block)
        return block
    
    def add_transaction(self, transaction):
        if self.chain:
            self.chain[-1]['data'].append(transaction)
    
    def get_previous_block(self):
        return self.chain[-1] if self.chain else None
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                return new_proof
            new_proof += 1
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

blockchain = Blockchain()

def calculate_risk_score(username, db):
    return calculate_advanced_risk(username, db)

@app.post("/auth/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Username already exists"}
        cursor.execute("INSERT INTO users (username, password, role, status) VALUES (%s, %s, 'user', 'pending')", (username, password))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS", "message": "Registration pending admin approval"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.post("/auth/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Invalid credentials"}
        if user["status"] == "pending":
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Account pending admin approval"}
        if user["status"] == "revoked":
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Access revoked by admin"}
        ip = request.client.host if request.client else "Unknown"
        geo = get_geolocation(ip)
        cursor.execute("INSERT INTO login_logs (user_id, login_time, ip_address, success, country, city) VALUES (%s, NOW(), %s, %s, %s, %s)", (username, geo["ip"], True, geo["country"], geo["city"]))
        db.commit()
        blockchain.add_transaction({"type": "LOGIN", "user": username, "success": True, "ip": geo["ip"], "location": f"{geo['city']}, {geo['country']}", "latitude": geo["latitude"], "longitude": geo["longitude"], "timestamp": str(datetime.now())})
        if len(blockchain.chain[-1]['data']) >= 3:
            previous_block = blockchain.get_previous_block()
            previous_proof = previous_block['proof']
            proof = blockchain.proof_of_work(previous_proof)
            previous_hash = blockchain.hash(previous_block)
            blockchain.create_block(proof, previous_hash)
        risk_data = calculate_risk_score(username, db)
        cursor.close()
        db.close()
        return {"status": "SUCCESS", "user": username, "role": user["role"], "location": f"{geo['city']}, {geo['country']}", "latitude": geo["latitude"], "longitude": geo["longitude"], "timezone": geo["timezone"], "isp": geo["isp"], "risk_score": risk_data["risk_score"], "risk_level": risk_data["risk_level"], "decision": risk_data["decision"], "access_zone": risk_data["zone"]}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Zero Trust Platform"}

@app.get("/security/analyze/admin")
def admin_view():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT l.user_id, (SELECT COUNT(*) FROM login_logs WHERE user_id=l.user_id) as total_logins, (SELECT MAX(login_time) FROM login_logs WHERE user_id=l.user_id) as last_login, (SELECT ip_address FROM login_logs WHERE user_id=l.user_id ORDER BY login_time DESC LIMIT 1) as ip_address, (SELECT country FROM login_logs WHERE user_id=l.user_id ORDER BY login_time DESC LIMIT 1) as country, (SELECT city FROM login_logs WHERE user_id=l.user_id ORDER BY login_time DESC LIMIT 1) as city, (SELECT mac_address FROM device_logs WHERE user_id=l.user_id ORDER BY first_seen DESC LIMIT 1) as mac_address, (SELECT wifi_ssid FROM device_logs WHERE user_id=l.user_id ORDER BY first_seen DESC LIMIT 1) as wifi_ssid, (SELECT hostname FROM device_logs WHERE user_id=l.user_id ORDER BY first_seen DESC LIMIT 1) as hostname, (SELECT os FROM device_logs WHERE user_id=l.user_id ORDER BY first_seen DESC LIMIT 1) as os, (SELECT status FROM users WHERE username=l.user_id) as status FROM login_logs l")
        users = cursor.fetchall()
        result = []
        for u in users:
            risk_data = calculate_risk_score(u["user_id"], db)
            result.append({"username": u["user_id"] or "unknown", "risk_score": risk_data["risk_score"], "risk_level": risk_data["risk_level"], "decision": risk_data["decision"], "zone": risk_data["zone"], "login_count": u["total_logins"] or 0, "last_login": str(u["last_login"]) if u["last_login"] else None, "signals": risk_data["signals"], "ip_address": u["ip_address"] or "N/A", "country": u["country"] or "Unknown", "city": u["city"] or "Unknown", "mac_address": u["mac_address"] or "N/A", "wifi_ssid": u["wifi_ssid"] or "N/A", "hostname": u["hostname"] or "N/A", "os": u["os"] or "N/A", "status": u["status"] or "active"})
        cursor.close()
        db.close()
        return {"users": result}
    except Exception as e:
        print(f"Admin view error: {e}")
        return {"users": []}

@app.get("/security/analyze/user/{username}")
def user_view(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM login_logs WHERE user_id=%s", (username,))
        total = cursor.fetchone()["total"]
        cursor.execute("SELECT * FROM login_logs WHERE user_id=%s ORDER BY login_time DESC LIMIT 1", (username,))
        last_login = cursor.fetchone()
        cursor.execute("SELECT * FROM device_logs WHERE user_id=%s ORDER BY first_seen DESC LIMIT 1", (username,))
        device = cursor.fetchone()
        risk_data = calculate_risk_score(username, db)
        cursor.close()
        db.close()
        return {"username": username, "risk_score": risk_data["risk_score"], "risk_level": risk_data["risk_level"], "decision": risk_data["decision"], "zone": risk_data["zone"], "signals": risk_data["signals"], "login_count": total, "last_login": str(last_login["login_time"]) if last_login else None, "accessible_resources": ["dashboard", "profile", "reports", "analytics"], "ip_address": last_login["ip_address"] if last_login else "N/A", "mac_address": device["mac_address"] if device else "N/A", "wifi_ssid": device["wifi_ssid"] if device else "N/A", "hostname": device["hostname"] if device else "N/A", "os": device["os"] if device else "N/A", "country": last_login["country"] if last_login else "Unknown", "city": last_login["city"] if last_login else "Unknown"}
    except:
        return {"username": username, "risk_score": 0, "risk_level": "LOW", "decision": "ALLOW", "zone": "PUBLIC", "signals": [], "login_count": 0, "last_login": None, "accessible_resources": ["dashboard", "profile"], "ip_address": "N/A", "mac_address": "N/A", "wifi_ssid": "N/A", "hostname": "N/A", "os": "N/A", "country": "Unknown", "city": "Unknown"}

@app.get("/admin/pending-users")
def get_pending_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, created_at FROM users WHERE status='pending' ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        db.close()
        return [{"username": u["username"], "created_at": str(u["created_at"])} for u in users]
    except:
        return []

@app.get("/admin/file-access")
def admin_files():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM file_access_logs ORDER BY access_time DESC LIMIT 100")
        files = cursor.fetchall()
        cursor.close()
        db.close()
        return {"file_logs": [{"user_id": f["user_id"], "file_name": f["file_name"], "action": f["action"], "access_time": str(f["access_time"]), "ip_address": f["ip_address"]} for f in files]}
    except:
        return {"file_logs": []}

@app.get("/audit/chain")
def audit():
    try:
        blocks_with_hash = []
        for block in blockchain.chain[-10:]:
            block_copy = block.copy()
            blocks_with_hash.append({'block_index': block_copy['index'], 'timestamp': block_copy['timestamp'], 'current_hash': blockchain.hash(block)[:64], 'previous_hash': block_copy['previous_hash'], 'event_type': 'BLOCK_CREATED', 'data': block_copy['data']})
        return {"blockchain": blocks_with_hash}
    except:
        return {"blockchain": []}

@app.post("/files/access")
async def file_access(request: Request):
    try:
        data = await request.json()
        db = get_db()
        cursor = db.cursor()
        ip = request.client.host if request.client else "Unknown"
        cursor.execute("INSERT INTO file_access_logs (user_id, file_name, action, ip_address, access_time) VALUES (%s,%s,%s,%s, NOW())", (data.get("user_id"), data.get("file_name"), data.get("action"), ip))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/files/list/{username}")
def list_files(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM file_access_logs WHERE user_id=%s ORDER BY access_time DESC LIMIT 50", (username,))
        files = cursor.fetchall()
        cursor.close()
        db.close()
        return files
    except:
        return []

@app.get("/admin/user-sessions/{username}")
def get_user_sessions(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT l.id as login_id, l.login_time, l.ip_address, l.city, l.country, l.success, d.device_id, d.mac_address, d.wifi_ssid, d.hostname, d.os FROM login_logs l LEFT JOIN device_logs d ON l.user_id = d.user_id WHERE l.user_id = %s AND l.success = 1 ORDER BY l.login_time DESC LIMIT 20", (username,))
        sessions = cursor.fetchall()
        session_list = []
        for i, session in enumerate(sessions):
            if i < len(sessions) - 1:
                next_login = sessions[i + 1]['login_time']
                duration = int((session['login_time'] - next_login).total_seconds())
                is_active = False
            else:
                duration = int((datetime.now() - session['login_time']).total_seconds())
                is_active = duration < 3600
            cursor.execute("SELECT file_name, action, access_time, ip_address FROM file_access_logs WHERE user_id = %s AND access_time >= %s AND access_time <= DATE_ADD(%s, INTERVAL 1 HOUR) ORDER BY access_time DESC", (username, session['login_time'], session['login_time']))
            file_activities = cursor.fetchall()
            session_list.append({'login_id': session['login_id'], 'login_time': str(session['login_time']), 'ip_address': session['ip_address'] or 'N/A', 'city': session['city'] or 'Unknown', 'country': session['country'] or 'Unknown', 'device_id': session['device_id'] or 'N/A', 'mac_address': session['mac_address'] or 'N/A', 'wifi_ssid': session['wifi_ssid'] or 'N/A', 'hostname': session['hostname'] or 'N/A', 'os': session['os'] or 'N/A', 'session_duration_seconds': abs(duration), 'is_active': is_active, 'last_activity': str(session['login_time']), 'file_activities': [{'file_name': f['file_name'], 'action': f['action'], 'access_time': str(f['access_time']), 'ip_address': f['ip_address']} for f in file_activities]})
        cursor.close()
        db.close()
        return {'sessions': session_list, 'total_sessions': len(session_list), 'active_sessions': sum(1 for s in session_list if s['is_active']), 'current_session_duration': session_list[0]['session_duration_seconds'] if session_list and session_list[0]['is_active'] else 0}
    except:
        return {'sessions': [], 'total_sessions': 0, 'active_sessions': 0, 'current_session_duration': 0}

@app.post("/agent/telemetry")
async def agent_telemetry(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        device = data.get("device", {})
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO device_logs (user_id, device_id, mac_address, os, wifi_ssid, hostname, ip_address, trusted, first_seen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, NOW()) ON DUPLICATE KEY UPDATE ip_address=VALUES(ip_address), first_seen=NOW()", (username, device.get("device_id"), device.get("mac"), device.get("os"), device.get("wifi", "N/A"), device.get("hostname"), device.get("ip"), False))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/realtime/stats")
def realtime_stats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM users WHERE status='active'")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as active FROM login_logs WHERE login_time > DATE_SUB(NOW(), INTERVAL 5 MINUTE)")
        active = cursor.fetchone()['active']
        cursor.close()
        db.close()
        return {"total_users": total, "active_now": active, "timestamp": datetime.now().isoformat()}
    except:
        return {"total_users": 0, "active_now": 0, "timestamp": datetime.now().isoformat()}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"type": "message", "client": client_id, "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
