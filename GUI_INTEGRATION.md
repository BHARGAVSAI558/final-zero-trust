# ✅ GUI TOOL - COMPLETE INTEGRATION

## How It Works:

### 1. GUI Tool (zero_trust_gui_v2.py):
- Collects real device data (MAC, WiFi, Hostname, OS)
- Sends to backend every 60 seconds via `/device/register`
- Dashboard button opens http://localhost:3000

### 2. Admin Dashboard:
- Auto-refreshes every 3 seconds
- Shows device data from GUI tool
- Updates in real-time

## 🚀 USAGE:

### Step 1: Start System
```bash
START.bat
```
Wait for browser to open

### Step 2: Start GUI Tool
```bash
AGENT_GUI.bat
```
Or:
```bash
cd agent
python zero_trust_gui_v2.py
```

### Step 3: In GUI Tool:
1. Enter username: `bhargav`
2. Click "START MONITORING"
3. See device info displayed
4. Click "📊 DASHBOARD" button → Opens admin dashboard

### Step 4: In Admin Dashboard:
1. Login as admin/admin123
2. Click "MORE DETAILS" on bhargav
3. See real device data:
   - MAC: Real MAC address
   - WiFi: Real WiFi SSID
   - Hostname: Real computer name
   - OS: Real operating system

## 🔄 Data Flow:

```
GUI Tool (zero_trust_gui_v2.py)
    ↓
Collects: MAC, WiFi, Hostname, OS
    ↓
Sends to: http://localhost:8000/device/register
    ↓
Backend stores in device_logs table
    ↓
Admin Dashboard fetches every 3 seconds
    ↓
Shows in "MORE DETAILS" modal
```

## ✅ What's Already Fixed:

1. ✓ GUI tool URL: Changed from Netlify to localhost:8000
2. ✓ Dashboard button: Opens localhost:3000
3. ✓ Device registration: Sends to /device/register
4. ✓ Admin dashboard: Auto-refresh every 3 seconds
5. ✓ Real-time updates: Device data updates automatically

## 🎯 Test It:

1. **Start system**: `START.bat`
2. **Start GUI**: `AGENT_GUI.bat`
3. **Enter username**: bhargav
4. **Click START MONITORING**
5. **Wait 60 seconds** (first telemetry send)
6. **Click 📊 DASHBOARD button**
7. **Login as admin**
8. **Click MORE DETAILS on bhargav**
9. **See real device data!**

## 📊 Expected Result:

```
💻 DEVICE FINGERPRINT
ID: abc123def456
MAC: 4b:2d:b4:d2:4a:2b  ← Real MAC
WiFi: KLEF-R             ← Real WiFi
Host: DESKTOP-PON5EUV    ← Real hostname
OS: Windows 11           ← Real OS
```

## 🔧 If Device Shows N/A:

1. Make sure GUI tool is running
2. Wait 60 seconds for first telemetry
3. Check GUI tool shows "✓ Device registered with backend"
4. Refresh admin dashboard (auto-refreshes every 3s)

## 💡 Key Points:

- GUI tool sends data every 60 seconds
- Admin dashboard refreshes every 3 seconds
- Device data updates automatically
- No manual refresh needed
- Dashboard button opens admin panel directly

## ✅ Everything is Connected!

GUI Tool → Backend → Admin Dashboard → Real-time Updates!
