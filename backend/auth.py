from fastapi import APIRouter, Request
from datetime import datetime
from database import get_db
import psycopg2.extras

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(request: Request, username: str, password: str):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    success = bool(user)
    ip = request.client.host
    
    # Get real public IP if behind proxy/NAT
    real_ip = ip
    try:
        import requests
        public_ip_response = requests.get("https://api.ipify.org?format=json", timeout=3).json()
        real_ip = public_ip_response.get("ip", ip)
    except:
        pass
    
    # Get geolocation from real public IP
    country = "Unknown"
    city = "Unknown"
    
    try:
        import requests
        # Try ip-api.com with real public IP
        geo = requests.get(f"http://ip-api.com/json/{real_ip}", timeout=3).json()
        if geo.get("status") == "success":
            country = geo.get("country", "Unknown")
            city = geo.get("city", "Unknown")
            lat = geo.get("lat")
            lon = geo.get("lon")
            if lat and lon:
                city = f"{city} ({lat:.2f}, {lon:.2f})"
    except:
        pass
    
    # If still unknown, try ipapi.co
    if country == "Unknown":
        try:
            import requests
            geo = requests.get(f"https://ipapi.co/{real_ip}/json/", timeout=3).json()
            country = geo.get("country_name", "Unknown")
            city = geo.get("city", "Unknown")
            lat = geo.get("latitude")
            lon = geo.get("longitude")
            if lat and lon:
                city = f"{city} ({lat:.2f}, {lon:.2f})"
        except:
            pass
    
    # If still unknown and local IP, mark as local
    if country == "Unknown" and (ip.startswith(("127.", "10.", "192.168.", "172.")) or ip in ["localhost", "::1"]):
        country = "Local Network"
        city = "Private IP"
    
    cursor.execute("""
        INSERT INTO login_logs (user_id, login_time, ip_address, success, country, city)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (username, datetime.now(), real_ip, success, country, city))
    db.commit()
    cursor.close()
    db.close()
    
    if not success:
        return {"status": "FAIL"}
    
    return {
        "status": "SUCCESS",
        "user": username,
        "role": user["role"],
        "location": f"{city}, {country}"
    }
