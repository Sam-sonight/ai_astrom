# backend/tests/test_astro_precision_api.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_astro_compute_precision_layer():
    payload = {
        "dt_local": "1977-11-16T00:10:00",
        "lat": 33.8938,
        "lon": 35.5018,
        "tz_name": "",
        "include_angles_in_aspects": True,
    }

    resp = client.post("/astro/compute", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    # Core fields
    assert "overview" in data
    assert "narrative" in data
    assert "markdown_report" in data

    # Precision JSON
    assert "tone_map" in data
    assert "precision_envelope" in data
    assert "precision_norm_map" in data

    env = data["precision_envelope"]
    assert isinstance(env, dict)
    assert "strongest" in env
