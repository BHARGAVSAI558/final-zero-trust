# 🚀 QUICK START GUIDE

## Option 1: Double-Click to Start (EASIEST)

### Start System:
```
Double-click: START.bat
```
This will:
- Start backend on http://localhost:8000
- Start frontend on http://localhost:3000
- Open browser automatically

### Start Agent:
```
Double-click: START_AGENT.bat bhargav
```
Or edit the file to change username.

## Option 2: Manual Start

### Terminal 1 - Backend:
```bash
cd backend
python main_advanced.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```

### Terminal 3 - Agent (Optional):
```bash
cd agent
python zero_trust_agent.py
# Enter username when prompted
```

## Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Login Credentials

### Admin:
- Username: `admin`
- Password: `admin123`

### Users:
- bhargav / bhargav123
- mahesh / mahesh123
- sai / sai123
- karthik / karthik123

## Troubleshooting

### Frontend not opening?
1. Check if port 3000 is free
2. Run: `cd frontend && npm start`
3. Browser should open automatically
4. If not, manually go to http://localhost:3000

### Backend not connecting?
1. Check if port 8000 is free
2. Verify MySQL is running
3. Check database credentials in main_advanced.py

### Agent not updating?
1. Verify backend is running on port 8000
2. Check agent URL is http://localhost:8000
3. Run agent with correct username

## File Structure

```
zero-trust-tool/
├── START.bat              ← Double-click to start system
├── START_AGENT.bat        ← Double-click to start agent
├── backend/
│   └── main_advanced.py   ← Backend server
├── frontend/
│   └── src/               ← React app
└── agent/
    └── zero_trust_agent.py ← Monitoring agent
```

## Quick Commands

```bash
# Start everything
START.bat

# Start agent for user "bhargav"
START_AGENT.bat bhargav

# Or manually
cd agent
python zero_trust_agent.py
# Type: bhargav
```

## What to Expect

1. **Backend starts**: Shows "Zero Trust System - JWT + 5min Sessions"
2. **Frontend starts**: Browser opens to http://localhost:3000
3. **Login page**: Black screen with green matrix grid
4. **Agent starts**: Shows device info and sends telemetry every 60s

## Demo Flow

1. Start system: `START.bat`
2. Login as admin: admin/admin123
3. See all users in dashboard
4. Start agent: `START_AGENT.bat bhargav`
5. Login as bhargav in another browser
6. Admin clicks "MORE DETAILS" on bhargav
7. See complete session history with device fingerprints!
