from typing import List

from fastapi import APIRouter, HTTPException
from starlette import status
from backend.database import db_dependency
from models.Actions import Actions
from schemas.ActionSchema import CreateAction, BaseAction
router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BaseAction)
async def create_action(action: CreateAction, db: db_dependency):
    db_action = Actions(**action.model_dump())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action


@router.get('/{campaign_id}', status_code=status.HTTP_200_OK, response_model=List[BaseAction])
async def get_action_by_campaign_id(campaign_id: int, db: db_dependency):
    actions = db.query(Actions).filter(Actions.campaignId == campaign_id).all()
    if not actions:
        raise HTTPException(status_code=404, detail="No actions for this campaign")
    return actions


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_action_by_id(action_id: int, db: db_dependency):

    deleted_action = db.query(Actions).filter(Actions.id == action_id).first()

    if deleted_action is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {action_id} you requested for does not exist")
    deleted_action.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=BaseAction)
def update_action_by_id(update_action: CreateAction, action_id: int, db: db_dependency):

    action = db.query(Actions).filter(Actions.id == action_id).first()

    if action is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{action_id} does not exist")
    action.update(update_action.model_dump(), synchronize_session=False)
    db.commit()

    return action
