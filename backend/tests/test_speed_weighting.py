from backend.astro_engine.context_weights import apply_contextual_weights
from backend.models.horoscope_profile import PlanetPrecision

def test_speed_bonus_and_penalty():
    base = PlanetPrecision(
        essential=0.6, accidental=0.5, hierarchy=0.4, house=0.3,
        speed=0.7, stability=0.8, temperament=0.6, neighbor=0.4
    )

    fast_ctx = {"speed_ratio": 1.2}
    slow_ctx = {"speed_ratio": 0.8}

    fast = apply_contextual_weights("Mercury", base, fast_ctx)
    slow = apply_contextual_weights("Mercury", base, slow_ctx)

    assert fast.speed > base.speed
    assert slow.speed < base.speed
    assert fast.accidental > slow.accidental
