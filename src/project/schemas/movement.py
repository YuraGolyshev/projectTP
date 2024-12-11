from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class MovementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    from_storage_place_id: int
    to_storage_place_id: int
    movement_date: date