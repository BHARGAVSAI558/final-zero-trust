import requests
import json

response = requests.get("http://localhost:8000/admin/user-sessions/mahesh")
data = response.json()

print("=== API RESPONSE ===")
print(json.dumps(data, indent=2, default=str))
