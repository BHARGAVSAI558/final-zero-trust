# Zero Trust Insider Threat Monitoring System - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 8.0+

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and set JWT_SECRET to a secure random string
```

3. **Setup Database**
```bash
mysql -u root -p < schema.sql
```

4. **Run Backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Run Frontend**
```bash
npm start
```

Access at: http://localhost:3000

### Default Credentials
- Username: `admin`
- Password: `admin123`

---

## 🔒 Security Features

### ✅ Implemented
- JWT Authentication with bcrypt password hashing
- Rate limiting (SlowAPI)
- Geolocation tracking
- UEBA with 13+ behavioral signals
- Micro-segmentation (4 security zones)
- Blockchain audit trail
- Connection pooling
- Environment-based configuration

### 🎯 UEBA Signals Detected
1. ODD_LOGIN_TIME - Logins outside 6 AM - 10 PM
2. FAILED_LOGIN - Failed authentication attempts
3. MULTIPLE_LOGIN_ATTEMPTS - >5 logins in session
4. EXTERNAL_NETWORK - Non-private IP addresses
5. UNKNOWN_DEVICE_ID - Unrecognized MAC addresses
6. HOTSPOT_NETWORK - Mobile hotspot connections
7. UNTRUSTED_DEVICE - Devices not marked as trusted
8. DEVICE_CHANGE_DETECTED - >2 different devices
9. SENSITIVE_FILE_ACCESS - Access to credentials/secrets
10. GEOLOCATION_ANOMALY - >2 different countries
11. MULTIPLE_IP_ADDRESSES - >3 different IPs
12. FILE_DELETION - File deletion operations
13. EXCESSIVE_FILE_ACCESS - >20 file operations

### 🛡️ Micro-Segmentation Zones
- **Public** (Risk ≤100): dashboard, profile
- **Internal** (Risk ≤50): reports, analytics
- **Sensitive** (Risk ≤30): admin, config, credentials
- **Critical** (Risk ≤10): database, secrets, keys

---

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - User login (returns JWT)
- `POST /auth/register` - User registration

### Security Analysis
- `GET /security/analyze/admin` - Admin view (all users)
- `GET /security/analyze/user/{username}` - User-specific view

### Monitoring
- `GET /admin/file-access` - File access logs
- `GET /audit/chain` - Blockchain audit trail
- `POST /agent/heartbeat` - Device telemetry submission
- `GET /microsegment/check/{resource}` - Check resource access

### Health
- `GET /health` - Service health check

---

## 🌐 Production Deployment

### Backend (AWS EC2 / DigitalOcean)

1. **Install System Dependencies**
```bash
sudo apt update
sudo apt install python3-pip mysql-server nginx
```

2. **Setup Application**
```bash
git clone <your-repo>
cd backend
pip install -r requirements.txt
```

3. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **Run with Gunicorn**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

5. **Setup Systemd Service**
```ini
[Unit]
Description=Zero Trust API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
ExecStart=/usr/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
Restart=always

[Install]
WantedBy=multi-user.target
```

### Frontend (Vercel / Netlify)

1. **Build Production**
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**
```bash
npm install -g vercel
vercel --prod
```

3. **Update API URL**
Edit `src/api/api.js` and change baseURL to your production backend URL.

---

## 🔧 Environment Variables

### Backend (.env)
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-secure-password
DB_NAME=zerotrust
JWT_SECRET=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_URL=https://api.yourdomain.com
FRONTEND_URL=https://yourdomain.com
RATE_LIMIT_PER_MINUTE=10
```

---

## 📈 Monitoring & Maintenance

### Database Backups
```bash
mysqldump -u root -p zerotrust > backup_$(date +%Y%m%d).sql
```

### Log Monitoring
```bash
tail -f /var/log/nginx/access.log
journalctl -u zerotrust-api -f
```

### Performance Tuning
- Enable MySQL query caching
- Use Redis for session storage
- Implement CDN for frontend assets
- Enable gzip compression in Nginx

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📝 License
MIT License - See LICENSE file

## 🤝 Support
For issues and questions, open a GitHub issue or contact support.
