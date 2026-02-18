import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== DEVICE DATA CHECK ===\n")

# Check mahesh's device data
cursor.execute("""
    SELECT user_id, device_id, mac_address, wifi_ssid, hostname, os, ip_address, last_seen
    FROM device_logs
    WHERE user_id = 'mahesh'
    ORDER BY last_seen DESC
""")

devices = cursor.fetchall()

print(f"Found {len(devices)} device records for mahesh:\n")

for i, dev in enumerate(devices, 1):
    print(f"Device #{i}:")
    print(f"  Device ID: {dev['device_id']}")
    print(f"  MAC: {dev['mac_address']}")
    print(f"  WiFi: {dev['wifi_ssid']}")
    print(f"  Hostname: {dev['hostname']}")
    print(f"  OS: {dev['os']}")
    print(f"  IP: {dev['ip_address']}")
    print(f"  Last Seen: {dev['last_seen']}")
    print()

# Check what admin dashboard query returns
print("=== ADMIN DASHBOARD QUERY ===\n")
cursor.execute("""
    SELECT mac_address, wifi_ssid, hostname, os, ip_address, last_seen
    FROM device_logs 
    WHERE user_id='mahesh' 
      AND (mac_address IS NOT NULL OR hostname IS NOT NULL)
    ORDER BY last_seen DESC 
    LIMIT 1
""")

result = cursor.fetchone()

if result:
    print("Admin dashboard will show:")
    print(f"  MAC: {result['mac_address']}")
    print(f"  WiFi: {result['wifi_ssid']}")
    print(f"  Hostname: {result['hostname']}")
    print(f"  OS: {result['os']}")
    print(f"  IP: {result['ip_address']}")
else:
    print("No device data found with MAC or hostname!")

cursor.close()
db.close()
