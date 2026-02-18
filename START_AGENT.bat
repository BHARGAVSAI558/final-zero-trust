@echo off
if "%1"=="" (
    echo ========================================
    echo ERROR: Username required!
    echo ========================================
    echo Usage: START_AGENT.bat [username]
    echo Example: START_AGENT.bat bhargav
    echo.
    pause
    exit /b
)

echo ========================================
echo ZERO TRUST AGENT - STARTING
echo ========================================
echo User: %1
echo Backend: http://localhost:8000
echo ========================================
echo.

cd agent
python zero_trust_agent.py %1

pause
