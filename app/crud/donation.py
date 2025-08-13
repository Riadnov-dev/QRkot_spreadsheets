from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate]):
    """Class for implementing unique methods of the Donation model."""

    async def get_user_donations(
        self, user_id: int, session: AsyncSession
    ) -> list[Donation]:
        """Retrieve a list of donations made by the user."""
        donations = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return donations.scalars().all()

    async def get_active_donations(
            self, session: AsyncSession
    ) -> list[Donation]:
        """Retrieve a list of active donations."""
        donations = await session.execute(
            select(self.model).where(self.model.fully_invested is False)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
