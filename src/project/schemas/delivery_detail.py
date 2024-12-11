from pydantic import BaseModel, Field, ConfigDict

class DeliveryDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    delivery_id: int
    product_id: int
    quantity: int
    price: float