# Zero Trust Security Platform

## Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL 8.0+

## Setup Instructions

### 1. Database Setup
```bash
# Login to MySQL
mysql -u root -p

# Run the schema file
source backend/schema.sql
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_mysql.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Run All Services
```bash
START_ALL.bat
```

### Option 2: Run Services Individually
```bash
# Terminal 1 - Backend
START_BACKEND.bat

# Terminal 2 - Frontend
START_FRONTEND.bat

# Terminal 3 - Agent (Optional)
cd agent
start_agent_service.bat
```

## Default Credentials
- Username: admin
- Password: admin123

## Project Structure
- `/backend` - FastAPI backend server
- `/frontend` - React frontend application
- `/agent` - Security monitoring agent
