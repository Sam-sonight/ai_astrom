# backend/astro_engine/house_calculator.py
import swisseph as swe
from backend.astro_engine.zodiac_utils import deg_to_sign, normalize_lon

def compute_placidus_cusps(jd_ut: float, lat: float, lon: float):
    """
    Compute Placidus house cusps (1–12), Ascendant, MC.
    Returns: (houses, asc, mc)
    """
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P')
    houses = []
    for i, cusp_lon in enumerate(cusps, start=1):
        sign, deg_in_sign = deg_to_sign(cusp_lon)
        houses.append({
            "house": i,
            "lon": normalize_lon(cusp_lon),
            "sign": sign,
            "deg_in_sign": deg_in_sign
        })
    asc = ascmc[0]
    mc = ascmc[1]
    return houses, asc, mc

def assign_house(lon: float, cusps: list[float]) -> int:
    """
    Determine which house a longitude belongs to (Placidus).
    """
    lon = normalize_lon(lon)
    for i in range(12):
        start = normalize_lon(cusps[i])
        end = normalize_lon(cusps[(i+1) % 12])
        if start < end:
            if start <= lon < end:
                return i+1
        else:
            # Wrap-around (e.g. House 12 crossing 360°)
            if lon >= start or lon < end:
                return i+1
    return 12
