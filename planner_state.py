from typing import List, Dict, Optional
from pydantic import BaseModel

class PlannerState(BaseModel):
    preferences: Optional[str] = None
    destinations: Optional[List[str]] = None
    dest_desc: Optional[List[str]] = None
    weather_data: Optional[Dict] = None
    flights: Optional[Dict[str, List[Dict]]] = None 
    hotels: Optional[List[Dict]] = None
    itinerary: Optional[str] = None
    final_plan: Optional[str] = None
    attempts: int = 0
    weather_data_raw: Optional[Dict] = None
    flight_data_raw: Optional[Dict] = None
    source: Optional[str] = None
    depart_date: Optional[str] = None
    trip_days: Optional[int] = None
    return_date: Optional[str] = None
    best_flights: Optional[List[Dict]] = None

