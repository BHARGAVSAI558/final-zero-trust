import sys
sys.path.insert(0, 'backend')
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

try:
    response = client.get("/security/analyze/admin")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
