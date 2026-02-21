from fastapi import APIRouter, HTTPException, Depends
from mysql_database import get_db
from activity_tracker import ActivityTracker
import json

router = APIRouter()

@router.get("/admin/user-devices/{username}")
async def get_user_devices(username: str):
    """Get real device fingerprints for user"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT device_id, mac_address, hostname, os, ip_address, wifi_ssid,
                   device_type, trusted, first_seen, last_seen, login_count,
                   browser, screen_resolution, timezone
            FROM device_logs 
            WHERE user_id = %s 
            ORDER BY last_seen DESC
        """, (username,))
        devices = cursor.fetchall()
        
        # Convert datetime to string
        for device in devices:
            if device['first_seen']:
                device['first_seen'] = device['first_seen'].isoformat()
            if device['last_seen']:
                device['last_seen'] = device['last_seen'].isoformat()
        
        return {"devices": devices}

@router.get("/admin/file-access")
async def get_file_access(user: str = None, limit: int = 50):
    """Get real file access logs"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        if user:
            cursor.execute("""
                SELECT file_name, file_path, action, file_size, 
                       COALESCE(sensitivity_level, 'internal') as sensitivity,
                       ip_address, access_time, device_id, risk_flag
                FROM file_access_logs 
                WHERE user_id = %s 
                ORDER BY access_time DESC 
                LIMIT %s
            """, (user, limit))
        else:
            cursor.execute("""
                SELECT user_id, file_name, file_path, action, file_size, 
                       COALESCE(sensitivity_level, 'internal') as sensitivity,
                       ip_address, access_time, device_id, risk_flag
                FROM file_access_logs 
                ORDER BY access_time DESC 
                LIMIT %s
            """, (limit,))
        
        file_logs = cursor.fetchall()
        
        for log in file_logs:
            if log.get('access_time'):
                log['access_time'] = log['access_time'].isoformat()
        
        return {"file_logs": file_logs}

@router.get("/admin/login-history/{username}")
async def get_login_history(username: str):
    """Get real login history"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.login_time, l.logout_time, l.ip_address, l.city, l.country, 
                   l.success, l.failure_reason, l.device_fingerprint, l.user_agent,
                   COALESCE(l.mac_address, 'N/A') as mac_address,
                   COALESCE(l.hostname, 'N/A') as hostname,
                   COALESCE(l.device_os, 'N/A') as device_os,
                   COALESCE(l.wifi_ssid, 'N/A') as wifi_ssid
            FROM login_logs l
            WHERE l.user_id = %s 
            ORDER BY l.login_time DESC 
            LIMIT 20
        """, (username,))
        
        login_history = cursor.fetchall()
        
        for login in login_history:
            if login['login_time']:
                login['login_time'] = login['login_time'].isoformat()
            if login['logout_time']:
                login['logout_time'] = login['logout_time'].isoformat()
        
        return {"login_history": login_history}

@router.get("/admin/network-activity")
async def get_network_activity(user: str = None, limit: int = 50):
    """Get real network activity"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        if user:
            cursor.execute("""
                SELECT user_id, 
                       COALESCE(connection_type, 'Unknown') as connection,
                       CONCAT(COALESCE(remote_ip, 'N/A'), ':', COALESCE(remote_port, 0)) as destination,
                       COALESCE(protocol, 'N/A') as protocol,
                       remote_port as port,
                       external, 
                       timestamp
                FROM network_logs 
                WHERE user_id = %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (user, limit))
        else:
            cursor.execute("""
                SELECT user_id, 
                       COALESCE(connection_type, 'Unknown') as connection,
                       CONCAT(COALESCE(remote_ip, 'N/A'), ':', COALESCE(remote_port, 0)) as destination,
                       COALESCE(protocol, 'N/A') as protocol,
                       remote_port as port,
                       external, 
                       timestamp
                FROM network_logs 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (limit,))
        
        network_logs = cursor.fetchall()
        
        for log in network_logs:
            if log.get('timestamp'):
                log['timestamp'] = log['timestamp'].isoformat()
        
        return {"network_logs": network_logs}

@router.get("/security/analyze/admin")
async def get_security_analysis():
    """Get real user security analysis"""
    from advanced_ueba import calculate_advanced_risk
    
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get active users
        cursor.execute("""
            SELECT u.username, u.status,
                   (SELECT COUNT(*) FROM login_logs WHERE user_id = u.username) as login_count
            FROM users u
            WHERE u.status = 'active'
        """)
        
        users = cursor.fetchall()
        
        # Get additional info for each user
        for user in users:
            # Calculate dynamic risk score
            db2 = get_db()
            risk_data = calculate_advanced_risk(user['username'], db2)
            db2.close()
            
            user['risk_score'] = risk_data['risk_score']
            user['risk_level'] = risk_data['risk_level']
            user['decision'] = risk_data['decision']
            user['zone'] = risk_data['zone']
            user['signals'] = risk_data['signals']
            
            # Get latest device
            cursor.execute("""
                SELECT hostname, ip_address, device_id, mac_address, os, wifi_ssid
                FROM device_logs
                WHERE user_id = %s
                ORDER BY last_seen DESC
                LIMIT 1
            """, (user['username'],))
            device = cursor.fetchone()
            
            # Get latest login
            cursor.execute("""
                SELECT city, country, login_time
                FROM login_logs
                WHERE user_id = %s
                ORDER BY login_time DESC
                LIMIT 1
            """, (user['username'],))
            login = cursor.fetchone()
            
            # Merge data
            if device:
                user.update(device)
            else:
                user.update({'hostname': 'N/A', 'ip_address': 'N/A', 'device_id': 'N/A', 'mac_address': 'N/A', 'os': 'N/A', 'wifi_ssid': 'N/A'})
            
            if login:
                user['city'] = login['city']
                user['country'] = login['country']
                user['login_time'] = login['login_time'].isoformat() if login['login_time'] else None
            else:
                user['city'] = 'Unknown'
                user['country'] = 'Unknown'
                user['login_time'] = None
        
        return {"users": users}

@router.get("/admin/audit-chain")
async def get_audit_chain():
    """Get blockchain audit trail"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT block_index, timestamp, event_type, user_id, event_data,
                   current_hash, previous_hash
            FROM blockchain_audit 
            ORDER BY block_index DESC 
            LIMIT 50
        """)
        
        blockchain = cursor.fetchall()
        
        # Convert datetime to string
        for block in blockchain:
            if block['timestamp']:
                block['timestamp'] = block['timestamp'].isoformat()
            if block['event_data']:
                block['event_data'] = json.loads(block['event_data'])
        
        return {"blockchain": blockchain}

@router.post("/track/login")
async def track_login_endpoint(data: dict):
    """Track user login"""
    session_id = ActivityTracker.track_login(
        user_id=data['username'],
        ip_address=data.get('ip_address', '127.0.0.1'),
        mac_address=data.get('mac_address', 'unknown'),
        hostname=data.get('hostname', 'unknown'),
        os_info=data.get('os', 'unknown'),
        wifi_ssid=data.get('wifi_ssid', 'unknown'),
        user_agent=data.get('user_agent', 'unknown'),
        success=data.get('success', True)
    )
    return {"session_id": session_id}

@router.post("/track/file-access")
async def track_file_access_endpoint(data: dict):
    """Track file access"""
    ActivityTracker.track_file_access(
        user_id=data['username'],
        file_name=data['file_name'],
        file_path=data.get('file_path', ''),
        action=data['action'],
        file_size=data.get('file_size', 0),
        ip_address=data.get('ip_address'),
        device_id=data.get('device_id')
    )
    return {"status": "tracked"}

@router.post("/track/network")
async def track_network_endpoint(data: dict):
    """Track network connection"""
    ActivityTracker.track_network_connection(
        user_id=data['username'],
        remote_ip=data['remote_ip'],
        remote_port=data['remote_port'],
        protocol=data['protocol'],
        is_external=data.get('is_external', False)
    )
    return {"status": "tracked"}