from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime
import swisseph as swe


from models.natal import NatalChartResponse
from services.swisseph_service import get_planet_positions



router = APIRouter()

# @router.get("/natal-chart", response_model= NatalChartResponse, response_model_exclude_defaults=False)

@router.get("/natal-chart", response_model=NatalChartResponse)

def natal_chart(
    datetime_str: str,
    lat: float,
    lon: float,
    zodiac_type: str = Query("tropical", enum=["tropical", "sidereal"]),
    coordinate_system: str = Query("geocentric", enum=["geocentric", "heliocentric"]),
    ayanamsa: Optional[str] = Query("lahiri")

):

    dt = datetime.fromisoformat(datetime_str)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 + dt.second / 3600)
    planets = get_planet_positions(jd, lat, lon, zodiac_type, coordinate_system, ayanamsa)

    
    return NatalChartResponse(
        datetime=datetime_str,
        latitude=lat,
        longitude=lon,
        planets=planets
    )


