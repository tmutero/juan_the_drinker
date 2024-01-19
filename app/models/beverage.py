from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Beverage(Base):
    __tablename__ = "beverage"

    beverage_id: Mapped[intpk]
    name: Mapped[str100 | None]
    codebar: Mapped[str100 | None]
    type: Mapped[str100 | None]
    alcoholUnits: Mapped[float | None]
    



