import sys
import psutil
from psutil import AccessDenied
import platform
import socket
import uuid
import requests
import time
import os
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
USERNAME = sys.argv[1] if len(sys.argv) > 1 else input("Enter your username: ")
INTERVAL = 60  # Send data every 60 seconds

def get_mac_address():
    """Get real MAC address"""
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    return mac

def get_wifi_ssid():
    """Get WiFi SSID (Windows)"""
    try:
        import subprocess
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
        for line in result.split('\n'):
            if 'SSID' in line and 'BSSID' not in line:
                return line.split(':')[1].strip()
    except:
        pass
    return "Unknown"

def get_device_info():
    """Collect device fingerprint"""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    return {
        "device_id": str(uuid.getnode()),
        "mac": get_mac_address(),
        "os": f"{platform.system()} {platform.release()}",
        "hostname": hostname,
        "ip": ip,
        "wifi": get_wifi_ssid()
    }

def monitor_file_access():
    """Monitor recent file access"""
    files = []
    sensitive_paths = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        "C:\\Windows\\System32"
    ]
    
    for path in sensitive_paths:
        if os.path.exists(path):
            try:
                for root, dirs, filenames in os.walk(path):
                    for filename in filenames[:5]:  # Limit to 5 files per folder
                        filepath = os.path.join(root, filename)
                        try:
                            stat = os.stat(filepath)
                            files.append({
                                "name": filename,
                                "path": filepath,
                                "action": "read",
                                "size": stat.st_size,
                                "sensitivity": "sensitive" if "System32" in filepath else "internal"
                            })
                        except:
                            pass
                    break  # Only check top level
            except:
                pass
    
    return files[:10]  # Return max 10 files

def monitor_network():
    """Monitor network connections (works without admin)"""
    connections = []
    try:
        # Try psutil first (requires admin on Windows)
        for conn in psutil.net_connections(kind='inet')[:10]:
            if conn.raddr:
                connections.append({
                    "type": "TCP" if conn.type == 1 else "UDP",
                    "ip": conn.raddr.ip,
                    "port": conn.raddr.port,
                    "protocol": "TCP" if conn.type == 1 else "UDP",
                    "external": not conn.raddr.ip.startswith(('192.168', '10.', '127.'))
                })
    except (PermissionError, AccessDenied):
        # Fallback: Use netstat (no admin needed)
        try:
            import subprocess
            result = subprocess.check_output(['netstat', '-n'], encoding='utf-8', errors='ignore')
            for line in result.split('\n'):
                if 'ESTABLISHED' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        remote = parts[2]
                        if ':' in remote:
                            ip, port = remote.rsplit(':', 1)
                            connections.append({
                                "type": "TCP",
                                "ip": ip,
                                "port": int(port),
                                "protocol": "TCP",
                                "external": not ip.startswith(('192.168', '10.', '127.'))
                            })
                            if len(connections) >= 10:
                                break
        except:
            pass
    except Exception:
        pass
    
    return connections

def send_telemetry():
    """Send telemetry to backend"""
    try:
        data = {
            "username": USERNAME,
            "device": get_device_info(),
            "files": monitor_file_access(),
            "network": monitor_network()
        }
        
        response = requests.post(f"{BACKEND_URL}/agent/telemetry", json=data, timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] OK Telemetry sent successfully")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] FAIL: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("ZERO TRUST AGENT - DEVICE MONITORING")
    print("=" * 60)
    print(f"User: {USERNAME}")
    print(f"Backend: {BACKEND_URL}")
    print(f"Interval: {INTERVAL}s")
    print(f"MAC: {get_mac_address()}")
    print(f"WiFi: {get_wifi_ssid()}")
    print(f"Hostname: {socket.gethostname()}")
    print("=" * 60)
    print("Agent started. Press Ctrl+C to stop.\n")
    
    while True:
        send_telemetry()
        time.sleep(INTERVAL)
