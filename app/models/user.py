from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"email={self.email}, "
        )
