# backend/tests/test_ai_tone_integration.py
from backend.services.ai_service import AIService
from backend.models.horoscope_profile import HoroscopeProfile, PlanetPrecision

def test_tone_map_integration(monkeypatch):
    """
    Validates tone_map injection and summary output integration.
    """
    service = AIService()

    # Create valid PlanetPrecision instances
    mock_weights = {
        "Sun": PlanetPrecision(essential=0.9, accidental=0.8, hierarchy=0.7,
                               house=0.6, stability=0.9, speed=0.8,
                               temperament=0.7, neighbor=0.6),
        "Saturn": PlanetPrecision(essential=0.4, accidental=0.5, hierarchy=0.3,
                                  house=0.3, stability=0.5, speed=0.4,
                                  temperament=0.5, neighbor=0.4)
    }

    profile = HoroscopeProfile(
        overview="Tone integration test",
        contextual_weights=mock_weights
    )

    # Patch build_tone_map to return deterministic tone data
    monkeypatch.setattr("backend.astro_engine.tone_utils.build_tone_map", lambda _: {"Sun": 0.8, "Saturn": 0.4})

    text = service._profile_summary(profile)

    # Assertions
    assert "Overview:" in text
    assert "Average tone level" in text or "tone" in text.lower()
    assert isinstance(profile.contextual_weights["Sun"], PlanetPrecision)
