from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def ensure_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Check if a project with the given ID exists."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Project with the specified ID not found!"
        )
    return charity_project


async def ensure_project_name_is_unique(
    project_name: str, session: AsyncSession
) -> None:
    """Check if the project name is unique."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A project with this name already exists!"
        )


async def ensure_project_can_be_updated(
    charity_project: CharityProject, update_data: CharityProjectUpdate
) -> None:
    """Check if the project can be updated."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="It is not possible to edit the project as it is already closed!",
        )
    if (
        update_data.full_amount and (
            update_data.full_amount < charity_project.invested_amount)
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="The new amount cannot be less than the already invested amount!"
        )


async def ensure_project_is_not_funded(charity_project: CharityProject
                                       ) -> None:
    """Check that no funds have been invested in the project."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="The project is already funded, deletion is not possible!"
        )
