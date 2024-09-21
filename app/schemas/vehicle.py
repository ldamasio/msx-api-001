from pydantic import BaseModel, ConfigDict

class VehicleBase(BaseModel):
    name: str
    brand: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    created_at: str
    updated_at: str

    class ConfigDict():
        from_attributes = True
