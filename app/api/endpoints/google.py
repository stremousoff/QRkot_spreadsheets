from http import HTTPStatus
from http.client import HTTPException

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_async_session
from app.core.exceptions import MaxRowsLimit, MaxColumnsLimit
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
        spreadsheet_id, spreadsheet_url = await spreadsheets_create(
            wrapper_service, close_projects
        )
    except (MaxRowsLimit, MaxColumnsLimit) as error:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            f"Ошибка создания таблицы: {error}"
        )
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(
        spreadsheet_id, wrapper_service, close_projects
    )
    return {"spreadsheetUrl": spreadsheet_url}
