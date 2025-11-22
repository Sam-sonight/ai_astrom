# backend/astro_engine/tests/test_hierarchy_house.py
from backend.astro_engine.dispositor_chain import build_dispositor_chain
from backend.astro_engine.house_blending import blend_nearby_houses
from backend.astro_engine.neighboring_influence import propagate_house_energy
from backend.astro_engine.temperament_index import temperament_profile

def test_dispositor_chain_simple():
    positions = {"Sun": "Leo", "Mars": "Aries", "Venus": "Scorpio"}
    dom = build_dispositor_chain(positions)
    assert dom["Mars"] > 0.5 and "Venus" in dom

def test_house_blending_weights_sum_to_one():
    w = blend_nearby_houses(5, 2.0)
    assert abs(sum(w.values()) - 1) < 0.01

def test_neighboring_influence_conserves_energy():
    houses = {i: 1.0 for i in range(1, 13)}
    new = propagate_house_energy(houses)
    assert round(sum(new.values()), 2) == round(sum(houses.values()), 2)

def test_temperament_profile_output_structure():
    elems = {"Fire": 3, "Water": 2, "Air": 1, "Earth": 4}
    mods = {"Cardinal": 3, "Fixed": 5, "Mutable": 2}
    power = {"Sun": 1.0, "Mars": 0.8, "Venus": 0.5}
    result = temperament_profile(elems, mods, power)
    assert "elements" in result and "balance_index" in result
