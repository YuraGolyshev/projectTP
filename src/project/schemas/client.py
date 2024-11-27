from pydantic import BaseModel, Field, ConfigDict


class ClientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    password: str
    phone_number: str | None = Field(default=None)
