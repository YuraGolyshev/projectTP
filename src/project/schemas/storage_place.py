from pydantic import BaseModel, Field, ConfigDict

class StoragePlaceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    storage_type: str
    warehouse_id: int
    available_places: int