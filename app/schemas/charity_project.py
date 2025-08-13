from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.schemas.base import BaseDB


FULL_AMOUNT_1 = 25000
FULL_AMOUNT_2 = 40000
FULL_AMOUNT_3 = 15000
FULL_AMOUNT_4 = 30000


class CharityProjectBase(BaseModel):
    """Base Pydantic schema for a charity project."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic schema for updating a charity project."""

    class Config:
        schema_extra = {
            "examples": {
                "example_1": {
                    "summary": "Update medical fund for cats",
                    "description": "Updating fundraising information",
                    "value": {
                        "name": "Cat Medical Fund",
                        "description": "Raising funds for medical treatment",
                        "full_amount": FULL_AMOUNT_1,
                    },
                },
                "example_2": {
                    "summary": "Update winter shelter for cats",
                    "description": "Updating construction details",
                    "value": {
                        "name": "Winter Shelter for Cats",
                        "description": "Building a warm shelter for cats",
                        "full_amount": FULL_AMOUNT_2,
                    },
                },
            }
        }

    @validator("name", "description", "full_amount")
    def fields_cannot_be_null(cls, value):
        """Validate that required fields are not set to null when updating."""
        if value is None:
            raise ValueError("Field cannot be empty!")
        return value


class CharityProjectCreate(CharityProjectBase):
    """Pydantic schema for creating a charity project."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            "examples": {
                "example_1": {
                    "summary": "Create a fund for purchasing cat food",
                    "description": "Fundraising to buy food",
                    "value": {
                        "name": "Cat Food Fund",
                        "description": "Raising funds to buy quality food",
                        "full_amount": FULL_AMOUNT_3,
                    },
                },
                "example_2": {
                    "summary": "Create a fund for cat sterilization",
                    "description": "Fundraising for sterilization",
                    "value": {
                        "name": "Cat Sterilization Fund",
                        "description": "Raising funds for sterilization",
                        "full_amount": FULL_AMOUNT_4,
                    },
                },
            }
        }


class CharityProjectDB(CharityProjectBase, BaseDB):
    """Pydantic schema for representing a charity project."""
