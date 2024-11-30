from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_crud
from app.services.google_api import (
    spreadsheets_create,
    set_user_permissions,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post("/")
async def root(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> dict[str, str]:
    close_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        wrapper_service
    )
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(
        spreadsheet_id, close_projects, wrapper_service
    )
    return {"таблица с результатом доступна по ссылке": spreadsheet_url}
