from typing import TypedDict, Optional

class TripState(TypedDict):
    request: str
    parsed: Optional[dict]
    flight: str
    hotels: Optional[dict]
    calendar_note: str
    itinerary: str
