from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.base import Base
from app.core.constans import INVEST_AMOUNT_DEFAULT


class Investment(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint("full_amount > 0"),
        # так не работает, оставил старый вариант
        # CheckConstraint("0 <= invested_amount <= full_amount"),
        CheckConstraint("invested_amount >= 0"),
        CheckConstraint("invested_amount <= full_amount"),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=INVEST_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"fully_invested={self.fully_invested}, "
            f"invested_amount={self.invested_amount}, "
            f"create_date={self.create_date}, "
        )
