import socket
import platform
import subprocess
import requests
import hashlib
import re
from datetime import datetime, timezone

BACKEND_URL = "http://127.0.0.1:8000/agent/heartbeat"

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "UNKNOWN"

def get_wifi_ssid():
    try:
        output = subprocess.check_output(
            "netsh wlan show interfaces", shell=True
        ).decode(errors="ignore")
        for line in output.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except:
        pass
    return "UNKNOWN"

def get_mac():
    try:
        output = subprocess.check_output(
            "getmac /v /fo list", shell=True
        ).decode(errors="ignore")

        match = re.search(
            r"(?:[0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}", output
        )
        return match.group(0).replace("-", ":") if match else "UNKNOWN"
    except:
        return "UNKNOWN"

def fingerprint(mac, hostname):
    raw = f"{mac}|{hostname}"
    return hashlib.sha256(raw.encode()).hexdigest()

def collect(username):
    host = socket.gethostname()
    mac = get_mac()
    return {
        "user": username,
        "ip_address": get_ip(),
        "mac_address": mac,
        "wifi_ssid": get_wifi_ssid(),
        "hostname": host,
        "os": platform.system(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fingerprint": fingerprint(mac, host)
    }

if __name__ == "__main__":
    user = input("Enter username: ").strip()
    payload = collect(user)
    res = requests.post(BACKEND_URL, json=payload)
    print(res.text)
