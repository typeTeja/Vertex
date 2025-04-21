from pydantic import BaseModel
from typing import List


class PlanetPosition(BaseModel):
    name: str
    longitude: float
    retrograde: bool
    near_vertex: bool = False # Optional field
    

class NatalChartResponse(BaseModel):
    datetime: str
    latitude: float
    longitude: float
    planets: List[PlanetPosition]
