from backend.astro_engine.tone_utils import build_tone_map
from backend.models.horoscope_profile import PlanetPrecision

def test_tone_map_generation():
    weights = {
        "Sun": PlanetPrecision(essential=0.8, accidental=0.7, hierarchy=0.9, house=0.6, stability=0.9),
        "Moon": PlanetPrecision(essential=0.5, accidental=0.5, hierarchy=0.4, house=0.6, stability=0.7)
    }
    tone = build_tone_map(weights)
    assert isinstance(tone, dict)
    assert "Sun" in tone
    assert 0.0 <= tone["Sun"] <= 1.0
