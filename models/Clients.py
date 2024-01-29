from backend.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Clients(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    country = Column(String, nullable=True)
    area = Column(String, nullable=True)
    notes = Column(String, nullable=True)
