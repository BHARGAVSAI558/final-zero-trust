# 🚀 QUICK START - LOCAL SETUP

## Prerequisites
✅ MySQL installed (root password: root123)
✅ Python 3.7+ installed
✅ Node.js installed

## Setup Steps (5 minutes)

### 1. Setup MySQL Database
Open MySQL Workbench or Command Line and run:
```bash
mysql -u root -p
# Enter password: root123
```

Then copy-paste entire content from: `setup_mysql.sql`

### 2. Start Backend
```bash
cd e:\zero-trust-tool\backend
python main_local.py
```

You should see:
```
🛡️ Zero Trust System - LOCAL MODE
Backend running on: http://localhost:8000
API Docs: http://localhost:8000/docs
```

### 3. Start Frontend
Open NEW terminal:
```bash
cd e:\zero-trust-tool\frontend
npm start
```

Browser will open: http://localhost:3000

### 4. Login & Test
- Username: `admin`
- Password: `admin123`

## ✅ Verify Everything Works

1. **Login** - Should see admin dashboard
2. **Register** - Click "New User? Register Here"
3. **Approve** - See pending user in yellow box
4. **File Access** - Click READ/WRITE/DELETE buttons
5. **Risk Score** - Should update in real-time
6. **Blockchain** - Should show blocks after 3+ logins

## 🎯 For Review Tomorrow

**Show these features:**
1. Admin dashboard with real-time monitoring
2. User registration & approval workflow
3. UEBA risk scoring (0-100)
4. Micro-segmentation (4 zones)
5. File access logging
6. Blockchain audit trail
7. Revoke access functionality

## 📊 Test Data

**Default Users:**
- admin / admin123 (Admin role)
- bhargav / admin123 (User role)

**Register New User:**
- Username: testuser
- Password: test123
- Status: Pending (needs admin approval)

## 🐛 Troubleshooting

**Backend won't start:**
- Check MySQL is running
- Verify database `zero_trust` exists
- Check port 8000 is free

**Frontend won't start:**
- Run: `npm install`
- Check port 3000 is free

**Can't login:**
- Check backend is running
- Open http://localhost:8000/health
- Should see: {"status":"healthy"}

**No data showing:**
- Check browser console (F12)
- Verify API calls going to localhost:8000
- Check MySQL has data: `SELECT * FROM users;`

## 🎤 Presentation Tips

1. **Start with problem** - Traditional security fails
2. **Show solution** - Zero Trust continuous verification
3. **Live demo** - All features working
4. **Compare** - Better than Microsoft ATP for SMBs
5. **Conclude** - Enterprise-ready prototype

## ✅ ALL REQUIREMENTS MET

✅ Input: Login records, file logs, device fingerprints
✅ Output: Risk score (0-100), Access decision (ALLOW/DENY)
✅ UEBA: 13+ behavioral signals
✅ Micro-segmentation: 4 security zones
✅ Dashboard: Real-time suspicious activities
✅ Comparison: vs Microsoft ATP

**YOU'RE READY FOR REVIEW! 🚀**
