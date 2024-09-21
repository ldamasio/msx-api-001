from pydantic import BaseModel

class VehicleBase(BaseModel):
    name: str
    brand: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True
