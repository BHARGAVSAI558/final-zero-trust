import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading, socket, platform, uuid, hashlib, requests, psutil, time, webbrowser
from datetime import datetime
from collections import deque
import json

BACKEND = "http://localhost:8000"

class UnifiedSOCAgent:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ ZERO TRUST - Advanced SOC Agent")
        self.root.geometry("1400x900")
        self.root.configure(bg='#000000')
        self.username = None
        self.monitoring = False
        self.device_info = {}
        self.show_login()
    
    def show_login(self):
        self.login_frame = tk.Frame(self.root, bg='#000000')
        self.login_frame.pack(fill='both', expand=True)
        
        center = tk.Frame(self.login_frame, bg='#000000')
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(center, text="⚡", font=('Arial', 60), bg='#000000', fg='#00ff00').pack(pady=10)
        tk.Label(center, text="ZERO TRUST SOC AGENT", font=('Courier New', 28, 'bold'), bg='#000000', fg='#00ff00').pack()
        tk.Label(center, text="Advanced Security Monitoring", font=('Courier New', 12), bg='#000000', fg='#00ffff').pack(pady=5)
        
        tk.Label(center, text="Enter Username:", font=('Courier New', 12, 'bold'), bg='#000000', fg='#00ff00').pack(pady=(30,10))
        self.user_entry = tk.Entry(center, font=('Courier New', 14), bg='#001100', fg='#00ff00', insertbackground='#00ff00', width=30, bd=2, relief='solid')
        self.user_entry.pack(pady=10)
        self.user_entry.bind('<Return>', lambda e: self.start_monitoring())
        
        tk.Button(center, text="[ START MONITORING ]", command=self.start_monitoring, font=('Courier New', 12, 'bold'), bg='#001100', fg='#00ff00', activebackground='#00ff00', activeforeground='#000000', bd=2, relief='solid', padx=40, pady=10, cursor='hand2').pack(pady=20)
    
    def start_monitoring(self):
        self.username = self.user_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Username required!")
            return
        
        self.collect_device_info()
        self.register_device()
        self.login_frame.destroy()
        self.create_dashboard()
        self.monitoring = True
        threading.Thread(target=self.monitor_loop, daemon=True).start()
    
    def collect_device_info(self):
        self.device_info = {
            "username": self.username,
            "hostname": socket.gethostname(),
            "os": f"{platform.system()} {platform.release()}",
            "ip": socket.gethostbyname(socket.gethostname()),
            "mac": ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,48,8)][::-1]),
            "device_id": hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16],
            "cpu_count": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        }
    
    def register_device(self):
        try:
            requests.post(f"{BACKEND}/device/register", json=self.device_info, timeout=5)
        except:
            pass
    
    def create_dashboard(self):
        main = tk.Frame(self.root, bg='#000000')
        main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main, bg='#001100', bd=2, relief='solid')
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(header, text="⚡ ZERO TRUST SOC AGENT", font=('Courier New', 20, 'bold'), bg='#001100', fg='#00ff00').pack(side='left', padx=20, pady=10)
        tk.Label(header, text=f"User: {self.username}", font=('Courier New', 10), bg='#001100', fg='#00ffff').pack(side='left')
        
        self.status_label = tk.Label(header, text="● MONITORING", font=('Courier New', 12, 'bold'), bg='#001100', fg='#00ff00')
        self.status_label.pack(side='right', padx=20)
        
        # Stats
        stats = tk.Frame(main, bg='#000000')
        stats.pack(fill='x', pady=(0,10))
        
        self.stat_boxes = {}
        for i, (label, key) in enumerate([("RISK SCORE", "risk"), ("CPU", "cpu"), ("MEMORY", "mem"), ("FILES", "files"), ("NETWORK", "net")]):
            box = tk.Frame(stats, bg='#00ff00', bd=2, relief='solid')
            box.grid(row=0, column=i, padx=5, sticky='ew')
            stats.grid_columnconfigure(i, weight=1)
            inner = tk.Frame(box, bg='#001100')
            inner.pack(fill='both', expand=True, padx=2, pady=2)
            tk.Label(inner, text=label, font=('Courier New', 8, 'bold'), bg='#001100', fg='#888888').pack(pady=(5,0))
            self.stat_boxes[key] = tk.Label(inner, text="0", font=('Courier New', 16, 'bold'), bg='#001100', fg='#00ff00')
            self.stat_boxes[key].pack(pady=(0,5))
        
        # Content
        content = tk.Frame(main, bg='#000000')
        content.pack(fill='both', expand=True)
        
        # Left panel
        left = tk.Frame(content, bg='#000000', width=450)
        left.pack(side='left', fill='both', padx=(0,5))
        left.pack_propagate(False)
        
        device_panel = self.create_panel(left, "💻 DEVICE FINGERPRINT")
        device_panel.pack(fill='x', pady=(0,10))
        self.device_text = tk.Text(device_panel, height=10, font=('Courier New', 9), bg='#000000', fg='#00ff00', bd=0)
        self.device_text.pack(padx=10, pady=10, fill='x')
        self.device_text.insert('1.0', f"""USERNAME:  {self.device_info['username']}
HOSTNAME:  {self.device_info['hostname']}
OS:        {self.device_info['os']}
IP:        {self.device_info['ip']}
MAC:       {self.device_info['mac']}
DEVICE ID: {self.device_info['device_id']}
CPU CORES: {self.device_info['cpu_count']}
MEMORY:    {self.device_info['memory_gb']} GB""")
        self.device_text.config(state='disabled')
        
        activity_panel = self.create_panel(left, "📊 LIVE ACTIVITY")
        activity_panel.pack(fill='both', expand=True)
        self.activity_text = scrolledtext.ScrolledText(activity_panel, font=('Courier New', 9), bg='#000000', fg='#00ff00', wrap='word', bd=0)
        self.activity_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Right panel
        right = tk.Frame(content, bg='#000000')
        right.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        files_panel = self.create_panel(right, "📁 FILE ACCESS LOG")
        files_panel.pack(fill='both', expand=True, pady=(0,10))
        self.files_text = scrolledtext.ScrolledText(files_panel, font=('Courier New', 9), bg='#000000', fg='#00ff00', wrap='none', bd=0)
        self.files_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        network_panel = self.create_panel(right, "🌐 NETWORK CONNECTIONS")
        network_panel.pack(fill='both', expand=True)
        self.network_text = scrolledtext.ScrolledText(network_panel, font=('Courier New', 9), bg='#000000', fg='#00ff00', wrap='none', bd=0)
        self.network_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Controls
        controls = tk.Frame(main, bg='#000000')
        controls.pack(fill='x', pady=(10,0))
        
        tk.Button(controls, text="[ OPEN WEB DASHBOARD ]", command=lambda: webbrowser.open('http://localhost:3000'), font=('Courier New', 10, 'bold'), bg='#001100', fg='#00ff00', bd=2, relief='solid', padx=20, pady=8).pack(side='left', padx=5)
        tk.Button(controls, text="[ SEND TELEMETRY NOW ]", command=self.send_telemetry, font=('Courier New', 10, 'bold'), bg='#001100', fg='#00ffff', bd=2, relief='solid', padx=20, pady=8).pack(side='left', padx=5)
        tk.Button(controls, text="[ EXIT ]", command=self.root.quit, font=('Courier New', 10, 'bold'), bg='#001100', fg='#ff0000', bd=2, relief='solid', padx=20, pady=8).pack(side='right', padx=5)
    
    def create_panel(self, parent, title):
        panel = tk.Frame(parent, bg='#00ff00', bd=2, relief='solid')
        inner = tk.Frame(panel, bg='#001100')
        inner.pack(fill='both', expand=True, padx=2, pady=2)
        tk.Label(inner, text=title, font=('Courier New', 10, 'bold'), bg='#001100', fg='#00ff00').pack(anchor='w', padx=10, pady=10)
        tk.Frame(inner, bg='#00ff00', height=2).pack(fill='x', padx=10)
        return inner
    
    def monitor_loop(self):
        while self.monitoring:
            try:
                # Update stats
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                net_count = len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
                
                self.stat_boxes['cpu'].config(text=f"{cpu:.0f}%")
                self.stat_boxes['mem'].config(text=f"{mem:.0f}%")
                self.stat_boxes['net'].config(text=str(net_count))
                
                # Log activity
                self.log_activity(f"[{datetime.now().strftime('%H:%M:%S')}] CPU: {cpu:.1f}% | MEM: {mem:.1f}% | NET: {net_count} conn")
                
                # Update network connections
                self.update_network()
                
                # Send telemetry every 30 seconds
                if int(time.time()) % 30 == 0:
                    self.send_telemetry()
                
                time.sleep(2)
            except:
                pass
    
    def log_activity(self, msg):
        try:
            self.activity_text.insert('end', msg + '\n')
            self.activity_text.see('end')
            if int(self.activity_text.index('end-1c').split('.')[0]) > 100:
                self.activity_text.delete('1.0', '2.0')
        except:
            pass
    
    def update_network(self):
        try:
            self.network_text.delete('1.0', 'end')
            self.network_text.insert('end', f"{'LOCAL':<25} {'REMOTE':<25} {'STATUS':<15}\n")
            self.network_text.insert('end', "-" * 70 + "\n")
            for conn in psutil.net_connections()[:20]:
                if conn.status == 'ESTABLISHED':
                    local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    self.network_text.insert('end', f"{local:<25} {remote:<25} {conn.status:<15}\n")
        except:
            pass
    
    def send_telemetry(self):
        try:
            data = {
                "username": self.username,
                "device": self.device_info,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "cpu": psutil.cpu_percent(),
                    "memory": psutil.virtual_memory().percent,
                    "disk": psutil.disk_usage('/').percent,
                    "network_connections": len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
                }
            }
            requests.post(f"{BACKEND}/agent/telemetry", json=data, timeout=5)
            self.log_activity(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Telemetry sent to backend")
        except Exception as e:
            self.log_activity(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Telemetry failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedSOCAgent(root)
    root.mainloop()
