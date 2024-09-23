import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
import string
import random

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

def create_user(db: Session, username: str, password: str):
    user_data = {"username": username, "password": password}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    return response.json()

def get_token(username: str, password: str):
    user_data = {"username": username, "password": password}
    response = client.post("/users/token", data=user_data)
    assert response.status_code == 201
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def authenticated_client(db: Session):
    # Cria um usuário para os testes
    username = generate_random_username()
    password = "testpass"
    create_user(db, username, password)
    # Obtém o token de acesso do usuário criado
    token = get_token(username, password)
    # Adiciona o token ao cliente para as requisições subsequentes
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client  # Retorna o cliente autenticado

def create_vehicle(client: TestClient, db: Session, name: str, brand: str, year: int) -> int:
    response = client.post("/vehicles/", json={
        "name": name,
        "brand": brand,
        "year": year
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name
    assert data["brand"] == brand
    assert data["year"] == year
    return data["id"]

# Testa se um veículo é criado com sucesso
def test_create_vehicle(authenticated_client, db):
    vehicle_id = create_vehicle(authenticated_client, db, "Toyota bZ4X", "Toyota", 2024)

# Testa se um veículo é retornado com sucesso usando um ID
def test_read_vehicle(authenticated_client, db):
    vehicle_id = create_vehicle(authenticated_client, db, "Hyundai HB20", "Hyundai", 2023)
    response = authenticated_client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    retrieved_vehicle = response.json()
    assert retrieved_vehicle["name"] == "Hyundai HB20"
    assert retrieved_vehicle["brand"] == "Hyundai"
    assert retrieved_vehicle["year"] == 2023

def test_vehicles_pagination(authenticated_client, db):
    # Cria 51 veículos para testar a paginação
    num_vehicles = 51
    for i in range(num_vehicles):
        create_vehicle(authenticated_client, db, "Hyundai HB20", "Hyundai", 2015)
    # Testa a paginação com o limite de 50 veículos
    page_size = 50
    for page in range(1, (num_vehicles // page_size) + 2):
        # Contrói a URL com os parâmetros página e tamanho
        url = f"/vehicles/?page={page}&size={page_size}"
        response = authenticated_client.get(url)
        assert response.status_code == 200
        data = response.json()
        # Verifica o limite de veículos na resposta
        assert len(data) <= page_size

# Testa a atualização do status de um veículo
def test_update_vehicle_status(authenticated_client, db):
    vehicle_id = create_vehicle(authenticated_client, db, "Hyundai HB20", "Hyundai", 2023)
    response = authenticated_client.put(f"/vehicles/{vehicle_id}", json={"status": "CONECTADO"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle status updated successfully"
    assert data["status"] == "CONECTADO"
    response = authenticated_client.put(f"/vehicles/{vehicle_id}", json={"status": "DESCONECTADO"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle status updated successfully"
    assert data["status"] == "DESCONECTADO"

def test_delete_vehicle(authenticated_client, db):
    vehicle_id = create_vehicle(authenticated_client, db, "Hyundai HB20", "Hyundai", 2023)
    response = authenticated_client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle deleted successfully"
    # Verifica se o veículo foi realmente excluído
    response = authenticated_client.get(f"/vehicles/{vehicle_id}")
    # O veículo não deve ser encontrado após a exclusão
    assert response.status_code == 404
