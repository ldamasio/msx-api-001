from pydantic import BaseModel
from datetime import datetime

# Classe base que será herdada por outras classes
class VehicleBase(BaseModel):
    name: str
    brand: str
    year: int

    # Definindo a configuração de ORM na classe base (parent)
    class ConfigDict():
        from_attributes = True

# Classe para criação de um veículo
class VehicleCreate(VehicleBase):
    pass

# Classe para leitura de um veículo
class VehicleRead(VehicleBase):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
