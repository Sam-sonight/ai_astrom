# backend/astro_engine/time_utils.py
from datetime import datetime, timezone
from timezonefinder import TimezoneFinder
import pytz
import math

tf = TimezoneFinder()

def resolve_tz(lat: float, lon: float) -> str:
    """Return IANA timezone name for coordinates."""
    tz = tf.timezone_at(lat=lat, lng=lon)
    if not tz:
        raise ValueError("Timezone not found for given coordinates.")
    return tz

def local_to_utc(dt_local: datetime, tz_name: str) -> datetime:
    """Convert local datetime to UTC."""
    tz = pytz.timezone(tz_name)
    dt_localized = tz.localize(dt_local)
    return dt_localized.astimezone(pytz.utc)

def to_julian_day(dt_utc: datetime) -> float:
    """Compute Julian Day (UT)."""
    # Algorithm: Meeus / USNO
    year, month = dt_utc.year, dt_utc.month
    day = dt_utc.day + (dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)/24
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year/100)
    B = 2 - A + math.floor(A/4)
    jd = math.floor(365.25*(year+4716)) + math.floor(30.6001*(month+1)) + day + B - 1524.5
    return jd
