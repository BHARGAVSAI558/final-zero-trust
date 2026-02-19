@echo off
title Zero Trust Platform
color 0A
echo ========================================
echo    ZERO TRUST SECURITY PLATFORM
echo ========================================
echo.
echo Starting all services...
echo.

start "Backend" cmd /k "cd backend && uvicorn main:app --reload"
timeout /t 3 /nobreak >nul

start "Frontend" cmd /k "cd frontend && npm start"
timeout /t 3 /nobreak >nul

echo.
echo All services started!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
