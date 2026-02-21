import sys
sys.path.insert(0, 'e:/zero-trust-tool/backend')

from mysql_database import get_db
from advanced_ueba import calculate_advanced_risk

try:
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT username, status FROM users WHERE status='active'")
    users = cursor.fetchall()
    
    for user in users:
        username = user["username"]
        print(f"Processing {username}...")
        
        cursor.execute("SELECT COUNT(*) as total FROM login_logs WHERE user_id=%s", (username,))
        total = cursor.fetchone()["total"]
        print(f"  Login count: {total}")
        
        cursor.execute("SELECT * FROM login_logs WHERE user_id=%s ORDER BY login_time DESC LIMIT 1", (username,))
        last_login = cursor.fetchone()
        print(f"  Last login: {last_login}")
        
        cursor.execute("SELECT * FROM device_logs WHERE user_id=%s ORDER BY last_seen DESC LIMIT 1", (username,))
        device = cursor.fetchone()
        print(f"  Device: {device}")
        
        risk_data = calculate_advanced_risk(username, db)
        print(f"  Risk: {risk_data}")
        print()
        
    cursor.close()
    db.close()
    print("SUCCESS!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
