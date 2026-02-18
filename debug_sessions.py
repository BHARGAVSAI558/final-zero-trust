import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== CHECKING MAHESH LOGIN DATA ===\n")

# Check login_logs
cursor.execute("SELECT COUNT(*) as count FROM login_logs WHERE user_id='mahesh'")
print(f"Total login_logs for mahesh: {cursor.fetchone()['count']}")

cursor.execute("SELECT COUNT(*) as count FROM login_logs WHERE user_id='mahesh' AND success=1")
print(f"Successful logins for mahesh: {cursor.fetchone()['count']}")

# Check sessions
cursor.execute("SELECT COUNT(*) as count FROM sessions WHERE user_id='mahesh'")
print(f"Total sessions for mahesh: {cursor.fetchone()['count']}")

# Check if login_id exists in login_logs
cursor.execute("SELECT id, login_time, device_id, mac_address FROM login_logs WHERE user_id='mahesh' AND success=1 ORDER BY login_time DESC LIMIT 5")
logins = cursor.fetchall()
print(f"\n=== RECENT LOGINS ===")
for login in logins:
    print(f"ID: {login['id']}, Time: {login['login_time']}, Device: {login['device_id']}, MAC: {login['mac_address']}")

# Check sessions with login_id
cursor.execute("SELECT session_id, login_id, created_at, is_active FROM sessions WHERE user_id='mahesh' ORDER BY created_at DESC LIMIT 5")
sessions = cursor.fetchall()
print(f"\n=== RECENT SESSIONS ===")
for session in sessions:
    print(f"Session: {session['session_id'][:16]}..., Login_ID: {session['login_id']}, Created: {session['created_at']}, Active: {session['is_active']}")

# Check device_logs
cursor.execute("SELECT device_id, mac_address, hostname, os, wifi_ssid, last_seen FROM device_logs WHERE user_id='mahesh' ORDER BY last_seen DESC LIMIT 3")
devices = cursor.fetchall()
print(f"\n=== DEVICE LOGS ===")
for device in devices:
    print(f"Device: {device['device_id']}, MAC: {device['mac_address']}, Host: {device['hostname']}, OS: {device['os']}, WiFi: {device['wifi_ssid']}, Last: {device['last_seen']}")

cursor.close()
db.close()
