from fastapi import FastAPI
from models import Clients, Campaigns, Actions
from backend.database import engine
from routers import CampaignRouter, ClientRouter, ActionRouter

app = FastAPI()
Campaigns.Base.metadata.create_all(bind=engine)
Actions.Base.metadata.create_all(bind=engine)
Clients.Base.metadata.create_all(bind=engine)


app.include_router(CampaignRouter.router, tags=['Campaigns'], prefix='/api/campaigns')
app.include_router(ClientRouter.router, tags=['Clients'], prefix='/api/clients')
app.include_router(ActionRouter.router, tags=['Actions'], prefix='/api/actions')


@app.get("/api/healthchecker")
async def root():
    return {"message": "Hello World"}


