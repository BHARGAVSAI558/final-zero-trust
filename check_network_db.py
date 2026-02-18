import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor(dictionary=True)

print("=== NETWORK CONNECTIONS IN DATABASE ===\n")

cursor.execute("SELECT COUNT(*) as count FROM network_connections")
total = cursor.fetchone()['count']
print(f"Total network connections: {total}\n")

if total > 0:
    cursor.execute("""
        SELECT user_id, remote_ip, remote_port, protocol, is_external, connection_time 
        FROM network_connections 
        ORDER BY connection_time DESC 
        LIMIT 10
    """)
    connections = cursor.fetchall()
    
    print("Recent network connections:")
    for conn in connections:
        print(f"  User: {conn['user_id']}, IP: {conn['remote_ip']}:{conn['remote_port']}, "
              f"Protocol: {conn['protocol']}, External: {conn['is_external']}, "
              f"Time: {conn['connection_time']}")
else:
    print("No network connections found in database!")
    print("\nPossible reasons:")
    print("1. Agent not running")
    print("2. Agent not sending network data")
    print("3. Backend not saving network data")

cursor.close()
db.close()
