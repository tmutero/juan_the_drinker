from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Stock(Base):
    __tablename__ = "stock"

    stock_id: Mapped[intpk]
    name: Mapped[str100 | None]
    price: Mapped[float | None]
    bar_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("bar.bar_id"))
    beverage_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("beverage.beverage_id"))

    

    








