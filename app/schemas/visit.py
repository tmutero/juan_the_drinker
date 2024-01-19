from pydantic import BaseModel, field_validator
from datetime import date, datetime, time, timedelta


class VisitBase(BaseModel):
    visitedOn: datetime

class VisitIn(VisitBase):
    bar_id : int
    quantity: int
    happy_hour : bool
    stock_id : int


class VisitOut(VisitBase):
    visit_id: int
    drinks : int
    happy_hour: bool
    bar_name : str
    beverage: str

class VisitChange(VisitBase):
    bar_id : int
    quantity: int
    happy_hour : bool
    stock_id : int
    visit_id : int


    

    
