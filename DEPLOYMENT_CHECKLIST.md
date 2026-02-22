# ✅ DEPLOYMENT CHECKLIST

Print this and check off as you go!

---

## 📝 PREPARATION (Before Starting)

- [ ] Code works on localhost (test with START_ALL.bat)
- [ ] Created GitHub account
- [ ] Created Netlify account  
- [ ] Created Render account
- [ ] Created Railway OR Supabase account
- [ ] Have GitHub repository URL ready

---

## 🗄️ STEP 1: DATABASE SETUP

### Railway (MySQL) - Choose this OR Supabase
- [ ] Logged into Railway
- [ ] Created new project
- [ ] Provisioned MySQL
- [ ] Copied MYSQL_HOST
- [ ] Copied MYSQL_USER
- [ ] Copied MYSQL_PASSWORD
- [ ] Copied MYSQL_DATABASE
- [ ] Ran schema.sql in query tool
- [ ] Verified tables created

### Supabase (PostgreSQL) - Choose this OR Railway
- [ ] Logged into Supabase
- [ ] Created new project
- [ ] Saved database password
- [ ] Copied connection details
- [ ] Modified schema.sql for PostgreSQL
- [ ] Ran schema in SQL Editor
- [ ] Verified tables created

---

## 📤 STEP 2: PUSH TO GITHUB

- [ ] Opened terminal in project folder
- [ ] Ran: git init
- [ ] Ran: git add .
- [ ] Ran: git commit -m "Initial commit"
- [ ] Ran: git branch -M main
- [ ] Ran: git remote add origin [YOUR_REPO_URL]
- [ ] Ran: git push -u origin main
- [ ] Verified files on GitHub website

---

## 🖥️ STEP 3: DEPLOY BACKEND (RENDER)

- [ ] Logged into Render
- [ ] Clicked "New Web Service"
- [ ] Connected GitHub repository
- [ ] Selected "final-zero-trust" repo
- [ ] Set name: zero-trust-backend
- [ ] Set build command: pip install -r requirements.txt
- [ ] Set start command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
- [ ] Added environment variable: DB_HOST
- [ ] Added environment variable: DB_USER
- [ ] Added environment variable: DB_PASSWORD
- [ ] Added environment variable: DB_NAME
- [ ] Added environment variable: DB_PORT
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment (5-10 min)
- [ ] Copied backend URL: ___________________________
- [ ] Tested: [BACKEND_URL]/health (should return {"status":"healthy"})

---

## 🌐 STEP 4: DEPLOY FRONTEND (NETLIFY)

- [ ] Logged into Netlify
- [ ] Clicked "Add new site"
- [ ] Selected "Import an existing project"
- [ ] Connected GitHub
- [ ] Selected "final-zero-trust" repo
- [ ] Set base directory: frontend
- [ ] Set build command: npm run build
- [ ] Set publish directory: frontend/build
- [ ] Clicked "Advanced" → "New variable"
- [ ] Added: REACT_APP_API_URL = [YOUR_RENDER_URL]
- [ ] Clicked "Deploy site"
- [ ] Waited for deployment (3-5 min)
- [ ] Copied frontend URL: ___________________________
- [ ] Opened URL in browser
- [ ] Verified login page loads

---

## 🔄 STEP 5: UPDATE CORS

- [ ] Opened backend/main.py in editor
- [ ] Found allow_origins in CORS middleware
- [ ] Added Netlify URL to allow_origins list
- [ ] Saved file
- [ ] Ran: git add backend/main.py
- [ ] Ran: git commit -m "Update CORS"
- [ ] Ran: git push origin main
- [ ] Waited for Render auto-deploy (2-3 min)
- [ ] Verified deployment in Render dashboard

---

## 🧪 STEP 6: TESTING

- [ ] Opened frontend URL in browser
- [ ] Clicked "Register"
- [ ] Created test account
- [ ] Checked database - user record created
- [ ] Logged in as admin (admin/admin123)
- [ ] Approved test user
- [ ] Logged out
- [ ] Logged in as test user
- [ ] Verified dashboard loads
- [ ] Checked browser console - no CORS errors
- [ ] Checked Render logs - no errors

---

## 🎯 FINAL VERIFICATION

- [ ] Frontend URL works: ___________________________
- [ ] Backend URL works: ___________________________
- [ ] Database has data
- [ ] Login works
- [ ] Admin dashboard works
- [ ] User dashboard works
- [ ] No console errors
- [ ] No CORS errors

---

## 📝 SAVE THESE URLS

**Frontend (Netlify)**: ___________________________

**Backend (Render)**: ___________________________

**Database**: Railway / Supabase (circle one)

**GitHub Repo**: https://github.com/BHARGAVSAI558/final-zero-trust

---

## 🎉 SUCCESS!

If all boxes are checked, your Zero Trust platform is LIVE! 🚀

Share these URLs with your mentor:
- Frontend: [Your Netlify URL]
- API Docs: [Your Render URL]/docs

---

## 📞 IF SOMETHING FAILS

1. Check Render logs (Dashboard → Logs)
2. Check Netlify deploy logs (Deploys → Deploy log)
3. Check browser console (F12)
4. Verify environment variables
5. Read error messages carefully
6. Google the error
7. Check DEPLOYMENT_GUIDE.md

---

**Date Deployed**: _______________

**Time Taken**: _______________

**Notes**: 
_________________________________________________
_________________________________________________
_________________________________________________
