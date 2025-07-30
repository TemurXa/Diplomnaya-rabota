from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):

    name: str
    phone: str
    password: str
    age: int
    avatar: str
    reg_date: Optional[datetime] = datetime.now()
    birthday_date: datetime
    number_of_sells: Optional[int] = 0
    number_of_purchases: Optional[int] = 0

class Book(BaseModel):

    name: str
    price: float
    photo: str
    genre: str
    post_date: Optional[datetime] = datetime.now()
    number_of_pages: int