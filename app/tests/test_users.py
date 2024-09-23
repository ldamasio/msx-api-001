import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, oauth2_scheme
import random
import string

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.close()

def generate_random_username(length=10):
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    return username

def get_token(username: str, password: str):
    user_data = {"username": username, "password": password}
    response = client.post("/users/token", data=user_data)
    assert response.status_code == 201
    return response.json()["access_token"]

def create_user(db: Session, username: str, password: str):
    user_data = {"username": username, "password": password}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.json()

def test_create_user(db: Session):
    random_username0 = generate_random_username()
    user_data = create_user(db, random_username0, "testpass")
    #Verifica se o username foi criado
    assert user_data["username"] == random_username0

def test_delete_self(db: Session):
    random_username1 = generate_random_username()
    user_data = create_user(db, random_username1, "testpass")
    token = get_token(random_username1, "testpass")
    response = client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_change_password(db: Session):
    random_username2 = generate_random_username()
    user_data = create_user(db, random_username2, "oldpass")
    token = get_token(random_username2, "oldpass")
    new_password = "StrongP@ss123"
    response = client.put("/users/me/password", data={"new_password": new_password}, headers={"Authorization": f"Bearer {token}"})
    print('pedro')
    print(response.json())
    print('pedro')
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"
    # Verifica se a nova senha funciona (tenta logar com a nova senha)
    login_response = client.post("/users/token", data={"username": random_username2, "password": new_password})
    assert login_response.status_code == 201

