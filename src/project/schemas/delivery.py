from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class DeliverySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_sum: float
    supplier_id: int
    delivery_date: date