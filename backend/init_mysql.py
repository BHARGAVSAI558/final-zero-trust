import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="root", database="zerotrust")
cursor = db.cursor()
cursor.execute("INSERT IGNORE INTO users (username, password, role, status) VALUES ('admin', 'admin123', 'admin', 'active')")
db.commit()
cursor.close()
db.close()
print("Admin user created")
