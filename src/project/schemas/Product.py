from pydantic import BaseModel, Field, ConfigDict

class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    article: int
    unit: str
    product_group_id: int
    producer_id: int