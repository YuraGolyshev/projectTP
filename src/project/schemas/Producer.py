from pydantic import BaseModel, Field, ConfigDict

class ProducerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str