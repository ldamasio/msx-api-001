from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from pwdlib.hash import argon2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rota para adicionar um novo usuário
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = argon2.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota para deletar o próprio usuário
@router.delete("/me", response_model=dict)
def delete_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Aqui você deve decodificar o token para obter o usuário atual
    current_user = get_current_user(token)  # Implementar essa função conforme necessário
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Rota para trocar a senha do usuário
@router.put("/me/password")
def change_password(new_password: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token)  # Implementar essa função conforme necessário
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = argon2.hash(new_password)
    db.commit()
    return {"message": "Password updated successfully"}

