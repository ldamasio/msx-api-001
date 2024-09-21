from pydantic import BaseSettings
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()