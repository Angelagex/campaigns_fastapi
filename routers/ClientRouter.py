from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status
from backend.database import db_dependency
from models.Clients import Clients
from models.Campaigns import Campaigns
from schemas.ClientSchema import CreateClient, BaseClient
router = APIRouter()
import uuid


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BaseClient)
async def create_client(client: CreateClient, db: db_dependency):
    db_client = Clients(**client.model_dump())
    db_client.id = uuid.UUID(uuid.uuid4().hex)
    print(db_client)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[BaseClient])
async def get_all_clients(db: db_dependency):
    clients = db.query(Clients).all()
    if not clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existing clients")
    return clients


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_client_by_id(client_id: int, db: db_dependency):

    deleted_client = db.query(Clients).filter(Clients.id == client_id).first()

    if deleted_client is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {client_id} you requested for does not exist")

    campaigns_related = db.query(Campaigns).filter(Campaigns.clientId == client_id).first()

    if len(campaigns_related) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The id: {client_id} have related campaigns, delete them first before proceed")
    deleted_client.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=BaseClient)
def update_client_by_id(update_client: CreateClient, client_id: int, db: db_dependency):

    client = db.query(Clients).filter(Clients.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{client_id} does not exist")
    client.update(**update_client.model_dump(), synchronize_session=False)
    db.commit()

    return client
