"""
dignities.py
Compute essential dignity score for a planet given its sign.
"""

from backend.astro_engine.astro_config import DIGNITY_SCORES

# rulerships and exaltations (partial; full mapping later)
RULERSHIP = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Pluto",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Uranus",
    "Pisces": "Neptune",
}

EXALTATION = {
    "Aries": "Sun",
    "Taurus": "Moon",
    "Cancer": "Jupiter",
    "Virgo": "Mercury",
    "Capricorn": "Mars",
    "Pisces": "Venus",
}

def essential_dignity(planet: str, sign: str) -> float:
    """
    Returns essential dignity weight for given planet/sign.
    """
    score = 0.0
    if RULERSHIP.get(sign) == planet:
        score += DIGNITY_SCORES["rulership"]
    elif EXALTATION.get(sign) == planet:
        score += DIGNITY_SCORES["exaltation"]
    else:
        score += DIGNITY_SCORES["peregrine"]
    return round(score, 3)
