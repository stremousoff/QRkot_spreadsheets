from datetime import datetime
from typing import TypeVar, Optional, Generic

from pydantic import BaseModel
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model):
        self.model = model

    async def get_object(
        self, object_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        return (
            (
                await session.execute(
                    select(self.model).where(self.model.id == object_id)
                )
            )
            .scalars()
            .first()
        )

    async def get_all_objects(self, session: AsyncSession) -> list[ModelType]:
        return (await session.execute(select(self.model))).scalars().all()

    async def get_all_objects_is_unclosed(
        self, session: AsyncSession
    ) -> list[ModelType]:
        return (
            (
                await session.execute(
                    select(self.model)
                    .where(self.model.fully_invested == 0)
                    .order_by(asc("create_date"))
                )
            )
            .scalars()
            .all()
        )

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[ModelType] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        creat_obj_for_db = self.model(**obj_in_data)
        session.add(creat_obj_for_db)
        return creat_obj_for_db

    @staticmethod
    async def delete(db_object: ModelType, session: AsyncSession) -> ModelType:
        await session.delete(db_object)
        await session.commit()
        return db_object

    @classmethod
    async def patch(
        cls, db_obj: ModelType, obj_in: UpdateSchemaType, session: AsyncSession
    ) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
            await session.commit()
            await session.refresh(db_obj)
        return db_obj
