@echo off
title Project Health Check
color 0B

echo ========================================
echo   ZERO TRUST PROJECT HEALTH CHECK
echo ========================================
echo.

echo [1/5] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo OK
echo.

echo [2/5] Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    pause
    exit /b 1
)
echo OK
echo.

echo [3/5] Checking MySQL...
mysql --version
if %errorlevel% neq 0 (
    echo WARNING: MySQL command not found in PATH
    echo Make sure MySQL is installed and running
)
echo.

echo [4/5] Checking Backend Dependencies...
cd backend
python -c "import fastapi, uvicorn, mysql.connector" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Some backend dependencies missing
    echo Run: pip install -r requirements.txt
) else (
    echo OK
)
cd ..
echo.

echo [5/5] Checking Frontend Dependencies...
cd frontend
if exist node_modules (
    echo OK
) else (
    echo WARNING: node_modules not found
    echo Run: npm install
)
cd ..
echo.

echo ========================================
echo   HEALTH CHECK COMPLETE
echo ========================================
echo.
echo Next steps:
echo 1. Run SETUP_DATABASE.bat (if not done)
echo 2. Run START_ALL.bat to start the application
echo.
pause
