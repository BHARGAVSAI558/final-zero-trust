@echo off
title Zero Trust Security Platform - Startup

echo ========================================
echo   ZERO TRUST SECURITY PLATFORM
echo ========================================
echo.

echo [1/3] Starting Agent Service...
cd agent
start "Agent Service" cmd /k "python agent_service.py"
cd ..
timeout /t 2 /nobreak >nul

echo [2/3] Starting Backend Server...
cd backend
start "Backend Server" cmd /k "uvicorn main:app --reload --port 8000"
cd ..
timeout /t 3 /nobreak >nul

echo [3/3] Starting Frontend...
cd frontend
start "Frontend" cmd /k "npm start"
cd ..

echo.
echo ========================================
echo   ALL SERVICES STARTED!
echo ========================================
echo.
echo Agent Service: Port 9999
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause >nul
