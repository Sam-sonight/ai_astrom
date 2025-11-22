# backend/services/ai_service.py
from __future__ import annotations
from typing import List
from backend.core.config import settings
from backend.models.horoscope_profile import HoroscopeProfile

import logging
logger = logging.getLogger("ai_service")

# --- Try dynamic SDK import ---
_OPENAI_READY = False
try:
    if settings.AI_PROVIDER.lower() == "openai" and settings.OPENAI_API_KEY:
        try:
            from openai import OpenAI
            _client = OpenAI(api_key=settings.OPENAI_API_KEY)
            _OPENAI_READY = True
            _MODE = "new"
        except Exception:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            _OPENAI_READY = True
            _MODE = "legacy"
except Exception as e:
    logger.warning(f"AIService init failed: {e}")
    _OPENAI_READY = False


class AIService:
    """
    Unified AI narrative generator.
    - Option B: OpenAI (chat completion)
    - Option A: deterministic fallback
    """

    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = getattr(settings, "AI_MAX_TOKENS", 800)

    # -------------------------------------------------------
    # PUBLIC
    # -------------------------------------------------------
    def generate_interpretation(self, profile: HoroscopeProfile) -> str:
        if self.provider == "openai" and _OPENAI_READY:
            try:
                return self._generate_with_openai(profile)
            except Exception as e:
                logger.error(f"OpenAI call failed → fallback: {e}")
                return self._generate_fallback(profile)
        return self._generate_fallback(profile)

    # -------------------------------------------------------
    def _generate_with_openai(self, profile: HoroscopeProfile) -> str:
        sys_prompt = (
            "You are a professional astrologer writing a highly personalized natal horoscope.\n"
            "Guidelines:\n"
            "- Produce 170–230 words in one or two paragraphs.\n"
            "- Integrate ASC/MC, dominant elements, 3–5 key placements or aspects.\n"
            "- Respect which planets are strongest/weaker (precision envelope).\n"
            "- Tone: warm, modern, intelligent, not fatalistic.\n"
            "- Conclude with a grounded, empowering insight.\n"
        )

        user_prompt = (
            "Use the structured analysis below to craft a precise interpretation:\n\n"
            f"{self._profile_summary(profile)}\n\n"
            f"{self._build_precision_prompt(profile)}"
        )

        if _MODE == "new":
            resp = _client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return (resp.choices[0].message.content or "").strip()

        # legacy
        import openai
        resp = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        c = resp["choices"][0]
        content = c["message"]["content"] if isinstance(c["message"], dict) else c.message.content
        return (content or "").strip()

    # -------------------------------------------------------
    def _generate_fallback(self, profile: HoroscopeProfile) -> str:
        parts: List[str] = []

        if profile.overview:
            parts.append(profile.overview.rstrip(".") + ".")

        if profile.house_focus:
            parts.append("Focus areas: " + ", ".join(map(str, profile.house_focus)) + ".")

        if profile.precision_summaries:
            # Take 1–2 key precision sentences
            top = list(profile.precision_summaries.values())[:2]
            parts.append("Planetary emphasis: " + " ".join(top))

        if profile.aspects:
            aspects = ", ".join(f"{a.p1} {a.aspect} {a.p2}" for a in profile.aspects[:2])
            parts.append("Notable aspects: " + aspects + ".")

        parts.append(
            "Practical tip: anchor yourself in one intention today and act with consistency rather than speed."
        )
        return " ".join(parts).strip()

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------
    def _profile_summary(self, profile: HoroscopeProfile) -> str:
        lines = [f"- Overview: {profile.overview}"]
        for p in (profile.placements or [])[:5]:
            lines.append(f"- {p.name}: {p.composite or p.text_sign or ''}")
        for a in (profile.aspects or [])[:5]:
            lines.append(f"- {a.p1} {a.aspect} {a.p2}: {a.text or ''}")
        return "\n".join(lines)

    def _build_precision_prompt(self, profile: HoroscopeProfile) -> str:
        env = profile.precision_envelope or {}

        strongest = env.get("strongest", [])
        weakest = env.get("weakest", [])
        planet_summaries = env.get("planet_summaries", {})
        tone_avg = env.get("tone_average", 0.0)
        tone_tend = env.get("tone_tendencies", [])

        lines: List[str] = ["Precision envelope insights:"]

        if strongest:
            s = ", ".join(f"{i['planet']} ({i['strength']})" for i in strongest)
            lines.append(f"- Strongest influences: {s}")

        if weakest:
            w = ", ".join(f"{i['planet']} ({i['strength']})" for i in weakest)
            lines.append(f"- Weaker influences: {w}")

        if tone_tend:
            lines.append(f"- Tone tendency: {tone_tend[0]} (avg={tone_avg})")

        if planet_summaries:
            top2 = list(planet_summaries.values())[:2]
            lines.append("- Key planetary summaries: " + "; ".join(top2))

        return "\n".join(lines)
