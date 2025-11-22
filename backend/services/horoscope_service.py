# backend/services/horoscope_service.py
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

from backend.astro_engine.models.chart_model import ChartModel, PlanetPlacement, AspectLink
from backend.models.horoscope_profile import (
    HoroscopeProfile,
    PlacementText,
    AspectText,
    PlanetPrecision,
)
from backend.core.config import settings

from backend.astro_engine.context_weights import apply_contextual_weights
from backend.astro_engine.tone_utils import build_tone_map
from backend.services.precision_summary_service import build_precision_summary
from backend.services.precision_envelope import build_precision_envelope

# ---------------------------------------------------
# KB LOADING
# ---------------------------------------------------
INTERP_DIR = Path(settings.DATA_DIR) / "interpretations"


def _load_json_safe(path: Path) -> dict:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


KB_PLANET_IN_SIGN = _load_json_safe(INTERP_DIR / "planet_in_sign.json")
KB_PLANET_IN_HOUSE = _load_json_safe(INTERP_DIR / "planet_in_house.json")
KB_ASPECTS = _load_json_safe(INTERP_DIR / "aspects.json")
KB_ELEMENTS = _load_json_safe(INTERP_DIR / "elements.json")
KB_MODALITIES = _load_json_safe(INTERP_DIR / "modalities.json")
KB_HOUSE_KEYWORDS = _load_json_safe(INTERP_DIR / "house_keywords.json")
KB_PLANETARY_ARCH = _load_json_safe(INTERP_DIR / "planetary_archetypes.json")

PLACEMENT_ORDER = [
    "Ascendant", "Sun", "Moon", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "MC"
]


# ---------------------------------------------------
# Helpers
# ---------------------------------------------------
def _get_sign_text(planet: str, sign: Optional[str]) -> str:
    if not sign:
        return ""
    return KB_PLANET_IN_SIGN.get(planet, {}).get(sign, "") or ""


def _get_house_text(planet: str, house: Optional[int]) -> str:
    if not house:
        return ""
    return KB_PLANET_IN_HOUSE.get(planet, {}).get(str(house), "") or ""


def _get_aspect_text(p1: str, p2: str, aspect: str) -> str:
    t = KB_ASPECTS.get(p1, {}).get(p2, {}).get(aspect)
    if t:
        return t
    return KB_ASPECTS.get(p2, {}).get(p1, {}).get(aspect, "") or ""


def _house_focus_from_positions(chart: ChartModel) -> Tuple[List[int], List[str]]:
    focus: List[int] = []
    texts: List[str] = []
    key_houses = {1, 4, 7, 10}

    for p in chart.planets:
        if p.house in key_houses and p.house not in focus:
            focus.append(p.house)

    if 1 not in focus:
        focus.append(1)
    if 10 not in focus:
        focus.append(10)

    for h in focus:
        txt = ""
        if isinstance(KB_HOUSE_KEYWORDS.get(str(h)), dict):
            txt = KB_HOUSE_KEYWORDS.get(str(h), {}).get("description", "")
        else:
            txt = KB_HOUSE_KEYWORDS.get(str(h), "")

        if not txt:
            generic = {
                1: "identity & self-presentation",
                4: "home & roots",
                7: "partnerships & contracts",
                10: "career & reputation",
            }
            txt = generic.get(h, "")

        if txt:
            texts.append(f"{h}ᵗʰ house: {txt}")

    return focus, texts


def _collect_strengths_challenges(chart: ChartModel) -> Tuple[List[str], List[str]]:
    strengths: List[str] = []
    challenges: List[str] = []

    if "Fire" in (chart.dominant_elements or []):
        strengths.append("Strong initiative and creative drive.")
    if "Fixed" in (chart.dominant_modalities or []):
        strengths.append("Persistence and follow-through under pressure.")

    for a in chart.aspects:
        if a.aspect in ("square", "opposition") and a.orb <= 4.0:
            challenges.append(f"Tension between {a.p1} and {a.p2} calls for balance and patience.")
            if len(challenges) >= 4:
                break

    return strengths[:4], challenges[:4]


# ---------------------------------------------------
# CORE
# ---------------------------------------------------
def analyze_chart(chart: ChartModel, max_aspects: int = 12) -> HoroscopeProfile:
    """
    Deterministic chart interpretation + Phase 9 precision layers.
    """

    placements_out: List[PlacementText] = []

    asc_arche = KB_PLANETARY_ARCH.get("Ascendant", {}).get("description", "")
    mc_arche = KB_PLANETARY_ARCH.get("MC", {}).get("description", "")

    planet_by_name: Dict[str, PlanetPlacement] = {p.name: p for p in chart.planets}
    ordered_names = [n for n in PLACEMENT_ORDER if n in planet_by_name] + \
                    [p.name for p in chart.planets if p.name not in PLACEMENT_ORDER]

    # Placements
    for name in ordered_names:
        p = planet_by_name[name]
        sign_text = _get_sign_text(p.name, p.sign)
        house_text = _get_house_text(p.name, p.house)

        composite_parts: List[str] = []
        if KB_PLANETARY_ARCH.get(p.name, {}).get("description"):
            composite_parts.append(KB_PLANETARY_ARCH[p.name]["description"])
        if sign_text:
            composite_parts.append(sign_text)
        if house_text:
            ht = house_text[0].lower() + house_text[1:] if house_text and house_text[0].isalpha() else house_text
            composite_parts.append(f"In the {p.house}ᵗʰ house, {ht}")

        comp_str = " ".join([s.strip().rstrip(".") for s in composite_parts if s]).strip()
        composite = (comp_str + ".") if comp_str else None

        placements_out.append(
            PlacementText(
                name=p.name,
                sign=p.sign,
                house=p.house,
                text_sign=sign_text or None,
                text_house=house_text or None,
                composite=composite,
            )
        )

    # Aspects
    aspect_texts: List[AspectText] = []
    for a in chart.aspects[:max_aspects]:
        txt = _get_aspect_text(a.p1, a.p2, a.aspect)
        aspect_texts.append(
            AspectText(
                p1=a.p1,
                aspect=a.aspect,
                p2=a.p2,
                orb=a.orb,
                text=txt or None,
            )
        )

    # House focus, strengths, challenges
    house_focus, house_focus_texts = _house_focus_from_positions(chart)
    strengths, challenges = _collect_strengths_challenges(chart)

    asc_line = f"Ascendant in {chart.asc.sign} {chart.asc.deg_in_sign:.1f}°." if chart.asc else ""
    mc_line = f"MC in {chart.mc.sign} {chart.mc.deg_in_sign:.1f}°." if chart.mc else ""
    overview = " ".join([
        asc_line,
        mc_line,
        f"Dominant elements: {', '.join(chart.dominant_elements or [])}.",
        f"Dominant modalities: {', '.join(chart.dominant_modalities or [])}.",
    ]).strip()

    profile = HoroscopeProfile(
        meta=chart.meta,
        overview=overview or None,
        dominant_elements=chart.dominant_elements or [],
        dominant_modalities=chart.dominant_modalities or [],
        elements_count=chart.elements or {},
        modalities_count=chart.modalities or {},
        asc_summary=asc_arche or None,
        mc_summary=mc_arche or None,
        placements=placements_out,
        aspects=aspect_texts,
        house_focus=house_focus,
        house_focus_texts=house_focus_texts,
        strengths=strengths,
        challenges=challenges,
        tips=[
            "Channel fixed determination into one priority at a time.",
            "Balance action (fire) with reflection and rest.",
        ],
    )

    # -------------------------------------------
    # Phase 9.5 — Baseline PlanetPrecision + Contextual weights + Tone
    # -------------------------------------------
    base_precision: Dict[str, PlanetPrecision] = {}

    for p in chart.planets:
        # Very light heuristics; dignities engine can overwrite later.
        if p.house in (1, 4, 7, 10):
            house_weight = 0.7
        elif p.house in (2, 5, 8, 11):
            house_weight = 0.5
        else:
            house_weight = 0.3

        hierarchy = 0.8 if p.name in ("Sun", "Moon", "Ascendant", "MC") else 0.5

        base_precision[p.name] = PlanetPrecision(
            essential=0.0,
            accidental=0.0,
            aspectual=0.0,
            hierarchy=hierarchy,
            house=house_weight,
            speed=1.0,
            temperament=0.0,
            neighbor=0.0,
            stability=1.0,
        )

    contextual_weights: Dict[str, PlanetPrecision] = {}
    for p in chart.planets:
        ctx: Dict[str, object] = {}  # placeholder for future: sect, retrograde, oob, etc.
        contextual_weights[p.name] = apply_contextual_weights(p.name, base_precision[p.name], ctx)

    profile.contextual_weights = contextual_weights
    profile.tone_map = build_tone_map(contextual_weights)
    profile.intensity_vector = dict(profile.tone_map)

    # -------------------------------------------
    # Phase 9.6 — Precision summaries & influence maps
    # -------------------------------------------
    summaries, raw_map, norm_map = build_precision_summary(chart, contextual_weights)
    profile.precision_summaries = summaries
    profile.precision_raw_map = raw_map
    profile.precision_norm_map = norm_map

    # -------------------------------------------
    # Phase 9.7 — Precision envelope
    # -------------------------------------------
    profile.precision_envelope = build_precision_envelope(profile)

    # Optional debug logging
    if settings.DEBUG:
        try:
            from backend.core.logger import logger
            logger.info(
                f"Precision envelope strongest: {profile.precision_envelope.get('strongest', [])}"
            )
        except Exception:
            pass

    # Final deterministic narrative
    profile.final_narrative = render_natal_narrative(profile)
    return profile


def render_natal_narrative(profile: HoroscopeProfile) -> str:
    """Compact narrative (~120–170 words) using profile content."""
    parts: List[str] = []
    if profile.overview:
        parts.append(profile.overview)

    main = [p for p in profile.placements if p.name in ("Sun", "Moon", "Mercury")][:3]
    for pl in main:
        segs: List[str] = []
        if pl.composite:
            segs.append(pl.composite)
        elif pl.text_sign or pl.text_house:
            if pl.text_sign:
                segs.append(pl.text_sign)
            if pl.text_house:
                segs.append(
                    f"In the {pl.house}ᵗʰ house, "
                    f"{pl.text_house[0].lower() + pl.text_house[1:]}"
                )
        if segs:
            parts.append(" ".join(segs))

    noted = [a for a in profile.aspects if a.text][:3]
    if noted:
        parts.append(
            "Key dynamics: "
            + "; ".join([f"{a.p1} {a.aspect} {a.p2}" for a in noted])
            + "."
        )

    if profile.house_focus_texts:
        parts.append("Focus areas: " + "; ".join(profile.house_focus_texts) + ".")

    if profile.tips:
        parts.append(profile.tips[0])

    return " ".join([p.strip() for p in parts if p]).strip()
