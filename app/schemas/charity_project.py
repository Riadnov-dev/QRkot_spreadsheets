from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.base import BaseDB


class CharityProjectBase(BaseModel):
    """Базовая pydantic-схема благотворительного проекта."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic-схема для обновления благотворительного проекта."""

    class Config:
        schema_extra = {
            "examples": {
                "example_1": {
                    "summary": "Изменение медицинского фонда для котов",
                    "description": "Обновление информации о сборе средств",
                    "value": {
                        "name": "Cat Medical Fund",
                        "description": "Raising funds for medical treatment",
                        "full_amount": 25000,
                    },
                },
                "example_2": {
                    "summary": "Изменение зимнего убежища для котов",
                    "description": "Обновление информации о строительстве",
                    "value": {
                        "name": "Winter Shelter for Cats",
                        "description": "Building a warm shelter for cats",
                        "full_amount": 40000,
                    },
                },
            }
        }

    @validator("name", "description", "full_amount")
    def fields_cannot_be_null(cls, value):
        """Проверяет, что при изменении обязательных полей объекта,
        их значения не стали пустыми."""
        if value is None:
            raise ValueError("Поле не может быть пустым!")
        return value


class CharityProjectCreate(CharityProjectBase):
    """Pydantic-схема для создания благотворительного проекта."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            "examples": {
                "example_1": {
                    "summary": "Создание фонда на покупку корма для котов",
                    "description": "Сбор средств на покупку корма",
                    "value": {
                        "name": "Cat Food Fund",
                        "description": "Raising funds to buy quality food",
                        "full_amount": 15000,
                    },
                },
                "example_2": {
                    "summary": "Создание фонда для стерилизации котов",
                    "description": "Сбор средств для стерилизации",
                    "value": {
                        "name": "Cat Sterilization Fund",
                        "description": "Raising funds for sterilization",
                        "full_amount": 30000,
                    },
                },
            }
        }


class CharityProjectDB(CharityProjectBase, BaseDB):
    """Pydantic-схема для вывода информации о благотворительном проекте."""

    pass
