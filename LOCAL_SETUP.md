# LOCAL SETUP FOR ZERO TRUST SYSTEM

## 1. Install MySQL
Download and install MySQL from: https://dev.mysql.com/downloads/installer/

During installation:
- Set root password: `root123`
- Port: `3306`

## 2. Create Database
Open MySQL Workbench or Command Line:

```sql
CREATE DATABASE zero_trust;
USE zero_trust;

-- Users table with status for approval workflow
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'user',
    status VARCHAR(20) DEFAULT 'active',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Login logs for UEBA analysis
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    success BOOLEAN DEFAULT TRUE,
    country VARCHAR(100) DEFAULT 'Unknown',
    city VARCHAR(100) DEFAULT 'Unknown'
);

-- Device fingerprints
CREATE TABLE device_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    device_id VARCHAR(255) UNIQUE,
    mac_address VARCHAR(17),
    os VARCHAR(50),
    trusted BOOLEAN DEFAULT FALSE,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    wifi_ssid VARCHAR(100),
    hostname VARCHAR(100),
    ip_address VARCHAR(45)
);

-- File access logs for monitoring
CREATE TABLE file_access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    action VARCHAR(10) DEFAULT 'READ',
    ip_address VARCHAR(45),
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default users
INSERT INTO users (username, password, role, status) VALUES 
('admin', 'admin123', 'admin', 'active'),
('bhargav', 'admin123', 'user', 'active');
```

## 3. Install Python Dependencies
```bash
cd e:\zero-trust-tool\backend
pip install fastapi uvicorn mysql-connector-python requests python-multipart
```

## 4. Update Backend for MySQL
File: `backend/main_local.py` (created below)

## 5. Run Backend Locally
```bash
cd e:\zero-trust-tool\backend
python main_local.py
```

Backend will run on: http://localhost:8000

## 6. Update Frontend for Local
File: `frontend/src/api/api_local.js` (created below)

## 7. Run Frontend Locally
```bash
cd e:\zero-trust-tool\frontend
npm start
```

Frontend will run on: http://localhost:3000

## 8. Test Everything
1. Open http://localhost:3000
2. Login as admin/admin123
3. Register new user
4. Approve user from admin dashboard
5. Test file access
6. Check UEBA risk scores
7. View blockchain audit trail

All features will work locally with accurate timestamps and real-time data!
