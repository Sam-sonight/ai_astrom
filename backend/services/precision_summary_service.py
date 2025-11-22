# backend/services/precision_summary_service.py
"""
Phase 9.6 — Precision Summary Layer (v9.6-H)
Builds raw influence scores, normalized maps, and planet-level summaries.
"""

from __future__ import annotations
from typing import Dict, Tuple

from backend.astro_engine.models.chart_model import ChartModel, PlanetPlacement
from backend.models.horoscope_profile import PlanetPrecision


def build_precision_summary(
    chart: ChartModel,
    contextual_weights: Dict[str, PlanetPrecision]
) -> Tuple[Dict[str, str], Dict[str, float], Dict[str, float]]:
    """
    Returns:
        summaries: {planet -> text}
        raw_map:  {planet -> raw influence score}
        norm_map: {planet -> normalized 0–1 influence}
    """

    raw_map: Dict[str, float] = {}
    summaries: Dict[str, str] = {}

    # --------------------------------------------------
    # Test mode: chart is None → iterate over weights only
    # --------------------------------------------------
    if chart is None:
        for pname, w in contextual_weights.items():
            influence = (
                w.essential * 0.28 +
                w.accidental * 0.20 +
                w.aspectual * 0.18 +
                w.hierarchy * 0.12 +
                w.house * 0.12 +
                w.speed * 0.05 +
                w.temperament * 0.03 +
                w.neighbor * 0.02
            )
            raw_map[pname] = influence
            summaries[pname] = f"{pname}: baseline influence level ({influence:.2f})."

        if raw_map:
            min_v = min(raw_map.values())
            max_v = max(raw_map.values())
            if max_v != min_v:
                norm_map = {
                    k: round((v - min_v) / (max_v - min_v), 4)
                    for k, v in raw_map.items()
                }
            else:
                norm_map = {k: 0.5 for k in raw_map}
        else:
            norm_map = {}

        return summaries, raw_map, norm_map

    # --------------------------------------------------
    # Normal mode: we have a chart and can use houses etc.
    # --------------------------------------------------
    for planet in chart.planets:
        w = contextual_weights.get(planet.name)
        if not w:
            continue

        influence = (
            w.essential * 0.28 +
            w.accidental * 0.20 +
            w.aspectual * 0.18 +
            w.hierarchy * 0.12 +
            w.house * 0.12 +
            w.speed * 0.05 +
            w.temperament * 0.03 +
            w.neighbor * 0.02
        )

        raw_map[planet.name] = influence
        summaries[planet.name] = _build_precision_sentence(planet, w, influence)

    # Normalize
    if raw_map:
        min_v = min(raw_map.values())
        max_v = max(raw_map.values())
        if max_v != min_v:
            norm_map = {
                k: round((v - min_v) / (max_v - min_v), 4)
                for k, v in raw_map.items()
            }
        else:
            norm_map = {k: 0.5 for k in raw_map}
    else:
        norm_map = {}

    return summaries, raw_map, norm_map


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def _build_precision_sentence(
    planet: PlanetPlacement,
    w: PlanetPrecision,
    score: float
) -> str:
    traits = []

    if w.essential > 0.5:
        traits.append("strong essential dignity")
    if w.accidental > 0.5:
        traits.append("reinforced situational influence")
    if w.aspectual > 0.5:
        traits.append("high aspectual relevance")
    if w.house > 0.5:
        traits.append(f"impactful presence in the {planet.house}ᵗʰ house")
    if w.speed > 0.5:
        traits.append("heightened momentum")
    if w.stability < 0.7:
        traits.append("some instability or variability")

    if traits:
        return f"{planet.name}: " + ", ".join(traits) + f" (weighted influence score: {score:.2f})."

    return f"{planet.name}: baseline influence level ({score:.2f})."
