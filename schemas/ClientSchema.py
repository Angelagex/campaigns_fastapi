from pydantic import BaseModel
import uuid


class CreateClient(BaseModel):
    name: str
    email: str
    phone: str
    country: str
    area: str
    notes: str

    class Config:
        from_attributes = True


class BaseClient(CreateClient):
    id: uuid.UUID

    class Config:
        from_attributes = True
