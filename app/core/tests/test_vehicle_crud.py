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

#Testa se um veículo é criado com sucesso
def test_create_vehicle(db: Session):
    response = client.post("/vehicles/", json={
        "name": "Toyota bZ4X",
        "brand": "Toyota",
        "year": 2024
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Toyota bZ4X"
    assert data["brand"] == "Toyota"
    assert data["year"] == 2024

#Testa se um veículo é retornado com sucesso usando um ID
def test_read_vehicle(db: Session):
  vehicle_id = 1
  response = client.get(f"/vehicles/{vehicle_id}")
  assert response.status_code == 200
  retrieved_vehicle = response.json()
  assert retrieved_vehicle["name"] == "Toyota bZ4X"
  assert retrieved_vehicle["brand"] == "Toyota"
  assert retrieved_vehicle["year"] == 2024

def test_vehicles_pagination(db: Session):
  # Cria 100 veículos para testar a paginação
  num_vehicles = 100
#   for i in range(num_vehicles):
#       response = client.post("/vehicles/", json={
#           "name": "Hyundai HB20",
#           "brand": "Hyundai",
#           "year": 2015
#       })
#       assert response.status_code == 201
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

