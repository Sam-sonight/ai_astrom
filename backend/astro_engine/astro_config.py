# backend/astro_engine/astro_config.py

from enum import Enum

class Element(str, Enum):
    FIRE = "Fire"
    EARTH = "Earth"
    AIR = "Air"
    WATER = "Water"

class Modality(str, Enum):
    CARDINAL = "Cardinal"
    FIXED = "Fixed"
    MUTABLE = "Mutable"

ASPECT_ORBS = {
    "conjunction": 8.0,
    "opposition": 8.0,
    "trine": 7.0,
    "square": 6.0,
    "sextile": 5.0,
    "quincunx": 3.0,
    "semisextile": 2.0,
    "parallel": 1.0,
}

DIGNITY_SCORES = {
    "rulership": 1.00,
    "exaltation": 0.80,
    "triplicity": 0.60,
    "term": 0.40,
    "face": 0.25,
    "peregrine": 0.10,
    "detriment": -0.40,
    "fall": -0.80,
}

ACCIDENTAL_FACTORS = {
    "angular": 0.30,
    "succedent": 0.15,
    "cadent": 0.05,
    "retrograde": -0.10,
    "combust": -0.20,
}

ASPECT_WEIGHTS = {
    "conjunction": 1.00,
    "opposition": 0.90,
    "trine": 0.85,
    "square": 0.75,
    "sextile": 0.60,
    "quincunx": 0.40,
}

HOUSE_CUSP_SIGMA = 3.0
LOG_LEVEL = "INFO"

# ==========================================================
# Phase 9.4 — Contextual Weighting Constants
# ==========================================================
CONTEXT_RULES = {
    "angular_boost": 1.15,
    "succedent_boost": 1.05,
    "cadent_drop": 0.9,
    "retrograde_penalty": 0.85,
    "swift_bonus": 1.10,
    "cazimi_bonus": 1.20,
    "combust_penalty": 0.75,
    "under_beams_penalty": 0.9,
    "oob_penalty": 0.95,
    "sect_bonus": 1.05,
    "mutual_reception_bonus": 1.10,
    "speed_fast_bonus": 1.10,
    "speed_slow_penalty": 0.90,
}
