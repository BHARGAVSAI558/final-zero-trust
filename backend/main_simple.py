from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="zerotrust"
    )

app = FastAPI(title="Zero Trust Security Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": "Invalid credentials"}
        
        if user["status"] != "active":
            cursor.close()
            db.close()
            return {"status": "FAIL", "message": f"Account {user['status']}"}
        
        cursor.close()
        db.close()
        
        return {
            "status": "SUCCESS",
            "user": username,
            "role": user["role"],
            "location": "Local, India"
        }
    except Exception as e:
        print(f"Login error: {e}")
        return {"status": "FAIL", "error": str(e)}

@app.get("/security/analyze/admin")
async def analyze_admin():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT username, role, status, risk_score FROM users WHERE role='user' AND status='active'")
        users = cursor.fetchall()
        
        result = []
        for user in users:
            result.append({
                "username": user['username'],
                "role": user['role'],
                "status": user['status'],
                "risk_score": user['risk_score'] or 0,
                "risk_level": "LOW",
                "decision": "ALLOW",
                "zone": "CRITICAL",
                "signals": [],
                "mac_address": "N/A",
                "wifi_ssid": "N/A",
                "hostname": "N/A",
                "os": "N/A",
                "ip_address": "127.0.0.1",
                "city": "Unknown",
                "country": "India"
            })
        
        cursor.close()
        db.close()
        
        return {"users": result}
    except Exception as e:
        print(f"Admin error: {e}")
        return {"users": []}

@app.get("/security/analyze/user/{username}")
async def analyze_user(username: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        
        if not user:
            return {"error": "User not found"}
        
        cursor.close()
        db.close()
        
        return {
            "username": user['username'],
            "role": user['role'],
            "status": user['status'],
            "risk_score": user['risk_score'] or 0,
            "risk_level": "LOW",
            "decision": "ALLOW",
            "zone": "CRITICAL",
            "signals": [],
            "accessible_resources": ["CRITICAL", "PUBLIC"],
            "mac_address": "N/A",
            "wifi_ssid": "N/A",
            "hostname": "N/A",
            "os": "N/A"
        }
    except Exception as e:
        print(f"User error: {e}")
        return {"error": str(e)}

@app.get("/admin/pending-users")
async def get_pending_users():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username, created_at FROM users WHERE status='pending'")
        pending = cursor.fetchall()
        cursor.close()
        db.close()
        return {"pending_users": pending}
    except:
        return {"pending_users": []}

@app.post("/admin/approve-user")
async def approve_user(username: str = Form(...), admin: str = Form(...), action: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        
        if action == "approve":
            cursor.execute("UPDATE users SET status='active' WHERE username=%s", (username,))
        elif action == "deny":
            cursor.execute("DELETE FROM users WHERE username=%s", (username,))
        
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAIL"}

@app.post("/admin/revoke-access")
async def revoke_access(username: str = Form(...), admin: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET status='revoked' WHERE username=%s", (username,))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAIL"}

@app.get("/admin/file-access")
async def admin_file_access():
    return {"file_logs": []}

@app.get("/audit/chain")
async def audit_chain():
    return {"blockchain": [], "length": 0, "valid": True}

@app.post("/files/access")
async def file_access(request: Request):
    return {"status": "SUCCESS"}

@app.get("/files/list/{username}")
async def list_files(username: str):
    return []

if __name__ == "__main__":
    import uvicorn
    print("🛡️ Zero Trust System - Simple Mode")
    print("✓ Basic Authentication | ✓ MySQL Database")
    uvicorn.run(app, host="0.0.0.0", port=8000)
