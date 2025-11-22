"""
context_weights.py — Phase 9.6 Contextual Weighting Engine
Applies localized, rule-based adjustments to PlanetPrecision metrics.
"""

from backend.astro_engine.astro_config import CONTEXT_RULES
from backend.models.horoscope_profile import PlanetPrecision


def apply_contextual_weights(planet: str, metrics: PlanetPrecision, ctx: dict) -> PlanetPrecision:
    """
    Adjusts PlanetPrecision axes based on contextual conditions.
    Args:
        planet: str — planet name (for logging or special cases)
        metrics: PlanetPrecision — existing score structure
        ctx: dict — contextual data flags and ratios
    Returns:
        PlanetPrecision — adjusted metrics (new instance)
    """
    m = metrics.model_copy(deep=True)

    # --- Angularity weighting ---
    house_type = ctx.get("house_type", "cadent")
    if house_type == "angular":
        m.accidental *= CONTEXT_RULES["angular_boost"]
        m.house *= CONTEXT_RULES["angular_boost"]
    elif house_type == "succedent":
        m.accidental *= CONTEXT_RULES["succedent_boost"]
    elif house_type == "cadent":
        m.accidental *= CONTEXT_RULES["cadent_drop"]

    # --- Motion / Speed weighting ---
    # Speed now plays a dual role: speed ratio and contextual “fast/slow” state
    if ctx.get("is_retrograde"):
        m.speed *= CONTEXT_RULES["retrograde_penalty"]
        m.accidental *= CONTEXT_RULES["retrograde_penalty"]
    else:
        speed_ratio = ctx.get("speed_ratio", 1.0)
        # speed_ratio > 1.1 → fast planet,  < 0.9 → slow or near-stationary
        if speed_ratio > 1.1:
            m.speed *= CONTEXT_RULES.get("speed_fast_bonus", 1.10)
            m.accidental *= 1.05
        elif speed_ratio < 0.9:
            m.speed *= CONTEXT_RULES.get("speed_slow_penalty", 0.90)
            m.accidental *= 0.95

    # --- Sun proximity effects ---
    sun_distance = ctx.get("sun_distance", 999)
    if sun_distance < 0.3:
        m.essential *= CONTEXT_RULES["cazimi_bonus"]
        m.accidental *= CONTEXT_RULES["cazimi_bonus"]
    elif sun_distance < 8.5:
        m.accidental *= CONTEXT_RULES["combust_penalty"]
    elif sun_distance < 17:
        m.accidental *= CONTEXT_RULES["under_beams_penalty"]

    # --- Sect / Reception ---
    if ctx.get("sect_match"):
        m.essential *= CONTEXT_RULES["sect_bonus"]
    if ctx.get("mutual_reception"):
        m.hierarchy *= CONTEXT_RULES["mutual_reception_bonus"]

    # --- Out-of-bounds declination ---
    if ctx.get("out_of_bounds"):
        m.accidental *= CONTEXT_RULES["oob_penalty"]
        m.stability = getattr(m, "stability", 1.0) * CONTEXT_RULES["oob_penalty"]

    # --- Clamp all values between -1 and +1 ---
    for field in m.__class__.model_fields:
        value = getattr(m, field)
        if isinstance(value, (float, int)):
            setattr(m, field, max(-1.0, min(1.0, value)))

    return m
