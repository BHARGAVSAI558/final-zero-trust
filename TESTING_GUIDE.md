# 🧪 ZERO TRUST - Testing Guide

## Quick Test Checklist

### ✅ Backend Tests

```bash
cd backend

# Test 1: Health Check
curl http://localhost:8000/health

# Test 2: Admin View
curl http://localhost:8000/security/analyze/admin

# Test 3: Real-time Stats
curl http://localhost:8000/realtime/stats

# Test 4: Zones
curl http://localhost:8000/zones
```

### ✅ Frontend Tests

1. **Login Test**
   - Open: http://localhost:3000
   - Login: admin / admin123
   - Verify: Dashboard loads

2. **Real-time Updates**
   - Watch dashboard auto-refresh every 2s
   - Check live activity feed
   - Verify stats update

3. **Role-Based Access**
   - Login as admin → See all users
   - Login as hr → See employee directory
   - Login as user → See personal workspace

### ✅ Agent Tests

1. **Device Registration**
   - Run: `python unified_soc_agent.py`
   - Enter username
   - Verify: Device info displayed

2. **Telemetry**
   - Watch CPU/Memory metrics update
   - Check network connections
   - Verify data sent to backend

3. **File Monitoring**
   - Access files from user dashboard
   - Check agent logs file activities
   - Verify backend receives data

## Detailed Test Scenarios

### Scenario 1: Insider Threat Detection

**Steps:**
1. Login as user at odd hours (after 8 PM)
2. Access sensitive files
3. Delete multiple files
4. Check admin dashboard

**Expected:**
- Risk score increases
- Signals appear: ODD_HOUR_LOGIN, FILE_DELETION
- Decision changes to RESTRICT/DENY

### Scenario 2: Multiple Device Detection

**Steps:**
1. Login from Device A
2. Login from Device B (different MAC)
3. Check admin dashboard

**Expected:**
- Signal: DEVICE_CHANGE
- Risk score increases
- Both devices logged

### Scenario 3: Real-time Monitoring

**Steps:**
1. Open admin dashboard
2. Run agent on employee machine
3. Perform file operations

**Expected:**
- Dashboard updates within 2s
- File logs appear immediately
- Activity feed shows events

### Scenario 4: Session Tracking

**Steps:**
1. Login as user
2. Access multiple files
3. Admin clicks "MORE DETAILS"

**Expected:**
- Session history displayed
- File activities listed
- Duration calculated
- Device fingerprint shown

## Performance Tests

### Load Test

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test backend
ab -n 1000 -c 10 http://localhost:8000/health

# Expected: <100ms average response time
```

### Stress Test

```bash
# Run multiple agents simultaneously
for i in {1..10}; do
  python unified_soc_agent.py user$i &
done

# Monitor backend CPU/Memory
# Expected: <80% CPU, <2GB RAM
```

## Security Tests

### Test 1: SQL Injection

```bash
# Try malicious input
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin' OR '1'='1&password=test"

# Expected: Login fails, no SQL error
```

### Test 2: XSS Prevention

```bash
# Try script injection
curl -X POST http://localhost:8000/files/access \
  -H "Content-Type: application/json" \
  -d '{"user_id":"<script>alert(1)</script>","file_name":"test.txt","action":"READ"}'

# Expected: Script not executed, data sanitized
```

### Test 3: Rate Limiting

```bash
# Rapid requests
for i in {1..100}; do
  curl http://localhost:8000/health &
done

# Expected: Some requests blocked after threshold
```

## Integration Tests

### Test 1: End-to-End Flow

1. User registers → Pending approval
2. Admin approves → User active
3. User logs in → Session created
4. Agent sends telemetry → Data logged
5. User accesses files → Risk calculated
6. Admin views dashboard → All data visible

### Test 2: WebSocket Connection

```javascript
// Test in browser console
const ws = new WebSocket('ws://localhost:8000/ws/test-client');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', e.data);
ws.send('test message');
```

## Automated Test Script

```python
# test_system.py
import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✓ Health check passed")

def test_login():
    data = {"username": "admin", "password": "admin123"}
    r = requests.post(f"{BASE_URL}/auth/login", data=data)
    assert r.json()["status"] == "SUCCESS"
    print("✓ Login test passed")

def test_admin_view():
    r = requests.get(f"{BASE_URL}/security/analyze/admin")
    assert "users" in r.json()
    print("✓ Admin view test passed")

def test_realtime_stats():
    r = requests.get(f"{BASE_URL}/realtime/stats")
    assert "total_users" in r.json()
    print("✓ Real-time stats test passed")

if __name__ == "__main__":
    print("Running system tests...")
    test_health()
    test_login()
    test_admin_view()
    test_realtime_stats()
    print("\n✅ All tests passed!")
```

Run: `python test_system.py`

## Browser Tests

### Chrome DevTools

1. Open: http://localhost:3000
2. Press F12
3. Check Console for errors
4. Check Network tab for API calls
5. Check WebSocket connection

### Expected Results:
- No console errors
- API calls return 200
- WebSocket shows "connected"
- Real-time updates working

## Database Tests

```sql
-- Connect to database
psql -U postgres -d zero

-- Test 1: Check tables
\dt

-- Test 2: Count users
SELECT COUNT(*) FROM users;

-- Test 3: Recent logins
SELECT * FROM login_logs ORDER BY login_time DESC LIMIT 10;

-- Test 4: Device logs
SELECT * FROM device_logs ORDER BY first_seen DESC LIMIT 10;

-- Test 5: File access
SELECT * FROM file_access_logs ORDER BY access_time DESC LIMIT 10;
```

## Troubleshooting Tests

### If Dashboard Not Updating:

```bash
# Check backend logs
# Look for WebSocket connections
# Verify interval is running

# Test manually
curl http://localhost:8000/realtime/stats
```

### If Agent Not Connecting:

```bash
# Check backend URL
# Verify port 8000 open
# Test connection
curl http://localhost:8000/health
```

### If Database Errors:

```bash
# Check PostgreSQL running
sudo systemctl status postgresql

# Test connection
psql -U postgres -d zero -c "SELECT 1;"
```

## Test Results Template

```
Test Date: ___________
Tester: ___________

Backend Tests:
[ ] Health check
[ ] Login
[ ] Admin view
[ ] Real-time stats
[ ] WebSocket

Frontend Tests:
[ ] Login page
[ ] Admin dashboard
[ ] User dashboard
[ ] HR dashboard
[ ] Real-time updates

Agent Tests:
[ ] Device registration
[ ] Telemetry
[ ] File monitoring
[ ] Network tracking

Integration Tests:
[ ] End-to-end flow
[ ] Role-based access
[ ] Session tracking
[ ] Risk calculation

Performance:
API Response: _____ ms
Dashboard Load: _____ s
Memory Usage: _____ MB

Issues Found:
1. ___________
2. ___________
3. ___________

Overall Status: PASS / FAIL
```

---

**⚡ ZERO TRUST - Quality Assurance**
