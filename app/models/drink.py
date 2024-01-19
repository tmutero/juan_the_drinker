from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Drink(Base):
    __tablename__ = "drink"

    drink_id: Mapped[intpk]
    quantity: Mapped[int | None]
    happy_hour : Mapped[bool]
    visit_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("visit.visit_id"))
    stock_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("stock.stock_id"))

