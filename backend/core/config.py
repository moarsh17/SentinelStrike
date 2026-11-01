import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentinel.db")
    TEST_SERVER_IP: str = os.getenv("TEST_SERVER_IP", "127.0.0.1")
    INTERFACE: str = os.getenv("INTERFACE", r"\Device\NPF_Loopback")  # Interface for PyShark to sniff on

settings = Settings()
