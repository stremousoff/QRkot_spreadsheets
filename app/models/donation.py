from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import Investment


class Donation(Investment):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f"{super().__repr__()}, "
            f"comment={self.comment}, "
            f"user_id={self.user_id}"
        )
