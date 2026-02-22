@echo off
title Initial GitHub Setup

echo ========================================
echo   ZERO TRUST - GITHUB SETUP
echo ========================================
echo.

echo This script will push your code to GitHub
echo Repository: https://github.com/BHARGAVSAI558/final-zero-trust.git
echo.
pause

echo.
echo Step 1: Initializing Git repository...
git init

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit - Zero Trust Security Platform"

echo.
echo Step 4: Setting main branch...
git branch -M main

echo.
echo Step 5: Adding remote repository...
git remote add origin https://github.com/BHARGAVSAI558/final-zero-trust.git

echo.
echo Step 6: Pushing to GitHub...
echo.
echo NOTE: You may need to enter your GitHub credentials
echo If you have 2FA enabled, use a Personal Access Token as password
echo.
git push -u origin main

echo.
echo ========================================
echo   GITHUB SETUP COMPLETE!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo NEXT STEPS:
echo 1. Go to https://github.com/BHARGAVSAI558/final-zero-trust
echo 2. Verify all files are uploaded
echo 3. Follow DEPLOYMENT_GUIDE.md to deploy to cloud
echo.
echo DEPLOYMENT PLATFORMS:
echo - Frontend: https://netlify.com
echo - Backend: https://render.com
echo - Database: https://supabase.com or https://railway.app
echo.
pause
