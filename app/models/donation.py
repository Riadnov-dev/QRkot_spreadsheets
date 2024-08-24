from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseCharityModel


class Donation(BaseCharityModel):
    """Модель пожертвования."""

    __tablename__ = "donation"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text, nullable=True)
