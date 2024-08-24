from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def ensure_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта с указанным ID."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект с указанным ID не найден!"
        )
    return charity_project


async def ensure_project_name_is_unique(
    project_name: str, session: AsyncSession
) -> None:
    """Проверка уникальности имени проекта."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


async def ensure_project_can_be_updated(
    charity_project: CharityProject, update_data: CharityProjectUpdate
) -> None:
    """Проверка возможности обновления проекта."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Невозможно редактировать проект, так как он уже закрыт!",
        )
    if (
        update_data.full_amount and (
            update_data.full_amount < charity_project.invested_amount)
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Новая сумма не может быть меньше уже вложенной!"
        )


async def ensure_project_is_not_funded(charity_project: CharityProject
                                       ) -> None:
    """Проверка на отсутствие внесенных средств в проект."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект уже профинансирован, удаление невозможно!"
        )
