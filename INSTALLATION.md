# 🚀 ZERO TRUST - Installation Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

## Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd zero-trust-tool
```

## Step 2: Database Setup

```bash
# Install PostgreSQL
# Create database
createdb zero

# Or use psql
psql -U postgres
CREATE DATABASE zero;
\q
```

## Step 3: Backend Setup

```bash
cd backend

# Install dependencies
pip install fastapi uvicorn psycopg2-binary requests python-multipart websockets

# Create .env file
echo "DATABASE_URL=postgresql://postgres:password@localhost/zero" > .env

# Initialize database
python init_db.py

# Run backend
python main.py
```

Backend will run on: http://localhost:8000

## Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: http://localhost:3000

## Step 5: Run SOC Agent

```bash
cd agent

# Install dependencies
pip install psutil requests

# Run agent (Windows)
START_SOC_AGENT.bat

# Run agent (Linux/Mac)
python unified_soc_agent.py
```

## Step 6: Create Admin User

```bash
# Connect to database
psql -U postgres -d zero

# Create admin user
INSERT INTO users (username, password, role, status) 
VALUES ('admin', 'admin123', 'admin', 'active');

# Create HR user
INSERT INTO users (username, password, role, status) 
VALUES ('hr', 'hr123', 'hr', 'active');

\q
```

## Step 7: Test the System

1. Open browser: http://localhost:3000
2. Login with:
   - Admin: `admin` / `admin123`
   - HR: `hr` / `hr123`
3. Run SOC Agent with your username
4. Monitor real-time updates

## Troubleshooting

### Backend Issues

**Database Connection Error:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify connection
psql -U postgres -d zero
```

**Import Error:**
```bash
pip install --upgrade fastapi uvicorn psycopg2-binary websockets
```

### Frontend Issues

**Module Not Found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port Already in Use:**
```bash
# Kill process on port 3000
npx kill-port 3000
npm start
```

### Agent Issues

**Tkinter Not Found:**
```bash
# Windows
pip install tk

# Linux
sudo apt-get install python3-tk

# Mac
brew install python-tk
```

**Connection Refused:**
- Ensure backend is running on port 8000
- Check firewall settings
- Verify BACKEND URL in agent code

## Production Deployment

### Backend (Render/Heroku)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Netlify/Vercel)

```bash
cd frontend
npm run build
# Deploy build/ folder
```

### Database (Supabase/AWS RDS)

Update DATABASE_URL in backend/.env:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://localhost/zero
JWT_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**HR:**
- Username: `hr`
- Password: `hr123`

⚠️ **IMPORTANT:** Change default passwords in production!

## Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database connected
- [ ] Admin login works
- [ ] SOC Agent connects
- [ ] Real-time updates working
- [ ] WebSocket connected
- [ ] File operations working

## Support

For issues:
1. Check logs in terminal
2. Verify all services running
3. Check database connection
4. Review error messages

## Next Steps

1. Customize roles and permissions
2. Add more UEBA signals
3. Configure email alerts
4. Set up SSL certificates
5. Deploy to production

---

**⚡ ZERO TRUST - Secure Your Organization**
