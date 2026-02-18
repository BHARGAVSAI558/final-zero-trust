@echo off
echo ========================================
echo ZERO TRUST SYSTEM - STARTUP
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "Backend" cmd /k "cd backend && python main_advanced.py"
timeout /t 5 /nobreak >nul

echo [2/2] Starting Frontend...
cd frontend
start "" http://localhost:3000
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo SYSTEM STARTED!
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Browser will open automatically...
echo Press any key to close this window...
pause >nul
