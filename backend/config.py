from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "zerotrust"
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    
    RATE_LIMIT_PER_MINUTE: int = 10
    IPINFO_TOKEN: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
