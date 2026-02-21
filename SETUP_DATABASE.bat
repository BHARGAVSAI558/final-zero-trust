@echo off
title Database Setup
color 0A

echo ========================================
echo   ZERO TRUST DATABASE SETUP
echo ========================================
echo.

echo This will create the database and tables...
echo.
echo Make sure MySQL is running!
echo.
pause

cd backend
mysql -u root -p < schema.sql

echo.
echo ========================================
echo   Database setup complete!
echo ========================================
echo.
pause
