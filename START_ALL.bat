@echo off
title Zero Trust Security Platform - Startup

echo ========================================
echo   ZERO TRUST SECURITY PLATFORM
echo ========================================
echo.

echo [1/3] Starting Auto Agent (Continuous Monitoring)...
cd agent
start "Auto Agent" cmd /k "python auto_agent.py"
cd ..
timeout /t 3 /nobreak >nul

echo [2/3] Starting Backend Server (Port 8000)...
cd backend
start "Backend Server" cmd /k "uvicorn main:app --reload --port 8000"
cd ..
timeout /t 5 /nobreak >nul

echo [3/3] Starting Frontend (Port 3000)...
cd frontend
start "Frontend" cmd /k "npm start"
cd ..

echo.
echo ========================================
echo   ALL SERVICES STARTED!
echo ========================================
echo.
echo Auto Agent: Continuous device monitoring
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo IMPORTANT: Keep all 3 windows open!
echo Agent updates device info every 10 seconds.
echo.
echo Press any key to exit this window...
pause >nul
