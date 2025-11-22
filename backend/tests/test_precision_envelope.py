# backend/tests/test_precision_envelope.py
import pytest

from backend.models.horoscope_profile import HoroscopeProfile, PlanetPrecision
from backend.services.precision_envelope import build_precision_envelope


def test_precision_envelope_basic():
    cw = {
        "Sun": PlanetPrecision(
            essential=0.8, accidental=0.7, aspectual=0.6, hierarchy=0.8,
            house=0.7, speed=0.9, temperament=0.6, neighbor=0.5, stability=0.9
        ),
        "Saturn": PlanetPrecision(
            essential=0.4, accidental=0.4, aspectual=0.3, hierarchy=0.3,
            house=0.3, speed=0.5, temperament=0.4, neighbor=0.3, stability=0.7
        ),
    }

    profile = HoroscopeProfile(
        overview="Test profile",
        contextual_weights=cw,
        precision_norm_map={"Sun": 0.9, "Saturn": 0.2},
        precision_summaries={
            "Sun": "Sun: strong essential dignity (weighted influence score: 0.80).",
            "Saturn": "Saturn: baseline influence level (0.40).",
        },
        tone_map={"Sun": 0.8, "Saturn": 0.5},
    )

    env = build_precision_envelope(profile)

    assert "strongest" in env and "weakest" in env
    assert env["strongest"][0]["planet"] == "Sun"
    assert "planet_summaries" in env
    assert "Sun" in env["planet_summaries"]
    assert isinstance(env.get("tone_average"), float)
    assert isinstance(env.get("tone_tendencies"), list)
