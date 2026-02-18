# 🛡️ Zero Trust Insider Threat Monitoring System - Complete Guide

## 📋 Table of Contents
1. [What is This Tool?](#what-is-this-tool)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Setup Instructions](#setup-instructions)
5. [How to Use](#how-to-use)
6. [Agent Deployment](#agent-deployment)
7. [Understanding the Dashboard](#understanding-the-dashboard)
8. [Security Features](#security-features)

---

## 🎯 What is This Tool?

A **production-ready Zero Trust security platform** that monitors insider threats in real-time using:
- **UEBA (User & Entity Behavior Analytics)** - Detects 13+ behavioral anomalies
- **Micro-segmentation** - 4-tier access control based on risk scores
- **Blockchain Audit Trail** - Immutable logging with Merkle tree validation
- **Continuous Verification** - Every access is verified, never trusted

### Real-World Use Cases:
1. **Prevent Data Exfiltration** - Detect employees copying sensitive files
2. **Insider Threat Detection** - Flag unusual login times, locations, devices
3. **Compliance** - Immutable audit trail for SOC 2, ISO 27001
4. **Access Control** - Automatically restrict high-risk users
5. **Incident Response** - Real-time alerts for suspicious behavior

---

## ✨ Key Features

### 1. **User & Entity Behavior Analytics (UEBA)**
Detects 13+ behavioral anomalies:
- ✅ Odd login times (outside 8 AM - 6 PM)
- ✅ Failed login attempts (brute force detection)
- ✅ Multiple IP addresses (impossible travel)
- ✅ Weekend/holiday access
- ✅ Unknown device IDs
- ✅ Untrusted devices
- ✅ Device changes
- ✅ Sensitive file access
- ✅ Geolocation anomalies
- ✅ File deletions (mass deletion detection)
- ✅ Excessive file access (data exfiltration risk)
- ✅ External network connections
- ✅ Hotspot network usage

### 2. **Micro-Segmentation (4 Tiers)**
Risk-based access control:
- **CRITICAL Zone** (Risk ≤20): High-security assets, databases, secrets
- **SENSITIVE Zone** (Risk ≤40): Confidential data, financial records
- **INTERNAL Zone** (Risk ≤60): Business resources, reports
- **PUBLIC Zone** (Risk >60): Basic resources only

### 3. **Real-Time Device Fingerprinting**
Collects actual device data:
- ✅ Real MAC address
- ✅ WiFi SSID (actual network name)
- ✅ Hostname
- ✅ Operating system
- ✅ IP address with geolocation (latitude/longitude)
- ✅ ISP information
- ✅ Timezone

### 4. **Blockchain Audit Trail**
- Merkle tree validation
- Proof-of-work consensus
- Immutable event logging
- Tamper-proof records

### 5. **Admin Approval Workflow**
- Users register → Status: PENDING
- Admin approves/denies → Status: ACTIVE/DELETED
- Admin can revoke access anytime → Status: REVOKED

### 6. **Session Management**
- 5-minute auto-logout
- Session validation on every request
- Automatic cleanup of expired sessions

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EMPLOYEE WORKSTATION                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Python Agent (zero_trust_agent.py)                │    │
│  │  - Monitors file access                            │    │
│  │  - Tracks network connections                      │    │
│  │  - Collects device fingerprint (MAC, WiFi, etc.)   │    │
│  │  - Sends telemetry every 60 seconds                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP POST
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │  FastAPI (main_advanced.py)                        │    │
│  │  - Receives telemetry                              │    │
│  │  - Calculates risk scores (UEBA)                   │    │
│  │  - Makes access decisions (ALLOW/DENY/RESTRICT)    │    │
│  │  - Logs to blockchain                              │    │
│  │  - Manages sessions (5-min timeout)                │    │
│  └────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  MySQL Database (zerotrust)                        │    │
│  │  - 10 tables (users, sessions, login_logs, etc.)   │    │
│  │  - TIMESTAMP(3) for millisecond precision          │    │
│  │  - Indexes for performance                         │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            ↑ HTTP GET/POST
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Admin Dashboard                                    │    │
│  │  - Real-time user monitoring                       │    │
│  │  - Approve/deny pending users                      │    │
│  │  - Revoke access                                   │    │
│  │  - View risk distribution charts                   │    │
│  │  - File access logs                                │    │
│  │  - Blockchain audit trail                          │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  User Dashboard                                     │    │
│  │  - Personal risk score                             │    │
│  │  - Accessible resources                            │    │
│  │  - Device fingerprint                              │    │
│  │  - Threat signals                                  │    │
│  │  - File access history                             │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Instructions

### 1. Database Setup
```bash
# Start MySQL
mysql -u root -p

# Create database and tables
source e:/zero-trust-tool/MIGRATE_DATABASE.sql

# Verify tables
USE zerotrust;
SHOW TABLES;
```

### 2. Backend Setup
```bash
cd backend
pip install fastapi uvicorn mysql-connector-python requests
python main_advanced.py
```

Backend runs on: http://localhost:8000

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

Frontend runs on: http://localhost:3000

### 4. Agent Setup (On Employee Machines)
```bash
cd agent
pip install -r requirements.txt
python zero_trust_agent.py
# Enter username when prompted
```

---

## 📖 How to Use

### For Administrators:

1. **Login**
   - URL: http://localhost:3000
   - Username: `admin`
   - Password: `admin123`

2. **Approve New Users**
   - Yellow box shows pending users
   - Click "✓ APPROVE" or "✗ DENY"

3. **Monitor Users**
   - View real-time risk scores
   - See device fingerprints (MAC, WiFi, IP)
   - Check threat signals
   - Review file access logs

4. **Revoke Access**
   - Click "🚫 REVOKE" button for any user
   - User immediately loses access

5. **View Blockchain Audit**
   - Scroll to bottom
   - See immutable event logs
   - Verify Merkle tree hashes

### For Regular Users:

1. **Register**
   - Click "📝 New User? Register Here"
   - Enter username and password
   - Wait for admin approval

2. **Login**
   - Enter approved credentials
   - View your risk score
   - See accessible resources

3. **Monitor Your Activity**
   - Check threat signals
   - View device fingerprint
   - See file access history

---

## 🔧 Agent Deployment

### What the Agent Does:
1. **Collects Device Fingerprint**
   - Real MAC address
   - WiFi SSID
   - Hostname
   - OS version
   - IP address

2. **Monitors File Access**
   - Documents folder
   - Downloads folder
   - System32 (Windows)
   - Tracks: filename, path, size, sensitivity

3. **Monitors Network**
   - Active TCP/UDP connections
   - External vs internal IPs
   - Detects data exfiltration attempts

4. **Sends Telemetry**
   - Every 60 seconds
   - To backend: http://localhost:8000/agent/telemetry

### Deploy Agent:
```bash
# On each employee machine
cd agent
python zero_trust_agent.py

# Enter username: john.doe
# Agent runs continuously
```

---

## 📊 Understanding the Dashboard

### Admin Dashboard:

**Stats Cards:**
- TOTAL USERS: All active users
- CRITICAL: Risk score 70-100
- HIGH: Risk score 50-69
- MEDIUM: Risk score 30-49
- LOW: Risk score 0-29

**Charts:**
- Pie Chart: Risk distribution
- Bar Chart: Top 10 threat scores
- Line Chart: Activity trend

**User Table Columns:**
- USER ID: Username
- RISK: Risk score (0-100)
- LEVEL: LOW/MEDIUM/HIGH/CRITICAL
- STATUS: active/pending/revoked
- ACCESS: ALLOW/RESTRICT/DENY
- DEVICE FINGERPRINT: MAC, WiFi, IP, hostname
- THREATS: Behavioral anomalies detected
- ACTIONS: Revoke button

### User Dashboard:

**Risk Cards:**
- THREAT LEVEL: Your risk score
- CLASSIFICATION: Risk level
- ACCESS CONTROL: ALLOW/DENY/RESTRICT
- SESSION COUNT: Total logins

**Threat Detection:**
- Shows all behavioral anomalies
- Examples: ODD_HOUR(3), FAILED_LOGIN(5), MULTI_IP(4)

**Device Fingerprint:**
- Your device details
- Location, IP, MAC, WiFi, hostname

**Accessible Resources:**
- Shows which zones you can access
- Based on your risk score

**File Access Control:**
- Simulate file operations
- READ/WRITE/DELETE buttons
- Color-coded by sensitivity

---

## 🔒 Security Features

### 1. **Zero Trust Principles**
- Never trust, always verify
- Least privilege access
- Assume breach mentality

### 2. **Continuous Verification**
- Every login verified
- Risk calculated in real-time
- Access decisions updated dynamically

### 3. **Behavioral Analytics**
- ML-like scoring algorithm
- 7 weighted categories
- Confidence scoring

### 4. **Immutable Audit Trail**
- Blockchain with Merkle tree
- Proof-of-work validation
- Tamper-proof logs

### 5. **Session Security**
- 5-minute timeout
- Automatic cleanup
- Session validation on every request

### 6. **Admin Controls**
- Approval workflow
- Revoke access anytime
- Real-time monitoring

---

## 🆚 Comparison with Enterprise Tools

| Feature | This Tool | Microsoft ATP | Splunk UEBA |
|---------|-----------|---------------|-------------|
| **Cost** | FREE | $5-10/user/month | $150/GB/day |
| **Deployment** | Self-hosted | Cloud | On-prem/Cloud |
| **Setup Time** | < 1 hour | Days/Weeks | Weeks |
| **UEBA Signals** | 13+ | 100+ | 50+ |
| **Blockchain** | ✅ Merkle tree | ❌ | ❌ |
| **Agent** | ✅ Python | ✅ Native | ✅ Forwarder |
| **Approval Workflow** | ✅ Built-in | ❌ | ❌ |
| **Customization** | Full control | Limited | Moderate |
| **Real-time** | ✅ 5s refresh | ✅ | ✅ |

---

## 🎓 Hackathon Presentation Tips

### Talking Points:
1. **Problem**: Insider threats cost $11.45M per incident (Ponemon Institute)
2. **Solution**: Zero Trust with UEBA + Blockchain
3. **Unique**: Blockchain audit trail, approval workflow, FREE
4. **Demo**: Show live agent → risk score → access decision
5. **Impact**: Prevent data breaches, ensure compliance

### Demo Flow (5 minutes):
1. Show admin dashboard (0:30)
2. Register new user (0:30)
3. Admin approves user (0:30)
4. Start agent on employee machine (1:00)
5. Show device fingerprint appearing (1:00)
6. Simulate suspicious activity (1:00)
7. Show risk score increase + access restriction (0:30)

---

## 📞 Support

For issues:
- Check backend console for errors
- Verify MySQL is running
- Ensure agent has network access
- Check browser console (F12)

---

**⭐ This tool demonstrates enterprise-level security monitoring at zero cost!**
