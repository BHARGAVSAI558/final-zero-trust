# 🔐 Zero Trust Security Platform

A comprehensive real-time security monitoring platform implementing Zero Trust principles with User and Entity Behavior Analytics (UEBA).

![Platform](https://img.shields.io/badge/Platform-Web%20%2B%20Desktop-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![React](https://img.shields.io/badge/React-19.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 Features

### 🔍 Real-Time Monitoring
- **Device Fingerprinting**: MAC address, hostname, WiFi SSID, OS details
- **Network Activity Tracking**: Monitor all network connections with domain resolution
- **File Access Monitoring**: Track read, edit, download, and delete operations
- **Geolocation Tracking**: GPS + IP-based location verification

### 🎯 Advanced Security
- **UEBA Risk Scoring**: Behavioral analytics with risk-based access control
- **Blockchain Audit Trail**: Immutable security event logging
- **Multi-Role Dashboards**: User, Admin, and SOC analyst interfaces
- **Anomaly Detection**: Odd-hour logins, multiple IPs, suspicious file access

### 📊 Analytics & Reporting
- **Threat Matrix**: Real-time user risk assessment
- **Login History**: Complete device and location tracking
- **Network Logs**: Domain-resolved connection monitoring
- **File Activity Stream**: Comprehensive file operation logs

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ ← User Interface (Netlify)
│  Port 3000      │
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│  FastAPI Backend│ ← Business Logic (Render)
│  Port 8000      │
└────────┬────────┘
         │ MySQL
┌────────▼────────┐
│  MySQL Database │ ← Data Storage (Supabase/Railway)
│  Port 3306      │
└─────────────────┘
         ▲
         │ HTTP POST
┌────────┴────────┐
│  Python Agent   │ ← Device Monitor (User's Computer)
│  Port 8888      │
└─────────────────┘
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+

### 1. Clone Repository
```bash
git clone https://github.com/BHARGAVSAI558/final-zero-trust.git
cd final-zero-trust
```

### 2. Setup Database
```bash
mysql -u root -p
source backend/schema.sql
```

### 3. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

**Agent:**
```bash
cd agent
pip install -r requirements.txt
```

### 4. Run Application
```bash
# Windows
START_ALL.bat

# Or run individually:
# Terminal 1: START_BACKEND.bat
# Terminal 2: START_FRONTEND.bat
# Terminal 3: cd agent && python auto_agent.py
```

### 5. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Default Credentials**:
- Username: `admin`
- Password: `admin123`

---

## ☁️ Cloud Deployment

### Deployment Stack
- **Frontend**: Netlify
- **Backend**: Render
- **Database**: Supabase (PostgreSQL) or Railway (MySQL)

### Quick Deploy

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/BHARGAVSAI558/final-zero-trust.git
git push -u origin main
```

2. **Deploy Backend (Render)**:
   - Connect GitHub repository
   - Set environment variables (DB credentials)
   - Deploy

3. **Deploy Frontend (Netlify)**:
   - Connect GitHub repository
   - Set `REACT_APP_API_URL` to Render backend URL
   - Deploy

📖 **Detailed Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📁 Project Structure

```
zero-trust-tool/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/        # Dashboard components
│   │   ├── Login.jsx     # Authentication
│   │   └── App.js        # Main app
│   └── package.json
│
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── advanced_ueba.py # Risk scoring
│   ├── mysql_database.py# Database connection
│   └── schema.sql       # Database schema
│
├── agent/               # Desktop monitoring agent
│   ├── auto_agent.py   # Main agent script
│   └── requirements.txt
│
└── DEPLOYMENT_GUIDE.md # Deployment instructions
```

---

## 🔐 Security Features

### Risk Scoring Algorithm

| Activity | Risk Points | Example |
|----------|-------------|---------|
| Critical file EDIT | +20 | Editing payroll.xlsx |
| Critical file DOWNLOAD | +12 | Downloading passwords.txt |
| File DELETE | +15 | Deleting any file |
| Odd-hour login | +10 | Login at 3 AM |
| Failed login | +5 each | Wrong password attempts |
| Multiple IPs | +8 | Login from different locations |

**Risk Levels**:
- 🟢 **LOW (0-20)**: Normal access
- 🟡 **MEDIUM (21-50)**: Monitor closely
- 🟠 **HIGH (51-80)**: Investigate immediately
- 🔴 **CRITICAL (81+)**: Block access

### Access Zones
- **PUBLIC**: Basic resources
- **INTERNAL**: Standard company data
- **CONFIDENTIAL**: Restricted access
- **RESTRICTED**: Denied

---

## 🛠️ Technologies Used

### Frontend
- React 19.2
- React Router
- Axios
- Chart.js
- React Icons

### Backend
- FastAPI
- MySQL Connector
- Python Requests
- WebSockets

### Agent
- psutil (network monitoring)
- getmac (MAC address)
- netsh (WiFi SSID)
- socket (DNS resolution)

---

## 📊 Dashboards

### 1. User Dashboard
- Personal risk score
- Recent activity
- Access permissions

### 2. Admin Dashboard
- User management
- Login history with device details
- File access logs
- User approval system

### 3. SOC Dashboard
- Threat matrix (all users)
- Real-time file activity stream
- Network connection monitoring
- Risk-based alerts

---

## 🔄 How It Works

### 1. Authentication Flow
```
User Login → GPS/IP Location → Device Fingerprint → Risk Calculation → Access Decision
```

### 2. Continuous Monitoring
```
Agent (every 10s) → Capture Device/Network/File Data → Send to Backend → Update Risk Score → Alert if Suspicious
```

### 3. Risk-Based Access
```
Low Risk → Full Access
Medium Risk → Limited Access + Monitoring
High Risk → Restricted Access + Alert Admin
Critical Risk → Block Access + Immediate Investigation
```

---

## 📈 Use Cases

### Corporate Security
- Insider threat detection
- Data exfiltration prevention
- Compliance monitoring (GDPR, HIPAA)

### Financial Services
- Fraud detection
- Account takeover prevention
- Transaction monitoring

### Healthcare
- Patient data access tracking
- HIPAA compliance
- Unauthorized access alerts

### E-commerce
- Fraudulent order detection
- Account security
- Payment monitoring

---

## 🐛 Known Limitations

- Agent requires installation on user devices
- Free tier services may have cold starts (Render)
- Browser-only deployment cannot access WiFi/MAC (security restriction)
- Polling-based monitoring (not true real-time WebSockets)

---

## 🚧 Future Enhancements

- [ ] Machine Learning-based anomaly detection
- [ ] Behavioral biometrics (typing patterns)
- [ ] Multi-factor authentication (MFA)
- [ ] Email/SMS alerts
- [ ] Mobile app (iOS/Android)
- [ ] Automated threat response
- [ ] Integration with SIEM tools
- [ ] Password hashing (bcrypt)
- [ ] JWT authentication

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👥 Contributors

- **Bhargav Sai** - [@BHARGAVSAI558](https://github.com/BHARGAVSAI558)

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review API documentation at `/docs` endpoint

---

## 🙏 Acknowledgments

Inspired by enterprise security solutions:
- CrowdStrike Falcon
- Microsoft Defender
- Splunk UBA
- Carbon Black

---

## ⭐ Star This Repository

If you find this project useful, please give it a star! ⭐

---

**Built with ❤️ for Zero Trust Security**
