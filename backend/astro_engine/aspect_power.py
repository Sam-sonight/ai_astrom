"""
aspect_power.py
Aspect strength computation with orb curve weighting.
"""

import math
from backend.astro_engine.astro_config import ASPECT_ORBS, ASPECT_WEIGHTS

def aspect_strength(aspect_type: str, orb: float, applying: bool=True) -> float:
    """
    Returns normalized aspect power between 0 and 1.
    """
    max_orb = ASPECT_ORBS.get(aspect_type, 5.0)
    base = ASPECT_WEIGHTS.get(aspect_type, 0.5)
    falloff = 1 - (orb / max_orb) ** 1.3
    strength = max(0, falloff) * base
    if applying:
        strength *= 1.15
    else:
        strength *= 0.90
    return round(min(1.0, strength), 3)
