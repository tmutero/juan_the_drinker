from pydantic import BaseModel, field_validator


class BeverageBase(BaseModel):

    name: str
    alcoholUnits: float
    type: str
    codebar : str
    
class BeverageIn(BeverageBase):
   pass


class BeverageOut(BeverageBase):
    beverage_id: int
