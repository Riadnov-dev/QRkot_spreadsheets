from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения данных о пользователе."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания нового пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""
