@echo off
title Push to GitHub

echo ========================================
echo   PUSHING TO GITHUB
echo ========================================
echo.

echo Step 1: Adding all files...
git add .

echo.
echo Step 2: Committing changes...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update deployment files

git commit -m "%commit_msg%"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo   PUSH COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Go to Render.com to deploy backend
echo 2. Go to Netlify.com to deploy frontend
echo 3. Check DEPLOYMENT_GUIDE.md for details
echo.
pause
