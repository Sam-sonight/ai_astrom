# backend/astro_engine/dispositor_chain.py
from __future__ import annotations
from typing import Dict

# Simplified sign rulerships (traditional)
RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

def build_dispositor_chain(planet_positions: Dict[str, str]) -> Dict[str, float]:
    """
    planet_positions: {planet: sign}
    Returns dominance map with 1.0 for self-rulership, diminishing recursively (0.5, 0.25…)
    """
    dominance = {p: 0.0 for p in planet_positions}
    for planet, sign in planet_positions.items():
        ruler = RULERS.get(sign)
        weight = 1.0
        visited = set()
        while ruler and ruler not in visited:
            visited.add(ruler)
            dominance[ruler] = dominance.get(ruler, 0) + weight
            ruler = RULERS.get(planet_positions.get(ruler, ""), None)
            weight *= 0.5
    return dominance
