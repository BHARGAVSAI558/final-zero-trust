@echo off
echo Starting Zero Trust System...
echo.

echo [1/2] Starting Backend...
cd backend
start cmd /k "echo Backend Server && uvicorn main:app --reload"
timeout /t 3 > nul

echo [2/2] Starting Frontend...
cd ..\frontend
start cmd /k "echo Frontend Server && npm start"

echo.
echo ✓ Both servers are starting...
echo ✓ Browser will open automatically
echo ✓ Login: admin / admin123
echo.
pause
