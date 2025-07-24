from pydantic import BaseModel
from datetime import date
from typing import List

class AlertRequest(BaseModel):
    location: str
    date: List[date]
    percentage: List[float]

class User(BaseModel):
    name: str
    email: str
