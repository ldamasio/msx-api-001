import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

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
