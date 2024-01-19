
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk, str100


class Visit(Base):
    __tablename__ = "visit"

    visit_id: Mapped[intpk]
    visitedOn =  mapped_column(Date)

    bar_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("bar.bar_id"))
    
   




