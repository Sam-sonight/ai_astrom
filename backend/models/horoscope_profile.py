# backend/models/horoscope_profile.py
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------
# Planet Precision Model
# ---------------------------------------------------------
class PlanetPrecision(BaseModel):
    essential: float = Field(0.0, description="Intrinsic dignity strength")
    accidental: float = Field(0.0, description="Positional/house strength")
    aspectual: float = Field(0.0, description="Aspect configuration strength")
    hierarchy: float = Field(0.0, description="Rulership and authority level")
    house: float = Field(0.0, description="House relevance")
    speed: float = Field(0.0, description="Orbital velocity relative to mean")
    temperament: float = Field(0.0, description="Elemental/temperamental bias")
    neighbor: float = Field(0.0, description="Influence from nearby planets")

    model_config = ConfigDict(extra="allow")


# ---------------------------------------------------------
# Text Models
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
# Horoscope Profile
# ---------------------------------------------------------
class HoroscopeProfile(BaseModel):
    meta: Dict[str, str] = Field(default_factory=dict)
    overview: Optional[str] = None

    dominant_elements: List[str] = Field(default_factory=list)
    dominant_modalities: List[str] = Field(default_factory=list)
    elements_count: Dict[str, int] = Field(default_factory=dict)
    modalities_count: Dict[str, int] = Field(default_factory=dict)

    asc_summary: Optional[str] = None
    mc_summary: Optional[str] = None

    placements: List[PlacementText] = Field(default_factory=list)
    aspects: List[AspectText] = Field(default_factory=list)

    house_focus: List[int] = Field(default_factory=list)
    house_focus_texts: List[str] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)
    challenges: List[str] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)

    # Phase 9 — Analysis Layers
    contextual_weights: Optional[Dict[str, PlanetPrecision]] = None
    tone_map: Optional[Dict[str, float]] = None
    intensity_vector: Optional[Dict[str, float]] = None

    final_narrative: Optional[str] = None

    precision_summary: Optional[Dict[str, str]] = None
    influence_raw: Optional[Dict[str, float]] = None
    influence_normalized: Optional[Dict[str, float]] = None

    precision_raw_map: Optional[Dict[str, float]] = None
    precision_norm_map: Optional[Dict[str, float]] = None

    precision_envelope: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
