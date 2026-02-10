from database import get_db
from datetime import datetime

def log_file_access(user, file_name, action="READ"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO file_access_logs
        (user_id, file_name, action, access_time)
        VALUES (%s,%s,%s,%s)
    """, (user, file_name, action, datetime.now()))
    db.commit()