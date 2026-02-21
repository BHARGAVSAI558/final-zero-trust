from fastapi import APIRouter, HTTPException, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse
from mysql_database import get_db
from activity_tracker import ActivityTracker
import os
import json
from datetime import datetime

router = APIRouter()

@router.get("/files/read/{filename}")
async def read_file(filename: str, user: str = None, action: str = "read"):
    """Read file by filename"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM files WHERE file_name = %s AND is_deleted = 0", (filename,))
        file = cursor.fetchone()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        content = file['file_content']
        sensitivity = file['sensitivity_level']
        
        # Track access in separate transaction
        if user:
            try:
                cursor.execute("""
                    INSERT INTO file_access_logs (user_id, file_name, action, sensitivity_level)
                    VALUES (%s, %s, %s, %s)
                """, (user, filename, action.upper(), sensitivity))
                conn.commit()
            except:
                pass
        
        return {"content": content, "filename": filename}
    finally:
        cursor.close()
        conn.close()

@router.post("/files/edit")
async def edit_file_legacy(request: Request):
    """Edit file by filename"""
    data = await request.json()
    filename = data.get('filename')
    content = data.get('content')
    user = data.get('user')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE files SET file_content = %s, file_size = %s
            WHERE file_name = %s AND is_deleted = 0
        """, (content, len(content.encode('utf-8')), filename))
        conn.commit()
        
        if user:
            cursor.execute("""
                INSERT INTO file_access_logs (user_id, file_name, action)
                VALUES (%s, %s, 'EDIT')
            """, (user, filename))
            conn.commit()
        
        return {"status": "SUCCESS"}
    finally:
        cursor.close()
        conn.close()

@router.post("/files/delete")
async def delete_file_legacy(request: Request):
    """Delete file by filename"""
    data = await request.json()
    filename = data.get('filename')
    user = data.get('user')
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE files SET is_deleted = 1 WHERE file_name = %s", (filename,))
        conn.commit()
        
        if user:
            cursor.execute("""
                INSERT INTO file_access_logs (user_id, file_name, action)
                VALUES (%s, %s, 'DELETE')
            """, (user, filename))
            conn.commit()
        
        return {"status": "SUCCESS"}
    finally:
        cursor.close()
        conn.close()

@router.get("/files/list")
async def list_files_legacy():
    """Legacy endpoint for file listing"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT file_name as name, file_size as size, 
                   sensitivity_level as sensitivity, updated_at as modified
            FROM files 
            WHERE is_deleted = 0 
            ORDER BY updated_at DESC
        """)
        files = cursor.fetchall()
        
        for file in files:
            file['modified'] = file['modified'].isoformat()
        
        cursor.close()
        conn.close()
        return {"files": files}
    except Exception as e:
        return {"files": []}

@router.get("/files")
async def list_files():
    """Get all files from database"""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, file_name, file_path, file_size, file_type, 
                   sensitivity_level, owner_id, created_at, updated_at
            FROM files 
            WHERE is_deleted = 0 
            ORDER BY updated_at DESC
        """)
        files = cursor.fetchall()
        
        # Convert datetime to string
        for file in files:
            file['created_at'] = file['created_at'].isoformat()
            file['updated_at'] = file['updated_at'].isoformat()
        
        cursor.close()
        conn.close()
        return {"files": files}
    except Exception as e:
        return {"files": []}

@router.get("/files/{file_id}")
async def get_file(file_id: int, username: str = None):
    """Get file content and track access"""
    try:
        with get_db() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM files WHERE id = %s AND is_deleted = 0", (file_id,))
            file = cursor.fetchone()
            
            if not file:
                raise HTTPException(status_code=404, detail="File not found")
            
            # Track file access if username provided
            if username:
                ActivityTracker.track_file_access(
                    user_id=username,
                    file_name=file['file_name'],
                    file_path=file['file_path'],
                    action='READ',
                    file_size=file['file_size']
                )
            
            return {
                "id": file['id'],
                "file_name": file['file_name'],
                "content": file['file_content'],
                "file_size": file['file_size'],
                "sensitivity_level": file['sensitivity_level'],
                "created_at": file['created_at'].isoformat(),
                "updated_at": file['updated_at'].isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/files/{file_id}/edit")
async def edit_file(file_id: int, request: Request):
    """Edit file content and track changes"""
    try:
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
            if username:
                ActivityTracker.track_file_access(
                    user_id=username,
                    file_name=file['file_name'],
                    file_path=file['file_path'],
                    action='WRITE',
                    file_size=new_size
                )
            
            return {"status": "SUCCESS", "message": "File updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/files/create")
async def create_file(request: Request):
    """Create new file and track creation"""
    try:
        data = await request.json()
        username = data.get('username')
        file_name = data.get('file_name')
        file_content = data.get('content', '')
        sensitivity = data.get('sensitivity', 'internal')
        
        with get_db() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # Check if file already exists
            cursor.execute("SELECT id FROM files WHERE file_name = %s AND is_deleted = 0", (file_name,))
            existing = cursor.fetchone()
            
            if existing:
                raise HTTPException(status_code=400, detail="File already exists")
            
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
            if username:
                ActivityTracker.track_file_access(
                    user_id=username,
                    file_name=file_name,
                    file_path=file_path,
                    action='CREATE',
                    file_size=file_size
                )
            
            return {"status": "SUCCESS", "file_id": file_id, "message": "File created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{file_id}")
async def delete_file(file_id: int, username: str = None):
    """Delete file and track deletion"""
    try:
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
            if username:
                ActivityTracker.track_file_access(
                    user_id=username,
                    file_name=file['file_name'],
                    file_path=file['file_path'],
                    action='DELETE',
                    file_size=file['file_size']
                )
            
            return {"status": "SUCCESS", "message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/files/access")
async def track_file_access(request: Request):
    """Track file access for real-time monitoring"""
    try:
        data = await request.json()
        username = data.get('user_id') or data.get('username')
        file_name = data.get('file_name')
        action = data.get('action', 'read')
        
        if username and file_name:
            ActivityTracker.track_file_access(
                user_id=username,
                file_name=file_name,
                file_path=f"/files/{file_name}",
                action=action.upper()
            )
        
        return {"status": "SUCCESS", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}