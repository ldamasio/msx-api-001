from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import get_db
from app.models.vehicle import Vehicle
# from app.schemas.vehicle import VehicleCreate, VehicleRead

router = APIRouter()

@router.post("/", status_code=201)
def create_vehicle(vehicle: dict):
    return {'msg':'hello-world'}

# @router.post("/", response_model=VehicleRead, status_code=201)
# def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
#     db_vehicle = Vehicle(**vehicle.dict())
#     db.add(db_vehicle)
#     db.commit()
#     db.refresh(db_vehicle)
#     return db_vehicle
