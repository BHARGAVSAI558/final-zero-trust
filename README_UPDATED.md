# ⚡ ZERO TRUST - Real-Time SOC Platform

## 🚀 WHAT'S NEW

### ✅ Real-Time Features
- **WebSocket Integration**: Live updates every 2 seconds
- **Real-Time Dashboard**: Auto-refresh with live activity feed
- **Advanced UEBA**: 10+ behavioral signals for threat detection
- **Unified SOC Agent**: All-in-one monitoring tool

### ✅ Enhanced UI/UX
- **Cyber Theme**: Professional dark mode with neon colors (#00ff00, #00ffff)
- **Professional Logo**: Custom animated logo component
- **Role-Based Dashboards**: Admin, HR, Security Analyst, Employee views
- **Live Activity Feed**: Real-time monitoring of all system events

### ✅ Advanced Agent Features
- **Device Fingerprinting**: MAC, IP, hostname, OS, hardware ID
- **Real-Time Telemetry**: CPU, memory, network, processes
- **Session Tracking**: Duration, idle detection, activity correlation
- **File Monitoring**: Detailed file access with operations tracking
- **Network Monitoring**: Live connection tracking

## 📦 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
pip install websockets
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Run SOC Agent
```bash
cd agent
START_SOC_AGENT.bat
# Enter your username when prompted
```

## 🎯 Features

### Backend (FastAPI)
- ✅ WebSocket support for real-time updates
- ✅ Advanced UEBA with 10+ signals
- ✅ Role-based access control (Admin, HR, User)
- ✅ Blockchain audit trail
- ✅ Real-time statistics endpoint

### Frontend (React)
- ✅ Real-time dashboard with 2s refresh
- ✅ Professional cyber-themed UI
- ✅ Role-based views (Admin, HR, Employee)
- ✅ Live activity monitoring
- ✅ Advanced data visualizations
- ✅ Session history with file activities

### SOC Agent (Python)
- ✅ Unified monitoring interface
- ✅ Advanced device fingerprinting
- ✅ Real-time system metrics
- ✅ File access monitoring
- ✅ Network connection tracking
- ✅ Automatic telemetry transmission

## 🎨 UI Theme

**Colors:**
- Primary: `#00ff00` (Matrix Green)
- Secondary: `#00ffff` (Cyan)
- Danger: `#ff0000` (Red Alert)
- Warning: `#ffaa00` (Orange)
- Background: `#000000` (Black)

**Typography:**
- Font: `Courier New`, `Consolas`, `Monaco`
- Style: Monospace, uppercase headers with brackets

## 📊 Dashboards

### Admin Dashboard
- Real-time user monitoring
- Risk score analysis
- File access logs
- Blockchain audit trail
- Session history with activities
- User approval/revocation

### HR Dashboard
- Employee directory
- Attendance tracking
- Status monitoring
- Location tracking

### User Dashboard
- Personal risk score
- Accessible resources
- Activity history
- Device information

## 🔧 Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://localhost/zero
JWT_SECRET=your-secret-key
```

### Frontend (api.js)
```javascript
const API_URL = "http://localhost:8000";
```

### Agent (unified_soc_agent.py)
```python
BACKEND = "http://localhost:8000"
```

## 🚀 Deployment

### Production Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Production Frontend
```bash
cd frontend
npm run build
# Deploy build/ folder to Netlify/Vercel
```

## 📈 Performance

- **API Response**: <100ms average
- **Dashboard Load**: <2s
- **Real-Time Updates**: Every 2 seconds
- **WebSocket Latency**: <50ms
- **Agent Telemetry**: Every 30 seconds

## 🔒 Security

- JWT authentication
- Rate limiting
- Geolocation tracking
- Blockchain audit trail
- Device fingerprinting
- Behavioral analytics

## 🎯 Use Cases

1. **Insider Threat Detection**: Monitor employee behavior
2. **Compliance**: Track file access and activities
3. **Incident Response**: Real-time alerting
4. **HR Management**: Employee monitoring
5. **Security Operations**: Centralized SOC

## 📞 Support

For issues:
- Check logs in backend console
- Verify database connection
- Ensure all services are running
- Check network connectivity

## 🏆 Credits

Built with:
- FastAPI (Backend)
- React 19 (Frontend)
- PostgreSQL (Database)
- Tkinter (SOC Agent)
- Chart.js (Visualizations)

---

**⚡ ZERO TRUST - Industry-Grade Security Platform**
