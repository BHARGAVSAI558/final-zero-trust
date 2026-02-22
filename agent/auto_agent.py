import socket
import platform
import uuid
import hashlib
import requests
import subprocess
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import psutil

BACKEND = "http://localhost:8000"
CURRENT_USER = None
LAST_CONNECTIONS = set()
LAST_RESET_TIME = time.time()

def get_wifi_ssid():
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8', errors='ignore')
        for line in result.split('\n'):
            if 'SSID' in line and 'BSSID' not in line:
                return line.split(':')[1].strip()
    except:
        pass
    return "N/A"

def get_real_mac_address():
    try:
        result = subprocess.check_output(['getmac', '/fo', 'csv', '/nh'], encoding='utf-8', errors='ignore')
        lines = result.strip().split('\n')
        for line in lines:
            if line and 'disconnected' not in line.lower():
                mac = line.split(',')[0].strip('"').strip()
                if mac and mac != 'N/A' and '-' in mac:
                    return mac.replace('-', ':').lower()
    except:
        pass
    return ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,48,8)][::-1])

def get_device_info():
    # Get local IP from active network interface
    local_ip = socket.gethostbyname(socket.gethostname())
    
    # Try to get the actual Wi-Fi IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        pass
    
    return {
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "ip": local_ip,
        "mac": get_real_mac_address(),
        "device_id": hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16],
        "wifi_ssid": get_wifi_ssid()
    }

def get_domain_name(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
        return domain
    except:
        # IP-based service detection
        if ip.startswith('142.250.') or ip.startswith('142.251.') or ip.startswith('216.239.') or ip.startswith('172.217.'):
            return 'google.com'
        elif ip.startswith('35.223.') or ip.startswith('35.186.'):
            return 'youtube.com'
        elif ip.startswith('104.18.') or ip.startswith('104.16.'):
            return 'cloudflare.com'
        elif ip.startswith('151.101.'):
            return 'fastly.net'
        elif ip.startswith('13.107.') or ip.startswith('20.42.') or ip.startswith('40.100.') or ip.startswith('40.104.'):
            return 'microsoft.com'
        elif ip.startswith('54.') or ip.startswith('52.') or ip.startswith('3.'):
            return 'amazonaws.com'
        elif ip.startswith('157.240.') or ip.startswith('31.13.'):
            return 'facebook.com'
        elif ip.startswith('108.174.'):
            return 'linkedin.com'
        else:
            return ip

def get_network_connections():
    global LAST_CONNECTIONS, LAST_RESET_TIME
    connections = []
    
    # Reset tracking every 30 seconds to allow re-logging
    if time.time() - LAST_RESET_TIME > 30:
        LAST_CONNECTIONS.clear()
        LAST_RESET_TIME = time.time()
    
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr:
                remote_ip = conn.raddr.ip
                remote_port = conn.raddr.port
                
                if remote_ip.startswith('127.') or remote_ip.startswith('192.168.') or remote_ip.startswith('10.'):
                    continue
                
                protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                is_external = not (remote_ip.startswith('192.168.') or remote_ip.startswith('10.') or remote_ip.startswith('172.'))
                domain = get_domain_name(remote_ip)
                
                conn_key = f"{remote_ip}:{remote_port}"
                if conn_key not in LAST_CONNECTIONS:
                    connections.append({
                        'remote_ip': remote_ip,
                        'remote_port': remote_port,
                        'protocol': protocol,
                        'external': is_external,
                        'domain': domain
                    })
                    LAST_CONNECTIONS.add(conn_key)
    except:
        pass
    return connections

def send_network_activity(username, connections):
    if not connections:
        print("  ℹ No new network connections")
        return
    print(f"  📡 Sending {len(connections)} network connections...")
    
    # Send all connections in one batch
    try:
        batch_data = [{
            'username': username,
            'remote_ip': conn['remote_ip'],
            'remote_port': conn['remote_port'],
            'protocol': conn['protocol'],
            'is_external': conn['external'],
            'domain': conn.get('domain', 'Unknown')
        } for conn in connections]
        
        response = requests.post(f"{BACKEND}/track/network/batch", json={'connections': batch_data}, timeout=5)
        if response.status_code == 200:
            print(f"  ✓ Logged {len(connections)} network connections")
        else:
            print(f"  ✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Network logging failed: {e}")

def update_user(username):
    try:
        device_info = get_device_info()
        data = {**device_info, "username": username}
        response = requests.post(f"{BACKEND}/device/register", json=data, timeout=5)
        if response.status_code == 200:
            print(f"✓ Updated {username}: MAC={device_info['mac']}, Host={device_info['hostname']}")
            connections = get_network_connections()
            if connections:
                send_network_activity(username, connections)
            return True
    except Exception as e:
        print(f"✗ Update failed: {e}")
    return False

class AgentHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_POST(self):
        global CURRENT_USER
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            username = data.get('username')
            
            if username:
                CURRENT_USER = username
                print(f"\n🔐 Login detected: {username}")
                update_user(username)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status":"OK"}')
                return
        
        self.send_response(400)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

def monitor_loop():
    global CURRENT_USER
    while True:
        if CURRENT_USER:
            update_user(CURRENT_USER)
        time.sleep(3)

if __name__ == "__main__":
    print("=" * 60)
    print("🛡️  ZERO TRUST AUTO-AGENT")
    print("=" * 60)
    
    device_info = get_device_info()
    print(f"\n📊 Device Information:")
    print(f"   MAC Address: {device_info['mac']}")
    print(f"   Hostname: {device_info['hostname']}")
    print(f"   OS: {device_info['os']}")
    print(f"   WiFi: {device_info['wifi_ssid']}")
    print(f"\n🔒 HTTP Server on port 8888")
    print(f"⚡ Monitoring device + network activity...\n")
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()
    
    # Start HTTP server
    server = HTTPServer(('localhost', 8888), AgentHandler)
    server.serve_forever()
