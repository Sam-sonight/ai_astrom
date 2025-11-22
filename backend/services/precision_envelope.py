# backend/services/precision_envelope.py
"""
Phase 9.7 — Precision Envelope Layer
Synthesizes contextual weights, precision summaries, tone maps,
and influence maps into a unified high-level psychological layer.

The envelope is deliberately front-end ready JSON:
{
  "strongest": [{"planet": "Sun", "strength": 0.92}, ...],
  "weakest": [{"planet": "Saturn", "strength": 0.21}, ...],
  "tone_tendencies": ["harmonized internal alignment"],
  "tone_average": 0.73,
  "planet_summaries": {
      "Sun": "...",
      "Saturn": "..."
  }
}
"""

from __future__ import annotations
from typing import Dict, Any, List
from backend.models.horoscope_profile import HoroscopeProfile, PlanetPrecision


def build_precision_envelope(profile: HoroscopeProfile) -> Dict[str, Any]:
    """
    Produces a meta-layer containing:
      - strongest planets (by normalized influence)
      - weakest planets
      - tone tendencies (average tone)
      - planetary precision summaries
    """

    cw: Dict[str, PlanetPrecision] = profile.contextual_weights or {}
    norm: Dict[str, float] = profile.precision_norm_map or {}
    summaries: Dict[str, str] = profile.precision_summaries or {}
    tone_map: Dict[str, float] = profile.tone_map or {}

    envelope: Dict[str, Any] = {}

    # --------------------------------------------------------
    # Strongest / weakest according to normalized influence
    # --------------------------------------------------------
    if norm:
        strongest = sorted(norm.items(), key=lambda x: x[1], reverse=True)[:3]
        weakest = sorted(norm.items(), key=lambda x: x[1])[:3]

        envelope["strongest"] = [{"planet": p, "strength": v} for p, v in strongest]
        envelope["weakest"] = [{"planet": p, "strength": v} for p, v in weakest]
    else:
        envelope["strongest"] = []
        envelope["weakest"] = []

    # --------------------------------------------------------
    # High-level “tone tendencies”
    # --------------------------------------------------------
    tendencies: List[str] = []

    avg_tone = None
    if tone_map:
        avg_tone = sum(tone_map.values()) / max(len(tone_map), 1)
        if avg_tone >= 0.65:
            tendencies.append("harmonized internal alignment")
        elif avg_tone >= 0.45:
            tendencies.append("balanced psychological tone")
        else:
            tendencies.append("strong contrast in inner dynamics")

    envelope["tone_tendencies"] = tendencies
    envelope["tone_average"] = round(avg_tone or 0.0, 3)

    # --------------------------------------------------------
    # Attach precision summaries exactly as stored on the profile
    # --------------------------------------------------------
    envelope["planet_summaries"] = summaries

    return envelope
