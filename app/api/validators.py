from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constans import ValidationError
from app.crud.charity_project import charity_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name(
    name: str,
    session: AsyncSession,
) -> None:
    if await charity_crud.get_project_id_by_name(name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.CHARITY_PROJECT_EXISTS.format(name),
        )


async def check_update_data(
    project_id: int, project_data: CharityProjectUpdate, session: AsyncSession
) -> CharityProject:
    db_project = await charity_crud.get_object(project_id, session)
    if db_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ValidationError.CHARITY_PROJECT_BY_ID_NOT_FOUND.format(
                project_id
            ),
        )
    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ValidationError.DONT_CHANGE_PROJECT_IF_INVEST_EXIST,
        )
    if (
        project_data.full_amount
        and project_data.full_amount < db_project.invested_amount
    ):
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, ValidationError.CHARITY_FULL_AMOUNT_ERROR
        )
    if project_data.name != db_project.name:
        await check_name(project_data.name, session)
    return db_project


async def check_invested_amount(
    project_id: int, session: AsyncSession
) -> CharityProject:
    db_project = await charity_crud.get_object(project_id, session)
    if db_project is None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, ValidationError.CHARITY_PROJECT_EXISTS
        )
    if db_project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            ValidationError.DONT_DELETE_PROJECT_IF_INVEST_EXIST,
        )
    return db_project
