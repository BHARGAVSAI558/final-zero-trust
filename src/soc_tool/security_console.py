#!/usr/bin/env python3
"""
ZERO TRUST SECURITY OPERATIONS CENTER
Real-Time Insider Threat Detection Platform
"""

import time
import json
import threading
from datetime import datetime
from pathlib import Path
from collections import deque
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

console = Console()

class CyberSOC:
    def __init__(self):
        self.running = True
        self.events = deque(maxlen=50)
        self.threats = deque(maxlen=20)
        self.devices = {}
        self.risk_scores = {}
        self.trust_scores = {}
        self.responses = deque(maxlen=10)
        
    def boot_sequence(self):
        """Cyberpunk boot animation"""
        boot_steps = [
            ("Initializing Zero Trust Engine...", 0.5),
            ("Loading UEBA ML Model...", 0.7),
            ("Loading Threat Intelligence Database...", 0.6),
            ("Initializing Device Fingerprint Engine...", 0.5),
            ("Starting Real-Time Monitoring...", 0.8),
            ("System Ready.", 0.3)
        ]
        
        console.clear()
        console.print("\n" * 5)
        console.print(Align.center(
            Text("ZERO TRUST SECURITY OPERATIONS CENTER", style="bold cyan"),
            vertical="middle"
        ))
        console.print(Align.center(
            Text("REAL-TIME INSIDER THREAT DETECTION PLATFORM", style="bold magenta"),
            vertical="middle"
        ))
        console.print("\n" * 2)
        
        for step, delay in boot_steps:
            console.print(f"[cyan]►[/cyan] {step}", style="bold green")
            time.sleep(delay)
        
        console.print("\n[bold green]✓ ALL SYSTEMS OPERATIONAL[/bold green]\n")
        time.sleep(1)
    
    def analyze_event(self, event):
        """Analyze event for threats"""
        user = event.get("user_id", "UNKNOWN")
        device_id = event.get("device_id", "UNKNOWN")
        ip = event.get("ip_address", "0.0.0.0")
        
        # Calculate risk score
        risk = 0
        signals = []
        
        if event.get("event_type") == "login":
            hour = datetime.now().hour
            if hour < 8 or hour > 18:
                risk += 15
                signals.append("ODD_HOUR_LOGIN")
            
            if not ip.startswith(("192.168", "10.")):
                risk += 25
                signals.append("EXTERNAL_NETWORK")
        
        if event.get("event_type") == "file_access":
            filename = event.get("file_name", "")
            if any(x in filename.lower() for x in ["secret", "credential", "password", ".env"]):
                risk += 40
                signals.append("SENSITIVE_FILE_ACCESS")
        
        # Device verification
        device_trust = "HIGH" if device_id in self.devices else "UNKNOWN"
        if device_trust == "UNKNOWN":
            risk += 30
            signals.append("UNKNOWN_DEVICE")
        
        # Calculate trust score
        trust = max(0, 100 - risk)
        
        # Store scores
        self.risk_scores[user] = risk
        self.trust_scores[user] = trust
        
        # Add to events
        self.events.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "user": user,
            "device": device_id,
            "ip": ip,
            "risk": risk,
            "trust": trust,
            "signals": signals,
            "type": event.get("event_type", "unknown")
        })
        
        # Check for threats
        if risk >= 70:
            threat = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "user": user,
                "device": device_id,
                "risk": risk,
                "signals": signals
            }
            self.threats.append(threat)
            
            # Automated response
            response = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "action": "ACCESS DENIED" if risk >= 90 else "RESTRICTED",
                "user": user,
                "reason": ", ".join(signals)
            }
            self.responses.append(response)
    
    def create_header(self):
        """Create cyberpunk header"""
        header = Text()
        header.append("╔═══════════════════════════════════════════════════════════════════════╗\n", style="bold cyan")
        header.append("║  ", style="bold cyan")
        header.append("ZERO TRUST SECURITY OPERATIONS CENTER", style="bold red")
        header.append("                      ║\n", style="bold cyan")
        header.append("║  ", style="bold cyan")
        header.append("REAL-TIME INSIDER THREAT DETECTION PLATFORM", style="bold magenta")
        header.append("                ║\n", style="bold cyan")
        header.append("╚═══════════════════════════════════════════════════════════════════════╝", style="bold cyan")
        return Panel(header, style="bold cyan", border_style="cyan")
    
    def create_live_events_panel(self):
        """Create live events table"""
        table = Table(box=box.ROUNDED, border_style="cyan", show_header=True, header_style="bold cyan")
        table.add_column("TIME", style="cyan", width=10)
        table.add_column("USER", style="magenta", width=12)
        table.add_column("DEVICE", style="yellow", width=12)
        table.add_column("IP", style="blue", width=15)
        table.add_column("TYPE", style="white", width=10)
        table.add_column("RISK", style="red", width=8)
        
        for event in list(self.events)[-10:]:
            risk_style = "red" if event["risk"] >= 70 else "yellow" if event["risk"] >= 50 else "green"
            table.add_row(
                event["time"],
                event["user"],
                event["device"],
                event["ip"],
                event["type"].upper(),
                f"[{risk_style}]{event['risk']}[/{risk_style}]"
            )
        
        return Panel(table, title="[bold cyan]LIVE LOGIN EVENTS[/bold cyan]", border_style="cyan")
    
    def create_risk_panel(self):
        """Create risk scores panel"""
        table = Table(box=box.ROUNDED, border_style="yellow", show_header=True, header_style="bold yellow")
        table.add_column("USER", style="magenta", width=15)
        table.add_column("RISK", style="red", width=10)
        table.add_column("TRUST", style="green", width=10)
        table.add_column("STATUS", style="white", width=15)
        
        for user in list(self.risk_scores.keys())[-8:]:
            risk = self.risk_scores[user]
            trust = self.trust_scores[user]
            status = "CRITICAL" if risk >= 90 else "HIGH" if risk >= 70 else "MEDIUM" if risk >= 50 else "SAFE"
            status_style = "red" if risk >= 70 else "yellow" if risk >= 50 else "green"
            
            table.add_row(
                user,
                f"[red]{risk}[/red]",
                f"[green]{trust}[/green]",
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        return Panel(table, title="[bold yellow]RISK SCORE MONITOR[/bold yellow]", border_style="yellow")
    
    def create_threats_panel(self):
        """Create active threats panel"""
        table = Table(box=box.ROUNDED, border_style="red", show_header=True, header_style="bold red")
        table.add_column("TIME", style="cyan", width=10)
        table.add_column("USER", style="magenta", width=12)
        table.add_column("DEVICE", style="yellow", width=12)
        table.add_column("RISK", style="red", width=8)
        table.add_column("SIGNALS", style="white", width=30)
        
        for threat in list(self.threats)[-8:]:
            table.add_row(
                threat["time"],
                threat["user"],
                threat["device"],
                f"[bold red]{threat['risk']}[/bold red]",
                ", ".join(threat["signals"][:2])
            )
        
        return Panel(table, title="[bold red]⚠ ACTIVE THREATS[/bold red]", border_style="red")
    
    def create_response_panel(self):
        """Create automated response panel"""
        table = Table(box=box.ROUNDED, border_style="magenta", show_header=True, header_style="bold magenta")
        table.add_column("TIME", style="cyan", width=10)
        table.add_column("ACTION", style="red", width=15)
        table.add_column("USER", style="magenta", width=12)
        table.add_column("REASON", style="white", width=35)
        
        for resp in list(self.responses)[-6:]:
            table.add_row(
                resp["time"],
                f"[bold red]{resp['action']}[/bold red]",
                resp["user"],
                resp["reason"][:35]
            )
        
        return Panel(table, title="[bold magenta]AUTOMATED RESPONSE[/bold magenta]", border_style="magenta")
    
    def create_stats_panel(self):
        """Create statistics panel"""
        total_events = len(self.events)
        total_threats = len(self.threats)
        total_responses = len(self.responses)
        
        stats = Text()
        stats.append(f"Total Events: ", style="cyan")
        stats.append(f"{total_events}\n", style="bold green")
        stats.append(f"Active Threats: ", style="yellow")
        stats.append(f"{total_threats}\n", style="bold red")
        stats.append(f"Responses: ", style="magenta")
        stats.append(f"{total_responses}\n", style="bold magenta")
        stats.append(f"Status: ", style="white")
        stats.append("MONITORING", style="bold green blink")
        
        return Panel(stats, title="[bold green]SYSTEM STATS[/bold green]", border_style="green")
    
    def create_layout(self):
        """Create dashboard layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        layout["left"].split_column(
            Layout(name="events"),
            Layout(name="threats")
        )
        
        layout["right"].split_column(
            Layout(name="risk"),
            Layout(name="response"),
            Layout(name="stats")
        )
        
        layout["header"].update(self.create_header())
        layout["events"].update(self.create_live_events_panel())
        layout["threats"].update(self.create_threats_panel())
        layout["risk"].update(self.create_risk_panel())
        layout["response"].update(self.create_response_panel())
        layout["stats"].update(self.create_stats_panel())
        
        footer_text = Text()
        footer_text.append("Press ", style="white")
        footer_text.append("Ctrl+C", style="bold red")
        footer_text.append(" to exit | ", style="white")
        footer_text.append(f"Last Update: {datetime.now().strftime('%H:%M:%S')}", style="cyan")
        layout["footer"].update(Panel(footer_text, border_style="cyan"))
        
        return layout
    
    def monitor_events(self):
        """Monitor events from backend or simulation"""
        # Simulate events for demo
        users = ["USR0042", "USR0015", "USR0089", "USR0123", "USR0056"]
        devices = ["DEV001", "DEV002", "DEV003", "DEV999"]
        ips = ["192.168.1.10", "192.168.1.20", "10.0.0.5", "203.45.67.89"]
        
        # Register known devices
        self.devices = {"DEV001": True, "DEV002": True, "DEV003": True}
        
        while self.running:
            import random
            
            # Generate random event
            event = {
                "user_id": random.choice(users),
                "device_id": random.choice(devices),
                "ip_address": random.choice(ips),
                "event_type": random.choice(["login", "file_access", "login"]),
                "file_name": random.choice(["report.pdf", "secrets.env", "data.xlsx", "credentials.txt"])
            }
            
            self.analyze_event(event)
            time.sleep(random.uniform(1, 3))
    
    def run(self):
        """Run the SOC console"""
        self.boot_sequence()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_events, daemon=True)
        monitor_thread.start()
        
        try:
            with Live(self.create_layout(), refresh_per_second=2, console=console) as live:
                while self.running:
                    live.update(self.create_layout())
                    time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[bold red]Shutting down SOC...[/bold red]")
            self.running = False

def main():
    """Main entry point"""
    soc = CyberSOC()
    soc.run()

if __name__ == "__main__":
    main()
