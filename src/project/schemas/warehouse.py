from pydantic import BaseModel, Field, ConfigDict

class WarehouseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    available_types: str
    address: str
    name: str
    available_places: int