import socket
import platform
import uuid
import hashlib
import requests
import psutil
import subprocess
from datetime import datetime
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BACKEND = "http://localhost:8000"
PORT = 9999

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
        print(f"\n📡 Sending device data for {username}:")
        print(f"   MAC: {device_info['mac']}")
        print(f"   Hostname: {device_info['hostname']}")
        print(f"   WiFi: {device_info['wifi_ssid']}")
        print(f"   OS: {device_info['os']}")
        
        response = requests.post(f"{BACKEND}/device/register", json=device_info, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Device data sent successfully for {username}")
            return True
        else:
            print(f"✗ Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to send device data: {e}")
        return False

class AgentHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'user' in params:
            username = params['user'][0]
            print(f"\n🔐 Login detected: {username}")
            send_device_data(username)
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(400)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

if __name__ == "__main__":
    print("=" * 50)
    print("🛡️  ZERO TRUST AGENT SERVICE")
    print("=" * 50)
    print(f"🔒 Agent HTTP Server Running on port {PORT}")
    print(f"⚡ Waiting for login triggers...")
    
    server = HTTPServer(('localhost', PORT), AgentHandler)
    server.serve_forever()
