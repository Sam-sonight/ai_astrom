"""
accidental_power.py
Computes accidental (situational) strength modifiers for a planet.
"""

from backend.astro_engine.astro_config import ACCIDENTAL_FACTORS

def house_strength(house_num: int) -> float:
    if house_num in [1, 4, 7, 10]:
        return ACCIDENTAL_FACTORS["angular"]
    elif house_num in [2, 5, 8, 11]:
        return ACCIDENTAL_FACTORS["succedent"]
    else:
        return ACCIDENTAL_FACTORS["cadent"]

def accidental_power(house_num: int, retrograde: bool=False, combust: bool=False) -> float:
    score = house_strength(house_num)
    if retrograde:
        score += ACCIDENTAL_FACTORS["retrograde"]
    if combust:
        score += ACCIDENTAL_FACTORS["combust"]
    return round(score, 3)
