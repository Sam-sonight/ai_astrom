# backend/tests/test_astro_ai_fallback.py
import pytest
from backend.services.ai_service import AIService
from backend.models.horoscope_profile import HoroscopeProfile

@pytest.mark.asyncio
async def test_ai_fallback_generation():
    """
    Validate AIService deterministic fallback works without OpenAI.
    """
    ai = AIService()
    dummy_profile = HoroscopeProfile(
        overview="Ascendant in Virgo 7.2°. MC in Gemini 4.8°.",
        dominant_elements=["Fire", "Water"],
        dominant_modalities=["Fixed"],
        placements=[],
        aspects=[],
        house_focus=[1, 4, 10],
    )

    text = ai.generate_interpretation(dummy_profile)
    assert isinstance(text, str)
    assert len(text) > 50
    # Should contain either key summary or fallback tip
    assert "Ascendant" in text or "Practical tip" in text
