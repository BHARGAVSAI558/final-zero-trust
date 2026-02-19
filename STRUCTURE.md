# Project Structure

```
zero-trust-tool/
├── backend/              # FastAPI Backend
│   ├── main.py          # Main API server
│   ├── advanced_ueba.py # Behavioral analytics
│   ├── websocket_manager.py # Real-time updates
│   ├── init_db.py       # Database initialization
│   └── requirements.txt # Python dependencies
│
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── pages/      # Dashboard pages
│   │   ├── components/ # Reusable components
│   │   ├── api/        # API calls
│   │   └── styles/     # CSS themes
│   └── package.json    # Node dependencies
│
├── agent/              # Monitoring Agent
│   ├── unified_soc_agent.py # Main agent
│   ├── zero_trust_agent.py  # Background agent
│   └── requirements.txt     # Agent dependencies
│
└── start.bat           # Quick start script
```

## Core Files

### Backend
- `main.py` - API endpoints, authentication, risk scoring
- `advanced_ueba.py` - User behavior analytics
- `websocket_manager.py` - Real-time communication
- `init_db.py` - Database setup

### Frontend
- `pages/AdminDashboard.jsx` - Admin monitoring view
- `pages/UserDashboard.jsx` - Employee workspace
- `pages/HRDashboard.jsx` - HR management
- `components/Logo.jsx` - Brand logo
- `LandingPage.jsx` - Public homepage

### Agent
- `unified_soc_agent.py` - GUI monitoring tool
- `zero_trust_agent.py` - Background service
