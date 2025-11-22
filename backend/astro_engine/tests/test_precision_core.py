"""
Unit tests for precision weighting modules.
"""

import pytest
from backend.astro_engine.dignities import essential_dignity
from backend.astro_engine.accidental_power import accidental_power
from backend.astro_engine.aspect_power import aspect_strength

def test_dignity_rulership():
    assert essential_dignity("Mars", "Aries") == 1.0
    assert essential_dignity("Venus", "Taurus") == 1.0
    assert essential_dignity("Jupiter", "Capricorn") == 0.1

def test_accidental_power_combust():
    val = accidental_power(1, retrograde=True, combust=True)
    assert round(val, 2) == pytest.approx(0.0, 0.2)

def test_aspect_strength_curve():
    strong = aspect_strength("trine", orb=1.0, applying=True)
    weak = aspect_strength("trine", orb=6.5, applying=False)
    assert strong > weak
    assert 0 <= strong <= 1
