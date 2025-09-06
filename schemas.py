from typing import List
from pydantic import BaseModel, Field

class ParsedTrip(BaseModel):
    city: str
    check_in: str
    nights: int
    budget_total_usd: int

class HotelOption(BaseModel):
    name: str
    price_per_night_usd: int
    location: str
    highlights: List[str]

class HotelsResponse(BaseModel):
    city: str
    check_in: str
    nights: int
    budget_total_usd: int
    suggestions: List[HotelOption] = Field(default_factory=list)
