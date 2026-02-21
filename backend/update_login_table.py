import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="zero_trust_db"
)

cursor = db.cursor()

# Add columns to login_logs table
try:
    cursor.execute("ALTER TABLE login_logs ADD COLUMN mac_address VARCHAR(50) DEFAULT 'Browser-Based'")
    print("✓ Added mac_address column")
except:
    print("mac_address column already exists")

try:
    cursor.execute("ALTER TABLE login_logs ADD COLUMN hostname VARCHAR(100) DEFAULT 'Web-Client'")
    print("✓ Added hostname column")
except:
    print("hostname column already exists")

try:
    cursor.execute("ALTER TABLE login_logs ADD COLUMN device_os TEXT DEFAULT NULL")
    print("✓ Added device_os column")
except:
    print("device_os column already exists")

try:
    cursor.execute("ALTER TABLE login_logs ADD COLUMN user_agent TEXT DEFAULT NULL")
    print("✓ Added user_agent column")
except:
    print("user_agent column already exists")

db.commit()
cursor.close()
db.close()

print("\n✓ Database updated successfully!")
