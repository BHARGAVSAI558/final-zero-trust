# QUICK START GUIDE

## Step 1: Setup Database
1. Make sure MySQL is running
2. Run: SETUP_DATABASE.bat
   (This will create the database and tables)

## Step 2: Install Dependencies

### Backend:
```
cd backend
pip install -r requirements.txt
```

### Frontend:
```
cd frontend
npm install
```

## Step 3: Start the Application

### Option A - Start Everything:
```
START_ALL.bat
```

### Option B - Start Individually:
```
# Terminal 1
START_BACKEND.bat

# Terminal 2
START_FRONTEND.bat
```

## Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Default Login
- Username: admin
- Password: admin123

## Troubleshooting

### Database Connection Error:
- Check MySQL is running
- Verify credentials in backend/.env
- Run SETUP_DATABASE.bat again

### Port Already in Use:
- Kill processes on ports 3000 and 8000
- Or change ports in the config files

### Module Not Found:
- Run: pip install -r backend/requirements.txt
- Run: npm install (in frontend folder)
