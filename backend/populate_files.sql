USE zerotrust;

INSERT INTO files (file_name, file_path, file_content, file_size, file_type, sensitivity_level, owner_id, is_deleted) VALUES
('Budget_2024_New.xlsx', '/files/Budget_2024_New.xlsx', 'Budget data for 2024', 1024, 'xlsx', 'confidential', 'admin', 0),
('Company_Secrets.txt', '/files/Company_Secrets.txt', 'Confidential company information', 512, 'txt', 'critical', 'admin', 0),
('Meeting_Notes.txt', '/files/Meeting_Notes.txt', 'Meeting notes from Q1 2024', 256, 'txt', 'internal', 'bhargav', 0),
('Public_Announcement.txt', '/files/Public_Announcement.txt', 'Public announcement draft', 128, 'txt', 'public', 'sanjay', 0),
('Project_Plan.docx', '/files/Project_Plan.docx', 'Project planning document', 2048, 'docx', 'internal', 'jeshwanth', 0),
('Financial_Report_Q1.pdf', '/files/Financial_Report_Q1.pdf', 'Q1 Financial Report', 4096, 'pdf', 'confidential', 'admin', 0);
