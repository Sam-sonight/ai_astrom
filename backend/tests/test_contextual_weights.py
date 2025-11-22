"""
test_contextual_weights.py — validates Phase 9.4 Contextual Weighting logic
"""

import pytest
from backend.astro_engine.context_weights import apply_contextual_weights
from backend.models.horoscope_profile import PlanetPrecision


@pytest.fixture
def base_metrics():
    return PlanetPrecision(
        essential=0.5,
        accidental=0.5,
        aspectual=0.2,
        hierarchy=0.4,
        house=0.3,
        speed=1.0,
        temperament=0.8,
        neighbor=0.2,
    )


def test_angular_boost(base_metrics):
    ctx = {"house_type": "angular"}
    m = apply_contextual_weights("Mars", base_metrics, ctx)
    assert m.accidental > 0.5
    assert m.house > 0.3


def test_retrograde_penalty(base_metrics):
    ctx = {"is_retrograde": True}
    m = apply_contextual_weights("Mercury", base_metrics, ctx)
    assert m.speed < base_metrics.speed


def test_combustion_penalty(base_metrics):
    ctx = {"sun_distance": 6.0}
    m = apply_contextual_weights("Venus", base_metrics, ctx)
    assert m.accidental < base_metrics.accidental


def test_cazimi_bonus(base_metrics):
    ctx = {"sun_distance": 0.2}
    m = apply_contextual_weights("Mercury", base_metrics, ctx)
    assert m.essential > base_metrics.essential


def test_oob_penalty(base_metrics):
    ctx = {"out_of_bounds": True}
    m = apply_contextual_weights("Mars", base_metrics, ctx)
    assert m.accidental < base_metrics.accidental


def test_mutual_reception_bonus(base_metrics):
    ctx = {"mutual_reception": True}
    m = apply_contextual_weights("Venus", base_metrics, ctx)
    assert m.hierarchy > base_metrics.hierarchy
