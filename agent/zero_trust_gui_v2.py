"""
Zero Trust Security Agent - Advanced GUI v3.0
Enterprise-grade security monitoring with modern interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import socket
import platform
import uuid
import hashlib
import requests
import psutil
from datetime import datetime
import time
import webbrowser
from collections import deque

BACKEND_URL = "http://localhost:8000"
CHECK_INTERVAL = 60  # 1 minute for demo

class ModernButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(relief='flat', cursor='hand2', borderwidth=0)

class ZeroTrustGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Trust Security Agent - Enterprise Edition")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0a0e27')
        self.root.resizable(True, True)
        
        self.username = None
        self.monitoring = False
        self.threat_count = 0
        self.scan_count = 0
        self.risk_score = 0
        self.cpu_history = deque([0]*20, maxlen=20)
        self.mem_history = deque([0]*20, maxlen=20)
        self.net_history = deque([0]*20, maxlen=20)
        
        # Animation state
        self.pulse_state = 0
        self.pulse_direction = 1
        
        self.create_modern_ui()
        self.start_animations()
        
    def create_modern_ui(self):
        # ===== HEADER BAR =====
        header = tk.Frame(self.root, bg='#0d1117', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo Section with Shield
        logo_frame = tk.Frame(header, bg='#0d1117')
        logo_frame.pack(side='left', padx=30, pady=15)
        
        # Animated Shield Icon
        self.shield_canvas = tk.Canvas(logo_frame, width=50, height=50, bg='#0d1117', 
                                      highlightthickness=0)
        self.shield_canvas.pack(side='left')
        self.draw_shield()
        
        # Title with modern styling
        title_container = tk.Frame(logo_frame, bg='#0d1117')
        title_container.pack(side='left', padx=15)
        
        tk.Label(title_container, text="ZERO TRUST", 
                font=('Segoe UI', 22, 'bold'), bg='#0d1117', 
                fg='#58a6ff').pack(anchor='w')
        tk.Label(title_container, text="Enterprise Security Agent v3.0", 
                font=('Segoe UI', 9), bg='#0d1117', 
                fg='#8b949e').pack(anchor='w')
        
        # Animated Status Indicator
        status_frame = tk.Frame(header, bg='#0d1117')
        status_frame.pack(side='right', padx=30)
        
        self.status_canvas = tk.Canvas(status_frame, width=120, height=50, 
                                      bg='#0d1117', highlightthickness=0)
        self.status_canvas.pack()
        self.status_text = "OFFLINE"
        self.status_color = '#f85149'
        
        # Main Container
        main = tk.Frame(self.root, bg='#0a0e27')
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # ===== LOGIN SCREEN =====
        self.login_frame = tk.Frame(main, bg='#0a0e27')
        self.login_frame.pack(expand=True)
        
        login_container = tk.Frame(self.login_frame, bg='#161b22', relief='flat')
        login_container.pack(pady=80)
        
        # Login header with icon
        login_header = tk.Frame(login_container, bg='#161b22')
        login_header.pack(pady=40, padx=60)
        
        tk.Label(login_header, text="🔐", font=('Arial', 48), 
                bg='#161b22').pack()
        tk.Label(login_header, text="SECURE AUTHENTICATION", 
                font=('Segoe UI', 20, 'bold'), bg='#161b22', 
                fg='#58a6ff').pack(pady=10)
        tk.Label(login_header, text="Enter your credentials to begin monitoring", 
                font=('Segoe UI', 10), bg='#161b22', 
                fg='#8b949e').pack()
        
        # Username input with modern styling
        input_frame = tk.Frame(login_container, bg='#161b22')
        input_frame.pack(pady=30, padx=60)
        
        tk.Label(input_frame, text="USERNAME", font=('Segoe UI', 9, 'bold'),
                bg='#161b22', fg='#8b949e').pack(anchor='w', pady=(0,8))
        
        entry_container = tk.Frame(input_frame, bg='#0d1117', relief='flat')
        entry_container.pack(fill='x', ipady=2)
        
        self.username_entry = tk.Entry(entry_container, font=('Segoe UI', 13), 
                                      bg='#0d1117', fg='#c9d1d9', 
                                      insertbackground='#58a6ff', relief='flat', 
                                      bd=0, width=30)
        self.username_entry.pack(padx=15, pady=12)
        self.username_entry.bind('<Return>', lambda e: self.start_monitoring())
        
        # Modern button
        btn_frame = tk.Frame(login_container, bg='#161b22')
        btn_frame.pack(pady=30, padx=60)
        
        self.start_btn = tk.Button(btn_frame, text="START MONITORING →",
                                   command=self.start_monitoring,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#238636', fg='#ffffff',
                                   activebackground='#2ea043',
                                   relief='flat', cursor='hand2',
                                   padx=40, pady=15)
        self.start_btn.pack()
        
        # Dashboard Screen
        self.dashboard_frame = tk.Frame(main, bg='#0a0e27')
        
        # Top Stats Row
        stats_row = tk.Frame(self.dashboard_frame, bg='#0a0e27')
        stats_row.pack(fill='x', pady=(0,20))
        
        self.create_stat_card(stats_row, "RISK SCORE", "0", "#ff4444", 0)
        self.create_stat_card(stats_row, "THREATS", "0", "#ff9500", 1)
        self.create_stat_card(stats_row, "SCANS", "0", "#00d4ff", 2)
        self.create_stat_card(stats_row, "STATUS", "SAFE", "#00ff88", 3)
        
        # Content Area
        content = tk.Frame(self.dashboard_frame, bg='#0a0e27')
        content.pack(fill='both', expand=True)
        
        # Left Panel - Device Info & Controls
        left_panel = tk.Frame(content, bg='#0a0e27', width=350)
        left_panel.pack(side='left', fill='both', padx=(0,10))
        left_panel.pack_propagate(False)
        
        # Device Info Card
        device_card = self.create_card(left_panel, "DEVICE INFORMATION")
        device_card.pack(fill='x', pady=(0,10))
        
        self.device_info = tk.Text(device_card, height=8, font=('Consolas', 9),
                                  bg='#0a0e27', fg='#00d4ff', bd=0, wrap='word')
        self.device_info.pack(padx=15, pady=10, fill='x')
        
        # Security Features Card
        features_card = self.create_card(left_panel, "SECURITY FEATURES")
        features_card.pack(fill='x', pady=(0,10))
        
        features = [
            "✓ Real-time File Monitoring",
            "✓ Network Traffic Analysis", 
            "✓ USB Device Detection",
            "✓ Login Behavior Analysis",
            "✓ Geolocation Tracking",
            "✓ Risk Score Calculation"
        ]
        
        for feature in features:
            tk.Label(features_card, text=feature, font=('Arial', 9),
                    bg='#1a1f3a', fg='#00ff88', anchor='w').pack(fill='x', padx=15, pady=2)
        
        tk.Label(features_card, text="", bg='#1a1f3a').pack(pady=5)
        
        # Control Buttons
        controls_card = self.create_card(left_panel, "CONTROLS")
        controls_card.pack(fill='x')
        
        btn_frame = tk.Frame(controls_card, bg='#1a1f3a')
        btn_frame.pack(pady=15, padx=15)
        
        ModernButton(btn_frame, text="📊 DASHBOARD", command=self.open_dashboard,
                    font=('Arial', 10, 'bold'), bg='#00d4ff', fg='#000000',
                    width=15, height=2).pack(pady=5, fill='x')
        
        ModernButton(btn_frame, text="🔄 REFRESH", command=self.manual_scan,
                    font=('Arial', 10, 'bold'), bg='#00ff88', fg='#000000',
                    width=15, height=2).pack(pady=5, fill='x')
        
        ModernButton(btn_frame, text="⛔ STOP", command=self.stop_monitoring,
                    font=('Arial', 10, 'bold'), bg='#ff4444', fg='#ffffff',
                    width=15, height=2).pack(pady=5, fill='x')
        
        # Right Panel - Activity Log
        right_panel = tk.Frame(content, bg='#0a0e27')
        right_panel.pack(side='right', fill='both', expand=True)
        
        log_card = self.create_card(right_panel, "ACTIVITY LOG")
        log_card.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_card, font=('Consolas', 9),
                                                  bg='#0a0e27', fg='#ffffff',
                                                  wrap='word', bd=0)
        self.log_text.pack(padx=15, pady=10, fill='both', expand=True)
        
        # Configure text tags for colored logs
        self.log_text.tag_config('info', foreground='#00d4ff')
        self.log_text.tag_config('success', foreground='#00ff88')
        self.log_text.tag_config('warning', foreground='#ff9500')
        self.log_text.tag_config('error', foreground='#ff4444')
        
    def create_card(self, parent, title):
        card = tk.Frame(parent, bg='#1a1f3a', relief='flat', bd=0)
        tk.Label(card, text=title, font=('Arial', 10, 'bold'),
                bg='#1a1f3a', fg='#00d4ff', anchor='w').pack(fill='x', padx=15, pady=(15,5))
        tk.Frame(card, bg='#00d4ff', height=2).pack(fill='x', padx=15)
        return card
    
    def draw_shield(self):
        """Draw animated shield icon"""
        self.shield_canvas.delete('all')
        points = [25, 5, 45, 15, 45, 35, 25, 45, 5, 35, 5, 15]
        self.shield_canvas.create_polygon(points, fill='#238636', outline='#3fb950', width=2)
        self.shield_canvas.create_line(15, 25, 22, 32, width=3, fill='#ffffff', capstyle='round')
        self.shield_canvas.create_line(22, 32, 35, 18, width=3, fill='#ffffff', capstyle='round')
    
    def draw_status_indicator(self):
        """Draw pulsing status indicator"""
        self.status_canvas.delete('all')
        x, y = 20, 25
        radius = 8 + self.pulse_state
        self.status_canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                      fill=self.status_color, outline='')
        self.status_canvas.create_text(50, 25, text=self.status_text,
                                      font=('Segoe UI', 11, 'bold'),
                                      fill=self.status_color, anchor='w')
    
    def start_animations(self):
        """Start background animations"""
        def animate():
            while True:
                self.pulse_state += self.pulse_direction * 0.5
                if self.pulse_state >= 3:
                    self.pulse_direction = -1
                elif self.pulse_state <= 0:
                    self.pulse_direction = 1
                
                try:
                    self.draw_status_indicator()
                except:
                    pass
                
                time.sleep(0.05)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def create_stat_card(self, parent, label, value, color, col):
        card = tk.Frame(parent, bg='#1a1f3a', relief='flat', bd=0)
        card.grid(row=0, column=col, padx=5, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        tk.Label(card, text=label, font=('Arial', 9),
                bg='#1a1f3a', fg='#888888').pack(pady=(15,5))
        
        value_label = tk.Label(card, text=value, font=('Arial', 24, 'bold'),
                              bg='#1a1f3a', fg=color)
        value_label.pack(pady=(0,15))
        
        if col == 0:
            self.risk_label = value_label
        elif col == 1:
            self.threat_label = value_label
        elif col == 2:
            self.scan_label = value_label
        elif col == 3:
            self.status_label = value_label
    
    def log(self, message, tag='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert('end', f"[{timestamp}] ", 'info')
        self.log_text.insert('end', f"{message}\n", tag)
        self.log_text.see('end')
        self.root.update()
    
    def start_monitoring(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return
        
        self.username = username
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(fill='both', expand=True)
        
        self.status_text = "ONLINE"
        self.status_color = '#3fb950'
        
        self.update_device_info()
        self.log("🚀 Zero Trust Agent v3.0 initialized", 'success')
        self.log(f"👤 User: {username}", 'info')
        
        self.monitoring = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        self.monitoring = False
        self.status_text = "OFFLINE"
        self.status_color = '#f85149'
        self.log("⛔ Monitoring stopped by user", 'warning')
    
    def open_dashboard(self):
        webbrowser.open('http://localhost:3000')
        self.log("🌐 Opening web dashboard...", 'info')
    
    def manual_scan(self):
        self.log("🔄 Manual scan initiated...", 'info')
        threading.Thread(target=self.perform_scan, daemon=True).start()
    
    def update_device_info(self):
        hostname = socket.gethostname()
        os_info = f"{platform.system()} {platform.release()}"
        ip = socket.gethostbyname(hostname)
        device_id = hashlib.sha256(f"{uuid.getnode()}-{hostname}".encode()).hexdigest()[:16]
        
        info = f"""
User:      {self.username}
Hostname:  {hostname}
OS:        {os_info}
IP:        {ip}
Device ID: {device_id}
Backend:   Connected
        """
        self.device_info.delete('1.0', 'end')
        self.device_info.insert('1.0', info.strip())
    
    def perform_scan(self):
        self.scan_count += 1
        self.scan_label.config(text=str(self.scan_count))
        
        threats = []
        
        # Check login time
        hour = datetime.now().hour
        if hour < 8 or hour > 18:
            threats.append(("⚠️ Odd-hour access detected", 'warning', 10))
        
        # Check weekend
        if datetime.now().weekday() >= 5:
            threats.append(("⚠️ Weekend access detected", 'warning', 5))
        
        # Check network
        try:
            connections = psutil.net_connections(kind='inet')
            external = sum(1 for c in connections if c.raddr and c.status == 'ESTABLISHED' 
                          and not c.raddr.ip.startswith(('10.', '192.168.', '172.')))
            if external > 10:
                threats.append((f"🌐 {external} external connections", 'warning', 15))
        except:
            pass
        
        # Check USB
        try:
            for partition in psutil.disk_partitions():
                if 'removable' in partition.opts.lower():
                    threats.append(("💾 USB device detected", 'error', 20))
                    break
        except:
            pass
        
        # Check CPU/Memory
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        if cpu > 80:
            threats.append((f"⚡ High CPU usage: {cpu}%", 'warning', 5))
        if mem > 80:
            threats.append((f"💾 High memory usage: {mem}%", 'warning', 5))
        
        # Update stats
        if threats:
            self.threat_count += len(threats)
            self.threat_label.config(text=str(self.threat_count))
            
            for msg, tag, risk in threats:
                self.log(msg, tag)
                self.risk_score += risk
            
            self.risk_label.config(text=str(min(self.risk_score, 100)))
            
            if self.risk_score > 50:
                self.status_label.config(text="DANGER", fg='#ff4444')
            elif self.risk_score > 30:
                self.status_label.config(text="WARNING", fg='#ff9500')
        else:
            self.log("✓ No threats detected", 'success')
    
    def monitor_loop(self):
        # Register device
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
            device_info = {
                "username": self.username,
                "device_id": hashlib.sha256(f"{uuid.getnode()}".encode()).hexdigest()[:16],
                "mac_address": mac,
                "hostname": socket.gethostname(),
                "os": f"{platform.system()} {platform.release()}",
                "wifi_ssid": "Unknown",
                "ip_address": socket.gethostbyname(socket.gethostname())
            }
            requests.post(f"{BACKEND_URL}/device/register", json=device_info, timeout=10)
            self.log("✓ Device registered with backend", 'success')
        except:
            self.log("⚠️ Running in offline mode", 'warning')
        
        while self.monitoring:
            self.perform_scan()
            for _ in range(CHECK_INTERVAL):
                if not self.monitoring:
                    break
                time.sleep(1)

def main():
    root = tk.Tk()
    app = ZeroTrustGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
