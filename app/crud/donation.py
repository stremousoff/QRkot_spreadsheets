from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User, Donation


class CRUDDonation(CRUDBase):
    @staticmethod
    async def get_current_user_donations(
        user: User, session: AsyncSession
    ) -> list[Donation]:
        return (
            (
                await session.execute(
                    select(Donation).where(Donation.user_id == user.id)
                )
            )
            .scalars()
            .all()
        )


donation_crud = CRUDDonation(Donation)
