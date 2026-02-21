@echo off
title Zero Trust Backend Server
color 0B

echo ========================================
echo   ZERO TRUST BACKEND SERVER
echo   Starting on http://localhost:8000
echo ========================================
echo.

cd backend
python run.py

pause
