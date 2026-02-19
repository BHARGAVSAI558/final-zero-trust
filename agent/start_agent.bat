@echo off
title Zero Trust Agent
color 0A
echo ========================================
echo    ZERO TRUST MONITORING AGENT
echo ========================================
echo.
cd /d "%~dp0"
python unified_soc_agent.py
pause
