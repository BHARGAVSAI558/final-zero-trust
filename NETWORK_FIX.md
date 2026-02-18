# Network Monitoring Fix

## Problem
Network activity showing "No network activity" in session history.

## Root Cause
`psutil.net_connections()` requires **administrator privileges** on Windows.

## Solution
Updated `zero_trust_agent.py` with fallback method:

1. **Try psutil first** (if admin privileges available)
2. **Fallback to netstat** (works without admin)

## How to Use

### Option 1: Run as Administrator (Recommended)
```bash
# Right-click Command Prompt → Run as Administrator
cd e:\zero-trust-tool\agent
python zero_trust_agent.py mahesh
```

### Option 2: Run Normally (Uses netstat fallback)
```bash
cd e:\zero-trust-tool\agent
python zero_trust_agent.py mahesh
```

## Testing
Run agent for 60 seconds, then check database:
```bash
python check_network_db.py
```

Should show network connections for the user.

## Expected Result
Session history will show:
- 🌐 NETWORK (10+)
- Remote IPs and ports
- TCP/UDP protocol
- Internal/External classification

## Status
✅ Fixed - Agent now collects network data without admin privileges
