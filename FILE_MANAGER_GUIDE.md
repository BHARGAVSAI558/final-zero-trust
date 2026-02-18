# 📁 File Manager Demo - Quick Start

## 🚀 How to Use

### 1. Start the File Manager
```bash
cd e:\zero-trust-tool
FILE_MANAGER.bat
```

### 2. File Operations

#### 📖 OPEN (Read)
1. Select a file from the list (e.g., `secrets.env`)
2. Click **OPEN** button
3. File content appears in the editor
4. ✅ Logged as READ action in database

#### ✏️ EDIT (Write)
1. Select a file
2. Click **OPEN** to load content
3. Click **EDIT** to enable editing
4. Modify the content
5. Click **SAVE** to save changes
6. ✅ Logged as WRITE action in database

#### 🗑️ DELETE
1. Select a file (e.g., `database.sql`)
2. Click **DELETE** button
3. Confirm deletion
4. File moves to recycle bin with timestamp
5. ✅ Logged as DELETE action in database

#### ♻️ RECYCLE BIN
1. Click **RECYCLE BIN** button
2. See all deleted files
3. Select a file
4. Click **RESTORE** to bring it back
5. Or click **DELETE FOREVER** to permanently remove

## 🎬 Demo Script

### Step 1: Show Files (30 seconds)
- Open file manager
- Show 8 files with different sensitivity levels
- Explain color coding: GREEN=public, BLUE=internal, ORANGE=sensitive, RED=critical

### Step 2: Read Critical File (1 minute)
- Select `secrets.env` (CRITICAL - red)
- Click OPEN
- Show environment variables
- **Point out:** "Every file access is logged in real-time"
- Switch to admin dashboard → Show file access log

### Step 3: Edit Sensitive File (1 minute)
- Select `admin.config` (SENSITIVE - orange)
- Click OPEN → Click EDIT
- Change `session_timeout = 300` to `session_timeout = 600`
- Click SAVE
- **Point out:** "WRITE action increases risk score"
- Check admin dashboard → Risk score increased

### Step 4: Delete Critical File (1 minute)
- Select `database.sql` (CRITICAL - red)
- Click DELETE → Confirm
- File disappears from list
- **Point out:** "Deleting critical files triggers alerts"
- Check admin dashboard → MASS_DELETE signal appears

### Step 5: Recycle Bin (1 minute)
- Click RECYCLE BIN button
- Show deleted file with timestamp
- Click RESTORE
- File reappears in main list
- **Point out:** "Prevents accidental data loss"

### Step 6: Permanent Delete (30 seconds)
- Delete file again
- Open recycle bin
- Click DELETE FOREVER → Confirm
- File permanently removed
- **Point out:** "Complete audit trail maintained"

## 🎯 Key Features to Highlight

1. **Real-time Logging** - Every action logged instantly
2. **Sensitivity Levels** - 4-tier classification (public/internal/sensitive/critical)
3. **Recycle Bin** - Prevents accidental deletion
4. **Risk Scoring** - Automatic threat detection
5. **Audit Trail** - Complete history in admin dashboard
6. **Zero Trust** - Verify every file access

## 📊 What Gets Logged

Each operation creates entries in:
- `file_access_logs` table
- Admin dashboard file logs
- Session history (linked to login)
- Risk calculation (if sensitive/critical)

## 🔥 Demo Impact

**Before operations:**
- Risk Score: 56 (HIGH)
- Signals: WEEKEND(14)

**After operations (READ + WRITE + DELETE critical files):**
- Risk Score: 81 (CRITICAL)
- Signals: WEEKEND(14), MASS_DELETE(3)
- Decision: DENY
- Zone: PUBLIC (restricted access)

## ✅ Status

✅ File manager GUI ready
✅ 8 demo files created
✅ CRUD operations working
✅ Recycle bin functional
✅ Backend logging integrated
✅ Risk scoring active

**Launch with:** `FILE_MANAGER.bat`
