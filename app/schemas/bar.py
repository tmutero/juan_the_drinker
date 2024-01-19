from app.schemas.stock import StockOut
from pydantic import BaseModel, field_validator
from typing import List

class BarBase(BaseModel):
    name: str
    address: str


class BarIn(BarBase):
   pass


class BarOut(BarBase):
    bar_id: int
    stock: list[StockOut]


class ChangeBarIn(BarBase):
    bar_id: int

    @field_validator("name")
    @classmethod
    def name_is_not_blank(cls, value):
        if not value:
            raise ValueError("Name field can't be blank!!!")
        return value

    @field_validator("address")
    @classmethod
    def address_is_not_blank(cls, value):
        if not value:
            raise ValueError("Address field can't be blank!!!")
        return value
