from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseDB(BaseModel):
    """Базовая pydantic-схема для вывода информации об объектах."""

    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
