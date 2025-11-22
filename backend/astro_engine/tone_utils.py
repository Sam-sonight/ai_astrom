# backend/astro_engine/tone_utils.py
from __future__ import annotations
from typing import Dict
from backend.models.horoscope_profile import PlanetPrecision

def build_tone_map(contextual_weights: Dict[str, PlanetPrecision]) -> Dict[str, float]:
    """
    Generate tone influence map (0.0–1.0 range) for AI narrative shaping.

    Each planet contributes a tone intensity score based on:
    - Essential and accidental strength (total 50%)
    - Hierarchy and house influence (30%)
    - Stability (20%)
    """
    tone_map: Dict[str, float] = {}

    for name, metrics in contextual_weights.items():
        base = (
            metrics.essential * 0.25 +
            metrics.accidental * 0.25 +
            metrics.hierarchy * 0.15 +
            metrics.house * 0.15 +
            metrics.stability * 0.20
        )
        tone_map[name] = round(min(max(base, 0.0), 1.0), 3)

    return tone_map
