import psutil
import requests

print("Testing Network Monitoring...\n")

# Test 1: Check if psutil can access network connections
try:
    connections = psutil.net_connections(kind='inet')
    print(f"OK Found {len(connections)} network connections")
    
    # Show first 5
    for i, conn in enumerate(connections[:5], 1):
        if conn.raddr:
            print(f"  {i}. {conn.raddr.ip}:{conn.raddr.port} ({conn.status})")
except PermissionError:
    print("ERROR: PermissionError - Need administrator privileges!")
    print("  Solution: Run as administrator or use alternative method")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Alternative - Check active connections via netstat
print("\n\nAlternative Method (No admin needed):")
try:
    import subprocess
    result = subprocess.check_output(['netstat', '-n'], encoding='utf-8', errors='ignore')
    lines = [l for l in result.split('\n') if 'ESTABLISHED' in l]
    print(f"OK Found {len(lines)} ESTABLISHED connections")
    for line in lines[:5]:
        print(f"  {line.strip()}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Send test data to backend
print("\n\nTesting Backend Connection:")
try:
    test_data = {
        "username": "test",
        "network": [
            {"type": "TCP", "ip": "142.250.185.46", "port": 443, "protocol": "TCP", "external": True},
            {"type": "TCP", "ip": "192.168.1.1", "port": 80, "protocol": "TCP", "external": False}
        ]
    }
    response = requests.post("http://localhost:8000/agent/telemetry", json=test_data, timeout=5)
    print(f"OK Backend response: {response.status_code}")
except Exception as e:
    print(f"ERROR Backend: {e}")
