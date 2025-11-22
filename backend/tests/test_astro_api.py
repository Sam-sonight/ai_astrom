import sys, os, pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.mark.asyncio
async def test_astro_compute_endpoint():
    """
    ✅ Integration test: /astro/compute
    Ensures endpoint returns all expected keys with valid data structure.
    """

    payload = {
        "dt_local": "1977-11-16T00:10:00",
        "lat": 33.8938,
        "lon": 35.5018,
        "tz_name": "",
        "include_angles_in_aspects": True
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/astro/compute", json=payload)
        assert response.status_code == 200, response.text

        data = response.json()
        assert "overview" in data
        assert "narrative" in data
        assert "markdown_report" in data

        # Optional: Save output for inspection
        out_path = os.path.join(os.getcwd(), "astro_response_test.json")
        with open(out_path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Saved response to {out_path}")
