# backend/services/report_builder.py
from __future__ import annotations
from typing import List
from backend.models.horoscope_profile import HoroscopeProfile, PlacementText, AspectText


def build_markdown_report(profile: HoroscopeProfile, ai_text: str) -> str:
    """Render a Markdown-formatted horoscope report."""
    lines: List[str] = []
    lines.append("# AI Astrom — Personalized Horoscope Report\n")

    if profile.overview:
        lines.append(f"**Overview:** {profile.overview}\n")

    if profile.house_focus:
        focus_str = ", ".join([str(h) for h in profile.house_focus])
        lines.append(f"**House Focus:** {focus_str}\n")

    # AI-generated interpretation
    lines.append("## Interpretation\n")
    lines.append(ai_text.strip() + "\n")

    # Placements
    if profile.placements:
        lines.append("## Key Placements\n")
        for p in profile.placements[:12]:
            summary = p.composite or p.text_sign or p.text_house or ""
            lines.append(f"- **{p.name} in {p.sign} (House {p.house})** — {summary}")

    # Aspects
    if profile.aspects:
        lines.append("\n## Notable Aspects\n")
        for a in profile.aspects[:12]:
            tag = f"**{a.p1} {a.aspect} {a.p2}** (orb {a.orb})"
            desc = (a.text or "").strip()
            lines.append(f"- {tag}: {desc}")

    return "\n".join(lines).strip()


def build_plain_text(profile: HoroscopeProfile, ai_text: str) -> str:
    """Render a plain text version of the report."""
    md = build_markdown_report(profile, ai_text)
    txt = (
        md.replace("# ", "")
          .replace("## ", "")
          .replace("**", "")
          .strip()
    )
    return txt
