# backend/astro_engine/zodiac_utils.py
import math

SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

ELEMENT_BY_SIGN = {
    "Aries":"Fire","Taurus":"Earth","Gemini":"Air","Cancer":"Water",
    "Leo":"Fire","Virgo":"Earth","Libra":"Air","Scorpio":"Water",
    "Sagittarius":"Fire","Capricorn":"Earth","Aquarius":"Air","Pisces":"Water"
}

MODALITY_BY_SIGN = {
    "Aries":"Cardinal","Taurus":"Fixed","Gemini":"Mutable","Cancer":"Cardinal",
    "Leo":"Fixed","Virgo":"Mutable","Libra":"Cardinal","Scorpio":"Fixed",
    "Sagittarius":"Mutable","Capricorn":"Cardinal","Aquarius":"Fixed","Pisces":"Mutable"
}

def normalize_lon(deg: float) -> float:
    """Normalize any angle to 0–360°."""
    return deg % 360.0

def deg_to_sign(lon: float) -> tuple[str,float]:
    """Return sign & degree-in-sign for a longitude."""
    lon = normalize_lon(lon)
    sign_index = int(lon // 30)
    deg_in_sign = lon % 30
    return SIGNS[sign_index], deg_in_sign

def element_and_modality_counts(planets: list[dict]) -> tuple[dict,dict]:
    """Count elements & modalities from planet placements."""
    elem_counts = {"Fire":0,"Earth":0,"Air":0,"Water":0}
    mod_counts = {"Cardinal":0,"Fixed":0,"Mutable":0}
    for p in planets:
        sign = p["sign"]
        elem_counts[ELEMENT_BY_SIGN[sign]] += 1
        mod_counts[MODALITY_BY_SIGN[sign]] += 1
    return elem_counts, mod_counts
