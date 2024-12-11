from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class ShipmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: str
    total_sum: float
    warehouse_id: int
    client_id: int
    shipment_date: date