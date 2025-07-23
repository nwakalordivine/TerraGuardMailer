from pydantic import BaseModel
from datetime import date

class AlertRequest(BaseModel):
    location: str
    date: date
    percentage: float
