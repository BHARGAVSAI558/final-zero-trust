@echo off
title Zero Trust - System Startup
color 0A

echo ========================================
echo    ZERO TRUST - SYSTEM STARTUP
echo ========================================
echo.

echo [1/3] Starting Backend Server...
start "Backend" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && npm start"
timeout /t 3 /nobreak >nul

echo [3/3] Starting SOC Agent...
start "SOC Agent" cmd /k "cd agent && python unified_soc_agent.py"

echo.
echo ========================================
echo    ALL SERVICES STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Agent:    Running in separate window
echo.
echo Press any key to exit...
pause >nul
