# backend/astro_engine/ephemeris_loader.py
import swisseph as swe
from datetime import datetime
from backend.astro_engine.time_utils import to_julian_day
import os

# --------------------------------------------------------------------
# 🌍 Setup: Swiss Ephemeris Path
# --------------------------------------------------------------------
# Make sure the ephemeris data files (seas_*.se1 etc.) are available in ./data/ephemeris
EPHE_PATH = os.path.join(os.getcwd(), "data", "ephemeris")
swe.set_ephe_path(EPHE_PATH)

# --------------------------------------------------------------------
# ⚙️ Flags: Tropical, Geocentric, Swiss Ephemeris precision
# --------------------------------------------------------------------
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED  # Ecliptic, true-of-date

# --------------------------------------------------------------------
# 🪐 Planet Constants
# --------------------------------------------------------------------
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

# --------------------------------------------------------------------
# 🧮 Compute Planetary Positions
# --------------------------------------------------------------------
def compute_planet_lon_lat(dt_utc: datetime) -> dict:
    """
    Compute ecliptic longitudes/latitudes/distances for main planets.
    Returns a dict like:
      {'Sun': {'lon': 56.18, 'lat': 0.00, 'dist': 1.011}, ...}
    """
    jd_ut = to_julian_day(dt_utc)
    results = {}

    for name, pid in PLANETS.items():
        planet_data, ret_flag = swe.calc_ut(jd_ut, pid, flags=FLAGS)
        lon, lat, dist = planet_data[:3]
        results[name] = {"lon": lon, "lat": lat, "dist": dist}

    return results
