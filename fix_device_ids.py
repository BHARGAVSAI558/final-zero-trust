import mysql.connector
import hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("FIXING ALL NULL DEVICE_IDS...\n")

# Get all login records with NULL device_id
cursor.execute("SELECT id, user_id, user_agent FROM login_logs WHERE device_id IS NULL AND user_agent IS NOT NULL")
null_records = cursor.fetchall()

print(f"Found {len(null_records)} records with NULL device_id")

# Update each record
for record in null_records:
    user_agent = record['user_agent'] or 'Unknown'
    device_id = hashlib.md5(f"{record['user_id']}{user_agent}".encode()).hexdigest()[:16]
    
    cursor.execute("UPDATE login_logs SET device_id=%s WHERE id=%s", (device_id, record['id']))

db.commit()
print(f"Updated {len(null_records)} records with generated device_id")

# Verify fix
cursor.execute("SELECT COUNT(*) as cnt FROM login_logs WHERE device_id IS NULL")
remaining = cursor.fetchone()['cnt']
print(f"Remaining NULL device_ids: {remaining}")

# Test query for sai
print("\nTesting session history for 'sai':")
cursor.execute("""
    SELECT 
        l.login_time,
        l.device_id,
        l.mac_address,
        s.is_active
    FROM login_logs l
    LEFT JOIN sessions s ON l.id = s.login_id
    WHERE l.user_id = 'sai' AND l.success = 1
    ORDER BY l.login_time DESC
""")
sai_data = cursor.fetchall()
print(f"Found {len(sai_data)} sessions for sai")
for s in sai_data:
    print(f"  {s['login_time']}: device_id={s['device_id']}, active={s['is_active']}")

cursor.close()
db.close()

print("\nFIX COMPLETE!")
print("Restart backend: cd backend && python main_advanced.py")
