from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name,
    check_update_data,
    check_invested_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investments import make_investments

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProject]:
    return await charity_crud.get_all_objects(session)


@router.post(
    "/",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
    charity_project: CharityProjectCreate = Body(
        example=CharityProjectCreate.Config.schema_extra["example"]
    ),
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await check_name(charity_project.name, session)
    new_charity_project = await charity_crud.create(charity_project, session)
    unclosed_donations = await donation_crud.get_all_objects_is_unclosed(
        session
    )
    if unclosed_donations:
        invested = make_investments(new_charity_project, unclosed_donations)
        session.add_all(invested)
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partial_update_charity_project(
    project_id: int,
    project_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project_db = await check_update_data(project_id, project_data, session)
    project_db = await charity_crud.patch(project_db, project_data, session)
    await session.commit()
    await session.refresh(project_db)
    return project_db


@router.delete(
    "/{project_id}",
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    return await charity_crud.delete(
        await check_invested_amount(project_id, session), session
    )
