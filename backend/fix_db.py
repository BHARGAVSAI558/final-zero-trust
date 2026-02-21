import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="root", database="zerotrust")
cursor = db.cursor()

# Add risk_score column if missing
try:
    cursor.execute("ALTER TABLE users ADD COLUMN risk_score INT DEFAULT 0")
    print("Added risk_score column")
except:
    print("risk_score column already exists")

db.commit()
cursor.close()
db.close()
print("Database fixed!")
