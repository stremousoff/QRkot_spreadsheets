from sqlalchemy import Column, String, Text, CheckConstraint

from app.core.constans import ValidationError, MAX_LENGTH_NAME
from app.models.base import Investment


class CharityProject(Investment):
    name = Column(
        String(MAX_LENGTH_NAME),
        unique=True,
        nullable=False,
    )
    description = Column(Text, nullable=False)

    _table_args__ = (
        CheckConstraint(
            "TRIM(name) != ''", name=ValidationError.NAME_REQUIRED
        ),
    )

    def __repr__(self):
        return (
            f"{super().__repr__()} "
            f"name={self.name}, "
            f"description={self.comment}"
        )
