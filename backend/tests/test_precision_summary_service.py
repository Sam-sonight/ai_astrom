# backend/tests/test_precision_summary_service.py
from backend.services.precision_summary_service import build_precision_summary
from backend.models.horoscope_profile import PlanetPrecision

def test_precision_summary_high_fidelity():
    mock = {
        "Sun": PlanetPrecision(
            essential=0.9, accidental=0.8, aspectual=0.6, hierarchy=0.7,
            house=0.6, speed=0.9, temperament=0.8, neighbor=0.7, stability=0.9
        ),
        "Saturn": PlanetPrecision(
            essential=0.5, accidental=0.4, aspectual=0.3, hierarchy=0.3,
            house=0.3, speed=0.5, temperament=0.4, neighbor=0.4, stability=0.5
        ),
    }
    summaries, raw_map, norm_map = build_precision_summary(None, mock)

    assert "Sun" in summaries and "Saturn" in summaries
    assert raw_map["Sun"] > raw_map["Saturn"]
    assert 0.0 <= norm_map["Sun"] <= 1.0
    assert "baseline" in summaries["Sun"]
