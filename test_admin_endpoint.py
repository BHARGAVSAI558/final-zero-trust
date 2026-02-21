import sys
sys.path.insert(0, 'backend')

from mysql_database import get_db
from advanced_ueba import calculate_advanced_risk

def admin_view():
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
                risk_data = calculate_advanced_risk(username, db)
                
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
        cursor.close()
        db.close()
        return {"users": result}
    except Exception as e:
        print(f"Admin view error: {e}")
        import traceback
        traceback.print_exc()
        return {"users": []}

result = admin_view()
print(f"SUCCESS! Got {len(result['users'])} users")
for u in result['users']:
    print(f"  - {u['username']}: {u['risk_level']}")
