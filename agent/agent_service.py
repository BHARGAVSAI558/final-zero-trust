import socket
import platform
import uuid
import hashlib
import requests
import psutil
import subprocess
from datetime import datetime
import time

BACKEND = "http://localhost:8000"
PORT = 9999  # Local port to listen for login triggers

def get_wifi_ssid():
    """Get WiFi SSID"""
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8', errors='ignore')
        for line in result.split('\n'):
            if 'SSID' in line and 'BSSID' not in line:
                return line.split(':')[1].strip()
    except:
        pass
    return "N/A"

def collect_device_info(username):
    """Collect complete device fingerprint"""
    return {
        "username": username,
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "ip": socket.gethostbyname(socket.gethostname()),
        "mac": ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,48,8)][::-1]),
        "device_id": hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16],
        "wifi_ssid": get_wifi_ssid()
    }

def send_device_data(username):
    """Send device data to backend on login"""
    try:
        device_info = collect_device_info(username)
        # Send to device register endpoint
        requests.post(f"{BACKEND}/device/register", json=device_info, timeout=5)
        # Also update the last login with MAC address
        requests.post(f"{BACKEND}/device/update-login", json=device_info, timeout=5)
        print(f"✓ Device data sent for {username}")
        return True
    except Exception as e:
        print(f"✗ Failed to send device data: {e}")
        return False

def start_listener():
    """Listen for login triggers from browser"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', PORT))
    server.listen(1)
    print(f"🔒 Zero Trust Agent Service Running on port {PORT}")
    print(f"⚡ Waiting for login triggers...")
    
    while True:
        try:
            client, addr = server.accept()
            data = client.recv(1024).decode('utf-8')
            
            if data.startswith("LOGIN:"):
                username = data.split(":")[1].strip()
                print(f"\n🔐 Login detected: {username}")
                send_device_data(username)
                client.send(b"OK")
            
            client.close()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("=" * 50)
    print("🛡️  ZERO TRUST AGENT SERVICE")
    print("=" * 50)
    start_listener()
