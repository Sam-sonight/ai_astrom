# backend/astro_engine/neighboring_influence.py
from typing import Dict

def propagate_house_energy(house_scores: Dict[int, float], bleed: float = 0.1) -> Dict[int, float]:
    """
    Spreads a small fraction of each house’s score to its neighbors (circularly 1–12).
    """
    new_scores = house_scores.copy()
    for h, val in house_scores.items():
        left = 12 if h == 1 else h - 1
        right = 1 if h == 12 else h + 1
        new_scores[left] += val * bleed
        new_scores[right] += val * bleed
        new_scores[h] -= val * bleed * 2
    return {h: round(v, 3) for h, v in new_scores.items()}
