from typing import Optional

from fastapi import APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject

router = APIRouter()


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_project_id_by_name(
        project_name: str, session: AsyncSession
    ) -> Optional[int]:
        return (
            (
                await session.execute(
                    select(CharityProject.id).where(
                        CharityProject.name == project_name
                    )
                )
            )
            .scalars()
            .first()
        )

    @staticmethod
    async def get_projects_by_completion_rate(
        session: AsyncSession,
    ) -> list[tuple[str]]:
        return (
            await session.execute(
                select(
                    [
                        CharityProject.name,
                        (
                            func.strftime("%J", CharityProject.close_date)
                            - func.strftime("%J", CharityProject.create_date)
                        ).label("duration_period"),
                        CharityProject.description,
                    ]
                )
                .where(CharityProject.fully_invested.is_(True))
                .order_by("duration_period")
            )
        ).all()


charity_crud = CRUDCharityProject(CharityProject)
