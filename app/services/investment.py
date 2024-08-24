from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest(
    obj_to_invest: Union[CharityProject, Donation],
    investments: Union[list[CharityProject], list[Donation]],
    session: AsyncSession,
) -> None:
    """Распределяет средства между проектами и пожертвованиями,
    закрывая их при полном финансировании.
    """
    close_date = datetime.now()

    for investment in investments:
        amount_to_invest = (
            obj_to_invest.full_amount - obj_to_invest.invested_amount
        )
        free_amount = investment.full_amount - investment.invested_amount

        if amount_to_invest >= free_amount:
            investment.invested_amount += free_amount
            obj_to_invest.invested_amount += free_amount
            investment.fully_invested = True
            investment.close_date = close_date
        else:
            investment.invested_amount += amount_to_invest
            obj_to_invest.invested_amount += amount_to_invest
            obj_to_invest.fully_invested = True
            obj_to_invest.close_date = close_date
            break

        session.add(investment)

    if obj_to_invest.invested_amount >= obj_to_invest.full_amount:
        obj_to_invest.fully_invested = True
        obj_to_invest.close_date = close_date

    session.add(obj_to_invest)
    await session.commit()
    await session.refresh(obj_to_invest)
