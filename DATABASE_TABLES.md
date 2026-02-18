# 📊 DATABASE TABLES - ZERO TRUST SYSTEM

## Overview
Total Tables: **4**
Database: **zero_trust**
Engine: **InnoDB**
Charset: **utf8mb4**

---

## TABLE 1: `users`
**Purpose:** Store user accounts with approval workflow

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| password | VARCHAR(255) | NOT NULL | User password (plain text for demo) |
| role | VARCHAR(10) | DEFAULT 'user' | User role: 'admin' or 'user' |
| status | VARCHAR(20) | DEFAULT 'active' | Account status: 'active', 'pending', 'revoked' |
| approved_by | VARCHAR(50) | NULL | Admin who approved the user |
| approved_at | TIMESTAMP | NULL | When user was approved |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

**Indexes:**
- `idx_username` on username
- `idx_status` on status
- `idx_role` on role

**Sample Data:**
```sql
INSERT INTO users (username, password, role, status) VALUES 
('admin', 'admin123', 'admin', 'active'),
('bhargav', 'admin123', 'user', 'active');
```

---

## TABLE 2: `login_logs`
**Purpose:** Track all login attempts for UEBA analysis

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique log ID |
| user_id | VARCHAR(50) | NOT NULL | Username who logged in |
| login_time | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When login occurred |
| ip_address | VARCHAR(45) | NULL | IP address of login |
| success | BOOLEAN | DEFAULT TRUE | Login success/failure |
| country | VARCHAR(100) | DEFAULT 'Unknown' | Country from IP |
| city | VARCHAR(100) | DEFAULT 'Unknown' | City from IP |

**Indexes:**
- `idx_user_id` on user_id
- `idx_login_time` on login_time
- `idx_success` on success

**Used For:**
- Odd-hour login detection
- Failed login attempts
- Multiple IP detection
- Weekend access monitoring
- Geolocation anomalies

---

## TABLE 3: `device_logs`
**Purpose:** Store device fingerprints for tracking

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique device ID |
| user_id | VARCHAR(50) | NOT NULL | Username owning device |
| device_id | VARCHAR(255) | UNIQUE | Unique device identifier |
| mac_address | VARCHAR(17) | NULL | MAC address (AA:BB:CC:DD:EE:FF) |
| os | VARCHAR(50) | NULL | Operating system |
| trusted | BOOLEAN | DEFAULT FALSE | Is device trusted |
| first_seen | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | First time device seen |
| wifi_ssid | VARCHAR(100) | NULL | WiFi network name |
| hostname | VARCHAR(100) | NULL | Computer hostname |
| ip_address | VARCHAR(45) | NULL | Current IP address |

**Indexes:**
- `idx_user_id` on user_id
- `idx_device_id` on device_id
- `idx_trusted` on trusted

**Used For:**
- Untrusted device detection
- Device change monitoring
- Network anomaly detection

---

## TABLE 4: `file_access_logs`
**Purpose:** Monitor all file access operations

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique log ID |
| user_id | VARCHAR(50) | NOT NULL | Username accessing file |
| file_name | VARCHAR(255) | NOT NULL | Name of file accessed |
| action | VARCHAR(10) | DEFAULT 'READ' | Action: READ, WRITE, DELETE |
| ip_address | VARCHAR(45) | NULL | IP address of access |
| access_time | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When file was accessed |

**Indexes:**
- `idx_user_id` on user_id
- `idx_access_time` on access_time
- `idx_action` on action

**Used For:**
- Excessive file access detection
- File deletion monitoring
- Sensitive file access tracking

---

## RELATIONSHIPS

```
users (1) -----> (N) login_logs
  |
  +------------> (N) device_logs
  |
  +------------> (N) file_access_logs
```

---

## UEBA SIGNALS USING THESE TABLES

### Signal 1: Odd-Hour Logins
```sql
SELECT COUNT(*) FROM login_logs 
WHERE user_id='username' 
AND (HOUR(login_time) < 8 OR HOUR(login_time) > 18)
AND login_time > DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

### Signal 2: Failed Login Attempts
```sql
SELECT COUNT(*) FROM login_logs 
WHERE user_id='username' 
AND success=0 
AND login_time > DATE_SUB(NOW(), INTERVAL 1 HOUR);
```

### Signal 3: Multiple IPs
```sql
SELECT COUNT(DISTINCT ip_address) FROM login_logs 
WHERE user_id='username' 
AND login_time > DATE_SUB(NOW(), INTERVAL 1 HOUR);
```

### Signal 4: Weekend Access
```sql
SELECT COUNT(*) FROM login_logs 
WHERE user_id='username' 
AND DAYOFWEEK(login_time) IN (1,7)
AND login_time > DATE_SUB(NOW(), INTERVAL 7 DAY);
```

### Signal 5: Untrusted Devices
```sql
SELECT COUNT(*) FROM device_logs 
WHERE user_id='username' 
AND trusted=0;
```

### Signal 6: Excessive File Access
```sql
SELECT COUNT(*) FROM file_access_logs 
WHERE user_id='username' 
AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

### Signal 7: File Deletions
```sql
SELECT COUNT(*) FROM file_access_logs 
WHERE user_id='username' 
AND action='DELETE' 
AND access_time > DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

---

## SAMPLE QUERIES FOR TESTING

### Create Admin User
```sql
INSERT INTO users (username, password, role, status) 
VALUES ('admin', 'admin123', 'admin', 'active');
```

### Create Regular User
```sql
INSERT INTO users (username, password, role, status) 
VALUES ('bhargav', 'admin123', 'user', 'active');
```

### Create Pending User (Needs Approval)
```sql
INSERT INTO users (username, password, role, status) 
VALUES ('testuser', 'test123', 'user', 'pending');
```

### Log a Login
```sql
INSERT INTO login_logs (user_id, ip_address, success, country, city) 
VALUES ('admin', '127.0.0.1', TRUE, 'India', 'Guntur');
```

### Register a Device
```sql
INSERT INTO device_logs (user_id, device_id, mac_address, os, hostname, ip_address) 
VALUES ('admin', 'DEVICE-001', 'AA:BB:CC:DD:EE:FF', 'Windows 11', 'ADMIN-PC', '127.0.0.1');
```

### Log File Access
```sql
INSERT INTO file_access_logs (user_id, file_name, action, ip_address) 
VALUES ('admin', 'secrets.env', 'READ', '127.0.0.1');
```

### View All Users
```sql
SELECT username, role, status, created_at FROM users;
```

### View Recent Logins
```sql
SELECT user_id, login_time, ip_address, city, country 
FROM login_logs 
ORDER BY login_time DESC 
LIMIT 10;
```

### View File Access History
```sql
SELECT user_id, file_name, action, access_time 
FROM file_access_logs 
ORDER BY access_time DESC 
LIMIT 10;
```

---

## DATABASE SIZE ESTIMATES

**For 100 users over 1 month:**
- users: ~10 KB
- login_logs: ~500 KB (100 users × 50 logins × 100 bytes)
- device_logs: ~20 KB (100 users × 2 devices × 100 bytes)
- file_access_logs: ~5 MB (100 users × 500 files × 100 bytes)

**Total: ~5.5 MB**

---

## BACKUP COMMAND

```bash
mysqldump -u root -p zero_trust > zero_trust_backup.sql
```

## RESTORE COMMAND

```bash
mysql -u root -p zero_trust < zero_trust_backup.sql
```

---

**All tables ready for Zero Trust System!**
