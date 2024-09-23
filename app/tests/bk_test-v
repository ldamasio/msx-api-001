import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.close()

def create_vehicle(db: Session, name: str, brand: str, year: int) -> int:
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

#Testa se um veículo é criado com sucesso
def test_create_vehicle(db: Session):
    vehicle_id = create_vehicle(db, "Toyota bZ4X", "Toyota", 2024)

#Testa se um veículo é retornado com sucesso usando um ID
def test_read_vehicle(db: Session):
  vehicle_id = create_vehicle(db, "Hyundai HB20", "Hyundai", 2023)
  response = client.get(f"/vehicles/{vehicle_id}")
  assert response.status_code == 200
  retrieved_vehicle = response.json()
  assert retrieved_vehicle["name"] == "Hyundai HB20"
  assert retrieved_vehicle["brand"] == "Hyundai"
  assert retrieved_vehicle["year"] == 2023

def test_vehicles_pagination(db: Session):
  # Cria 51 veículos para testar a paginação
  num_vehicles = 51
  for i in range(num_vehicles):
      response = client.post("/vehicles/", json={
          "name": "Hyundai HB20",
          "brand": "Hyundai",
          "year": 2015
      })
      assert response.status_code == 201
  # Testa a paginação com o limite de 50 veículos
  page_size = 50
  for page in range(1, (num_vehicles // page_size) + 2):
      # Contrói a URL com os parâmetros página e tamanho
      url = f"/vehicles/?page={page}&size={page_size}"
      response = client.get(url)
      assert response.status_code == 200
      data = response.json()

      # Verifica o limite de veículos na resposta
      assert len(data) <= page_size

# Testa a atualização do status de um veículo
def test_update_vehicle_status(db: Session):
    vehicle_id = create_vehicle(db, "Hyundai HB20", "Hyundai", 2023)
    response = client.put(f"/vehicles/{vehicle_id}", json={"status": "CONECTADO"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle status updated successfully"
    assert data["connected"] is True

    response = client.put(f"/vehicles/{vehicle_id}", json={"status": "DESCONECTADO"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle status updated successfully"
    assert data["connected"] is False

def test_delete_vehicle(db: Session):
    vehicle_id = create_vehicle(db, "Hyundai HB20", "Hyundai", 2023)
    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Vehicle deleted successfully"

    # Verifica se o veículo foi realmente excluído
    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 404  # O veículo não deve ser encontrado após a exclusão