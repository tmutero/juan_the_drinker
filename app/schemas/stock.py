from pydantic import BaseModel, field_validator


class StockBase(BaseModel):

    name: str
    price: float
    bar_id: int
    beverage_id: int

class StockIn(StockBase):
   pass


class StockOut(StockBase):
    stock_id: int


