# backend/models/horoscope_profile.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# PHASE 9 — PRECISION STRUCTURES
# ---------------------------------------------------------

class PlanetPrecision(BaseModel):
    """Normalized strength axes for precision analysis."""
    essential: float = Field(0.0)
    accidental: float = Field(0.0)
    aspectual: float = Field(0.0)
    hierarchy: float = Field(0.0)
    house: float = Field(0.0)
    speed: float = Field(0.0)
    temperament: float = Field(0.0)
    neighbor: float = Field(0.0)
    stability: float = Field(1.0)

    model_config = {"extra": "allow"}


# ---------------------------------------------------------
# TEXT STRUCTURES
# ---------------------------------------------------------

class PlacementText(BaseModel):
    name: str
    sign: Optional[str] = None
    house: Optional[int] = None
    text_sign: Optional[str] = None
    text_house: Optional[str] = None
    composite: Optional[str] = None


class AspectText(BaseModel):
    p1: str
    aspect: str
    p2: str
    orb: float
    text: Optional[str] = None


# ---------------------------------------------------------
# FINAL PROFILE CONTAINER
# ---------------------------------------------------------

class HoroscopeProfile(BaseModel):
    # Basic meta
    meta: Dict[str, str] = {}
    overview: Optional[str] = None

    # Element / modality
    dominant_elements: List[str] = []
    dominant_modalities: List[str] = []
    elements_count: Dict[str, int] = {}
    modalities_count: Dict[str, int] = {}

    # Angles
    asc_summary: Optional[str] = None
    mc_summary: Optional[str] = None

    # Placements & aspects
    placements: List[PlacementText] = []
    aspects: List[AspectText] = []

    # House emphasis
    house_focus: List[int] = []
    house_focus_texts: List[str] = []

    # Simple guidance
    strengths: List[str] = []
    challenges: List[str] = []
    tips: List[str] = []

    # Phase 9 — Precision data
    contextual_weights: Optional[Dict[str, PlanetPrecision]] = None

    tone_map: Optional[Dict[str, float]] = None
    intensity_vector: Optional[Dict[str, float]] = None
    final_narrative: Optional[str] = None

    # Precision scoring outputs
    precision_summaries: Optional[Dict[str, str]] = None
    precision_raw_map: Optional[Dict[str, float]] = None
    precision_norm_map: Optional[Dict[str, float]] = None

    # Envelope
    precision_envelope: Optional[Dict[str, Any]] = None

    model_config = {"extra": "allow"}
