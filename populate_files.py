import sys
sys.path.insert(0, 'backend')
from mysql_database import get_db

db = get_db()
cursor = db.cursor()

files = [
    ('Budget_2024_New.xlsx', '/files/Budget_2024_New.xlsx', 'Budget data for 2024', 1024, 'xlsx', 'confidential', 'admin'),
    ('Company_Secrets.txt', '/files/Company_Secrets.txt', 'Confidential company information', 512, 'txt', 'critical', 'admin'),
    ('Meeting_Notes.txt', '/files/Meeting_Notes.txt', 'Meeting notes from Q1 2024', 256, 'txt', 'internal', 'bhargav'),
    ('Public_Announcement.txt', '/files/Public_Announcement.txt', 'Public announcement draft', 128, 'txt', 'public', 'sanjay'),
    ('Project_Plan.docx', '/files/Project_Plan.docx', 'Project planning document', 2048, 'docx', 'internal', 'jeshwanth'),
    ('Financial_Report_Q1.pdf', '/files/Financial_Report_Q1.pdf', 'Q1 Financial Report', 4096, 'pdf', 'confidential', 'admin')
]

for f in files:
    cursor.execute("""
        INSERT INTO files (file_name, file_path, file_content, file_size, file_type, sensitivity_level, owner_id, is_deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
    """, f)

db.commit()
cursor.close()
db.close()
print("Files populated successfully!")
