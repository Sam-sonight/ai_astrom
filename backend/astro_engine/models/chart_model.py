# backend/astro_engine/models/chart_model.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class PlanetPlacement(BaseModel):
    name: str
    lon: float
    sign: str
    deg_in_sign: float
    lat: Optional[float] = None
    dist: Optional[float] = None
    house: Optional[int] = None

class HouseCusp(BaseModel):
    house: int
    lon: float
    sign: str
    deg_in_sign: float

class AspectLink(BaseModel):
    p1: str
    p2: str
    aspect: str
    angle: float
    orb: float

class ChartModel(BaseModel):
    meta: Dict[str, str]
    asc: Optional[PlanetPlacement] = None
    mc: Optional[PlanetPlacement] = None
    planets: List[PlanetPlacement]
    houses: List[HouseCusp]
    aspects: List[AspectLink]
    elements: Dict[str, int]
    modalities: Dict[str, int]
    dominant_elements: List[str]
    dominant_modalities: List[str]
