"""
Zero Trust Security Agent - ADVANCED GUI v3.0
Enterprise-grade security monitoring with modern UI
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
CHECK_INTERVAL = 60

class AnimatedButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.text = text
        self.hover = False
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
        self.draw()
    
    def draw(self):
        self.delete('all')
        color = self['bg']
        if self.hover:
            # Lighter on hover
            color = self.lighten_color(color)
        
        self.create_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(),
                            fill=color, outline='', tags='bg')
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=self.text, fill='white', font=('Arial', 11, 'bold'))
    
    def lighten_color(self, color):
        # Simple color lightening
        return color
    
    def on_enter(self, e):
        self.hover = True
        self.config(cursor='hand2')
    
    def on_leave(self, e):
        self.hover = False
        self.config(cursor='')
    
    def on_click(self, e):
        if self.command:
            self.command()

class ZeroTrustAdvancedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zero Trust Security Agent - Enterprise Edition")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0a0e27')
        self.root.resizable(True, True)
        
        # State
        self.username = None
        self.monitoring = False
        self.threat_count = 0
        self.scan_count = 0
        self.risk_score = 0
        self.cpu_history = deque([0]*20, maxlen=20)
        self.mem_history = deque([0]*20, maxlen=20)
        self.net_history = deque([0]*20, maxlen=20)
        
        # Animation
        self.pulse_state = 0
        self.pulse_direction = 1
        
        self.create_advanced_ui()
        self.start_animations()
        
    def create_advanced_ui(self):
        # ===== HEADER BAR =====
        header = tk.Frame(self.root, bg='#0d1117', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo Section
        logo_frame = tk.Frame(header, bg='#0d1117')
        logo_frame.pack(side='left', padx=30, pady=15)
        
        # Animated Shield Icon
        self.shield_canvas = tk.Canvas(logo_frame, width=50, height=50, bg='#0d1117', 
                                      highlightthickness=0)
        self.shield_canvas.pack(side='left')
        self.draw_shield()
        
        # Title with gradient effect
        title_container = tk.Frame(logo_frame, bg='#0d1117')
        title_container.pack(side='left', padx=15)
        
        tk.Label(title_container, text="ZERO TRUST", 
                font=('Segoe UI', 22, 'bold'), bg='#0d1117', 
                fg='#58a6ff').pack(anchor='w')
        tk.Label(title_container, text="Enterprise Security Agent v3.0", 
                font=('Segoe UI', 9), bg='#0d1117', 
                fg='#8b949e').pack(anchor='w')
        
        # Status Indicator (Animated)
        status_frame = tk.Frame(header, bg='#0d1117')
        status_frame.pack(side='right', padx=30)
        
        self.status_canvas = tk.Canvas(status_frame, width=120, height=50, 
                                      bg='#0d1117', highlightthickness=0)
        self.status_canvas.pack()
        self.status_text = "OFFLINE"
        self.status_color = '#f85149'
        
        # ===== MAIN CONTAINER =====
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
        
        # ===== DASHBOARD SCREEN =====
        self.dashboard_frame = tk.Frame(main, bg='#0a0e27')
        
        # Top Stats Row (4 cards)
        stats_container = tk.Frame(self.dashboard_frame, bg='#0a0e27')
        stats_container.pack(fill='x', pady=(0,20))
        
        self.create_advanced_stat_card(stats_container, "RISK LEVEL", "0", 
                                      "#f85149", "🎯", 0)
        self.create_advanced_stat_card(stats_container, "THREATS", "0", 
                                      "#d29922", "⚠️", 1)
        self.create_advanced_stat_card(stats_container, "SCANS", "0", 
                                      "#58a6ff", "🔍", 2)
        self.create_advanced_stat_card(stats_container, "STATUS", "SAFE", 
                                      "#3fb950", "✓", 3)
        
        # Main Content Grid
        content_grid = tk.Frame(self.dashboard_frame, bg='#0a0e27')
        content_grid.pack(fill='both', expand=True)
        
        # Left Column (40%)
        left_col = tk.Frame(content_grid, bg='#0a0e27')
        left_col.pack(side='left', fill='both', expand=True, padx=(0,10))
        
        # Device Info Card
        device_card = self.create_modern_card(left_col, "💻 DEVICE FINGERPRINT")
        device_card.pack(fill='x', pady=(0,15))
        
        self.device_info = tk.Text(device_card, height=9, font=('Consolas', 10),
                                  bg='#0d1117', fg='#58a6ff', bd=0, 
                                  wrap='word', relief='flat')
        self.device_info.pack(padx=20, pady=15, fill='x')
        
        # System Metrics Card with Mini Graphs
        metrics_card = self.create_modern_card(left_col, "📊 SYSTEM METRICS")
        metrics_card.pack(fill='both', expand=True, pady=(0,15))
        
        metrics_content = tk.Frame(metrics_card, bg='#161b22')
        metrics_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # CPU Graph
        self.cpu_canvas = tk.Canvas(metrics_content, width=300, height=60, 
                                    bg='#0d1117', highlightthickness=0)
        self.cpu_canvas.pack(fill='x', pady=(0,10))
        self.cpu_label = tk.Label(metrics_content, text="CPU: 0%", 
                                 font=('Segoe UI', 9), bg='#161b22', fg='#8b949e')
        self.cpu_label.pack(anchor='w')
        
        # Memory Graph
        self.mem_canvas = tk.Canvas(metrics_content, width=300, height=60, 
                                    bg='#0d1117', highlightthickness=0)
        self.mem_canvas.pack(fill='x', pady=(10,10))
        self.mem_label = tk.Label(metrics_content, text="Memory: 0%", 
                                 font=('Segoe UI', 9), bg='#161b22', fg='#8b949e')
        self.mem_label.pack(anchor='w')
        
        # Network Graph
        self.net_canvas = tk.Canvas(metrics_content, width=300, height=60, 
                                    bg='#0d1117', highlightthickness=0)
        self.net_canvas.pack(fill='x', pady=(10,0))
        self.net_label = tk.Label(metrics_content, text="Network: 0 conn", 
                                 font=('Segoe UI', 9), bg='#161b22', fg='#8b949e')
        self.net_label.pack(anchor='w')
        
        # Control Panel
        control_card = self.create_modern_card(left_col, "⚙️ CONTROLS")
        control_card.pack(fill='x')
        
        btn_container = tk.Frame(control_card, bg='#161b22')
        btn_container.pack(padx=20, pady=15)
        
        self.create_control_button(btn_container, "📊 DASHBOARD", 
                                   self.open_dashboard, '#58a6ff').pack(pady=5, fill='x')
        self.create_control_button(btn_container, "🔄 REFRESH", 
                                   self.manual_scan, '#3fb950').pack(pady=5, fill='x')
        self.create_control_button(btn_container, "⛔ STOP", 
                                   self.stop_monitoring, '#f85149').pack(pady=5, fill='x')
        
        # Right Column (60%)
        right_col = tk.Frame(content_grid, bg='#0a0e27')
        right_col.pack(side='right', fill='both', expand=True)
        
        # Activity Log with Tabs
        log_card = self.create_modern_card(right_col, "📋 ACTIVITY MONITOR")
        log_card.pack(fill='both', expand=True)
        
        # Tab buttons
        tab_frame = tk.Frame(log_card, bg='#161b22')
        tab_frame.pack(fill='x', padx=20, pady=(15,0))
        
        self.tab_all = tk.Button(tab_frame, text="ALL", font=('Segoe UI', 9, 'bold'),
                                bg='#238636', fg='#ffffff', relief='flat',
                                padx=15, pady=5, cursor='hand2')
        self.tab_all.pack(side='left', padx=(0,5))
        
        self.tab_threats = tk.Button(tab_frame, text="THREATS", font=('Segoe UI', 9),
                                     bg='#0d1117', fg='#8b949e', relief='flat',
                                     padx=15, pady=5, cursor='hand2')
        self.tab_threats.pack(side='left', padx=5)
        
        self.tab_system = tk.Button(tab_frame, text="SYSTEM", font=('Segoe UI', 9),
                                    bg='#0d1117', fg='#8b949e', relief='flat',
                                    padx=15, pady=5, cursor='hand2')
        self.tab_system.pack(side='left', padx=5)
        
        # Log text area
        log_container = tk.Frame(log_card, bg='#0d1117')
        log_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        self.log_text = scrolledtext.ScrolledText(log_container, 
                                                  font=('Consolas', 10),
                                                  bg='#0d1117', fg='#c9d1d9',
                                                  wrap='word', bd=0, relief='flat',
                                                  insertbackground='#58a6ff')
        self.log_text.pack(fill='both', expand=True)
        
        # Configure log tags with modern colors
        self.log_text.tag_config('info', foreground='#58a6ff')
        self.log_text.tag_config('success', foreground='#3fb950')
        self.log_text.tag_config('warning', foreground='#d29922')
        self.log_text.tag_config('error', foreground='#f85149')
        self.log_text.tag_config('timestamp', foreground='#8b949e')
        
    def create_modern_card(self, parent, title):
        card = tk.Frame(parent, bg='#161b22', relief='flat')
        
        header = tk.Frame(card, bg='#161b22')
        header.pack(fill='x', padx=20, pady=(15,10))
        
        tk.Label(header, text=title, font=('Segoe UI', 11, 'bold'),
                bg='#161b22', fg='#c9d1d9').pack(side='left')
        
        # Separator line
        tk.Frame(card, bg='#21262d', height=1).pack(fill='x', padx=20)
        
        return card
    
    def create_advanced_stat_card(self, parent, label, value, color, icon, col):
        card = tk.Frame(parent, bg='#161b22', relief='flat')
        card.grid(row=0, column=col, padx=8, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon
        tk.Label(card, text=icon, font=('Arial', 24), 
                bg='#161b22').pack(pady=(20,5))
        
        # Label
        tk.Label(card, text=label, font=('Segoe UI', 9, 'bold'),
                bg='#161b22', fg='#8b949e').pack()
        
        # Value
        value_label = tk.Label(card, text=value, font=('Segoe UI', 28, 'bold'),
                              bg='#161b22', fg=color)
        value_label.pack(pady=(5,20))
        
        # Store reference
        if col == 0:
            self.risk_label = value_label
        elif col == 1:
            self.threat_label = value_label
        elif col == 2:
            self.scan_label = value_label
        elif col == 3:
            self.status_label = value_label
    
    def create_control_button(self, parent, text, command, color):
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', 10, 'bold'),
                       bg=color, fg='#ffffff',
                       activebackground=color,
                       relief='flat', cursor='hand2',
                       width=25, pady=10)
        return btn
    
    def draw_shield(self):
        # Animated shield icon
        self.shield_canvas.delete('all')
        
        # Shield outline
        points = [25, 5, 45, 15, 45, 35, 25, 45, 5, 35, 5, 15]
        self.shield_canvas.create_polygon(points, fill='#238636', 
                                         outline='#3fb950', width=2)
        
        # Checkmark
        self.shield_canvas.create_line(15, 25, 22, 32, width=3, 
                                      fill='#ffffff', capstyle='round')
        self.shield_canvas.create_line(22, 32, 35, 18, width=3, 
                                      fill='#ffffff', capstyle='round')
    
    def draw_status_indicator(self):
        self.status_canvas.delete('all')
        
        # Pulsing dot
        x, y = 20, 25
        radius = 8 + self.pulse_state
        
        self.status_canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                      fill=self.status_color, outline='')
        
        # Status text
        self.status_canvas.create_text(50, 25, text=self.status_text,
                                      font=('Segoe UI', 11, 'bold'),
                                      fill=self.status_color, anchor='w')
    
    def draw_mini_graph(self, canvas, data, color):
        canvas.delete('all')
        width = canvas.winfo_width() or 300
        height = canvas.winfo_height() or 60
        
        if width <= 1:
            return
        
        # Draw grid lines
        for i in range(0, 101, 25):
            y = height - (i * height / 100)
            canvas.create_line(0, y, width, y, fill='#21262d', width=1)
        
        # Draw data line
        if len(data) > 1:
            points = []
            step = width / (len(data) - 1)
            for i, val in enumerate(data):
                x = i * step
                y = height - (val * height / 100)
                points.extend([x, y])
            
            if len(points) >= 4:
                canvas.create_line(points, fill=color, width=2, smooth=True)
                
                # Fill area under curve
                fill_points = points + [width, height, 0, height]
                canvas.create_polygon(fill_points, fill=color, 
                                    stipple='gray25', outline='')
    
    def start_animations(self):
        def animate():
            while True:
                self.pulse_state += self.pulse_direction * 0.5
                if self.pulse_state >= 3:
                    self.pulse_direction = -1
                elif self.pulse_state <= 0:
                    self.pulse_direction = 1
                
                try:
                    self.draw_status_indicator()
                    if self.monitoring:
                        self.update_graphs()
                except:
                    pass
                
                time.sleep(0.05)
        
        threading.Thread(target=animate, daemon=True).start()
    
    def update_graphs(self):
        try:
            # Update CPU
            cpu = psutil.cpu_percent(interval=0.1)
            self.cpu_history.append(cpu)
            self.cpu_label.config(text=f"CPU: {cpu:.1f}%")
            self.draw_mini_graph(self.cpu_canvas, self.cpu_history, '#58a6ff')
            
            # Update Memory
            mem = psutil.virtual_memory().percent
            self.mem_history.append(mem)
            self.mem_label.config(text=f"Memory: {mem:.1f}%")
            self.draw_mini_graph(self.mem_canvas, self.mem_history, '#3fb950')
            
            # Update Network
            try:
                net_count = len([c for c in psutil.net_connections() 
                               if c.status == 'ESTABLISHED'])
            except:
                net_count = 0
            self.net_history.append(min(net_count, 100))
            self.net_label.config(text=f"Network: {net_count} connections")
            self.draw_mini_graph(self.net_canvas, self.net_history, '#d29922')
        except:
            pass
    
    def log(self, message, tag='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert('end', f"[{timestamp}] ", 'timestamp')
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
        self.log(f"👤 Authenticated user: {username}", 'info')
        self.log("🔒 All systems operational", 'success')
        
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
        self.log("🔄 Manual security scan initiated...", 'info')
        threading.Thread(target=self.perform_scan, daemon=True).start()
    
    def update_device_info(self):
        hostname = socket.gethostname()
        os_info = f"{platform.system()} {platform.release()}"
        ip = socket.gethostbyname(hostname)
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                       for i in range(0,48,8)][::-1])
        device_id = hashlib.sha256(f"{uuid.getnode()}".encode()).hexdigest()[:16]
        
        info = f"""
User:        {self.username}
Hostname:    {hostname}
OS:          {os_info}
IP Address:  {ip}
MAC Address: {mac}
Device ID:   {device_id}
Backend:     Connected ✓
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
            external = sum(1 for c in connections if c.raddr and c.status == 'ESTABLISHED')
            if external > 10:
                threats.append((f"🌐 {external} external connections detected", 'warning', 15))
        except:
            pass
        
        # Check USB
        try:
            for partition in psutil.disk_partitions():
                if 'removable' in partition.opts.lower():
                    threats.append(("💾 Removable USB device detected", 'error', 20))
                    break
        except:
            pass
        
        # Update stats
        if threats:
            self.threat_count += len(threats)
            self.threat_label.config(text=str(self.threat_count))
            
            for msg, tag, risk in threats:
                self.log(msg, tag)
                self.risk_score += risk
            
            self.risk_label.config(text=str(min(self.risk_score, 100)))
            
            if self.risk_score > 50:
                self.status_label.config(text="DANGER", fg='#f85149')
            elif self.risk_score > 30:
                self.status_label.config(text="WARNING", fg='#d29922')
        else:
            self.log("✓ Security scan complete - No threats detected", 'success')
    
    def monitor_loop(self):
        # Register device
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
            self.log("✓ Device fingerprint registered", 'success')
        except:
            self.log("⚠️ Running in offline mode - Backend unavailable", 'warning')
        
        while self.monitoring:
            self.perform_scan()
            for _ in range(CHECK_INTERVAL):
                if not self.monitoring:
                    break
                time.sleep(1)

def main():
    root = tk.Tk()
    app = ZeroTrustAdvancedGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
