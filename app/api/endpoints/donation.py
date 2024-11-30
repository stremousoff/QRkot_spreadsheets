from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud

from app.models import User, Donation
from app.schemas.donation import (
    DonationDBShort,
    DonationDBFull,
    DonationCreate,
)
from app.services.investments import make_investments

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_all_objects(session)


@router.get("/my", response_model=list[DonationDBShort])
async def get_current_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> list[Donation]:
    return await donation_crud.get_current_user_donations(user, session)


@router.post(
    "/", response_model=DonationDBShort, response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate = Body(
        example=DonationCreate.Config.schema_extra["example"]
    ),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Donation:
    donation = await donation_crud.create(donation, session, user)
    unclosed_projects = await charity_crud.get_all_objects_is_unclosed(session)
    if unclosed_projects:
        invested = make_investments(donation, unclosed_projects)
        session.add_all(invested)
    await session.commit()
    await session.refresh(donation)
    return donation
