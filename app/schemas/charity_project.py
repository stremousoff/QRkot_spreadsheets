from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    Extra,
)
from pydantic.types import StrictInt

from app.core.constans import MIN_LENGTH_NAME, MAX_LENGTH_NAME


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_LENGTH_NAME, max_length=MAX_LENGTH_NAME
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH_NAME)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=MIN_LENGTH_NAME, max_length=MAX_LENGTH_NAME)
    description: str = Field(min_length=MIN_LENGTH_NAME)
    full_amount: PositiveInt
    invested_amount: int = 0

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "Сбор средств для кошечек",
                "description": "На всё хорошее",
                "full_amount": 1000,
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "Новое имя проекта",
                "description": "Новое описание проекта",
                "full_amount": 2000,
            }
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: StrictInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
