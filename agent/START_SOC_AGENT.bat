@echo off
title Zero Trust - Unified SOC Agent
color 0A
echo ========================================
echo    ZERO TRUST - UNIFIED SOC AGENT
echo ========================================
echo.
echo Starting advanced monitoring agent...
echo.
cd /d "%~dp0"
python unified_soc_agent.py
pause
