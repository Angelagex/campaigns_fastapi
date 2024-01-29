from backend.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Campaigns(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    country = Column(String, nullable=False)
    clientId = Column(UUID(as_uuid=True), ForeignKey('clients.id'), nullable=False)
    state = Column(String, nullable=False)
    notes = Column(String, nullable=True)
