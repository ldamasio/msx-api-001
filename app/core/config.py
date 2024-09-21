from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

print (BASE_DIR)
print (os.getenv('DATABASE_URL'))
print (os.getenv('SECRET_KEY'))
print (os.getenv('ALGORITHM'))
print (os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
print (int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
print (type(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
print (type(int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))))


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()
