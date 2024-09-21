from pydantic import BaseModel, ConfigDict

class VehicleBase(BaseModel):
    name: str
    brand: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class ConfigDict():
        from_attributes = True
