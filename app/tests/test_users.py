import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password  # Importando as funções de segurança

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.close()

def create_user(db: Session, username: str, password: str):
    response = client.post("/users/", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()

def get_token(username: str, password: str):
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_user(db: Session):
    user_data = create_user(db, "testuser", "testpass")
    assert user_data["username"] == "testuser"
    
    # Verifica se a senha foi hashada corretamente
    assert verify_password(user_data["hashed_password"], "testpass")

def test_delete_self(db: Session):
    user_data = create_user(db, "testuser_delete", "testpass")
    token = get_token("testuser_delete", "testpass")

    response = client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_change_password(db: Session):
    user_data = create_user(db, "testuser_change_pass", "oldpass")
    token = get_token("testuser_change_pass", "oldpass")

    new_password = "newpass"
    response = client.put("/users/me/password", json={"new_password": new_password}, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    # Verifica se a nova senha funciona (tenta logar com a nova senha)
    login_response = client.post("/token", data={"username": "testuser_change_pass", "password": new_password})
    assert login_response.status_code == 200

def test_fail_delete_other_user(db: Session):
    user1_data = create_user(db, "user1", "pass1")
    user2_data = create_user(db, "user2", "pass2")
    
    token1 = get_token("user1", "pass1")

    # Tenta deletar o segundo usuário com o token do primeiro usuário
    response = client.delete("/users/me", headers={"Authorization": f"Bearer {token1}"})
    
    assert response.status_code == 403  # Espera-se que não possa deletar outro usuário
