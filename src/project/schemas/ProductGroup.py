from pydantic import BaseModel, Field, ConfigDict

class ProductGroupSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str