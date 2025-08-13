from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data."""


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user."""


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data."""
