from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import BaseDB

EXAMPLE = 10000


class DonationCreate(BaseModel):
    """Pydantic schema for creating a donation."""
    full_amount: PositiveInt = Field(example=EXAMPLE)
    comment: Optional[str] = None


class DonationFullDB(DonationCreate, BaseDB):
    """Pydantic schema for representing full donation details."""
    user_id: int

    class Config:
        orm_mode = True


class DonationShortDB(DonationCreate):
    """Pydantic schema for representing short donation details."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
