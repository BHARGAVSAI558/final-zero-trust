import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zerotrust"
)

cursor = db.cursor()

# Add device_id to login_logs
try:
    cursor.execute("ALTER TABLE login_logs ADD COLUMN device_id VARCHAR(50)")
    print("✓ Added device_id to login_logs")
except:
    print("- device_id already exists in login_logs")

# Add login_id to sessions
try:
    cursor.execute("ALTER TABLE sessions ADD COLUMN login_id INT")
    print("✓ Added login_id to sessions")
except:
    print("- login_id already exists in sessions")

# Add login_count to device_logs
try:
    cursor.execute("ALTER TABLE device_logs ADD COLUMN login_count INT DEFAULT 0")
    print("✓ Added login_count to device_logs")
except:
    print("- login_count already exists in device_logs")

# Check if id column exists in login_logs
cursor.execute("SHOW COLUMNS FROM login_logs LIKE 'id'")
if not cursor.fetchone():
    cursor.execute("ALTER TABLE login_logs ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST")
    print("✓ Added id to login_logs")
else:
    print("- id already exists in login_logs")

# Create indexes
try:
    cursor.execute("CREATE INDEX idx_login_device ON login_logs(user_id, device_id)")
    print("✓ Created index idx_login_device")
except:
    print("- Index idx_login_device already exists")

try:
    cursor.execute("CREATE INDEX idx_session_login ON sessions(login_id)")
    print("✓ Created index idx_session_login")
except:
    print("- Index idx_session_login already exists")

try:
    cursor.execute("CREATE INDEX idx_device_user ON device_logs(user_id, device_id)")
    print("✓ Created index idx_device_user")
except:
    print("- Index idx_device_user already exists")

db.commit()
cursor.close()
db.close()

print("\n✅ Database schema updated successfully!")
