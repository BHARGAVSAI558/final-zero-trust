# Zero Trust Platform - Cloud Deployment Guide

## 🚀 Deployment Stack
- **Frontend**: Netlify (React)
- **Backend**: Render (FastAPI)
- **Database**: Supabase (PostgreSQL) or Railway (MySQL)

---

## 📋 Pre-Deployment Checklist

### 1. Create Accounts
- [ ] GitHub account (https://github.com)
- [ ] Netlify account (https://netlify.com)
- [ ] Render account (https://render.com)
- [ ] Supabase account (https://supabase.com) OR Railway (https://railway.app)

---

## 🗄️ STEP 1: Setup Database (Supabase/Railway)

### Option A: Supabase (PostgreSQL - Recommended)

1. **Create Project**:
   - Go to https://supabase.com
   - Click "New Project"
   - Name: `zero-trust-db`
   - Database Password: (save this!)
   - Region: Singapore (closest to you)

2. **Get Connection Details**:
   - Go to Project Settings → Database
   - Copy these values:
     ```
     Host: db.xxx.supabase.co
     Database: postgres
     Port: 5432
     User: postgres
     Password: [your password]
     ```

3. **Run Schema**:
   - Go to SQL Editor
   - Copy contents from `backend/schema.sql`
   - Replace MySQL syntax with PostgreSQL:
     - Change `AUTO_INCREMENT` to `SERIAL`
     - Change `DATETIME` to `TIMESTAMP`
     - Change `NOW()` to `CURRENT_TIMESTAMP`
   - Run the query

### Option B: Railway (MySQL - Easier)

1. **Create Project**:
   - Go to https://railway.app
   - Click "New Project"
   - Select "Provision MySQL"

2. **Get Connection Details**:
   - Click on MySQL service
   - Go to "Connect" tab
   - Copy:
     ```
     MYSQL_HOST
     MYSQL_PORT
     MYSQL_USER
     MYSQL_PASSWORD
     MYSQL_DATABASE
     ```

3. **Run Schema**:
   - Use MySQL client or Railway's built-in query tool
   - Copy and run `backend/schema.sql`

---

## 🔧 STEP 2: Push to GitHub

### From your project directory:

```bash
# Navigate to project
cd e:\zero-trust-tool

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment setup"

# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/BHARGAVSAI558/final-zero-trust.git

# Push
git push -u origin main
```

**Note**: If you get authentication error, use GitHub Personal Access Token:
- Go to GitHub → Settings → Developer Settings → Personal Access Tokens
- Generate new token (classic)
- Use token as password when pushing

---

## 🖥️ STEP 3: Deploy Backend (Render)

### 3.1 Update Backend for Production

**Edit `backend/mysql_database.py`** to use environment variables:

```python
import os
from mysql.connector import pooling

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "zero_trust"),
    "port": int(os.getenv("DB_PORT", "3306"))
}
```

**Edit `backend/main.py`** - Update CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.netlify.app",  # Add your Netlify URL
        "*"  # For testing only, remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3.2 Deploy on Render

1. **Go to Render Dashboard**:
   - https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect GitHub**:
   - Select your repository: `final-zero-trust`
   - Click "Connect"

3. **Configure Service**:
   ```
   Name: zero-trust-backend
   Region: Singapore
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   ```
   DB_HOST = [your database host]
   DB_USER = [your database user]
   DB_PASSWORD = [your database password]
   DB_NAME = [your database name]
   DB_PORT = 3306 (or 5432 for PostgreSQL)
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy your backend URL: `https://zero-trust-backend.onrender.com`

---

## 🌐 STEP 4: Deploy Frontend (Netlify)

### 4.1 Update Frontend API URL

**Edit `frontend/.env.production`**:
```
REACT_APP_API_URL=https://zero-trust-backend.onrender.com
```

**Update all API calls in frontend** to use environment variable:

**Edit `frontend/src/Login.jsx`** (and all other files with axios):
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Use API_URL in all axios calls
axios.post(`${API_URL}/auth/login`, formData)
```

### 4.2 Commit Changes

```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

### 4.3 Deploy on Netlify

1. **Go to Netlify**:
   - https://app.netlify.com
   - Click "Add new site" → "Import an existing project"

2. **Connect GitHub**:
   - Select "GitHub"
   - Authorize Netlify
   - Choose repository: `final-zero-trust`

3. **Configure Build**:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/build
   ```

4. **Add Environment Variable**:
   - Go to Site Settings → Environment Variables
   - Add:
     ```
     REACT_APP_API_URL = https://zero-trust-backend.onrender.com
     ```

5. **Deploy**:
   - Click "Deploy site"
   - Wait 3-5 minutes
   - Your site will be live at: `https://random-name.netlify.app`

6. **Custom Domain (Optional)**:
   - Go to Domain Settings
   - Change site name to: `zero-trust-platform`
   - URL becomes: `https://zero-trust-platform.netlify.app`

---

## 🔄 STEP 5: Update CORS in Backend

After getting Netlify URL, update backend CORS:

**Edit `backend/main.py`**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://zero-trust-platform.netlify.app",  # Your actual Netlify URL
        "http://localhost:3000"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Commit and push**:
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push origin main
```

Render will auto-deploy the update.

---

## 🧪 STEP 6: Test Deployment

1. **Visit your Netlify URL**: `https://zero-trust-platform.netlify.app`
2. **Register a new user**
3. **Login** (admin will need to approve)
4. **Check if data is saved** in Supabase/Railway database

---

## ⚠️ Important Notes

### Agent Deployment
The desktop agent **cannot run in cloud** - it needs to run on user's computer.

**For production**:
1. Package agent as executable: `pyinstaller auto_agent.py`
2. Distribute to users
3. Agent connects to cloud backend: `https://zero-trust-backend.onrender.com`

**Update `agent/auto_agent.py`**:
```python
BACKEND_URL = "https://zero-trust-backend.onrender.com"  # Change from localhost
```

### Free Tier Limitations

**Render Free**:
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ First request takes 30-60 seconds to wake up
- ✅ 750 hours/month free

**Netlify Free**:
- ✅ 100GB bandwidth/month
- ✅ Always active
- ✅ Unlimited sites

**Supabase Free**:
- ✅ 500MB database
- ✅ 2GB bandwidth/month
- ⚠️ Pauses after 7 days inactivity

---

## 🐛 Troubleshooting

### Backend not responding
- Check Render logs: Dashboard → Logs
- Verify environment variables are set
- Check database connection

### Frontend can't connect to backend
- Check CORS settings in `main.py`
- Verify `REACT_APP_API_URL` in Netlify
- Check browser console for errors

### Database connection failed
- Verify credentials in Render environment variables
- Check if database is active (Supabase/Railway dashboard)
- Test connection from Render shell

---

## 📱 Access Your Deployed App

**Frontend**: https://zero-trust-platform.netlify.app
**Backend API**: https://zero-trust-backend.onrender.com
**API Docs**: https://zero-trust-backend.onrender.com/docs

---

## 🔐 Security Recommendations

Before going live:
1. ✅ Add password hashing (bcrypt)
2. ✅ Use JWT tokens instead of sessions
3. ✅ Enable HTTPS only
4. ✅ Add rate limiting
5. ✅ Remove `allow_origins=["*"]` from CORS
6. ✅ Add input validation
7. ✅ Enable database backups

---

## 📞 Support

If you face issues:
1. Check Render logs
2. Check Netlify deploy logs
3. Check browser console (F12)
4. Verify all environment variables

Good luck with deployment! 🚀
