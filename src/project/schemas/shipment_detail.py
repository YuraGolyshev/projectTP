from pydantic import BaseModel, Field, ConfigDict

class ShipmentDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    shipment_id: int
    product_id: int
    quantity: int
    price: float