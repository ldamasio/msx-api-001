from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleRead

router = APIRouter()

# Rota para criar um novo veículo
@router.post("/", response_model=VehicleRead, status_code=201)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Cria um novo veículo.

    A criação requer os campos seguintes:

    - name
    - brand
    - year
    """
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# Rota para listar todos os veículos com paginação
@router.get("/", response_model=list[VehicleRead])
def get_vehicles(
    db: Session = Depends(get_db), page: int = Query(default=1, 
        description="Page number"),
    size: int = Query(default=50, 
        maximum=50, 
        description="Number of vehicles per page")
    ):
    """
    Lista os veículos.

    A listagem obedece uma regra de paginação de no máximo 50 
    veículos por requisição.
    """
    if size > 50:
        raise HTTPException(
            status_code=400, detail="Maximum page size allowed is 50"
        )

    offset = (page - 1) * size
    vehicles = db.query(Vehicle).offset(offset).limit(size).all()
    return vehicles

# Rota para buscar um veículo por ID
@router.get("/{vehicle_id}", response_model=VehicleRead)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Lista os detalhes de um veículo particular.

    É necessário passar o parâmetro id pelo método GET do protocolo HTTP.

    Serão retornados os seguintes campos do veículo específico:

    - name
    - brand
    - year
    - id
    - created_at
    - updated_at
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle


