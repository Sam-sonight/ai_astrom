# backend/astro_engine/aspects_detector.py
from typing import Dict, Iterable, List, Tuple, Optional
from backend.astro_engine.models.chart_model import AspectLink

# (name, angle, base_orb)
DEFAULT_ASPECT_DEFS: Tuple[Tuple[str, int, int], ...] = (
    ("conjunction", 0, 8),
    ("sextile", 60, 6),
    ("square", 90, 7),
    ("trine", 120, 8),
    ("quincunx", 150, 3),
    ("opposition", 180, 8),
)

def _angle_diff(a: float, b: float) -> float:
    """Smallest separation 0..180."""
    d = abs((a - b + 180.0) % 360.0 - 180.0)
    return d

def detect_aspects(
    lon_map: Dict[str, float],
    aspect_defs: Iterable[Tuple[str, int, int]] = DEFAULT_ASPECT_DEFS,
    moon_extra_orb: int = 2,
    include_pairs: Optional[Iterable[Tuple[str, str]]] = None,
) -> List[AspectLink]:
    """
    Detect aspects among bodies in lon_map.
    lon_map: {'Sun': 56.1, 'Moon': 320.5, ...}
    include_pairs: optional explicit pairs to check; if None, all unique pairs.
    """
    names = list(lon_map.keys())
    pairs: List[Tuple[str, str]]
    if include_pairs:
        pairs = list(include_pairs)
    else:
        pairs = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                pairs.append((names[i], names[j]))

    results: List[AspectLink] = []
    for p1, p2 in pairs:
        a1 = lon_map[p1]
        a2 = lon_map[p2]
        sep = _angle_diff(a1, a2)
        for name, angle, base_orb in aspect_defs:
            orb = base_orb
            if p1 == "Moon" or p2 == "Moon":
                orb = max(orb, base_orb + moon_extra_orb)
            delta = abs(sep - angle)
            if delta <= orb:
                results.append(
                    AspectLink(
                        p1=p1,
                        p2=p2,
                        aspect=name,
                        angle=round(sep, 3),
                        orb=round(delta, 3),
                    )
                )
    # sort by tightness (smaller orb first)
    results.sort(key=lambda x: (x.orb, abs(x.angle - 180.0)))
    return results
