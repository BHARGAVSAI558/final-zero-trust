@echo off
echo ========================================
echo ZERO TRUST SYSTEM - LOCAL SETUP
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
cd backend
pip install mysql-connector-python fastapi uvicorn requests python-multipart
echo.

echo Step 2: Starting Backend Server...
start cmd /k "python main_local.py"
timeout /t 3
echo.

echo Step 3: Starting Frontend...
cd ..\frontend
start cmd /k "npm start"
echo.

echo ========================================
echo SYSTEM STARTED!
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Login: admin / admin123
echo ========================================
pause
