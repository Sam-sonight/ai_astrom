# backend/astro_engine/temperament_index.py
from typing import Dict

def temperament_profile(element_scores: Dict[str, float],
                        modality_scores: Dict[str, float],
                        power_map: Dict[str, float]) -> Dict[str, float]:
    """
    Produces normalized temperament mix factoring elemental/modality bias + planetary power.
    """
    total_power = sum(power_map.values()) or 1
    weighted_elements = {e: element_scores.get(e, 0) * (total_power / 10) for e in element_scores}
    weighted_modalities = {m: modality_scores.get(m, 0) * (total_power / 10) for m in modality_scores}
    balance_index = sum(weighted_elements.values()) + sum(weighted_modalities.values())
    return {
        "elements": {k: round(v, 3) for k, v in weighted_elements.items()},
        "modalities": {k: round(v, 3) for k, v in weighted_modalities.items()},
        "balance_index": round(balance_index, 3)
    }
