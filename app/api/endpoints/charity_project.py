from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    ensure_project_can_be_updated,
    ensure_project_exists,
    ensure_project_is_not_funded,
    ensure_project_name_is_unique
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investment import invest

router = APIRouter()


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,
            summary="Получить список всех благотворительных проектов"
            )
async def retrieve_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка благотворительных проектов."""
    return await charity_project_crud.get_multi(session=session)


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],
             summary="Создание благотворительного проекта"
             )
async def create_charity_project(
        project: CharityProjectCreate = Body(
            ..., examples=CharityProjectCreate.Config.schema_extra['examples']
        ),
        session: AsyncSession = Depends(get_async_session)
):
    """Создание благотворительного проекта. Только для суперпользователей."""
    await ensure_project_name_is_unique(project.name, session)
    new_project = await charity_project_crud.create(
        data=project, session=session)
    active_donations = await donation_crud.get_active_objs(session)
    if active_donations:
        await invest(new_project, active_donations, session)
    return new_project


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],
              summary="Обновление благотворительного проекта"
              )
async def modify_charity_project(
        project_id: int,
        update_data: CharityProjectUpdate = Body(
            ..., examples=CharityProjectUpdate.Config.schema_extra['examples']
        ),
        session: AsyncSession = Depends(get_async_session)
):
    """Изменение благотворительного проекта. Только для суперпользователей."""
    charity_project = await ensure_project_exists(project_id, session)
    await ensure_project_can_be_updated(charity_project, update_data)
    if update_data.name is not None:
        await ensure_project_name_is_unique(update_data.name, session)
    updated_project = await charity_project_crud.update(
        db_obj=charity_project, data=update_data, session=session)
    active_donations = await donation_crud.get_active_objs(session)
    if active_donations:
        await invest(updated_project, active_donations, session)

    return updated_project


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)],
               summary="Удаление благотворительного проекта"
               )
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление благотворительного проекта. Только для суперпользователей."""
    charity_project = await ensure_project_exists(project_id, session)
    await ensure_project_is_not_funded(charity_project)
    return await charity_project_crud.delete(charity_project, session)
