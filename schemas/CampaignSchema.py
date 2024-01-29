from pydantic import BaseModel
import uuid


class CreateCampaign(BaseModel):
    title: str
    description: str
    country: str
    clientId: int
    state: str
    notes: str

    class Config:
        from_attributes = True


class BaseCampaign(CreateCampaign):
    id: uuid.UUID

    class Config:
        from_attributes = True
