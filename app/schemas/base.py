from datetime import datetime
from typing import Optional

from pydantic import BaseModel

INVESTED_AMOUNT = 0


class BaseDB(BaseModel):
    """Base Pydantic schema for representing object information."""

    id: int
    invested_amount: int = INVESTED_AMOUNT
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
