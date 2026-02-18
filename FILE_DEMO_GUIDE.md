# 📁 File Management Demo - CRUD Operations

## ✅ Created Demo Files

Located in `demo_files/` directory:

1. **dashboard.html** (public) - HTML dashboard
2. **reports.pdf** (internal) - Security report
3. **analytics.xlsx** (internal) - User analytics CSV
4. **profile.json** (public) - User profile JSON
5. **admin.config** (sensitive) - Configuration file
6. **credentials.txt** (sensitive) - API credentials
7. **database.sql** (critical) - Database schema
8. **secrets.env** (critical) - Environment secrets

## 🎯 Features

### CRUD Operations
- ✅ **CREATE** - Upload new files
- ✅ **READ** - View file contents
- ✅ **UPDATE** - Edit file contents
- ✅ **DELETE** - Move to recycle bin

### Recycle Bin
- ✅ View deleted files
- ✅ Restore files
- ✅ Permanent delete

## 🚀 API Endpoints

### List Files
```
GET /api/files/list
Response: {files: [{name, sensitivity, size, modified}]}
```

### Read File
```
GET /api/files/read/{filename}?user=mahesh
Response: {filename, content, size}
```

### Edit File
```
POST /api/files/edit
Body: {filename, content, user}
Response: {status, message}
```

### Delete File (Move to Recycle Bin)
```
POST /api/files/delete
Body: {filename, user}
Response: {status, message}
```

### List Recycle Bin
```
GET /api/files/recycle-bin
Response: {files: [{name, original_name, size, deleted}]}
```

### Restore File
```
POST /api/files/restore
Body: {filename, user}
Response: {status, message}
```

### Permanent Delete
```
DELETE /api/files/permanent-delete
Body: {filename, user}
Response: {status, message}
```

## 🎬 Demo Flow

### 1. Show Files List
User dashboard displays 8 files with sensitivity levels

### 2. Open File (READ)
Click "OPEN" → Shows file content
- Logs to `file_access_logs` table
- Appears in admin dashboard

### 3. Edit File (WRITE)
Click "EDIT" → Modify content → Save
- Updates file on disk
- Logs WRITE action
- Increases risk score if sensitive file

### 4. Delete File (DELETE)
Click "DELETE" → Moves to recycle bin
- File moved with timestamp prefix
- Logs DELETE action
- Triggers alert if critical file

### 5. Recycle Bin
View deleted files → Restore or permanent delete

## 📊 Security Monitoring

All file operations are tracked:
- **User** who performed action
- **File name** and sensitivity level
- **Action** (READ/WRITE/DELETE)
- **Timestamp** with millisecond precision
- **IP address** of request

### Risk Scoring
- DELETE critical file (secrets.env, database.sql) → +25 risk
- WRITE sensitive file → +15 risk
- READ 100+ files in 1 hour → +18 risk

## 🎯 Hackathon Demo Script

1. **Login as mahesh**
2. **Show file list** - 8 files with different sensitivity levels
3. **Open secrets.env** - Shows environment variables
4. **Edit admin.config** - Change session_timeout value
5. **Delete database.sql** - Moves to recycle bin
6. **Check admin dashboard** - See file access logs
7. **Risk score increases** - From 56 to 81 (MASS_DELETE triggered)
8. **Open recycle bin** - Show deleted file
9. **Restore database.sql** - File comes back
10. **Permanent delete** - Remove from recycle bin forever

## 🔥 Key Talking Points

- **Real-time Monitoring** - Every file action logged instantly
- **Sensitivity Levels** - 4 tiers (public, internal, sensitive, critical)
- **Recycle Bin** - Prevent accidental data loss
- **Audit Trail** - Complete history of who did what when
- **Risk Scoring** - Automatic threat detection
- **Zero Trust** - Verify every file access

## 📝 Status

✅ Demo files created
✅ API endpoints ready
✅ Recycle bin functional
✅ Logging integrated
✅ Risk scoring active

**Ready for demo!** 🚀
