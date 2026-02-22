from fastapi import FastAPI, Request, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import os
import requests
import hashlib
import json
import psycopg2.extras
from websocket_manager import manager
from advanced_ueba import calculate_advanced_risk
from database_file_api import router as file_router
from mysql_api import router as mysql_router
from realtime_file_api import router as realtime_file_router
from activity_tracker import ActivityTracker
from mysql_database import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Zero Trust Security Platform", lifespan=lifespan)

app.include_router(file_router)
app.include_router(mysql_router)
app.include_router(realtime_file_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_geolocation(ip):
    if ip == "127.0.0.1" or ip == "localhost":
        # Try multiple geolocation services for localhost
        try:
            geo = requests.get("https://ipapi.co/json/", timeout=3).json()
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
        
        try:
            geo = requests.get("http://ip-api.com/json/", timeout=3).json()
            if geo.get('status') == 'success':
                return {
                    "country": geo.get("country", "Unknown"),
                    "city": geo.get("city", "Unknown"),
                    "region": geo.get("regionName", "Unknown"),
                    "latitude": geo.get("lat", 0),
                    "longitude": geo.get("lon", 0),
                    "timezone": geo.get("timezone", "Unknown"),
                    "isp": geo.get("isp", "Unknown"),
                    "ip": geo.get("query", ip),
                    "postal": geo.get("zip", "Unknown")
                }
        except:
            pass
    
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3).json()
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
    
    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
        if geo.get('status') == 'success':
            return {
                "country": geo.get("country", "Unknown"),
                "city": geo.get("city", "Unknown"),
                "region": geo.get("regionName", "Unknown"),
                "latitude": geo.get("lat", 0),
                "longitude": geo.get("lon", 0),
                "timezone": geo.get("timezone", "Unknown"),
                "isp": geo.get("isp", "Unknown"),
                "ip": geo.get("query", ip),
                "postal": geo.get("zip", "Unknown")
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
async def login(request: Request, username: str = Form(...), password: str = Form(...), 
                city: str = Form(None), country: str = Form(None), 
                latitude: float = Form(None), longitude: float = Form(None)):
    try:
        db = get_db()
        cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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
        
        # Get real public IP
        try:
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
        except:
            try:
                public_ip = requests.get('https://icanhazip.com', timeout=3).text.strip()
            except:
                public_ip = request.client.host if request.client else "127.0.0.1"
        
        # Use provided location or fallback to IP geolocation
        if city and country:
            geo = {
                "ip": public_ip,
                "city": city,
                "country": country,
                "latitude": latitude or 0,
                "longitude": longitude or 0,
                "timezone": "Unknown",
                "isp": "Unknown"
            }
        else:
            geo = get_geolocation(public_ip)
        
        cursor.execute("INSERT INTO login_logs (user_id, login_time, ip_address, success, country, city, latitude, longitude, mac_address, hostname, device_os) VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                      (username, geo["ip"], True, geo["country"], geo["city"], geo.get("latitude", 0), geo.get("longitude", 0), "Pending", "Pending", "Pending"))
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
        return {"status": "SUCCESS", "user": username, "role": user["role"], "location": f"{geo['city']}, {geo['country']}", "latitude": geo["latitude"], "longitude": geo["longitude"], "timezone": geo.get("timezone", "Unknown"), "isp": geo.get("isp", "Unknown"), "risk_score": risk_data["risk_score"], "risk_level": risk_data["risk_level"], "decision": risk_data["decision"], "access_zone": risk_data["zone"]}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Zero Trust Platform"}

@app.get("/init-database")
def init_database():
    """Initialize database with tables and admin user - Call this once after deployment"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Create tables (PostgreSQL syntax)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(50),
                success BOOLEAN DEFAULT TRUE,
                country VARCHAR(100),
                city VARCHAR(100),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                mac_address VARCHAR(50) DEFAULT 'Pending',
                hostname VARCHAR(100) DEFAULT 'Pending',
                device_os VARCHAR(100) DEFAULT 'Pending',
                wifi_ssid VARCHAR(100) DEFAULT 'N/A'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                device_id VARCHAR(100),
                mac_address VARCHAR(50),
                os VARCHAR(100),
                os_version VARCHAR(50),
                wifi_ssid VARCHAR(100),
                hostname VARCHAR(100),
                ip_address VARCHAR(50),
                trusted BOOLEAN DEFAULT FALSE,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, device_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_access_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_path TEXT,
                action VARCHAR(50) NOT NULL,
                sensitivity_level VARCHAR(50) DEFAULT 'internal',
                ip_address VARCHAR(50),
                access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                device_id VARCHAR(100)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                connection_type VARCHAR(100),
                remote_ip VARCHAR(50),
                remote_port INT,
                protocol VARCHAR(20),
                external BOOLEAN DEFAULT FALSE,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert admin user if not exists
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role, status) VALUES (%s, %s, %s, %s)",
                ('admin', 'admin123', 'admin', 'active')
            )
        
        db.commit()
        cursor.close()
        db.close()
        
        return {
            "status": "SUCCESS",
            "message": "Database initialized successfully",
            "tables_created": ["users", "login_logs", "device_logs", "file_access_logs", "network_logs"],
            "admin_user": "admin / admin123"
        }
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.post("/device/register")
async def register_device(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        db = get_db()
        cursor = db.cursor()
        
        # Store device info
        cursor.execute("""
            INSERT INTO device_logs 
            (user_id, device_id, mac_address, os, wifi_ssid, hostname, ip_address, trusted, first_seen, last_seen) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s, NOW(), NOW()) 
            ON DUPLICATE KEY UPDATE 
            ip_address=VALUES(ip_address), 
            os=VALUES(os), 
            wifi_ssid=VALUES(wifi_ssid),
            hostname=VALUES(hostname),
            last_seen=NOW()
        """, (
            username, 
            data.get("device_id"), 
            data.get("mac"), 
            data.get("os"), 
            data.get("wifi_ssid", "N/A"), 
            data.get("hostname"), 
            data.get("ip"), 
            False
        ))
        
        # Update ONLY the most recent login that still has "Pending" values
        cursor.execute("""
            UPDATE login_logs 
            SET mac_address = %s, hostname = %s, device_os = %s, wifi_ssid = %s
            WHERE user_id = %s 
            AND mac_address = 'Pending'
            ORDER BY login_time DESC 
            LIMIT 1
        """, (data.get("mac"), data.get("hostname"), data.get("os"), data.get("wifi_ssid"), username))
        
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.get("/security/analyze/admin")
def admin_view():
    db = None
    cursor = None
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, status FROM users WHERE status='active'")
        users = cursor.fetchall()
        result = []
        for user in users:
            username = user["username"]
            try:
                cursor.execute("SELECT COUNT(*) as total FROM login_logs WHERE user_id=%s", (username,))
                total = cursor.fetchone()["total"]
                cursor.execute("SELECT * FROM login_logs WHERE user_id=%s ORDER BY login_time DESC LIMIT 1", (username,))
                last_login = cursor.fetchone()
                cursor.execute("SELECT * FROM device_logs WHERE user_id=%s ORDER BY last_seen DESC LIMIT 1", (username,))
                device = cursor.fetchone()
                
                db2 = get_db()
                risk_data = calculate_risk_score(username, db2)
                db2.close()
                
                ip_addr = "127.0.0.1"
                country = "India"
                city = "Sivarampuram"
                mac_addr = "Browser-Based"
                hostname_val = "Web-Client"
                os_val = "Windows 10"
                
                if last_login:
                    ip_addr = last_login.get("ip_address", "127.0.0.1")
                    country = last_login.get("country", "India")
                    city = last_login.get("city", "Sivarampuram")
                    if last_login.get("mac_address") and last_login.get("mac_address") != "Browser-Based":
                        mac_addr = last_login.get("mac_address")
                    if last_login.get("hostname") and last_login.get("hostname") != "Web-Client":
                        hostname_val = last_login.get("hostname")
                    if last_login.get("device_os"):
                        os_val = last_login.get("device_os")
                
                if device:
                    if mac_addr == "Browser-Based" and device.get("mac_address"):
                        mac_addr = device.get("mac_address")
                    if hostname_val == "Web-Client" and device.get("hostname"):
                        hostname_val = device.get("hostname")
                    if os_val == "Windows 10" and device.get("os"):
                        os_val = device.get("os")
                
                result.append({
                    "username": username,
                    "risk_score": risk_data["risk_score"],
                    "risk_level": risk_data["risk_level"],
                    "decision": risk_data["decision"],
                    "zone": risk_data["zone"],
                    "signals": risk_data["signals"],
                    "login_count": total,
                    "last_login": str(last_login["login_time"]) if last_login else None,
                    "ip_address": ip_addr,
                    "country": country,
                    "city": city,
                    "mac_address": mac_addr,
                    "wifi_ssid": device["wifi_ssid"] if device else "N/A",
                    "hostname": hostname_val,
                    "os": os_val,
                    "device_id": device["device_id"] if device else "Browser",
                    "status": user["status"]
                })
            except Exception as e:
                print(f"Error processing user {username}: {e}")
                import traceback
                traceback.print_exc()
                continue
        if cursor:
            cursor.close()
        if db:
            db.close()
        return {"users": result}
    except Exception as e:
        print(f"Admin view error: {e}")
        import traceback
        traceback.print_exc()
        if cursor:
            cursor.close()
        if db:
            db.close()
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
        return {"pending_users": [{"username": u["username"], "created_at": str(u["created_at"])} for u in users]}
    except:
        return {"pending_users": []}

@app.post("/admin/approve-user")
async def approve_user(username: str = Form(...), admin: str = Form(...), action: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        if action == 'approve':
            cursor.execute("UPDATE users SET status='active' WHERE username=%s", (username,))
            db.commit()
            blockchain.add_transaction({"type": "USER_APPROVED", "user": username, "admin": admin, "timestamp": str(datetime.now())})
            cursor.close()
            db.close()
            return {"status": "SUCCESS", "message": f"User {username} approved"}
        else:
            cursor.execute("DELETE FROM users WHERE username=%s", (username,))
            db.commit()
            blockchain.add_transaction({"type": "USER_REJECTED", "user": username, "admin": admin, "timestamp": str(datetime.now())})
            cursor.close()
            db.close()
            return {"status": "SUCCESS", "message": f"User {username} rejected"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

@app.post("/admin/revoke-access")
async def revoke_access(username: str = Form(...), admin: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET status='revoked' WHERE username=%s", (username,))
        db.commit()
        blockchain.add_transaction({"type": "ACCESS_REVOKED", "user": username, "admin": admin, "timestamp": str(datetime.now())})
        cursor.close()
        db.close()
        return {"status": "SUCCESS", "message": f"Access revoked for {username}"}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

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

@app.get("/admin/network-activity")
def admin_network():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, connection_type, remote_ip, remote_port, protocol, 
                   MIN(timestamp) as first_seen, MAX(timestamp) as last_seen, COUNT(*) as count
            FROM network_logs 
            WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            GROUP BY user_id, remote_ip, remote_port, protocol
            ORDER BY last_seen DESC 
            LIMIT 50
        """)
        network = cursor.fetchall()
        cursor.close()
        db.close()
        return {"network_logs": [{
            "user_id": n["user_id"], 
            "connection": n["connection_type"], 
            "destination": f"{n['remote_ip']}:{n['remote_port']}",
            "protocol": n["protocol"],
            "port": n["remote_port"],
            "timestamp": f"{n['first_seen'].strftime('%I:%M:%S %p')} - {n['last_seen'].strftime('%I:%M:%S %p')}" if n['count'] > 1 else n['last_seen'].strftime('%m/%d/%Y, %I:%M:%S %p')
        } for n in network]}
    except Exception as e:
        print(f"Network activity error: {e}")
        return {"network_logs": []}

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

@app.post("/track/network/batch")
async def track_network_batch(request: Request):
    try:
        data = await request.json()
        connections = data.get('connections', [])
        if not connections:
            return {"status": "SUCCESS", "count": 0}
        
        db = get_db()
        cursor = db.cursor()
        
        for conn in connections:
            cursor.execute("INSERT INTO network_logs (user_id, connection_type, remote_ip, remote_port, protocol, external, timestamp) VALUES (%s,%s,%s,%s,%s,%s, NOW())", 
                          (conn.get("username"), conn.get("domain", "External"), conn.get("remote_ip"), conn.get("remote_port"), conn.get("protocol"), conn.get("is_external", True)))
        
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS", "count": len(connections)}
    except Exception as e:
        print(f"Network batch error: {e}")
        return {"status": "FAIL", "error": str(e)}

@app.post("/track/network")
async def track_network(request: Request):
    try:
        data = await request.json()
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO network_logs (user_id, connection_type, remote_ip, remote_port, protocol, external, timestamp) VALUES (%s,%s,%s,%s,%s,%s, NOW())", 
                      (data.get("username"), "External", data.get("remote_ip"), data.get("remote_port"), data.get("protocol"), data.get("is_external", True)))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Network track error: {e}")
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
        files = data.get("files", [])
        network = data.get("network", [])
        
        db = get_db()
        cursor = db.cursor()
        
        # Store comprehensive device info
        cursor.execute("""
            INSERT INTO device_logs 
            (user_id, device_id, mac_address, os, os_version, wifi_ssid, hostname, ip_address, trusted, first_seen, last_seen) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, NOW(), NOW()) 
            ON DUPLICATE KEY UPDATE 
            ip_address=VALUES(ip_address), 
            os=VALUES(os), 
            os_version=VALUES(os_version),
            wifi_ssid=VALUES(wifi_ssid),
            hostname=VALUES(hostname),
            last_seen=NOW()
        """, (
            username, 
            device.get("device_id"), 
            device.get("mac"), 
            device.get("os"), 
            device.get("os_version"),
            device.get("wifi", "N/A"), 
            device.get("hostname"), 
            device.get("ip"), 
            False
        ))
        
        # Store file access logs with full details
        for file in files:
            cursor.execute("""
                INSERT INTO file_access_logs 
                (user_id, file_name, file_path, action, sensitivity_level, ip_address, access_time, device_id) 
                VALUES (%s,%s,%s,%s,%s,%s, NOW(),%s)
            """, (
                username, 
                file.get("name"), 
                file.get("path"),
                file.get("action", "READ").upper(),
                file.get("sensitivity", "internal"),
                device.get("ip", "Unknown"),
                device.get("device_id")
            ))
        
        # Store network connections
        for conn in network:
            cursor.execute("""
                INSERT INTO network_logs 
                (user_id, connection_type, remote_ip, remote_port, protocol, external, timestamp) 
                VALUES (%s,%s,%s,%s,%s,%s, NOW())
            """, (
                username, 
                conn.get("type"), 
                conn.get("ip"), 
                conn.get("port"), 
                conn.get("protocol"), 
                conn.get("external", False)
            ))
        
        db.commit()
        cursor.close()
        db.close()
        
        return {
            "status": "SUCCESS", 
            "files_logged": len(files), 
            "network_logged": len(network),
            "device_updated": True
        }
    except Exception as e:
        print(f"Telemetry error: {e}")
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
