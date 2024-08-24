from typing import Optional
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


class CRUDCharityProject(CRUDBase[CharityProject, CharityProjectUpdate]):
    """Класс для реализации уникальных методов модели CharityProject."""

    async def update(
        self, db_obj: CharityProject,
        data: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        """Внести изменения в благотворительный проект."""
        old_obj_data = jsonable_encoder(db_obj)
        new_obj_data = data.dict(exclude_unset=True)

        for field in old_obj_data:
            if field in new_obj_data:
                setattr(db_obj, field, new_obj_data[field])

        if db_obj.invested_amount >= db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self, db_obj: CharityProject, session: AsyncSession
    ) -> CharityProject:
        """Удалить благотворительный проект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получить по названию благотворительного проекта его id."""
        project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        """
        Возвращает список закрытых проектов,
        отсортированных по скорости сбора средств.
        """
        stmt = (
            select(self.model)
            .where(self.model.fully_invested.is_(True))
            .order_by(
                func.julianday(self.model.close_date) -
                func.julianday(self.model.create_date)
            )
        )
        projects = await session.execute(stmt)
        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
