@echo off
echo Killing backend processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Backend*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend...
cd backend
start "Backend Server" cmd /k "python run.py"
echo Backend started!
