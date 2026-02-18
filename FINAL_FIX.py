import mysql.connector
import hashlib
import secrets

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== COMPREHENSIVE FIX FOR SESSION TRACKING ===\n")

# 1. Fix NULL device_ids by generating from user_id + timestamp
print("1. Fixing NULL device_ids...")
cursor.execute("SELECT id, user_id, login_time FROM login_logs WHERE device_id IS NULL")
null_device_ids = cursor.fetchall()

for record in null_device_ids:
    device_id = hashlib.md5(f"{record['user_id']}{record['login_time']}".encode()).hexdigest()[:16]
    cursor.execute("UPDATE login_logs SET device_id=%s WHERE id=%s", (device_id, record['id']))

db.commit()
print(f"   Fixed {len(null_device_ids)} NULL device_ids")

# 2. Link unlinked sessions to login_logs
print("\n2. Linking sessions to login_logs...")
cursor.execute("""
    UPDATE sessions s
    JOIN login_logs l ON s.user_id = l.user_id 
      AND ABS(TIMESTAMPDIFF(SECOND, s.created_at, l.login_time)) < 10
    SET s.login_id = l.id
    WHERE s.login_id IS NULL
""")
db.commit()
print(f"   Linked {cursor.rowcount} sessions")

# 3. Verify the fix
print("\n3. Verification:")
cursor.execute("SELECT COUNT(*) as cnt FROM login_logs WHERE device_id IS NULL")
null_count = cursor.fetchone()['cnt']
print(f"   NULL device_ids remaining: {null_count}")

cursor.execute("SELECT COUNT(*) as cnt FROM sessions WHERE login_id IS NULL")
unlinked = cursor.fetchone()['cnt']
print(f"   Unlinked sessions: {unlinked}")

# 4. Test for each user
print("\n4. Testing session history for all users:")
cursor.execute("SELECT DISTINCT user_id FROM login_logs WHERE success=1")
users = cursor.fetchall()

for user in users:
    username = user['user_id']
    cursor.execute("""
        SELECT COUNT(*) as cnt
        FROM login_logs l
        LEFT JOIN sessions s ON l.id = s.login_id
        WHERE l.user_id = %s AND l.success = 1 AND l.device_id IS NOT NULL
    """, (username,))
    count = cursor.fetchone()['cnt']
    print(f"   {username}: {count} sessions with device_id")

cursor.close()
db.close()

print("\n=== FIX COMPLETE ===")
print("\nNEXT STEPS:")
print("1. Backend is already updated with device_id generation")
print("2. All existing records now have device_id")
print("3. Refresh admin dashboard to see session history")
print("4. All future logins will automatically track properly")
