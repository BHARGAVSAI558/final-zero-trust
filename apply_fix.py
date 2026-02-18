import mysql.connector

print("Applying permanent session tracking fix...")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

# Link existing sessions to login_logs
print("\n1. Linking sessions to login_logs...")
cursor.execute("""
    UPDATE sessions s
    LEFT JOIN login_logs l ON s.user_id = l.user_id 
      AND ABS(TIMESTAMPDIFF(SECOND, s.created_at, l.login_time)) < 5
    SET s.login_id = l.id
    WHERE s.login_id IS NULL AND l.id IS NOT NULL
""")
db.commit()
print(f"   Updated {cursor.rowcount} sessions")

# Update device_logs login_count
print("\n2. Updating device login counts...")
cursor.execute("""
    UPDATE device_logs d
    SET login_count = (
      SELECT COUNT(*) 
      FROM login_logs l 
      WHERE l.user_id = d.user_id 
        AND l.device_id = d.device_id 
        AND l.success = 1
    )
    WHERE d.login_count = 0 OR d.login_count IS NULL
""")
db.commit()
print(f"   Updated {cursor.rowcount} devices")

# Verify bhargav's data
print("\n3. Checking bhargav's data...")
cursor.execute("SELECT COUNT(*) as cnt FROM login_logs WHERE user_id='bhargav' AND success=1")
login_count = cursor.fetchone()['cnt']
print(f"   Login records: {login_count}")

cursor.execute("SELECT COUNT(*) as cnt FROM sessions WHERE user_id='bhargav'")
session_count = cursor.fetchone()['cnt']
print(f"   Session records: {session_count}")

cursor.execute("SELECT COUNT(*) as cnt FROM sessions WHERE user_id='bhargav' AND login_id IS NOT NULL")
linked_count = cursor.fetchone()['cnt']
print(f"   Linked sessions: {linked_count}")

# Show last login details
print("\n4. Last login details for bhargav:")
cursor.execute("""
    SELECT 
        l.login_time,
        l.ip_address,
        l.city,
        l.country,
        l.device_id,
        l.mac_address,
        s.is_active,
        TIMESTAMPDIFF(SECOND, s.created_at, COALESCE(s.last_activity, NOW(3))) as duration
    FROM login_logs l
    LEFT JOIN sessions s ON l.id = s.login_id
    WHERE l.user_id = 'bhargav' AND l.success = 1
    ORDER BY l.login_time DESC
    LIMIT 1
""")
last_login = cursor.fetchone()
if last_login:
    print(f"   Time: {last_login['login_time']}")
    print(f"   Location: {last_login['city']}, {last_login['country']}")
    print(f"   IP: {last_login['ip_address']}")
    print(f"   Device ID: {last_login['device_id']}")
    print(f"   MAC: {last_login['mac_address']}")
    print(f"   Active: {last_login['is_active']}")
    print(f"   Duration: {last_login['duration']}s")

cursor.close()
db.close()

print("\n✓ Fix applied successfully!")
print("\nNext steps:")
print("1. Restart backend: cd backend && python main_advanced.py")
print("2. Login as bhargav to create new session")
print("3. Check 'MORE DETAILS' in admin dashboard")
