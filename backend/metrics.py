def login_metrics(cursor):
    cursor.execute("""
        SELECT user_id,
               COUNT(*) AS total_logins,
               MAX(login_time) AS last_login
        FROM login_logs
        GROUP BY user_id
    """)
    return cursor.fetchall()
