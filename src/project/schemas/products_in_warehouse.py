from pydantic import BaseModel, Field, ConfigDict

class ProductsInWarehouseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    storage_place_id: int
    place_number: int