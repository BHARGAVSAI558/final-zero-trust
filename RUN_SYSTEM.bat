@echo off
echo ============================================================
echo ZERO TRUST SYSTEM - STARTING ALL COMPONENTS
echo ============================================================
echo.

echo [1/3] Starting Backend Server...
start "Backend" cmd /k "cd /d e:\zero-trust-tool\backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 5 /nobreak >nul

echo [2/3] Starting Frontend Dashboard...
start "Frontend" cmd /k "cd /d e:\zero-trust-tool\frontend && npm start"
timeout /t 5 /nobreak >nul

echo [3/3] Starting Monitoring Agent...
start "Agent" cmd /k "cd /d e:\zero-trust-tool\agent && python zero_trust_agent.py bhargav"

echo.
echo ============================================================
echo ALL COMPONENTS STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo Backend API:  http://localhost:8000
echo Frontend UI:  http://localhost:3000
echo Agent:        Running for user 'bhargav'
echo.
echo Press any key to exit (components will keep running)...
pause >nul
