from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import hash_password, verify_password, create_access_token, oauth2_scheme, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone

router = APIRouter()

# Rota para gerar o token JWT
@router.post("/token", response_model=Token, status_code=201)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Use o ID do usuário como 'sub'
    access_token = create_access_token(data={"sub": user.id})  
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para adicionar um novo usuário autenticado
@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota para trocar a senha do usuário
@router.put("/me/password", response_model=dict, status_code=200)
def change_password(new_password: str = Form(...), 
                    token: str = Depends(oauth2_scheme), 
                    db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not enough permission")
    user.hashed_password = hash_password(new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# Rota para deletar o próprio usuário
@router.delete("/me", status_code=204)
def delete_me(token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    user_to_delete = db.query(User).filter(User.id == current_user.id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    if user_to_delete.id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own user")
    db.delete(user_to_delete)
    db.commit()

