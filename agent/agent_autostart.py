import os
import sys
import winreg as reg

def add_to_startup():
    """Add agent to Windows startup"""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "ZeroTrustAgent"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_service.py")
    python_path = sys.executable
    command = f'"{python_path}" "{script_path}"'
    
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, app_name, 0, reg.REG_SZ, command)
        reg.CloseKey(key)
        print("✓ Agent added to Windows startup")
        print(f"  Command: {command}")
        return True
    except Exception as e:
        print(f"✗ Failed to add to startup: {e}")
        return False

if __name__ == "__main__":
    add_to_startup()
