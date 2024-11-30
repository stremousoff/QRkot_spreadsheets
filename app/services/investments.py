from datetime import datetime

from app.models.base import Investment


def make_investments(
    target: Investment, sources: list[Investment]
) -> list[Investment]:
    changed_objects = []
    for source in sources:
        investment_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        for item in (source, target):
            item.invested_amount += investment_amount
            if item.full_amount == item.invested_amount:
                item.fully_invested = True
                item.close_date = datetime.now()
        changed_objects.append(source)
        if target.fully_invested:
            break
    return changed_objects
