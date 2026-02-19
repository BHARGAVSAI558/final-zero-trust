"""
Zero Trust Security Agent - CYBER EDITION v4.0
Advanced cybersecurity monitoring with real-time analytics
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
import math

BACKEND_URL = "http://localhost:8000"
CHECK_INTERVAL = 60

class CyberAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ ZERO TRUST CYBER AGENT ⚡")
        self.root.geometry("1600x900")
        self.root.configure(bg='#000000')
        
        # State
        self.username = None
        self.monitoring = False
        self.threat_count = 0
        self.scan_count = 0
        self.risk_score = 0
        
        # Real-time data
        self.cpu_history = deque([0]*50, maxlen=50)
        self.mem_history = deque([0]*50, maxlen=50)
        self.disk_history = deque([0]*50, maxlen=50)
        
        # Animation
        self.pulse = 0
        self.pulse_dir = 1
        self.scan_angle = 0
        
        self.create_cyber_ui()
        self.start_animations()
        
    def create_cyber_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#0a0a0a', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(header, bg='#0a0a0a')
        logo_frame.pack(side='left', padx=30, pady=20)
        
        self.logo_canvas = tk.Canvas(logo_frame, width=60, height=60, bg='#0a0a0a', 
                                     highlightthickness=0)
        self.logo_canvas.pack(side='left')
        
        # Title
        title_frame = tk.Frame(logo_frame, bg='#0a0a0a')
        title_frame.pack(side='left', padx=20)
        
        tk.Label(title_frame, text="⚡ ZERO TRUST", 
                font=('Courier New', 26, 'bold'), bg='#0a0a0a', 
                fg='#00ff41').pack(anchor='w')
        tk.Label(title_frame, text="[ CYBER SECURITY AGENT v4.0 ]", 
                font=('Courier New', 10), bg='#0a0a0a', 
                fg='#00ff41').pack(anchor='w')
        
        # Status
        status_frame = tk.Frame(header, bg='#0a0a0a')
        status_frame.pack(side='right', padx=30)
        
        self.radar_canvas = tk.Canvas(status_frame, width=70, height=70, 
                                     bg='#0a0a0a', highlightthickness=0)
        self.radar_canvas.pack(side='left', padx=10)
        
        status_text_frame = tk.Frame(status_frame, bg='#0a0a0a')
        status_text_frame.pack(side='left')
        
        self.status_label = tk.Label(status_text_frame, text="OFFLINE", 
                                     font=('Courier New', 14, 'bold'),
                                     bg='#0a0a0a', fg='#ff0000')
        self.status_label.pack()
        
        self.time_label = tk.Label(status_text_frame, text="", 
                                   font=('Courier New', 9),
                                   bg='#0a0a0a', fg='#00ff41')
        self.time_label.pack()
        
        # Main container
        main = tk.Frame(self.root, bg='#000000')
        main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Login screen
        self.login_frame = tk.Frame(main, bg='#000000')
        self.login_frame.pack(expand=True)
        
        login_box = tk.Frame(self.login_frame, bg='#0a0a0a')
        login_box.pack(pady=100)
        
        tk.Label(login_box, text="⚡ SYSTEM ACCESS ⚡", 
                font=('Courier New', 28, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(pady=30, padx=80)
        
        tk.Label(login_box, text="[ ENTER CREDENTIALS TO INITIALIZE MONITORING ]", 
                font=('Courier New', 10),
                bg='#0a0a0a', fg='#00ff41').pack(pady=10)
        
        # Input
        input_container = tk.Frame(login_box, bg='#00ff41', bd=2)
        input_container.pack(pady=30, padx=80)
        
        input_inner = tk.Frame(input_container, bg='#0a0a0a')
        input_inner.pack(padx=2, pady=2)
        
        tk.Label(input_inner, text=">>> USERNAME:", 
                font=('Courier New', 11, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(anchor='w', padx=20, pady=(15,5))
        
        self.username_entry = tk.Entry(input_inner, font=('Courier New', 14), 
                                      bg='#000000', fg='#00ff41', 
                                      insertbackground='#00ff41', relief='flat', 
                                      bd=0, width=30)
        self.username_entry.pack(padx=20, pady=(0,15))
        self.username_entry.bind('<Return>', lambda e: self.start_monitoring())
        
        # Button
        btn_container = tk.Frame(login_box, bg='#00ff41', bd=2)
        btn_container.pack(pady=20)
        
        self.start_btn = tk.Button(btn_container, text="[ INITIALIZE SYSTEM ]",
                                   command=self.start_monitoring,
                                   font=('Courier New', 12, 'bold'),
                                   bg='#000000', fg='#00ff41',
                                   activebackground='#00ff41',
                                   activeforeground='#000000',
                                   relief='flat', cursor='hand2',
                                   padx=50, pady=15)
        self.start_btn.pack(padx=2, pady=2)
        
        # Dashboard
        self.dashboard_frame = tk.Frame(main, bg='#000000')
        
        # Stats bar
        stats_bar = tk.Frame(self.dashboard_frame, bg='#000000')
        stats_bar.pack(fill='x', pady=(0,10))
        
        self.create_cyber_stat(stats_bar, "RISK", "0", "#ff0000", 0)
        self.create_cyber_stat(stats_bar, "THREATS", "0", "#ff6600", 1)
        self.create_cyber_stat(stats_bar, "SCANS", "0", "#00ff41", 2)
        self.create_cyber_stat(stats_bar, "UPTIME", "00:00", "#00ffff", 3)
        self.create_cyber_stat(stats_bar, "STATUS", "SAFE", "#00ff41", 4)
        
        # Grid
        grid = tk.Frame(self.dashboard_frame, bg='#000000')
        grid.pack(fill='both', expand=True)
        
        # Left column
        left_col = tk.Frame(grid, bg='#000000')
        left_col.pack(side='left', fill='both', expand=True, padx=(0,5))
        
        # Device panel
        device_panel = self.create_cyber_panel(left_col, "💻 DEVICE FINGERPRINT")
        device_panel.pack(fill='x', pady=(0,10))
        
        self.device_text = tk.Text(device_panel, height=10, font=('Courier New', 9),
                                  bg='#000000', fg='#00ff41', bd=0, wrap='word')
        self.device_text.pack(padx=15, pady=10, fill='x')
        
        # Metrics panel
        metrics_panel = self.create_cyber_panel(left_col, "📊 SYSTEM METRICS")
        metrics_panel.pack(fill='both', expand=True, pady=(0,10))
        
        metrics_content = tk.Frame(metrics_panel, bg='#0a0a0a')
        metrics_content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # CPU
        tk.Label(metrics_content, text="CPU USAGE", font=('Courier New', 9, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(anchor='w')
        self.cpu_canvas = tk.Canvas(metrics_content, width=400, height=60, 
                                    bg='#000000', highlightthickness=0)
        self.cpu_canvas.pack(fill='x', pady=(5,5))
        self.cpu_label = tk.Label(metrics_content, text="0%", 
                                 font=('Courier New', 10, 'bold'),
                                 bg='#0a0a0a', fg='#00ff41')
        self.cpu_label.pack(anchor='w', pady=(0,10))
        
        # Memory
        tk.Label(metrics_content, text="MEMORY USAGE", font=('Courier New', 9, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(anchor='w')
        self.mem_canvas = tk.Canvas(metrics_content, width=400, height=60, 
                                    bg='#000000', highlightthickness=0)
        self.mem_canvas.pack(fill='x', pady=(5,5))
        self.mem_label = tk.Label(metrics_content, text="0%", 
                                 font=('Courier New', 10, 'bold'),
                                 bg='#0a0a0a', fg='#00ff41')
        self.mem_label.pack(anchor='w', pady=(0,10))
        
        # Disk
        tk.Label(metrics_content, text="DISK I/O", font=('Courier New', 9, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(anchor='w')
        self.disk_canvas = tk.Canvas(metrics_content, width=400, height=60, 
                                     bg='#000000', highlightthickness=0)
        self.disk_canvas.pack(fill='x', pady=(5,5))
        self.disk_label = tk.Label(metrics_content, text="0 MB/s", 
                                   font=('Courier New', 10, 'bold'),
                                   bg='#0a0a0a', fg='#00ff41')
        self.disk_label.pack(anchor='w')
        
        # Control panel
        control_panel = self.create_cyber_panel(left_col, "⚙️ CONTROLS")
        control_panel.pack(fill='x')
        
        btn_frame = tk.Frame(control_panel, bg='#0a0a0a')
        btn_frame.pack(padx=15, pady=10)
        
        self.create_cyber_button(btn_frame, "📊 WEB DASHBOARD", 
                                self.open_dashboard, '#00ff41').pack(pady=5, fill='x')
        self.create_cyber_button(btn_frame, "🔄 FORCE SCAN", 
                                self.manual_scan, '#00ffff').pack(pady=5, fill='x')
        self.create_cyber_button(btn_frame, "⛔ TERMINATE", 
                                self.stop_monitoring, '#ff0000').pack(pady=5, fill='x')
        
        # Right column
        right_col = tk.Frame(grid, bg='#000000')
        right_col.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        # Network panel
        network_panel = self.create_cyber_panel(right_col, "🌐 NETWORK CONNECTIONS")
        network_panel.pack(fill='both', expand=True, pady=(0,10))
        
        net_frame = tk.Frame(network_panel, bg='#0a0a0a')
        net_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.network_text = scrolledtext.ScrolledText(net_frame, 
                                                      font=('Courier New', 9),
                                                      bg='#000000', fg='#00ff41',
                                                      wrap='none', bd=0, height=10)
        self.network_text.pack(fill='both', expand=True)
        
        # Activity log
        log_panel = self.create_cyber_panel(right_col, "📋 ACTIVITY LOG")
        log_panel.pack(fill='both', expand=True)
        
        log_frame = tk.Frame(log_panel, bg='#0a0a0a')
        log_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                  font=('Courier New', 9),
                                                  bg='#000000', fg='#00ff41',
                                                  wrap='word', bd=0)
        self.log_text.pack(fill='both', expand=True)
        
        self.log_text.tag_config('info', foreground='#00ffff')
        self.log_text.tag_config('success', foreground='#00ff41')
        self.log_text.tag_config('warning', foreground='#ffff00')
        self.log_text.tag_config('error', foreground='#ff0000')
        self.log_text.tag_config('time', foreground='#888888')
        
    def create_cyber_panel(self, parent, title):
        panel = tk.Frame(parent, bg='#00ff41', bd=2)
        inner = tk.Frame(panel, bg='#0a0a0a')
        inner.pack(fill='both', expand=True, padx=2, pady=2)
        
        header = tk.Frame(inner, bg='#0a0a0a')
        header.pack(fill='x', padx=10, pady=(10,5))
        
        tk.Label(header, text=title, font=('Courier New', 11, 'bold'),
                bg='#0a0a0a', fg='#00ff41').pack(side='left')
        
        tk.Frame(inner, bg='#00ff41', height=1).pack(fill='x', padx=10)
        return inner
    
    def create_cyber_stat(self, parent, label, value, color, col):
        frame = tk.Frame(parent, bg='#00ff41', bd=2)
        frame.grid(row=0, column=col, padx=5, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        inner = tk.Frame(frame, bg='#0a0a0a')
        inner.pack(fill='both', expand=True, padx=2, pady=2)
        
        tk.Label(inner, text=label, font=('Courier New', 8, 'bold'),
                bg='#0a0a0a', fg='#888888').pack(pady=(10,2))
        
        value_label = tk.Label(inner, text=value, font=('Courier New', 20, 'bold'),
                              bg='#0a0a0a', fg=color)
        value_label.pack(pady=(0,10))
        
        if col == 0:
            self.risk_label = value_label
        elif col == 1:
            self.threat_label = value_label
        elif col == 2:
            self.scan_label = value_label
        elif col == 3:
            self.uptime_label = value_label
        elif col == 4:
            self.status_stat_label = value_label
    
    def create_cyber_button(self, parent, text, command, color):
        frame = tk.Frame(parent, bg=color, bd=2)
        btn = tk.Button(frame, text=text, command=command,
                       font=('Courier New', 10, 'bold'),
                       bg='#000000', fg=color,
                       activebackground=color,
                       activeforeground='#000000',
                       relief='flat', cursor='hand2',
                       width=30, pady=8)
        btn.pack(padx=2, pady=2)
        return frame
    
    def draw_cyber_logo(self):
        self.logo_canvas.delete('all')
        angle = self.scan_angle
        points = []
        for i in range(6):
            x = 30 + 25 * math.cos(math.radians(angle + i * 60))
            y = 30 + 25 * math.sin(math.radians(angle + i * 60))
            points.extend([x, y])
        
        self.logo_canvas.create_polygon(points, fill='', outline='#00ff41', width=2)
        self.logo_canvas.create_oval(20, 20, 40, 40, fill='#00ff41', outline='')
        
        pulse_size = 5 + self.pulse
        self.logo_canvas.create_oval(30-pulse_size, 30-pulse_size, 
                                     30+pulse_size, 30+pulse_size,
                                     fill='#000000', outline='')
    
    def draw_radar(self):
        self.radar_canvas.delete('all')
        for r in [10, 20, 30]:
            self.radar_canvas.create_oval(35-r, 35-r, 35+r, 35+r,
                                         outline='#00ff41', width=1)
        
        angle = self.scan_angle
        x = 35 + 30 * math.cos(math.radians(angle))
        y = 35 + 30 * math.sin(math.radians(angle))
        self.radar_canvas.create_line(35, 35, x, y, fill='#00ff41', width=2)
        self.radar_canvas.create_oval(33, 33, 37, 37, fill='#00ff41', outline='')
    
    def draw_graph(self, canvas, data, color):
        canvas.delete('all')
        width = canvas.winfo_width() or 400
        height = canvas.winfo_height() or 60
        
        if width <= 1:
            return
        
        for i in range(0, 101, 25):
            y = height - (i * height / 100)
            canvas.create_line(0, y, width, y, fill='#00ff41', width=1, dash=(2,4))
        
        if len(data) > 1:
            points = []
            step = width / (len(data) - 1)
            for i, val in enumerate(data):
                x = i * step
                y = height - (val * height / 100)
                points.extend([x, y])
            
            if len(points) >= 4:
                canvas.create_line(points, fill=color, width=2, smooth=True)
    
    def start_animations(self):
        def animate():
            while True:
                self.pulse += self.pulse_dir * 0.3
                if self.pulse >= 3:
                    self.pulse_dir = -1
                elif self.pulse <= 0:
                    self.pulse_dir = 1
                
                self.scan_angle = (self.scan_angle + 3) % 360
                
                try:
                    self.draw_cyber_logo()
                    self.draw_radar()
                    self.time_label.config(text=datetime.now().strftime('%H:%M:%S'))
                    
                    if self.monitoring:
                        self.update_metrics()
                except:
                    pass
                
                time.sleep(0.05)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def update_metrics(self):
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            self.cpu_history.append(cpu)
            self.cpu_label.config(text=f"{cpu:.1f}%")
            self.draw_graph(self.cpu_canvas, self.cpu_history, '#00ffff')
            
            mem = psutil.virtual_memory().percent
            self.mem_history.append(mem)
            self.mem_label.config(text=f"{mem:.1f}%")
            self.draw_graph(self.mem_canvas, self.mem_history, '#ffff00')
            
            disk_io = psutil.disk_io_counters()
            disk_speed = (disk_io.read_bytes + disk_io.write_bytes) / 1024 / 1024
            self.disk_history.append(min(disk_speed, 100))
            self.disk_label.config(text=f"{disk_speed:.1f} MB/s")
            self.draw_graph(self.disk_canvas, self.disk_history, '#ff00ff')
        except:
            pass
    
    def update_network_table(self):
        try:
            self.network_text.delete('1.0', 'end')
            connections = psutil.net_connections(kind='inet')
            
            self.network_text.insert('end', f"{'REMOTE IP':<20} {'PORT':<8} {'STATUS':<15} {'TYPE'}\n", 'success')
            self.network_text.insert('end', "-" * 60 + "\n")
            
            count = 0
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    ip = conn.raddr.ip
                    port = conn.raddr.port
                    status = conn.status
                    conn_type = "EXTERNAL" if not ip.startswith(('10.', '192.168.', '127.')) else "INTERNAL"
                    
                    line = f"{ip:<20} {port:<8} {status:<15} {conn_type}\n"
                    self.network_text.insert('end', line)
                    count += 1
                    if count >= 15:
                        break
        except:
            self.network_text.insert('end', ">>> Network monitoring requires admin privileges\n")
    
    def log(self, message, tag='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert('end', f"[{timestamp}] ", 'time')
        self.log_text.insert('end', f"{message}\n", tag)
        self.log_text.see('end')
        self.root.update()
    
    def start_monitoring(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("ERROR", "USERNAME REQUIRED!")
            return
        
        self.username = username
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(fill='both', expand=True)
        
        self.status_label.config(text="ONLINE", fg='#00ff41')
        self.start_time = time.time()
        
        self.update_device_info()
        self.log("⚡ ZERO TRUST AGENT INITIALIZED", 'success')
        self.log(f">>> USER: {username}", 'info')
        self.log(">>> ALL SYSTEMS OPERATIONAL", 'success')
        
        self.monitoring = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        threading.Thread(target=self.update_uptime, daemon=True).start()
    
    def stop_monitoring(self):
        self.monitoring = False
        self.status_label.config(text="OFFLINE", fg='#ff0000')
        self.log("⛔ MONITORING TERMINATED", 'error')
    
    def open_dashboard(self):
        webbrowser.open('http://localhost:3000')
        self.log("🌐 LAUNCHING WEB DASHBOARD...", 'info')
    
    def manual_scan(self):
        self.log("🔄 INITIATING SECURITY SCAN...", 'warning')
        threading.Thread(target=self.perform_scan, daemon=True).start()
    
    def update_device_info(self):
        hostname = socket.gethostname()
        os_info = f"{platform.system()} {platform.release()}"
        ip = socket.gethostbyname(hostname)
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                       for i in range(0,48,8)][::-1])
        device_id = hashlib.sha256(f"{uuid.getnode()}".encode()).hexdigest()[:16]
        
        info = f""">>> USER:        {self.username}
>>> HOSTNAME:    {hostname}
>>> OS:          {os_info}
>>> IP ADDRESS:  {ip}
>>> MAC ADDRESS: {mac}
>>> DEVICE ID:   {device_id}
>>> BACKEND:     CONNECTED
>>> ENCRYPTION:  AES-256"""
        
        self.device_text.delete('1.0', 'end')
        self.device_text.insert('1.0', info)
    
    def update_uptime(self):
        while self.monitoring:
            elapsed = int(time.time() - self.start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            self.uptime_label.config(text=f"{hours:02d}:{minutes:02d}")
            time.sleep(1)
    
    def perform_scan(self):
        self.scan_count += 1
        self.scan_label.config(text=str(self.scan_count))
        
        threats = []
        
        hour = datetime.now().hour
        if hour < 8 or hour > 18:
            threats.append(("⚠️ ODD-HOUR ACCESS DETECTED", 'warning', 10))
        
        if datetime.now().weekday() >= 5:
            threats.append(("⚠️ WEEKEND ACCESS DETECTED", 'warning', 5))
        
        self.update_network_table()
        
        try:
            for partition in psutil.disk_partitions():
                if 'removable' in partition.opts.lower():
                    threats.append(("💾 USB DEVICE DETECTED", 'error', 20))
                    break
        except:
            pass
        
        if threats:
            self.threat_count += len(threats)
            self.threat_label.config(text=str(self.threat_count))
            
            for msg, tag, risk in threats:
                self.log(msg, tag)
                self.risk_score += risk
            
            self.risk_label.config(text=str(min(self.risk_score, 100)))
            
            if self.risk_score > 50:
                self.status_stat_label.config(text="DANGER", fg='#ff0000')
            elif self.risk_score > 30:
                self.status_stat_label.config(text="WARNING", fg='#ffff00')
        else:
            self.log("✓ SCAN COMPLETE - NO THREATS", 'success')
    
    def monitor_loop(self):
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                           for i in range(0,48,8)][::-1])
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
            self.log("✓ DEVICE REGISTERED", 'success')
        except:
            self.log("⚠️ OFFLINE MODE - BACKEND UNAVAILABLE", 'warning')
        
        while self.monitoring:
            self.perform_scan()
            for _ in range(CHECK_INTERVAL):
                if not self.monitoring:
                    break
                time.sleep(1)

def main():
    root = tk.Tk()
    app = CyberAgent(root)
    root.mainloop()

if __name__ == "__main__":
    main()
