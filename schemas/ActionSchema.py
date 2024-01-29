from pydantic import BaseModel
import uuid


class CreateAction(BaseModel):
    title: str
    description: str
    campaignId: int
    state: str
    notes: str

    class Config:
        from_attributes = True


class BaseAction(CreateAction):
    id: uuid.UUID

    class Config:
        from_attributes = True
