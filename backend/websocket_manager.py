from fastapi import WebSocket
from typing import List, Dict
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user:
            if user not in self.user_connections:
                self.user_connections[user] = []
            self.user_connections[user].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user: str = None):
        self.active_connections.remove(websocket)
        if user and user in self.user_connections:
            if websocket in self.user_connections[user]:
                self.user_connections[user].remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass
    
    async def send_to_user(self, user: str, message: dict):
        if user in self.user_connections:
            for connection in self.user_connections[user]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()
