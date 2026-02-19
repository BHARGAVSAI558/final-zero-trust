@echo off
title Zero Trust - Backend Server
color 0A
echo ========================================
echo    ZERO TRUST - BACKEND SERVER
echo ========================================
echo.
echo Starting backend on port 8000...
echo.
cd /d "%~dp0"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
