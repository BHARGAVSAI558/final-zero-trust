import subprocess
import sys
import os
import time

def start_agent_background():
    """Start agent service in background"""
    agent_path = os.path.join(os.path.dirname(__file__), 'agent', 'agent_service.py')
    
    if sys.platform == 'win32':
        # Windows - start in background
        subprocess.Popen(
            [sys.executable, agent_path],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        # Linux/Mac
        subprocess.Popen(
            [sys.executable, agent_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    print("✓ Agent service started in background")
    time.sleep(2)

if __name__ == "__main__":
    start_agent_background()
