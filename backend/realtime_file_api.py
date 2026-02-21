from fastapi import APIRouter, HTTPException, Depends, Request
from mysql_database import get_db
from activity_tracker import ActivityTracker
import json
from datetime import datetime

router = APIRouter()

@router.get("/files/list/{username}")
async def list_user_files(username: str):
    """Get real files from database"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, file_name, file_path, file_size, file_type, 
                   sensitivity_level, created_at, updated_at
            FROM files 
            WHERE is_deleted = 0 
            ORDER BY updated_at DESC
        """)
        files = cursor.fetchall()
        
        # Convert datetime to string
        for file in files:
            file['created_at'] = file['created_at'].isoformat()
            file['updated_at'] = file['updated_at'].isoformat()
        
        return {"files": files}

@router.get("/files/content/{file_id}")
async def get_file_content(file_id: int, username: str):
    """Get file content and track access"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM files WHERE id = %s AND is_deleted = 0", (file_id,))
        file = cursor.fetchone()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Track file access
        ActivityTracker.track_file_access(
            user_id=username,
            file_name=file['file_name'],
            file_path=file['file_path'],
            action='READ',
            file_size=file['file_size']
        )
        
        return {
            "file_name": file['file_name'],
            "file_content": file['file_content'],
            "file_size": file['file_size'],
            "sensitivity_level": file['sensitivity_level']
        }

@router.post("/files/edit/{file_id}")
async def edit_file(file_id: int, request: Request):
    """Edit file content and track changes"""
    data = await request.json()
    username = data.get('username')
    new_content = data.get('content', '')
    
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get current file
        cursor.execute("SELECT * FROM files WHERE id = %s AND is_deleted = 0", (file_id,))
        file = cursor.fetchone()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Update file content
        new_size = len(new_content.encode('utf-8'))
        cursor.execute("""
            UPDATE files SET file_content = %s, file_size = %s, updated_at = NOW()
            WHERE id = %s
        """, (new_content, new_size, file_id))
        
        # Track file modification
        ActivityTracker.track_file_access(
            user_id=username,
            file_name=file['file_name'],
            file_path=file['file_path'],
            action='WRITE',
            file_size=new_size
        )
        
        return {"status": "SUCCESS", "message": "File updated successfully"}

@router.post("/files/create")
async def create_file(request: Request):
    """Create new file and track creation"""
    data = await request.json()
    username = data.get('username')
    file_name = data.get('file_name')
    file_content = data.get('content', '')
    sensitivity = data.get('sensitivity', 'internal')
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        file_path = f"/user_files/{file_name}"
        file_size = len(file_content.encode('utf-8'))
        file_type = file_name.split('.')[-1] if '.' in file_name else 'txt'
        
        cursor.execute("""
            INSERT INTO files (file_name, file_path, file_content, file_size, 
                             file_type, sensitivity_level, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (file_name, file_path, file_content, file_size, file_type, sensitivity, username))
        
        file_id = cursor.lastrowid
        
        # Track file creation
        ActivityTracker.track_file_access(
            user_id=username,
            file_name=file_name,
            file_path=file_path,
            action='CREATE',
            file_size=file_size
        )
        
        return {"status": "SUCCESS", "file_id": file_id, "message": "File created successfully"}

@router.delete("/files/delete/{file_id}")
async def delete_file(file_id: int, username: str):
    """Delete file and track deletion"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get file info before deletion
        cursor.execute("SELECT * FROM files WHERE id = %s AND is_deleted = 0", (file_id,))
        file = cursor.fetchone()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Mark as deleted
        cursor.execute("UPDATE files SET is_deleted = 1 WHERE id = %s", (file_id,))
        
        # Track file deletion
        ActivityTracker.track_file_access(
            user_id=username,
            file_name=file['file_name'],
            file_path=file['file_path'],
            action='DELETE',
            file_size=file['file_size']
        )
        
        return {"status": "SUCCESS", "message": "File deleted successfully"}

@router.get("/files/recent-activity/{username}")
async def get_recent_activity(username: str, limit: int = 20):
    """Get user's recent file activity"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT file_name, file_path, action, file_size, 
                   sensitivity_level, access_time, ip_address
            FROM file_access_logs 
            WHERE user_id = %s 
            ORDER BY access_time DESC 
            LIMIT %s
        """, (username, limit))
        
        activities = cursor.fetchall()
        
        # Convert datetime to string
        for activity in activities:
            activity['access_time'] = activity['access_time'].isoformat()
        
        return {"activities": activities}