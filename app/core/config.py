from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    PROJECT_NAME: str = "API MSX Veículos"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()
