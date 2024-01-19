from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base, intpk, str100


class Bar(Base):
    __tablename__ = "bar"

    bar_id: Mapped[intpk]
    name: Mapped[str100]
    address: Mapped[str100]

    stock = relationship("Stock")

    
 
 
 
    


