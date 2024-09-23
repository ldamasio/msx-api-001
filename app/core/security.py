from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import jwt
from app.models.user import User


# Cria uma instância do PasswordHash com o algoritmo recomendado (Argon2)
password_hash = PasswordHash.recommended()

# Função para hashear uma senha usando Argon2.
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# Função para verificar se a senha corresponde ao seu hash
def verify_password(hashed_password: str, password: str) -> bool:
    return password_hash.verify(hashed_password, password)

# Função para criar um token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

# Configuração do OAuth2 para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para obter o usuário atual logado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, 
        settings.JWT_SECRET_KEY, 
        algorithms=[settings.JWT_ALGORITHM]
        )
        # Assume que o ID do usuário está no campo 'sub'
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, 
            detail="Invalid authentication credentials"
            )
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user  # Retorna o usuário encontrado
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, 
        detail="Invalid authentication credentials")