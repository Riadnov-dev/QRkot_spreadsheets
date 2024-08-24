from typing import Generic, Optional, Type, TypeVar, Union, Any

from pydantic import BaseModel
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.core.db import Base
from app.models import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """Базовый класс для выполнения операций получения и создания объектов."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self, obj_id: int,
            session: AsyncSession
    ) -> Optional[ModelType]:
        """Получить объект модели по id."""
        obj = await session.execute(select(self.model).where(
            self.model.id == obj_id)
        )
        return obj.scalars().first()

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """Получить список объектов модели с поддержкой пагинации."""
        db_objs = await session.execute(select(self.model).offset(
            skip).limit(limit))
        return db_objs.scalars().all()

    async def create(
        self, data: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> ModelType:
        """Создать объект модели и записать в БД."""
        new_obj_data = data.dict()
        if user is not None:
            new_obj_data["user_id"] = user.id
        new_obj = self.model(**new_obj_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def get_active_objs(self, session: AsyncSession) -> list[ModelType]:
        """Получить список активных объектов модели."""
        active_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested == false())
            .order_by(self.model.id)
        )
        return active_objs.scalars().all()

    async def update(
        self,
        db_obj: ModelType,
        obj_in: Union[CreateSchemaType, dict[str, Any]],
        session: AsyncSession,
    ) -> ModelType:
        """Обновить объект модели в БД."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
