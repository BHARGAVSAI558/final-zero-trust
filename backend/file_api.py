"""
File Management API for Zero Trust Demo
Handles CRUD operations with recycle bin
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import shutil
from datetime import datetime
from typing import List, Optional

router = APIRouter()

DEMO_FILES_DIR = "demo_files"
RECYCLE_BIN_DIR = "demo_files/recycle_bin"

# Ensure directories exist
os.makedirs(DEMO_FILES_DIR, exist_ok=True)
os.makedirs(RECYCLE_BIN_DIR, exist_ok=True)

class FileInfo(BaseModel):
    name: str
    sensitivity: str
    size: int
    modified: str
    content: Optional[str] = None

class FileOperation(BaseModel):
    filename: str
    content: Optional[str] = None
    user: str

# File sensitivity mapping
SENSITIVITY_MAP = {
    "dashboard.html": "public",
    "reports.pdf": "internal",
    "analytics.xlsx": "internal",
    "profile.json": "public",
    "admin.config": "sensitive",
    "credentials.txt": "sensitive",
    "database.sql": "critical",
    "secrets.env": "critical"
}

@router.get("/files/list")
async def list_files():
    """List all files in demo directory"""
    files = []
    for filename in os.listdir(DEMO_FILES_DIR):
        filepath = os.path.join(DEMO_FILES_DIR, filename)
        if os.path.isfile(filepath) and filename != ".gitkeep":
            stat = os.stat(filepath)
            files.append({
                "name": filename,
                "sensitivity": SENSITIVITY_MAP.get(filename, "internal"),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    return {"files": files}

@router.get("/files/read/{filename}")
async def read_file(filename: str, user: str):
    """Read file content"""
    filepath = os.path.join(DEMO_FILES_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(404, "File not found")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Log to backend
        import requests
        requests.post("http://localhost:8000/files/access", json={
            "user_id": user,
            "file_name": filename,
            "action": "READ"
        }, timeout=2)
        
        return {"filename": filename, "content": content, "size": len(content)}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/files/edit")
async def edit_file(operation: FileOperation):
    """Edit file content"""
    filepath = os.path.join(DEMO_FILES_DIR, operation.filename)
    if not os.path.exists(filepath):
        raise HTTPException(404, "File not found")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(operation.content)
        
        # Log to backend
        import requests
        requests.post("http://localhost:8000/files/access", json={
            "user_id": operation.user,
            "file_name": operation.filename,
            "action": "WRITE"
        }, timeout=2)
        
        return {"status": "SUCCESS", "message": f"{operation.filename} updated"}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/files/delete")
async def delete_file(operation: FileOperation):
    """Move file to recycle bin"""
    filepath = os.path.join(DEMO_FILES_DIR, operation.filename)
    if not os.path.exists(filepath):
        raise HTTPException(404, "File not found")
    
    try:
        # Move to recycle bin with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        recycled_name = f"{timestamp}_{operation.filename}"
        recycle_path = os.path.join(RECYCLE_BIN_DIR, recycled_name)
        shutil.move(filepath, recycle_path)
        
        # Log to backend
        import requests
        requests.post("http://localhost:8000/files/access", json={
            "user_id": operation.user,
            "file_name": operation.filename,
            "action": "DELETE"
        }, timeout=2)
        
        return {"status": "SUCCESS", "message": f"{operation.filename} moved to recycle bin"}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/files/recycle-bin")
async def list_recycle_bin():
    """List files in recycle bin"""
    files = []
    for filename in os.listdir(RECYCLE_BIN_DIR):
        filepath = os.path.join(RECYCLE_BIN_DIR, filename)
        if os.path.isfile(filepath):
            # Extract original filename (remove timestamp prefix)
            original_name = "_".join(filename.split("_")[2:]) if "_" in filename else filename
            stat = os.stat(filepath)
            files.append({
                "name": filename,
                "original_name": original_name,
                "size": stat.st_size,
                "deleted": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    return {"files": files}

@router.post("/files/restore")
async def restore_file(operation: FileOperation):
    """Restore file from recycle bin"""
    recycle_path = os.path.join(RECYCLE_BIN_DIR, operation.filename)
    if not os.path.exists(recycle_path):
        raise HTTPException(404, "File not found in recycle bin")
    
    try:
        # Extract original filename
        original_name = "_".join(operation.filename.split("_")[2:]) if "_" in operation.filename else operation.filename
        restore_path = os.path.join(DEMO_FILES_DIR, original_name)
        
        # Check if file already exists
        if os.path.exists(restore_path):
            raise HTTPException(400, f"{original_name} already exists")
        
        shutil.move(recycle_path, restore_path)
        return {"status": "SUCCESS", "message": f"{original_name} restored"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete("/files/permanent-delete")
async def permanent_delete(operation: FileOperation):
    """Permanently delete file from recycle bin"""
    recycle_path = os.path.join(RECYCLE_BIN_DIR, operation.filename)
    if not os.path.exists(recycle_path):
        raise HTTPException(404, "File not found in recycle bin")
    
    try:
        os.remove(recycle_path)
        return {"status": "SUCCESS", "message": "File permanently deleted"}
    except Exception as e:
        raise HTTPException(500, str(e))
