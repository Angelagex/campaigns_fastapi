from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status
from backend.database import db_dependency
from models.Campaigns import Campaigns
from schemas.CampaignSchema import CreateCampaign, BaseCampaign
router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BaseCampaign)
async def create_campaign(campaign: CreateCampaign, db: db_dependency):
    #db_campaign = Campaigns(title=campaign.title, description=campaign.description, country=campaign.country, clientId=campaign.clientId, state=campaign.state, notes=campaign.notes)
    db_campaign = Campaigns(**campaign.model_dump())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@router.get('/{client_id}', status_code=status.HTTP_200_OK, response_model=List[BaseCampaign])
async def get_campaign_by_client_id(client_id: int, db: db_dependency):
    campaigns = db.query(Campaigns).filter(Campaigns.clientId == client_id).all()
    if not campaigns:
        raise HTTPException(status_code=404, detail="No campaigns for this client")
    return campaigns


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign_by_id(campaign_id: int, db: db_dependency):

    deleted_campaign = db.query(Campaigns).filter(Campaigns.id == campaign_id).first()

    if deleted_campaign is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {campaign_id} you requested for does not exist")
    deleted_campaign.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', response_model=BaseCampaign)
def update_campaign_by_id(update_campaign: CreateCampaign, campaign_id: int, db: db_dependency):

    campaign = db.query(Campaigns).filter(Campaigns.id == campaign_id).first()

    if campaign is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{campaign_id} does not exist")
    campaign.update(update_campaign.model_dump(), synchronize_session=False)
    db.commit()

    return campaign
