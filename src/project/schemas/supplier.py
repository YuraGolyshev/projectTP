from pydantic import BaseModel, Field, ConfigDict

class SupplierSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str