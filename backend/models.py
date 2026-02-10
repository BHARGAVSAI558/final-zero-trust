from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: str
    role: str

class HeartbeatPayload(BaseModel):
    user: str
    ip_address: str
    mac_address: str
    wifi_ssid: str
    hostname: str
    os: str
    timestamp: str
    fingerprint: str
