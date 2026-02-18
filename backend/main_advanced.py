from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import requests
import hashlib
import json
import secrets
import time
import mysql.connector
import jwt

# Import file management router
from file_api import router as file_router

# JWT Configuration
JWT_SECRET = "zero-trust-secret-key-2024-hackathon"
JWT_ALGORITHM = "HS256"
SESSION_TIMEOUT = 300  # 5 minutes

security = HTTPBearer()

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="zerotrust"
    )

app = FastAPI(title="Zero Trust Security Platform - Advanced")

# Include file management router
app.include_router(file_router, prefix="/api", tags=["files"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://zer0-trust.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_jwt_token(username: str, role: str):
    """Create JWT token with 5-minute expiry"""
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(seconds=SESSION_TIMEOUT),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Session expired - please login again")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid session token")

def get_real_geolocation(ip):
    # Skip geolocation for localhost/private IPs - instant response
    if ip in ['127.0.0.1', 'localhost'] or ip.startswith('192.168.') or ip.startswith('10.'):
        return {"country": "India", "city": "Local", "latitude": 0, "longitude": 0, "isp": "Local Network", "ip": ip}
    
    # Try ipapi.co with reduced timeout
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=2).json()
        if not geo.get('error') and geo.get('city'):
            return {
                "country": geo.get("country_name", "Unknown"),
                "city": geo.get("city", "Unknown"),
                "latitude": geo.get("latitude", 0),
                "longitude": geo.get("longitude", 0),
                "isp": geo.get("org", "Unknown"),
                "ip": geo.get("ip", ip)
            }
    except:
        pass
    
    # Quick fallback
    return {"country": "India", "city": "Unknown", "latitude": 0, "longitude": 0, "isp": "Unknown", "ip": ip}

class AdvancedBlockchain:
    def __init__(self):
        self.chain = []
        self.pending = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = {
            'index': 0,
            'timestamp': datetime.now().isoformat(),
            'proof': 100,
            'previous_hash': '0',
            'transactions': [],
            'merkle_root': hashlib.sha256(b"genesis").hexdigest()
        }
        self.chain.append(genesis)
    
    def create_block(self, proof, prev_hash):
        block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(),
            'proof': proof,
            'previous_hash': prev_hash,
            'transactions': self.pending,
            'merkle_root': self.merkle_root(self.pending)
        }
        current_hash = self.hash(block)
        self.pending = []
        self.chain.append(block)
        
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO blockchain_audit (block_index, timestamp, event_type, event_data, 
                                             previous_hash, current_hash, merkle_root, nonce)
                VALUES (%s, NOW(3), 'BLOCK', %s, %s, %s, %s, %s)
            """, (block['index'], json.dumps(block['transactions']), prev_hash, 
                  current_hash, block['merkle_root'], proof))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print(f"Blockchain DB error: {e}")
        
        return block
    
    def add_transaction(self, tx):
        tx['tx_id'] = secrets.token_hex(16)
        tx['timestamp'] = datetime.now().isoformat()
        self.pending.append(tx)
        
        if len(self.pending) >= 3:
            prev = self.chain[-1]
            proof = self.pow(prev['proof'])
            self.create_block(proof, self.hash(prev))
    
    def merkle_root(self, txs):
        if not txs:
            return hashlib.sha256(b"empty").hexdigest()
        hashes = [hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest() for t in txs]
        while len(hashes) > 1:
            if len(hashes) % 2:
                hashes.append(hashes[-1])
            hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest() 
                     for i in range(0, len(hashes), 2)]
        return hashes[0]
    
    def pow(self, prev):
        proof = 1
        while True:
            h = hashlib.sha256(str(proof**2 - prev**2).encode()).hexdigest()
            if h[:4] == '0000':
                return proof
            proof += 1
    
    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

blockchain = AdvancedBlockchain()

def calculate_risk(username, db):
    risk = 0
    signals = []
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT COUNT(*) as c FROM login_logs 
        WHERE user_id=%s AND (HOUR(login_time) < 8 OR HOUR(login_time) > 18)
        AND login_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)
    """, (username,))
    odd = cursor.fetchone()['c']
    if odd > 0:
        risk += odd * 8
        signals.append(f"ODD_HOUR({odd})")
    
    cursor.execute("""
        SELECT COUNT(*) as c FROM login_logs 
        WHERE user_id=%s AND success=0 
        AND login_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
    """, (username,))
    failed = cursor.fetchone()['c']
    if failed > 2:
        risk += failed * 12
        signals.append(f"FAILED_LOGIN({failed})")
    
    cursor.execute("""
        SELECT COUNT(DISTINCT ip_address) as c FROM login_logs 
        WHERE user_id=%s AND login_time > DATE_SUB(NOW(), INTERVAL 2 HOUR)
    """, (username,))
    ips = cursor.fetchone()['c']
    if ips > 3:
        risk += 15
        signals.append(f"MULTI_IP({ips})")
    
    cursor.execute("""
        SELECT COUNT(*) as c FROM login_logs 
        WHERE user_id=%s AND DAYOFWEEK(login_time) IN (1,7)
        AND login_time > DATE_SUB(NOW(), INTERVAL 7 DAY)
    """, (username,))
    weekend = cursor.fetchone()['c']
    if weekend > 3:
        risk += weekend * 4
        signals.append(f"WEEKEND({weekend})")
    
    cursor.execute("""
        SELECT COUNT(*) as c FROM file_access_logs 
        WHERE user_id=%s AND action IN ('DELETE', 'delete')
        AND access_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
    """, (username,))
    dels = cursor.fetchone()['c']
    if dels > 10:
        risk += 25
        signals.append(f"MASS_DELETE({dels})")
    
    cursor.execute("""
        SELECT COUNT(*) as c FROM file_access_logs 
        WHERE user_id=%s AND access_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
    """, (username,))
    files = cursor.fetchone()['c']
    if files > 100:
        risk += 18
        signals.append(f"EXCESSIVE_FILES({files})")
    
    cursor.close()
    
    risk = min(risk, 100)
    confidence = min(len(signals) * 10, 100) if signals else 0
    
    if risk <= 20:
        return {"risk_score": risk, "level": "LOW", "decision": "ALLOW", "zone": "CRITICAL", "signals": signals, "confidence": confidence}
    elif risk <= 40:
        return {"risk_score": risk, "level": "MEDIUM", "decision": "ALLOW", "zone": "SENSITIVE", "signals": signals, "confidence": confidence}
    elif risk <= 60:
        return {"risk_score": risk, "level": "HIGH", "decision": "RESTRICT", "zone": "INTERNAL", "signals": signals, "confidence": confidence}
    else:
        return {"risk_score": risk, "level": "CRITICAL", "decision": "DENY", "zone": "PUBLIC", "signals": signals, "confidence": confidence}

@app.post("/auth/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Username exists"}
        
        cursor.execute("""
            INSERT INTO users (username, password, role, status, created_at)
            VALUES (%s, %s, 'user', 'pending', NOW(3))
        """, (username, password))
        db.commit()
        
        blockchain.add_transaction({"type": "REGISTER", "user": username, "ip": request.client.host})
        
        cursor.close()
        db.close()
        
        return {"status": "SUCCESS", "message": "Registration successful! Waiting for admin approval."}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.post("/auth/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        ip = request.client.host
        geo = get_real_geolocation(ip)
        
        # Get browser device info from headers
        user_agent = request.headers.get('user-agent', 'Unknown')
        device_id = hashlib.md5(f"{username}{user_agent}".encode()).hexdigest()[:16]
        
        success = bool(user)
        
        # Insert login log with device info
        cursor.execute("""
            INSERT INTO login_logs (user_id, login_time, ip_address, success, country, city, latitude, longitude, isp, device_id, user_agent)
            VALUES (%s, NOW(3), %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, geo["ip"], success, geo["country"], geo["city"], geo["latitude"], geo["longitude"], geo["isp"], device_id, user_agent))
        login_id = cursor.lastrowid
        db.commit()
        
        if not user:
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Invalid credentials"}
        
        if user["status"] == "pending":
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Account pending approval"}
        
        if user["status"] == "revoked":
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Access revoked"}
        
        # Create JWT token
        token = create_jwt_token(username, user["role"])
        
        # Save session to DB with login_id reference
        session_id = secrets.token_hex(32)
        cursor.execute("""
            INSERT INTO sessions (session_id, user_id, ip_address, created_at, last_activity, expires_at, is_active, login_id)
            VALUES (%s, %s, %s, NOW(3), NOW(3), DATE_ADD(NOW(3), INTERVAL 5 MINUTE), 1, %s)
        """, (session_id, username, geo["ip"], login_id))
        db.commit()
        
        # Update device_logs with browser info initially
        cursor.execute("""
            INSERT INTO device_logs (user_id, device_id, ip_address, first_seen, last_seen, login_count)
            VALUES (%s, %s, %s, NOW(3), NOW(3), 1)
            ON DUPLICATE KEY UPDATE last_seen=NOW(3), ip_address=%s, login_count=login_count+1
        """, (username, device_id, geo["ip"], geo["ip"]))
        db.commit()
        
        risk = calculate_risk(username, db)
        
        cursor.execute("UPDATE users SET risk_score=%s, last_login=NOW(3) WHERE username=%s", 
                      (risk["risk_score"], username))
        db.commit()
        
        cursor.execute("""
            INSERT INTO access_decisions (user_id, resource_type, decision, risk_score, zone, timestamp)
            VALUES (%s, 'LOGIN', %s, %s, %s, NOW(3))
        """, (username, risk["decision"], risk["risk_score"], risk["zone"]))
        db.commit()
        
        if risk["risk_score"] > 40:
            severity = "high" if risk["risk_score"] > 60 else "medium"
            cursor.execute("""
                INSERT INTO risk_events (user_id, event_type, risk_score, confidence_score, severity, description, detected_at)
                VALUES (%s, 'HIGH_RISK_LOGIN', %s, %s, %s, %s, NOW(3))
            """, (username, risk["risk_score"], risk["confidence"], severity, ", ".join(risk["signals"])))
            db.commit()
        
        blockchain.add_transaction({
            "type": "LOGIN",
            "user": username,
            "ip": geo["ip"],
            "location": f"{geo['city']}, {geo['country']}",
            "risk": risk["risk_score"],
            "decision": risk["decision"]
        })
        
        cursor.close()
        db.close()
        
        return {
            "status": "SUCCESS",
            "token": token,
            "session_id": token,
            "user": username,
            "role": user["role"],
            "location": f"{geo['city']}, {geo['country']}",
            "latitude": geo["latitude"],
            "longitude": geo["longitude"],
            "isp": geo["isp"],
            "risk_score": risk["risk_score"],
            "risk_level": risk["level"],
            "decision": risk["decision"],
            "access_zone": risk["zone"],
            "confidence": risk["confidence"],
            "signals": risk["signals"],
            "session_timeout": SESSION_TIMEOUT
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/security/analyze/admin")
async def analyze_admin():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.username, u.role, u.status, u.risk_score, u.last_login,
                   (SELECT COUNT(*) FROM login_logs WHERE user_id=u.username) as login_count,
                   (SELECT COUNT(*) FROM sessions WHERE user_id=u.username AND is_active=1) as active_sessions
            FROM users u WHERE u.status='active' AND u.role='user' ORDER BY u.risk_score DESC
        """)
        users = cursor.fetchall()
        
        result = []
        for user in users:
            risk = calculate_risk(user['username'], db)
            
            # Get latest device info from device_logs OR agent data
            cursor.execute("""
                SELECT mac_address, wifi_ssid, hostname, os, ip_address, last_seen
                FROM device_logs 
                WHERE user_id=%s 
                  AND (mac_address IS NOT NULL OR hostname IS NOT NULL)
                ORDER BY last_seen DESC 
                LIMIT 1
            """, (user['username'],))
            device = cursor.fetchone()
            
            # Get last login with location
            cursor.execute("""
                SELECT ip_address, city, country, login_time
                FROM login_logs WHERE user_id=%s AND success=1 ORDER BY login_time DESC LIMIT 1
            """, (user['username'],))
            location = cursor.fetchone()
            
            # Calculate current session duration
            cursor.execute("""
                SELECT TIMESTAMPDIFF(SECOND, created_at, NOW(3)) as duration
                FROM sessions WHERE user_id=%s AND is_active=1 ORDER BY created_at DESC LIMIT 1
            """, (user['username'],))
            session_dur = cursor.fetchone()
            
            result.append({
                "username": user['username'],
                "user": user['username'],
                "role": user['role'],
                "status": user['status'],
                "risk_score": risk['risk_score'],
                "risk_level": risk['level'],
                "decision": risk['decision'],
                "zone": risk['zone'],
                "signals": risk['signals'],
                "confidence": risk['confidence'],
                "login_count": user['login_count'],
                "total_logins": user['login_count'],
                "active_sessions": user['active_sessions'],
                "session_duration": session_dur['duration'] if session_dur else 0,
                "last_login": user['last_login'],
                "mac_address": device['mac_address'] if device else "N/A",
                "wifi_ssid": device['wifi_ssid'] if device else "N/A",
                "hostname": device['hostname'] if device else "N/A",
                "os": device['os'] if device else "N/A",
                "ip_address": device['ip_address'] if device else (location['ip_address'] if location else "N/A"),
                "city": location['city'] if location else "Unknown",
                "country": location['country'] if location else "Unknown"
            })
        
        cursor.close()
        db.close()
        
        return {"users": result}
    except Exception as e:
        return {"error": str(e), "users": []}

@app.get("/security/analyze/user/{username}")
async def analyze_user(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        
        if not user:
            return {"error": "User not found"}
        
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as successful
            FROM login_logs WHERE user_id=%s
        """, (username,))
        login_stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT COUNT(*) as total FROM file_access_logs WHERE user_id=%s
        """, (username,))
        file_stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT device_id, mac_address, os, hostname, wifi_ssid, ip_address, last_seen
            FROM device_logs WHERE user_id=%s ORDER BY last_seen DESC LIMIT 1
        """, (username,))
        device = cursor.fetchone()
        
        cursor.execute("""
            SELECT ip_address, city, country, latitude, longitude, isp, login_time
            FROM login_logs WHERE user_id=%s AND success=1 ORDER BY login_time DESC LIMIT 1
        """, (username,))
        last_login = cursor.fetchone()
        
        risk = calculate_risk(username, db)
        
        cursor.close()
        db.close()
        
        return {
            "username": user['username'],
            "role": user['role'],
            "status": user['status'],
            "risk_score": risk['risk_score'],
            "risk_level": risk['level'],
            "decision": risk['decision'],
            "zone": risk['zone'],
            "login_count": login_stats['total'],
            "total_logins": login_stats['total'],
            "successful_logins": login_stats['successful'],
            "file_access_count": file_stats['total'],
            "signals": risk['signals'],
            "confidence": risk['confidence'],
            "accessible_resources": [risk['zone'], "PUBLIC"] if risk['decision'] == 'ALLOW' else ["PUBLIC"],
            "mac_address": device['mac_address'] if device else "N/A",
            "wifi_ssid": device['wifi_ssid'] if device else "N/A",
            "hostname": device['hostname'] if device else "N/A",
            "os": device['os'] if device else "N/A",
            "ip_address": last_login['ip_address'] if last_login else "N/A",
            "city": last_login['city'] if last_login else "Unknown",
            "country": last_login['country'] if last_login else "Unknown",
            "last_login": last_login['login_time'].isoformat() if last_login and last_login['login_time'] else None
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/pending-users")
async def get_pending_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, email, department, created_at FROM users WHERE status='pending' ORDER BY created_at DESC")
        pending = cursor.fetchall()
        cursor.close()
        db.close()
        return {"pending_users": pending}
    except Exception as e:
        return {"error": str(e)}

@app.post("/admin/approve-user")
async def approve_user_alt(username: str = Form(...), admin: str = Form(...), action: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        
        if action == "approve":
            cursor.execute("""
                UPDATE users SET status='active', approved_by=%s, approved_at=NOW(3) 
                WHERE username=%s
            """, (admin, username))
            blockchain.add_transaction({"type": "APPROVE", "user": username, "admin": admin})
        elif action == "deny":
            cursor.execute("DELETE FROM users WHERE username=%s AND status='pending'", (username,))
            blockchain.add_transaction({"type": "DENY", "user": username, "admin": admin})
        
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/admin/revoke-access")
async def revoke_user_access(username: str = Form(...), admin: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET status='revoked' WHERE username=%s", (username,))
        db.commit()
        cursor.close()
        db.close()
        
        blockchain.add_transaction({"type": "REVOKE", "user": username, "admin": admin})
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/file-access")
async def admin_file_access():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, file_name, file_path, action, access_time, ip_address, sensitivity_level
            FROM file_access_logs ORDER BY access_time DESC LIMIT 100
        """)
        logs = cursor.fetchall()
        cursor.close()
        db.close()
        return {"file_logs": logs}
    except Exception as e:
        return {"error": str(e)}

@app.get("/audit/chain")
async def audit_chain():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT block_index, timestamp, event_type, event_data, current_hash, merkle_root, previous_hash
            FROM blockchain_audit ORDER BY block_index DESC LIMIT 50
        """)
        blocks = cursor.fetchall()
        cursor.close()
        db.close()
        return {"blockchain": blocks, "length": len(blocks), "valid": True}
    except Exception as e:
        return {"blockchain": blockchain.chain, "length": len(blockchain.chain), "valid": True}

@app.post("/files/access")
async def file_access(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        file_name = data.get("file_name")
        action = data.get("action", "READ").upper()
        
        db = get_db()
        cursor = db.cursor()
        
        ip = request.client.host
        
        sensitivity = "critical" if "secret" in file_name.lower() or "database" in file_name.lower() else \
                     "sensitive" if "admin" in file_name.lower() or "credential" in file_name.lower() else \
                     "internal" if "report" in file_name.lower() or "analytics" in file_name.lower() else "public"
        
        cursor.execute("""
            INSERT INTO file_access_logs (user_id, file_name, action, ip_address, access_time, sensitivity_level)
            VALUES (%s, %s, %s, %s, NOW(3), %s)
        """, (user_id, file_name, action, ip, sensitivity))
        db.commit()
        
        cursor.close()
        db.close()
        
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/files/list/{username}")
async def list_files(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT file_name, action, ip_address, access_time
            FROM file_access_logs WHERE user_id=%s ORDER BY access_time DESC LIMIT 50
        """, (username,))
        files = cursor.fetchall()
        cursor.close()
        db.close()
        return files
    except Exception as e:
        return []

@app.post("/device/register")
async def register_device(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        device_id = data.get("device_id")
        mac_address = data.get("mac_address")
        os = data.get("os")
        wifi_ssid = data.get("wifi_ssid")
        hostname = data.get("hostname")
        ip_address = request.client.host
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("""
            INSERT INTO device_logs (user_id, device_id, mac_address, os, hostname, wifi_ssid, ip_address, first_seen, last_seen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(3), NOW(3))
            ON DUPLICATE KEY UPDATE last_seen=NOW(3), ip_address=%s, mac_address=%s, wifi_ssid=%s
        """, (username, device_id, mac_address, os, hostname, wifi_ssid, ip_address, ip_address, mac_address, wifi_ssid))
        db.commit()
        
        cursor.close()
        db.close()
        
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/user-sessions/{username}")
async def get_user_sessions(username: str):
    """Get complete session history with device fingerprints and activities per session"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get all login sessions with device info and linked activities
        cursor.execute("""
            SELECT 
                l.id as login_id,
                l.login_time,
                l.ip_address,
                l.city,
                l.country,
                l.device_id,
                l.mac_address as login_mac,
                l.user_agent,
                s.session_id,
                s.is_active,
                s.created_at as session_start,
                s.last_activity,
                TIMESTAMPDIFF(SECOND, s.created_at, COALESCE(s.last_activity, NOW(3))) as session_duration_seconds
            FROM login_logs l
            LEFT JOIN sessions s ON l.id = s.login_id
            WHERE l.user_id = %s AND l.success = 1
            ORDER BY l.login_time DESC
            LIMIT 50
        """, (username,))
        sessions = cursor.fetchall()
        
        # Get latest device info from device_logs (GUI tool data)
        cursor.execute("""
            SELECT mac_address, wifi_ssid, hostname, os
            FROM device_logs 
            WHERE user_id = %s AND (mac_address IS NOT NULL OR hostname IS NOT NULL)
            ORDER BY last_seen DESC LIMIT 1
        """, (username,))
        device_info = cursor.fetchone()
        
        # Apply device info to all sessions
        for session in sessions:
            session['mac_address'] = device_info['mac_address'] if device_info else (session['login_mac'] or 'N/A')
            session['wifi_ssid'] = device_info['wifi_ssid'] if device_info else 'N/A'
            session['hostname'] = device_info['hostname'] if device_info else 'N/A'
            session['os'] = device_info['os'] if device_info else 'N/A'
        
        # For each session, get file and network activity
        for session in sessions:
            login_time = session['login_time']
            next_login_time = None
            
            # Find next login time to bound activities
            cursor.execute("""
                SELECT login_time FROM login_logs 
                WHERE user_id = %s AND login_time > %s AND success = 1
                ORDER BY login_time ASC LIMIT 1
            """, (username, login_time))
            next_login = cursor.fetchone()
            if next_login:
                next_login_time = next_login['login_time']
            
            # Get file activities for this session
            if next_login_time:
                cursor.execute("""
                    SELECT file_name, file_path, action, access_time, sensitivity_level
                    FROM file_access_logs
                    WHERE user_id = %s AND access_time >= %s AND access_time < %s
                    ORDER BY access_time ASC
                """, (username, login_time, next_login_time))
            else:
                cursor.execute("""
                    SELECT file_name, file_path, action, access_time, sensitivity_level
                    FROM file_access_logs
                    WHERE user_id = %s AND access_time >= %s
                    ORDER BY access_time ASC
                """, (username, login_time))
            session['file_activities'] = cursor.fetchall()
            
            # Get network activities for this session
            if next_login_time:
                cursor.execute("""
                    SELECT remote_ip, remote_port, protocol, is_external, connection_time
                    FROM network_connections
                    WHERE user_id = %s AND connection_time >= %s AND connection_time < %s
                    ORDER BY connection_time ASC
                """, (username, login_time, next_login_time))
            else:
                cursor.execute("""
                    SELECT remote_ip, remote_port, protocol, is_external, connection_time
                    FROM network_connections
                    WHERE user_id = %s AND connection_time >= %s
                    ORDER BY connection_time ASC
                """, (username, login_time))
            session['network_activities'] = cursor.fetchall()
        
        # Get user stats
        cursor.execute("""
            SELECT COUNT(*) as active_sessions
            FROM sessions WHERE user_id = %s AND is_active = 1
        """, (username,))
        active_sessions = cursor.fetchone()['active_sessions']
        
        cursor.execute("""
            SELECT TIMESTAMPDIFF(SECOND, created_at, NOW(3)) as duration
            FROM sessions WHERE user_id = %s AND is_active = 1 
            ORDER BY created_at DESC LIMIT 1
        """, (username,))
        current_duration = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        return {
            "username": username,
            "sessions": sessions,
            "total_sessions": len(sessions),
            "active_sessions": active_sessions,
            "current_session_duration": current_duration['duration'] if current_duration else 0
        }
    except Exception as e:
        print(f"Error in get_user_sessions: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "sessions": [], "total_sessions": 0, "active_sessions": 0, "current_session_duration": 0}

@app.post("/agent/telemetry")
async def agent_telemetry(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        
        db = get_db()
        cursor = db.cursor()
        
        if "files" in data:
            for f in data["files"]:
                cursor.execute("""
                    INSERT INTO file_access_logs (user_id, file_name, file_path, action, file_size, 
                                                  sensitivity_level, access_time)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(3))
                """, (username, f.get("name"), f.get("path"), f.get("action"), 
                      f.get("size"), f.get("sensitivity", "internal")))
        
        if "network" in data:
            for n in data["network"]:
                cursor.execute("""
                    INSERT INTO network_connections (user_id, connection_type, remote_ip, remote_port,
                                                    protocol, is_external, connection_time)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(3))
                """, (username, n.get("type"), n.get("ip"), n.get("port"), 
                      n.get("protocol"), n.get("external", False)))
        
        if "device" in data:
            d = data["device"]
            cursor.execute("""
                INSERT INTO device_logs (user_id, device_id, mac_address, os, hostname, 
                                        wifi_ssid, ip_address, first_seen, last_seen, login_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(3), NOW(3), 1)
                ON DUPLICATE KEY UPDATE 
                    last_seen=NOW(3), 
                    mac_address=COALESCE(%s, mac_address), 
                    wifi_ssid=COALESCE(%s, wifi_ssid), 
                    ip_address=%s,
                    hostname=COALESCE(%s, hostname),
                    os=COALESCE(%s, os)
            """, (username, d.get("id"), d.get("mac"), d.get("os"), 
                  d.get("hostname"), d.get("wifi"), d.get("ip"),
                  d.get("mac"), d.get("wifi"), d.get("ip"),
                  d.get("hostname"), d.get("os")))
        
        db.commit()
        cursor.close()
        db.close()
        
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("Zero Trust System - JWT + 5min Sessions")
    print("JWT Authentication | Device Fingerprints | Blockchain")
    uvicorn.run(app, host="0.0.0.0", port=8000)
