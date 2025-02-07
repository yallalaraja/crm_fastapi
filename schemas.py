from pydantic import BaseModel
from typing import Optional

# Pydantic schema for User response (without password)
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # This tells Pydantic to treat SQLAlchemy models as dicts

# Pydantic schema for Customer response
class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True
