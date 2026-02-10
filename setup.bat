@echo off
echo ========================================
echo Zero Trust System - Setup Script
echo ========================================
echo.

echo [1/5] Setting up Backend...
cd backend

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Please edit backend\.env and set JWT_SECRET before continuing!
    pause
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/5] Setting up Database...
echo Please ensure MySQL is running and execute schema.sql manually:
echo mysql -u root -p ^< schema.sql
pause

echo.
echo [3/5] Setting up Frontend...
cd ..\frontend

echo Installing Node dependencies...
call npm install

echo.
echo [4/5] Setup Complete!
echo.
echo To start the application:
echo.
echo Backend:  cd backend ^&^& uvicorn main:app --reload
echo Frontend: cd frontend ^&^& npm start
echo.
echo Default login: admin / admin123
echo.
echo [5/5] Opening documentation...
start ..\README.md

pause
