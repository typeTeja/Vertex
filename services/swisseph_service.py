import swisseph as swe
from typing import List
from models.natal import PlanetPosition

swe.set_ephe_path('/ephe')  # Adjust to your ephemeris file path

# Planet ID map
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Earth": swe.EARTH,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Rahu": swe.MEAN_NODE,  # North Node
    "Ketu": swe.TRUE_NODE   # South Node (True Node used with inverse logic if needed)
}

# Supported Ayanamsas
AYANAMSAS = {
    "lahiri": swe.SIDM_LAHIRI,
    "krishnamurti": swe.SIDM_KRISHNAMURTI,
    "raman": swe.SIDM_RAMAN,
    "ushashashi": swe.SIDM_USHASHASHI,
    "yukteshwar": swe.SIDM_YUKTESHWAR,
    "true_citra": swe.SIDM_TRUE_CITRA,
    "aryabhata": swe.SIDM_ARYABHATA,
    "suryasiddhanta": swe.SIDM_SURYASIDDHANTA,
    "jangam": swe.SIDM_JN_BHASIN,
    "fagan": swe.SIDM_FAGAN_BRADLEY
}

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

#formatted = format_longitude(longitude)
# Get planet positions including Vertex and near-vertex logic
def get_planet_positions(
    julian_day: float,
    lat: float,
    lon: float,
    zodiac_type: str = "tropical",
    coordinate_system: str = "geocentric",
    ayanamsa: str = "lahiri"
) -> List[PlanetPosition]:
    
    # Set sidereal mode if needed
    if zodiac_type == "sidereal":
        sid_mode = AYANAMSAS.get(ayanamsa.lower(), swe.SIDM_LAHIRI)
        swe.set_sid_mode(sid_mode)
    
    # Set calculation flags
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    if coordinate_system == "heliocentric":
        flags |= swe.FLG_HELCTR

    # Vertex (still geocentric)
    cusps, ascmc = swe.houses_ex(julian_day, lat, lon, b'A')
    vertex_long = ascmc[swe.VERTEX]

    positions = []

    # Loop through planets
    for name, planet_id in PLANETS.items():
        pos, _ = swe.calc_ut(julian_day, planet_id, flags)
        longitude = pos[0]
        speed = pos[3]
        retrograde = speed < 0

        # Check if within ±5° of Vertex
        diff = abs(longitude - vertex_long)
        diff = min(diff, 360 - diff)
        near_vertex = diff <= 5

        positions.append(PlanetPosition(
            name=name,
            longitude=longitude,
            retrograde=retrograde,
            near_vertex=near_vertex
            
        ))

    # Add Vertex itself
    positions.append(PlanetPosition(
        name="Vertex",
        longitude=vertex_long,
        retrograde=False,
        near_vertex=False
    ))

    return positions