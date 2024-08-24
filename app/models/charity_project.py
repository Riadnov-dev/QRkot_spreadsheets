from sqlalchemy import Column, String, Text

from app.models.base import BaseCharityModel


class CharityProject(BaseCharityModel):
    """Модель благотворительного проекта."""

    __tablename__ = "charityproject"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return self.name
