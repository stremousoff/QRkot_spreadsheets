from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_async_session
from app.core.constans import GoogleApiError
from app.core.exceptions import MaxCellLimit
from app.core.google_client import get_service
from app.crud.charity_project import charity_crud
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post("/")
async def make_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> dict[str, str]:
    close_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )
    try:
        spreadsheet_id, spreadsheet_url, table_data, rows, columns = (
            await spreadsheets_create(wrapper_service, close_projects)
        )
    except MaxCellLimit as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=GoogleApiError.SPREADSHEET_CREATE_ERROR.format(error),
        )
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(
        spreadsheet_id, wrapper_service, table_data, rows, columns
    )
    return {"spreadsheetUrl": spreadsheet_url}
