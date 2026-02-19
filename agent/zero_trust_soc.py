"""
ZERO TRUST - Security Operations Center (SOC) Agent
Real-time cybersecurity monitoring tool
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
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

class SOCAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("ZERO TRUST - Security Operations Center")
        self.root.geometry("1920x1080")
        self.root.configure(bg='#000000')
        self.root.state('zoomed')
        
        self.username = None
        self.monitoring = False
        self.loading_progress = 0
        
        # Real-time data
        self.cpu_data = deque([0]*60, maxlen=60)
        self.mem_data = deque([0]*60, maxlen=60)
        self.net_data = deque([0]*60, maxlen=60)
        
        # Backend data
        self.user_data = {}
        self.all_users = []
        self.file_logs = []
        self.blockchain = []
        self.sessions = []
        
        # Animation
        self.scan_angle = 0
        self.pulse = 0
        
        self.show_loading_screen()
        
    def show_loading_screen(self):
        # Loading screen
        self.loading_frame = tk.Frame(self.root, bg='#000000')
        self.loading_frame.pack(fill='both', expand=True)
        
        # Center content
        center = tk.Frame(self.loading_frame, bg='#000000')
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo
        tk.Label(center, text="⚡", font=('Arial', 80), 
                bg='#000000', fg='#00ff00').pack(pady=20)
        
        tk.Label(center, text="ZERO TRUST", 
                font=('Courier New', 40, 'bold'),
                bg='#000000', fg='#00ff00').pack()
        
        tk.Label(center, text="Security Operations Center", 
                font=('Courier New', 16),
                bg='#000000', fg='#00ff00').pack(pady=10)
        
        # Loading bar
        self.loading_bar_frame = tk.Frame(center, bg='#00ff00', width=500, height=30)
        self.loading_bar_frame.pack(pady=30)
        self.loading_bar_frame.pack_propagate(False)
        
        self.loading_bar = tk.Frame(self.loading_bar_frame, bg='#000000', width=0, height=26)
        self.loading_bar.place(x=2, y=2)
        
        self.loading_text = tk.Label(center, text="Initializing systems...", 
                                     font=('Courier New', 12),
                                     bg='#000000', fg='#00ff00')
        self.loading_text.pack(pady=10)
        
        # Username input
        tk.Label(center, text="Enter Username:", 
                font=('Courier New', 12, 'bold'),
                bg='#000000', fg='#00ff00').pack(pady=(30,10))
        
        self.username_entry = tk.Entry(center, font=('Courier New', 14), 
                                      bg='#001100', fg='#00ff00', 
                                      insertbackground='#00ff00',
                                      width=30, bd=2, relief='solid')
        self.username_entry.pack(pady=10)
        self.username_entry.bind('<Return>', lambda e: self.start_loading())
        
        start_btn = tk.Button(center, text="[ INITIALIZE ]",
                             command=self.start_loading,
                             font=('Courier New', 12, 'bold'),
                             bg='#001100', fg='#00ff00',
                             activebackground='#00ff00',
                             activeforeground='#000000',
                             bd=2, relief='solid',
                             padx=40, pady=10, cursor='hand2')
        start_btn.pack(pady=20)
        
    def start_loading(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username required!")
            return
        
        self.username = username
        self.username_entry.config(state='disabled')
        
        # Start loading animation
        threading.Thread(target=self.loading_animation, daemon=True).start()
        
    def loading_animation(self):
        steps = [
            "Connecting to backend...",
            "Authenticating user...",
            "Loading security modules...",
            "Initializing threat detection...",
            "Starting network monitor...",
            "Loading device fingerprint...",
            "Fetching user data...",
            "Loading blockchain audit...",
            "Initializing real-time graphs...",
            "System ready!"
        ]
        
        for i, step in enumerate(steps):
            self.loading_text.config(text=step)
            progress = int((i + 1) / len(steps) * 496)
            self.loading_bar.config(width=progress)
            self.root.update()
            time.sleep(0.5)
        
        # Load data from backend
        self.fetch_backend_data()
        
        # Show main interface
        self.loading_frame.destroy()
        self.create_soc_interface()
        
    def fetch_backend_data(self):
        try:
            r = requests.get(f"{BACKEND_URL}/security/analyze/user/{self.username}", timeout=5)
            if r.status_code == 200:
                self.user_data = r.json()
            
            r = requests.get(f"{BACKEND_URL}/security/analyze/admin", timeout=5)
            if r.status_code == 200:
                self.all_users = r.json().get('users', [])
            
            r = requests.get(f"{BACKEND_URL}/admin/file-access", timeout=5)
            if r.status_code == 200:
                self.file_logs = r.json().get('file_logs', [])
            
            r = requests.get(f"{BACKEND_URL}/audit/chain", timeout=5)
            if r.status_code == 200:
                self.blockchain = r.json().get('blockchain', [])
            
            r = requests.get(f"{BACKEND_URL}/admin/user-sessions/{self.username}", timeout=5)
            if r.status_code == 200:
                self.sessions = r.json().get('sessions', [])
        except:
            pass
    
    def create_soc_interface(self):
        # Main container
        main = tk.Frame(self.root, bg='#000000')
        main.pack(fill='both', expand=True)
        
        # Top header
        header = tk.Frame(main, bg='#001100', height=80, bd=2, relief='solid')
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(header, bg='#001100')
        logo_frame.pack(side='left', padx=20)
        
        self.logo_canvas = tk.Canvas(logo_frame, width=50, height=50, 
                                     bg='#001100', highlightthickness=0)
        self.logo_canvas.pack(side='left')
        
        title_frame = tk.Frame(logo_frame, bg='#001100')
        title_frame.pack(side='left', padx=15)
        
        tk.Label(title_frame, text="⚡ ZERO TRUST SOC", 
                font=('Courier New', 20, 'bold'),
                bg='#001100', fg='#00ff00').pack(anchor='w')
        tk.Label(title_frame, text=f"User: {self.username}", 
                font=('Courier New', 10),
                bg='#001100', fg='#00ff00').pack(anchor='w')
        
        # Status indicators
        status_frame = tk.Frame(header, bg='#001100')
        status_frame.pack(side='right', padx=20)
        
        self.status_canvas = tk.Canvas(status_frame, width=60, height=60, 
                                       bg='#001100', highlightthickness=0)
        self.status_canvas.pack(side='left', padx=10)
        
        status_text = tk.Frame(status_frame, bg='#001100')
        status_text.pack(side='left')
        
        self.status_label = tk.Label(status_text, text="● ONLINE", 
                                     font=('Courier New', 12, 'bold'),
                                     bg='#001100', fg='#00ff00')
        self.status_label.pack()
        
        self.time_label = tk.Label(status_text, text="", 
                                   font=('Courier New', 10),
                                   bg='#001100', fg='#00ff00')
        self.time_label.pack()
        
        # Stats bar
        stats_bar = tk.Frame(main, bg='#000000', height=100)
        stats_bar.pack(fill='x', pady=10, padx=10)
        stats_bar.pack_propagate(False)
        
        risk_score = self.user_data.get('risk_score', 0)
        risk_level = self.user_data.get('risk_level', 'LOW')
        decision = self.user_data.get('decision', 'ALLOW')
        zone = self.user_data.get('zone', 'PUBLIC')
        login_count = self.user_data.get('login_count', 0)
        
        self.create_stat_box(stats_bar, "RISK SCORE", str(risk_score), self.get_risk_color(risk_score), 0)
        self.create_stat_box(stats_bar, "RISK LEVEL", risk_level, self.get_risk_color(risk_score), 1)
        self.create_stat_box(stats_bar, "DECISION", decision, '#00ff00' if decision == 'ALLOW' else '#ff0000', 2)
        self.create_stat_box(stats_bar, "ACCESS ZONE", zone, '#00ffff', 3)
        self.create_stat_box(stats_bar, "TOTAL LOGINS", str(login_count), '#ffff00', 4)
        self.create_stat_box(stats_bar, "ACTIVE USERS", str(len(self.all_users)), '#ff00ff', 5)
        
        # Main grid
        grid = tk.Frame(main, bg='#000000')
        grid.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left column (30%)
        left_col = tk.Frame(grid, bg='#000000', width=500)
        left_col.pack(side='left', fill='both', padx=(0,5))
        left_col.pack_propagate(False)
        
        # Device info
        device_panel = self.create_panel(left_col, "💻 DEVICE FINGERPRINT")
        device_panel.pack(fill='x', pady=(0,10))
        
        device_text = tk.Text(device_panel, height=12, font=('Courier New', 9),
                             bg='#000000', fg='#00ff00', bd=0, wrap='word')
        device_text.pack(padx=10, pady=10, fill='x')
        
        hostname = socket.gethostname()
        os_info = f"{platform.system()} {platform.release()}"
        ip = self.user_data.get('ip_address', socket.gethostbyname(hostname))
        mac = self.user_data.get('mac_address', 'N/A')
        
        device_info = f""">>> USERNAME:    {self.username}
>>> HOSTNAME:    {hostname}
>>> OS:          {os_info}
>>> IP ADDRESS:  {ip}
>>> MAC ADDRESS: {mac}
>>> CITY:        {self.user_data.get('city', 'Unknown')}
>>> COUNTRY:     {self.user_data.get('country', 'Unknown')}
>>> WIFI:        {self.user_data.get('wifi_ssid', 'N/A')}
>>> DEVICE ID:   {hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16]}
>>> STATUS:      ACTIVE"""
        
        device_text.insert('1.0', device_info)
        device_text.config(state='disabled')
        
        # System metrics
        metrics_panel = self.create_panel(left_col, "📊 SYSTEM METRICS")
        metrics_panel.pack(fill='both', expand=True, pady=(0,10))
        
        metrics_content = tk.Frame(metrics_panel, bg='#001100')
        metrics_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(metrics_content, text="CPU USAGE", font=('Courier New', 9, 'bold'),
                bg='#001100', fg='#00ff00').pack(anchor='w')
        self.cpu_canvas = tk.Canvas(metrics_content, width=450, height=70, 
                                    bg='#000000', highlightthickness=0)
        self.cpu_canvas.pack(fill='x', pady=5)
        self.cpu_label = tk.Label(metrics_content, text="0%", 
                                 font=('Courier New', 10, 'bold'),
                                 bg='#001100', fg='#00ff00')
        self.cpu_label.pack(anchor='w', pady=(0,10))
        
        tk.Label(metrics_content, text="MEMORY USAGE", font=('Courier New', 9, 'bold'),
                bg='#001100', fg='#00ff00').pack(anchor='w')
        self.mem_canvas = tk.Canvas(metrics_content, width=450, height=70, 
                                    bg='#000000', highlightthickness=0)
        self.mem_canvas.pack(fill='x', pady=5)
        self.mem_label = tk.Label(metrics_content, text="0%", 
                                 font=('Courier New', 10, 'bold'),
                                 bg='#001100', fg='#00ff00')
        self.mem_label.pack(anchor='w', pady=(0,10))
        
        tk.Label(metrics_content, text="NETWORK ACTIVITY", font=('Courier New', 9, 'bold'),
                bg='#001100', fg='#00ff00').pack(anchor='w')
        self.net_canvas = tk.Canvas(metrics_content, width=450, height=70, 
                                    bg='#000000', highlightthickness=0)
        self.net_canvas.pack(fill='x', pady=5)
        self.net_label = tk.Label(metrics_content, text="0 conn", 
                                 font=('Courier New', 10, 'bold'),
                                 bg='#001100', fg='#00ff00')
        self.net_label.pack(anchor='w')
        
        # Controls
        control_panel = self.create_panel(left_col, "⚙️ CONTROLS")
        control_panel.pack(fill='x')
        
        btn_frame = tk.Frame(control_panel, bg='#001100')
        btn_frame.pack(padx=10, pady=10)
        
        self.create_button(btn_frame, "📊 WEB DASHBOARD", self.open_dashboard).pack(pady=5, fill='x')
        self.create_button(btn_frame, "🔄 REFRESH DATA", self.refresh_data).pack(pady=5, fill='x')
        self.create_button(btn_frame, "⛔ EXIT", self.root.quit).pack(pady=5, fill='x')
        
        # Middle column (35%)
        mid_col = tk.Frame(grid, bg='#000000')
        mid_col.pack(side='left', fill='both', expand=True, padx=5)
        
        # All users table
        users_panel = self.create_panel(mid_col, f"👥 ALL USERS ({len(self.all_users)})")
        users_panel.pack(fill='both', expand=True, pady=(0,10))
        
        users_frame = tk.Frame(users_panel, bg='#001100')
        users_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.users_text = scrolledtext.ScrolledText(users_frame, 
                                                    font=('Courier New', 9),
                                                    bg='#000000', fg='#00ff00',
                                                    wrap='none', bd=0)
        self.users_text.pack(fill='both', expand=True)
        
        # Header
        self.users_text.insert('end', f"{'USER':<15} {'RISK':<6} {'LEVEL':<10} {'DECISION':<10} {'LOGINS':<8} {'CITY':<15}\n")
        self.users_text.insert('end', "-" * 80 + "\n")
        
        # Data
        for user in self.all_users[:20]:
            username = user.get('username', 'N/A')[:14]
            risk = str(user.get('risk_score', 0))
            level = user.get('risk_level', 'LOW')[:9]
            decision = user.get('decision', 'ALLOW')[:9]
            logins = str(user.get('login_count', 0))
            city = user.get('city', 'Unknown')[:14]
            
            line = f"{username:<15} {risk:<6} {level:<10} {decision:<10} {logins:<8} {city:<15}\n"
            self.users_text.insert('end', line)
        
        self.users_text.config(state='disabled')
        
        # File access logs
        files_panel = self.create_panel(mid_col, f"📁 FILE ACCESS LOGS ({len(self.file_logs)})")
        files_panel.pack(fill='both', expand=True)
        
        files_frame = tk.Frame(files_panel, bg='#001100')
        files_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.files_text = scrolledtext.ScrolledText(files_frame, 
                                                    font=('Courier New', 9),
                                                    bg='#000000', fg='#00ff00',
                                                    wrap='none', bd=0)
        self.files_text.pack(fill='both', expand=True)
        
        # Header
        self.files_text.insert('end', f"{'USER':<12} {'FILE':<25} {'ACTION':<8} {'TIME':<20}\n")
        self.files_text.insert('end', "-" * 70 + "\n")
        
        # Data
        for log in self.file_logs[:30]:
            user = log.get('user_id', 'N/A')[:11]
            file = log.get('file_name', 'N/A')[:24]
            action = log.get('action', 'N/A')[:7]
            time_str = str(log.get('access_time', ''))[:19]
            
            line = f"{user:<12} {file:<25} {action:<8} {time_str:<20}\n"
            self.files_text.insert('end', line)
        
        self.files_text.config(state='disabled')
        
        # Right column (35%)
        right_col = tk.Frame(grid, bg='#000000')
        right_col.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        # Session history
        sessions_panel = self.create_panel(right_col, f"🔐 SESSION HISTORY ({len(self.sessions)})")
        sessions_panel.pack(fill='both', expand=True, pady=(0,10))
        
        sessions_frame = tk.Frame(sessions_panel, bg='#001100')
        sessions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.sessions_text = scrolledtext.ScrolledText(sessions_frame, 
                                                       font=('Courier New', 9),
                                                       bg='#000000', fg='#00ff00',
                                                       wrap='word', bd=0)
        self.sessions_text.pack(fill='both', expand=True)
        
        for i, session in enumerate(self.sessions[:10]):
            self.sessions_text.insert('end', f"\n>>> SESSION #{i+1}\n")
            self.sessions_text.insert('end', f"Login Time: {session.get('login_time', 'N/A')}\n")
            self.sessions_text.insert('end', f"IP Address: {session.get('ip_address', 'N/A')}\n")
            self.sessions_text.insert('end', f"Location:   {session.get('city', 'N/A')}, {session.get('country', 'N/A')}\n")
            self.sessions_text.insert('end', f"Device ID:  {session.get('device_id', 'N/A')}\n")
            self.sessions_text.insert('end', f"Status:     {'ACTIVE' if session.get('is_active') else 'ENDED'}\n")
            
            files = session.get('file_activities', [])
            if files:
                self.sessions_text.insert('end', f"Files ({len(files)}): ")
                self.sessions_text.insert('end', ', '.join([f"{f.get('file_name')}({f.get('action')})" for f in files[:3]]))
                self.sessions_text.insert('end', '\n')
            
            nets = session.get('network_activities', [])
            if nets:
                self.sessions_text.insert('end', f"Network ({len(nets)}): ")
                self.sessions_text.insert('end', ', '.join([f"{n.get('remote_ip')}" for n in nets[:3]]))
                self.sessions_text.insert('end', '\n')
        
        self.sessions_text.config(state='disabled')
        
        # Blockchain audit
        blockchain_panel = self.create_panel(right_col, f"⛓️ BLOCKCHAIN AUDIT ({len(self.blockchain)})")
        blockchain_panel.pack(fill='both', expand=True)
        
        blockchain_frame = tk.Frame(blockchain_panel, bg='#001100')
        blockchain_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.blockchain_text = scrolledtext.ScrolledText(blockchain_frame, 
                                                         font=('Courier New', 9),
                                                         bg='#000000', fg='#00ff00',
                                                         wrap='word', bd=0)
        self.blockchain_text.pack(fill='both', expand=True)
        
        for block in self.blockchain[:15]:
            self.blockchain_text.insert('end', f"\n>>> BLOCK #{block.get('block_index', 0)}\n", 'header')
            self.blockchain_text.insert('end', f"Timestamp: {block.get('timestamp', 'N/A')}\n")
            self.blockchain_text.insert('end', f"Hash:      {str(block.get('current_hash', 'N/A'))[:40]}...\n")
            self.blockchain_text.insert('end', f"Event:     {block.get('event_type', 'N/A')}\n")
        
        self.blockchain_text.config(state='disabled')
        
        # Start monitoring
        self.monitoring = True
        threading.Thread(target=self.update_loop, daemon=True).start()
        threading.Thread(target=self.animation_loop, daemon=True).start()
    
    def create_panel(self, parent, title):
        panel = tk.Frame(parent, bg='#00ff00', bd=2, relief='solid')
        inner = tk.Frame(panel, bg='#001100')
        inner.pack(fill='both', expand=True, padx=2, pady=2)
        
        header = tk.Frame(inner, bg='#001100')
        header.pack(fill='x', padx=10, pady=10)
        
        tk.Label(header, text=title, font=('Courier New', 11, 'bold'),
                bg='#001100', fg='#00ff00').pack(side='left')
        
        tk.Frame(inner, bg='#00ff00', height=2).pack(fill='x', padx=10)
        
        return inner
    
    def create_stat_box(self, parent, label, value, color, col):
        frame = tk.Frame(parent, bg='#00ff00', bd=2, relief='solid')
        frame.grid(row=0, column=col, padx=5, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)
        
        inner = tk.Frame(frame, bg='#001100')
        inner.pack(fill='both', expand=True, padx=2, pady=2)
        
        tk.Label(inner, text=label, font=('Courier New', 8, 'bold'),
                bg='#001100', fg='#888888').pack(pady=(10,5))
        
        tk.Label(inner, text=value, font=('Courier New', 18, 'bold'),
                bg='#001100', fg=color).pack(pady=(0,10))
    
    def create_button(self, parent, text, command):
        frame = tk.Frame(parent, bg='#00ff00', bd=2, relief='solid')
        btn = tk.Button(frame, text=text, command=command,
                       font=('Courier New', 10, 'bold'),
                       bg='#001100', fg='#00ff00',
                       activebackground='#00ff00',
                       activeforeground='#000000',
                       relief='flat', cursor='hand2',
                       width=35, pady=8)
        btn.pack(padx=2, pady=2)
        return frame
    
    def get_risk_color(self, risk):
        if risk >= 70:
            return '#ff0000'
        elif risk >= 50:
            return '#ff6600'
        elif risk >= 30:
            return '#ffff00'
        else:
            return '#00ff00'
    
    def draw_logo(self):
        self.logo_canvas.delete('all')
        angle = self.scan_angle
        points = []
        for i in range(6):
            x = 25 + 20 * math.cos(math.radians(angle + i * 60))
            y = 25 + 20 * math.sin(math.radians(angle + i * 60))
            points.extend([x, y])
        
        self.logo_canvas.create_polygon(points, fill='', outline='#00ff00', width=2)
        self.logo_canvas.create_oval(18, 18, 32, 32, fill='#00ff00', outline='')
    
    def draw_radar(self):
        self.status_canvas.delete('all')
        for r in [10, 20, 30]:
            self.status_canvas.create_oval(30-r, 30-r, 30+r, 30+r,
                                          outline='#00ff00', width=1)
        
        angle = self.scan_angle
        x = 30 + 25 * math.cos(math.radians(angle))
        y = 30 + 25 * math.sin(math.radians(angle))
        self.status_canvas.create_line(30, 30, x, y, fill='#00ff00', width=2)
    
    def draw_graph(self, canvas, data, color):
        canvas.delete('all')
        width = canvas.winfo_width() or 450
        height = canvas.winfo_height() or 70
        
        if width <= 1:
            return
        
        for i in range(0, 101, 25):
            y = height - (i * height / 100)
            canvas.create_line(0, y, width, y, fill='#003300', width=1)
        
        if len(data) > 1:
            points = []
            step = width / (len(data) - 1)
            for i, val in enumerate(data):
                x = i * step
                y = height - (val * height / 100)
                points.extend([x, y])
            
            if len(points) >= 4:
                canvas.create_line(points, fill=color, width=2, smooth=True)
    
    def animation_loop(self):
        while self.monitoring:
            self.scan_angle = (self.scan_angle + 3) % 360
            
            try:
                self.draw_logo()
                self.draw_radar()
                self.time_label.config(text=datetime.now().strftime('%H:%M:%S'))
            except:
                pass
            
            time.sleep(0.05)
    
    def update_loop(self):
        while self.monitoring:
            try:
                # Update system metrics
                cpu = psutil.cpu_percent(interval=0.1)
                self.cpu_data.append(cpu)
                self.cpu_label.config(text=f"{cpu:.1f}%")
                self.draw_graph(self.cpu_canvas, self.cpu_data, '#00ffff')
                
                mem = psutil.virtual_memory().percent
                self.mem_data.append(mem)
                self.mem_label.config(text=f"{mem:.1f}%")
                self.draw_graph(self.mem_canvas, self.mem_data, '#ffff00')
                
                try:
                    net_count = len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
                except:
                    net_count = 0
                self.net_data.append(min(net_count, 100))
                self.net_label.config(text=f"{net_count} conn")
                self.draw_graph(self.net_canvas, self.net_data, '#ff00ff')
            except:
                pass
            
            time.sleep(1)
    
    def refresh_data(self):
        self.fetch_backend_data()
        messagebox.showinfo("Success", "Data refreshed from backend!")
    
    def open_dashboard(self):
        webbrowser.open('http://localhost:3000')

def main():
    root = tk.Tk()
    app = SOCAgent(root)
    root.mainloop()

if __name__ == "__main__":
    main()
