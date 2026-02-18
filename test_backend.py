import requests
import json

BASE_URL = "http://localhost:8000"
USERNAME = "jesh"

print("=" * 60)
print("TESTING ZERO TRUST BACKEND")
print("=" * 60)

# Test 1: Get user data
print("\n1. Testing /security/analyze/user/{username}")
response = requests.get(f"{BASE_URL}/security/analyze/user/{USERNAME}")
print(f"Status: {response.status_code}")
data = response.json()
print(json.dumps(data, indent=2))

# Test 2: Register device
print("\n2. Testing /device/register")
device_data = {
    "username": USERNAME,
    "device_id": "TEST-DEVICE-123",
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "os": "Windows 11",
    "wifi_ssid": "TestWiFi",
    "hostname": "TEST-PC"
}
response = requests.post(f"{BASE_URL}/device/register", json=device_data)
print(f"Status: {response.status_code}")
print(response.json())

# Test 3: File access
print("\n3. Testing /files/access")
file_data = {
    "user_id": USERNAME,
    "file_name": "test_report.pdf",
    "action": "READ"
}
response = requests.post(f"{BASE_URL}/files/access", json=file_data)
print(f"Status: {response.status_code}")
print(response.json())

# Test 4: Get file list
print("\n4. Testing /files/list/{username}")
response = requests.get(f"{BASE_URL}/files/list/{USERNAME}")
print(f"Status: {response.status_code}")
files = response.json()
print(f"Files found: {len(files)}")
if files:
    print(json.dumps(files[0], indent=2, default=str))

# Test 5: Get user data again (should show device info now)
print("\n5. Re-testing /security/analyze/user/{username} (after device registration)")
response = requests.get(f"{BASE_URL}/security/analyze/user/{USERNAME}")
data = response.json()
print(f"MAC Address: {data.get('mac_address')}")
print(f"WiFi SSID: {data.get('wifi_ssid')}")
print(f"Hostname: {data.get('hostname')}")
print(f"OS: {data.get('os')}")
print(f"IP Address: {data.get('ip_address')}")

print("\n" + "=" * 60)
print("TESTS COMPLETE")
print("=" * 60)
