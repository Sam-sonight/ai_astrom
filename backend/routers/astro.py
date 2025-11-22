# backend/routers/astro.py
from fastapi import APIRouter, HTTPException

from backend.models.astro_request import ChartRequest
from backend.astro_engine.chart_generator import build_natal_chart
from backend.services.horoscope_service import analyze_chart
from backend.services.ai_service import AIService
from backend.services.report_builder import build_markdown_report

router = APIRouter(prefix="/astro", tags=["Astrology"])


@router.post("/compute")
def compute_chart(request: ChartRequest):
    """
    Compute natal chart → analyze → AI narrative → Markdown report + precision JSON.
    """
    try:
        # 1️⃣ Generate natal chart
        chart = build_natal_chart(
            request.dt_local,
            request.lat,
            request.lon,
            request.tz_name,
            request.include_angles_in_aspects,
        )

        # 2️⃣ Deterministic analysis + precision layers
        profile = analyze_chart(chart, max_aspects=12)

        # 3️⃣ AI-enhanced narrative (LLM + precision envelope)
        ai = AIService()
        narrative = ai.generate_interpretation(profile)

        # 4️⃣ Markdown report
        report_md = build_markdown_report(profile, narrative)

        return {
            "overview": profile.overview,
            "dominant_elements": profile.dominant_elements,
            "dominant_modalities": profile.dominant_modalities,
            "narrative": narrative,
            "markdown_report": report_md,
            # Precision JSON for UI / analytics:
            "tone_map": profile.tone_map or {},
            "precision_raw_map": profile.precision_raw_map or {},
            "precision_norm_map": profile.precision_norm_map or {},
            "precision_envelope": profile.precision_envelope or {},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart computation failed: {e}")
