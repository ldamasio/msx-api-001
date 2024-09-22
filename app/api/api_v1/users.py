from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings
from datetime import datetime, timedelta

# Configuração do OAuth2 para autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# Função para criar um token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decodifica o token usando a chave secreta definida nas configurações
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")  # Assume que o ID do usuário está no campo 'sub'
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user  # Retorna o usuário encontrado

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Rota para adicionar um novo usuário
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash da senha usando a função definida em security.py
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Rota para deletar o próprio usuário
@router.delete("/me", response_model=dict)
def delete_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)  # Passa o banco de dados para a função
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

# Rota para trocar a senha do usuário
@router.put("/me/password", response_model=dict)
def change_password(new_password: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)  # Passa o banco de dados para a função
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash da nova senha usando a função definida em security.py
    user.hashed_password = hash_password(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}
