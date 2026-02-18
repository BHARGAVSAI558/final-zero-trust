import mysql.connector
import json

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== COMPREHENSIVE SYSTEM DIAGNOSIS ===\n")

# 1. Check all users
print("1. ALL USERS IN SYSTEM:")
cursor.execute("SELECT username, role, status FROM users")
users = cursor.fetchall()
for u in users:
    print(f"   - {u['username']} ({u['role']}) - {u['status']}")

# 2. Check login_logs structure and data
print("\n2. LOGIN_LOGS ANALYSIS:")
cursor.execute("SELECT user_id, COUNT(*) as cnt, MAX(login_time) as last_login FROM login_logs WHERE success=1 GROUP BY user_id")
login_stats = cursor.fetchall()
for stat in login_stats:
    print(f"   {stat['user_id']}: {stat['cnt']} logins, last: {stat['last_login']}")

# 3. Check if device_id is being populated
print("\n3. DEVICE_ID POPULATION CHECK:")
cursor.execute("SELECT user_id, device_id, mac_address, login_time FROM login_logs WHERE success=1 ORDER BY login_time DESC LIMIT 10")
recent_logins = cursor.fetchall()
for login in recent_logins:
    print(f"   {login['user_id']}: device_id={login['device_id']}, mac={login['mac_address']}, time={login['login_time']}")

# 4. Check sessions table
print("\n4. SESSIONS TABLE:")
cursor.execute("SELECT user_id, COUNT(*) as cnt, SUM(is_active) as active FROM sessions GROUP BY user_id")
session_stats = cursor.fetchall()
for stat in session_stats:
    print(f"   {stat['user_id']}: {stat['cnt']} total sessions, {stat['active']} active")

# 5. Check if sessions are linked to login_logs
print("\n5. SESSION-LOGIN LINKAGE:")
cursor.execute("SELECT COUNT(*) as total FROM sessions")
total_sessions = cursor.fetchone()['total']
cursor.execute("SELECT COUNT(*) as linked FROM sessions WHERE login_id IS NOT NULL")
linked_sessions = cursor.fetchone()['linked']
print(f"   Total sessions: {total_sessions}")
print(f"   Linked sessions: {linked_sessions}")
print(f"   Unlinked: {total_sessions - linked_sessions}")

# 6. Test the actual query used by /admin/user-sessions endpoint
print("\n6. TESTING SESSION HISTORY QUERY FOR 'sai':")
cursor.execute("""
    SELECT 
        l.id,
        l.login_time,
        l.ip_address,
        l.city,
        l.country,
        l.device_id,
        l.mac_address as login_mac,
        l.user_agent,
        s.session_id,
        s.is_active,
        TIMESTAMPDIFF(SECOND, s.created_at, COALESCE(s.last_activity, NOW(3))) as session_duration
    FROM login_logs l
    LEFT JOIN sessions s ON l.user_id = s.user_id AND l.id = s.login_id
    WHERE l.user_id = 'sai' AND l.success = 1
    ORDER BY l.login_time DESC
    LIMIT 5
""")
sai_sessions = cursor.fetchall()
print(f"   Found {len(sai_sessions)} sessions for 'sai'")
for sess in sai_sessions:
    print(f"   - {sess['login_time']}: device_id={sess['device_id']}, session_id={sess['session_id']}, active={sess['is_active']}")

# 7. Check if the issue is NULL device_id
print("\n7. NULL DEVICE_ID CHECK:")
cursor.execute("SELECT user_id, COUNT(*) as cnt FROM login_logs WHERE success=1 AND device_id IS NULL GROUP BY user_id")
null_device = cursor.fetchall()
if null_device:
    print("   Users with NULL device_id:")
    for u in null_device:
        print(f"   - {u['user_id']}: {u['cnt']} logins")
else:
    print("   No NULL device_id found")

# 8. Check device_logs
print("\n8. DEVICE_LOGS TABLE:")
cursor.execute("SELECT user_id, device_id, mac_address, hostname, os, login_count FROM device_logs")
devices = cursor.fetchall()
if devices:
    for dev in devices:
        print(f"   {dev['user_id']}: {dev['device_id']}, MAC={dev['mac_address']}, Host={dev['hostname']}, Count={dev['login_count']}")
else:
    print("   No devices registered")

# 9. Root cause analysis
print("\n9. ROOT CAUSE ANALYSIS:")
cursor.execute("SELECT COUNT(*) as cnt FROM login_logs WHERE success=1 AND (device_id IS NULL OR device_id = '')")
null_count = cursor.fetchone()['cnt']
if null_count > 0:
    print(f"   ISSUE FOUND: {null_count} login records have NULL/empty device_id")
    print("   CAUSE: Backend not generating device_id on login")
    print("   FIX: Update backend login endpoint to generate device_id from user_agent")
else:
    print("   All login records have device_id")
    cursor.execute("SELECT COUNT(*) as cnt FROM sessions WHERE login_id IS NULL")
    unlinked = cursor.fetchone()['cnt']
    if unlinked > 0:
        print(f"   ISSUE FOUND: {unlinked} sessions not linked to login_logs")
        print("   FIX: Run UPDATE query to link sessions")

cursor.close()
db.close()

print("\n=== DIAGNOSIS COMPLETE ===")
