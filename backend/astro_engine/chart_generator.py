# backend/astro_engine/chart_generator.py
from __future__ import annotations
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from backend.astro_engine.time_utils import resolve_tz, local_to_utc, to_julian_day
from backend.astro_engine.ephemeris_loader import compute_planet_lon_lat
from backend.astro_engine.house_calculator import compute_placidus_cusps, assign_house
from backend.astro_engine.zodiac_utils import deg_to_sign, normalize_lon, element_and_modality_counts
from backend.astro_engine.models.chart_model import ChartModel, PlanetPlacement, HouseCusp
from backend.astro_engine.aspects_detector import detect_aspects

def _houses_lons_from_struct(houses_struct: List[Dict]) -> List[float]:
    """Extract raw cusp longitudes (1→12) from computed house dicts."""
    # houses_struct is list of dicts with keys: house, lon, sign, deg_in_sign
    # Ensure index order 1..12
    houses_struct_sorted = sorted(houses_struct, key=lambda h: h["house"])
    return [float(h["lon"]) for h in houses_struct_sorted]

def _build_angle_point(name: str, lon_value: float) -> PlanetPlacement:
    sign, deg = deg_to_sign(lon_value)
    return PlanetPlacement(
        name=name,
        lon=normalize_lon(lon_value),
        sign=sign,
        deg_in_sign=deg,
        lat=None,
        dist=None,
        house=None,
    )

def build_natal_chart(
    dt_local: datetime,
    lat: float,
    lon: float,
    tz_name: Optional[str] = None,
    include_angles_in_aspects: bool = False,
) -> ChartModel:
    """
    End-to-end natal chart generator (tropical, Placidus).
    - dt_local: naive local datetime of birth
    - lat/lon: birthplace coordinates (lon East positive per SE)
    - tz_name: optional override; if None, resolved from coords
    """
    # --- Resolve timezone & UTC / JD
    tz = tz_name or resolve_tz(lat, lon)
    dt_utc = local_to_utc(dt_local, tz)
    jd_ut = to_julian_day(dt_utc)

    # --- Planetary positions
    planets_raw = compute_planet_lon_lat(dt_utc)  # {'Sun': {'lon', 'lat', 'dist'}, ...}

    # --- Houses + Asc/MC (Placidus)
    houses_struct, asc_lon, mc_lon = compute_placidus_cusps(jd_ut, lat, lon)
    cusps_lons = _houses_lons_from_struct(houses_struct)

    # --- Planet placements (sign + house)
    planets: List[PlanetPlacement] = []
    for name, data in planets_raw.items():
        sign, deg = deg_to_sign(data["lon"])
        h = assign_house(data["lon"], cusps_lons)
        planets.append(
            PlanetPlacement(
                name=name,
                lon=normalize_lon(data["lon"]),
                sign=sign,
                deg_in_sign=deg,
                lat=float(data["lat"]) if data.get("lat") is not None else None,
                dist=float(data["dist"]) if data.get("dist") is not None else None,
                house=h,
            )
        )

    # --- Angle points
    asc_pp = _build_angle_point("Ascendant", asc_lon)
    mc_pp = _build_angle_point("MC", mc_lon)

    # --- Aspects (natal): planets only by default; optionally include angles
    lon_map: Dict[str, float] = {p.name: p.lon for p in planets}
    if include_angles_in_aspects:
        lon_map["Ascendant"] = asc_pp.lon
        lon_map["MC"] = mc_pp.lon
    aspects = detect_aspects(lon_map)

    # --- Elements / Modalities
    elem_counts, mod_counts = element_and_modality_counts([p.model_dump() for p in planets])

    if elem_counts:
        max_e = max(elem_counts.values())
        dominant_elems = [k for k, v in elem_counts.items() if v == max_e and v > 0]
    else:
        dominant_elems = []
    if mod_counts:
        max_m = max(mod_counts.values())
        dominant_mods = [k for k, v in mod_counts.items() if v == max_m and v > 0]
    else:
        dominant_mods = []

    # --- Houses model -> HouseCusp list
    houses_model: List[HouseCusp] = [
        HouseCusp(house=h["house"], lon=h["lon"], sign=h["sign"], deg_in_sign=h["deg_in_sign"])
        for h in houses_struct
    ]

    # --- Meta block
    meta = {
        "tz_name": tz,
        "dt_local": dt_local.isoformat(),
        "dt_utc": dt_utc.isoformat(),
        "jd_ut": f"{jd_ut:.6f}",
    }

    # --- Build ChartModel
    chart = ChartModel(
        meta=meta,
        asc=asc_pp,
        mc=mc_pp,
        planets=planets,
        houses=houses_model,
        aspects=aspects,
        elements=elem_counts,
        modalities=mod_counts,
        dominant_elements=dominant_elems,
        dominant_modalities=dominant_mods,
    )
    return chart
