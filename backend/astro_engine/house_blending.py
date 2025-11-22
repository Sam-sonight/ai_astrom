# backend/astro_engine/house_blending.py
import math
from typing import Dict

HOUSE_CUSP_SIGMA = 3.0

def house_influence(house_angle_diff: float) -> float:
    """Returns Gaussian weight based on angular distance (°) from house cusp."""
    return math.exp(-0.5 * (house_angle_diff / HOUSE_CUSP_SIGMA) ** 2)

def blend_nearby_houses(current_house: int, offset: float) -> Dict[int, float]:
    """
    offset: degrees from house cusp (+ toward next house)
    Returns weights for current and adjacent houses summing ≈ 1.
    """
    base = house_influence(offset)
    adj = house_influence(30 - abs(offset))
    total = base + adj
    if total == 0: return {current_house: 1.0}
    w1, w2 = base / total, adj / total
    next_house = 1 if current_house == 12 else current_house + 1
    return {current_house: round(w1, 3), next_house: round(w2, 3)}
