from mysql_database import get_db
import hashlib
import uuid
from datetime import datetime
import json

class ActivityTracker:
    
    @staticmethod
    def track_login(user_id, ip_address, mac_address, hostname, os_info, wifi_ssid, user_agent, success=True, failure_reason=None):
        """Track user login with device fingerprinting"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        device_fingerprint = hashlib.md5(f"{mac_address}{hostname}{user_agent}".encode()).hexdigest()
        
        # Insert login log
        cursor.execute("""
            INSERT INTO login_logs (user_id, session_id, ip_address, mac_address, 
                                  location, success, failure_reason, device_fingerprint, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, session_id, ip_address, mac_address, "Unknown", success, failure_reason, device_fingerprint, user_agent))
        
        login_id = cursor.lastrowid
        
        if success:
            # Create active session
            cursor.execute("""
                INSERT INTO sessions (session_id, user_id, ip_address, user_agent, 
                                    expires_at, login_id)
                VALUES (%s, %s, %s, %s, DATE_ADD(NOW(), INTERVAL 8 HOUR), %s)
            """, (session_id, user_id, ip_address, user_agent, login_id))
            
            # Track device
            ActivityTracker.track_device(user_id, device_fingerprint, mac_address, hostname, os_info, ip_address, wifi_ssid)
        
        conn.commit()
        cursor.close()
        conn.close()
        return session_id
    
    @staticmethod
    def track_device(user_id, device_id, mac_address, hostname, os_info, ip_address, wifi_ssid):
        """Track device fingerprint"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if device exists
        cursor.execute("SELECT id FROM device_logs WHERE device_id = %s AND user_id = %s", (device_id, user_id))
        if cursor.fetchone():
            # Update existing device
            cursor.execute("""
                UPDATE device_logs SET last_seen = NOW(), ip_address = %s, 
                       login_count = login_count + 1
                WHERE device_id = %s AND user_id = %s
            """, (ip_address, device_id, user_id))
        else:
            # Insert new device
            cursor.execute("""
                INSERT INTO device_logs (user_id, device_id, mac_address, hostname, 
                                       os, ip_address, wifi_ssid, device_type, trusted)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Desktop', 0)
            """, (user_id, device_id, mac_address, hostname, os_info, ip_address, wifi_ssid))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def track_file_access(user_id, file_name, file_path, action, file_size=0, ip_address=None, device_id=None):
        """Track file operations in real-time"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Determine sensitivity level
        sensitive_files = ['secret', 'confidential', 'salary', 'password', 'private']
        sensitivity = 'critical' if any(word in file_name.lower() for word in sensitive_files) else 'internal'
        
        cursor.execute("""
            INSERT INTO file_access_logs (user_id, file_name, file_path, action, 
                                        file_size, sensitivity_level, ip_address, device_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, file_name, file_path, action, file_size, sensitivity, ip_address, device_id))
        
        # Create blockchain audit entry
        ActivityTracker.create_audit_entry('FILE_ACCESS', user_id, {
            'file_name': file_name,
            'action': action,
            'sensitivity': sensitivity
        })
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def track_network_connection(user_id, remote_ip, remote_port, protocol, is_external=False):
        """Track network connections"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO network_connections (user_id, remote_ip, remote_port, 
                                               protocol, is_external)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, remote_ip, remote_port, protocol, is_external))
            
            # Also insert into network_logs for compatibility
            cursor.execute("""
                INSERT INTO network_logs (user_id, remote_ip, remote_port, 
                                        protocol, external)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, remote_ip, remote_port, protocol, is_external))
    
    @staticmethod
    def create_risk_event(user_id, event_type, risk_score, severity, description):
        """Create risk event"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO risk_events (user_id, event_type, risk_score, severity, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, event_type, risk_score, severity, description))
    
    @staticmethod
    def create_audit_entry(event_type, user_id, event_data):
        """Create blockchain audit entry"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Get last block
            cursor.execute("SELECT MAX(block_index) FROM blockchain_audit")
            result = cursor.fetchone()
            block_index = (result[0] or 0) + 1
            
            # Create hash
            data_str = json.dumps(event_data, sort_keys=True)
            current_hash = hashlib.sha256(f"{block_index}{event_type}{user_id}{data_str}".encode()).hexdigest()
            
            cursor.execute("""
                INSERT INTO blockchain_audit (block_index, event_type, user_id, 
                                            event_data, current_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (block_index, event_type, user_id, json.dumps(event_data), current_hash))
    
    @staticmethod
    def update_user_risk_score(user_id, new_risk_score):
        """Update user risk score"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET risk_score = %s WHERE username = %s", (new_risk_score, user_id))
    
    @staticmethod
    def logout_user(session_id):
        """Track user logout"""
        with get_db() as conn:
            cursor = conn.cursor()
            
            # Update session
            cursor.execute("""
                UPDATE sessions SET is_active = 0, last_activity = NOW() 
                WHERE session_id = %s
            """, (session_id,))
            
            # Update login log
            cursor.execute("""
                UPDATE login_logs SET logout_time = NOW() 
                WHERE session_id = %s
            """, (session_id,))