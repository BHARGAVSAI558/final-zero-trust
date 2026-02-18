import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== ALL DEVICE_LOGS FOR MAHESH ===\n")
cursor.execute("SELECT device_id, mac_address, hostname, os, wifi_ssid, ip_address, last_seen FROM device_logs WHERE user_id='mahesh' ORDER BY last_seen DESC")
devices = cursor.fetchall()

for i, device in enumerate(devices, 1):
    print(f"Device #{i}:")
    print(f"  Device ID: {device['device_id']}")
    print(f"  MAC: {device['mac_address']}")
    print(f"  Hostname: {device['hostname']}")
    print(f"  OS: {device['os']}")
    print(f"  WiFi: {device['wifi_ssid']}")
    print(f"  IP: {device['ip_address']}")
    print(f"  Last Seen: {device['last_seen']}")
    print()

cursor.close()
db.close()
