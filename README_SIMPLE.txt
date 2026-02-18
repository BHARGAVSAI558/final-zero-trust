# ========================================
# ZERO TRUST SYSTEM - SIMPLE INSTRUCTIONS
# ========================================

## TO START THE SYSTEM:

1. Double-click: START.bat
2. Wait 10 seconds
3. Browser opens automatically to http://localhost:3000
4. Login with: admin / admin123

## TO START AGENT (for real device data):

Double-click ONE of these:
- AGENT_BHARGAV.bat
- AGENT_MAHESH.bat
- AGENT_SAI.bat

## WHAT YOU'LL SEE:

### START.bat opens:
- 2 terminal windows (backend + frontend)
- Browser with login page

### AGENT_*.bat shows:
- Device info (MAC, WiFi, Hostname)
- "Telemetry sent successfully" every 60 seconds

## IF BROWSER DOESN'T OPEN:

Manually go to: http://localhost:3000

## AGENT IS OPTIONAL:

- Without agent: Device shows "N/A" (browser limitation)
- With agent: Device shows real MAC, WiFi, Hostname, OS

## DEMO FLOW:

1. START.bat → Opens system
2. Login as admin
3. See users in dashboard
4. AGENT_BHARGAV.bat → Start monitoring
5. Login as bhargav (different browser/incognito)
6. Admin clicks "MORE DETAILS" on bhargav
7. See complete session history with device data!

## THAT'S IT!

Just double-click START.bat to begin!
