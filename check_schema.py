import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor()

# Check login_logs structure
print("=== LOGIN_LOGS TABLE ===")
cursor.execute("DESCRIBE login_logs")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")

print("\n=== SESSIONS TABLE ===")
cursor.execute("DESCRIBE sessions")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")

print("\n=== DEVICE_LOGS TABLE ===")
cursor.execute("DESCRIBE device_logs")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")

# Check if bhargav has any login records
print("\n=== BHARGAV LOGIN RECORDS ===")
cursor.execute("SELECT COUNT(*) FROM login_logs WHERE user_id='bhargav'")
print(f"Total logins: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM sessions WHERE user_id='bhargav'")
print(f"Total sessions: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM device_logs WHERE user_id='bhargav'")
print(f"Total devices: {cursor.fetchone()[0]}")

# Check last login
cursor.execute("SELECT login_time, ip_address, success FROM login_logs WHERE user_id='bhargav' ORDER BY login_time DESC LIMIT 1")
result = cursor.fetchone()
if result:
    print(f"Last login: {result[0]} from {result[1]} (success={result[2]})")
else:
    print("No login records found")

cursor.close()
db.close()
