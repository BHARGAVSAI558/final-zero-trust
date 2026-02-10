# ⚡ Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env and set JWT_SECRET (IMPORTANT!)
# Example: JWT_SECRET=your-super-secret-key-min-32-characters-long
notepad .env

# Setup database
mysql -u root -p < schema.sql
```

### Step 2: Frontend Setup (2 minutes)

```bash
cd frontend

# Install dependencies
npm install
```

### Step 3: Start Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Step 4: Login

Open browser: http://localhost:3000

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

## ✅ Verification Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can login with admin/admin123
- [ ] Dashboard loads with data
- [ ] No console errors

---

## 🔧 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Install missing dependencies
pip install -r requirements.txt --upgrade
```

### Frontend won't start
```bash
# Clear cache and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install
```

### Database connection error
```bash
# Verify MySQL is running
mysql -u root -p -e "SHOW DATABASES;"

# Check credentials in .env file
notepad backend\.env
```

### Login fails
```bash
# Verify database has users
mysql -u root -p zerotrust -e "SELECT * FROM users;"

# If empty, run schema.sql again
mysql -u root -p < backend\schema.sql
```

---

## 📊 Test the System

### 1. Create Test User
```bash
# In Python console
from security import hash_password
from database import get_db

db = get_db()
cursor = db.cursor()
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
    ("testuser", hash_password("test123"), "user")
)
db.commit()
```

### 2. Generate Test Data
```bash
# Run agent to create device logs
cd agent
python agent.py
# Enter username: testuser
```

### 3. View Dashboard
- Login as admin to see all users
- Login as testuser to see personal view

---

## 🎯 Next Steps

1. **Change default password** (Security!)
2. **Configure .env properly** (Set strong JWT_SECRET)
3. **Read DEPLOYMENT.md** (For production)
4. **Explore API docs** (http://localhost:8000/docs)
5. **Test all features** (UEBA, micro-segmentation, audit)

---

## 📚 Documentation

- [README.md](README.md) - Full project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) - What's new
- API Docs: http://localhost:8000/docs

---

## 🆘 Need Help?

**Common Issues:**

1. **"Module not found"** → Run `pip install -r requirements.txt`
2. **"Port already in use"** → Kill process or change port
3. **"Database connection failed"** → Check MySQL is running
4. **"Invalid token"** → Clear localStorage and login again
5. **"CORS error"** → Check FRONTEND_URL in .env

**Still stuck?** Check the full documentation or open an issue.

---

**🎉 You're all set! Start monitoring insider threats with Zero Trust!**
