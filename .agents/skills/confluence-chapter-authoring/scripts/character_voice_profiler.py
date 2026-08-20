#!/usr/bin/env python3
"""
Linguistic Dialect & Character Voice Profiler for The Stellar Confluence Universe
Audits chapter dialogue quotes against faction-specific cultural speech patterns,
metaphors, and vocabulary banks to ensure authentic character voices across all 74 storylines.
"""

import os
import sys
import json
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_project_root():
    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, "00_System_State")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))

PROJECT_ROOT = find_project_root()
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

import chapter_engine

FACTION_VOCABULARY_BANKS = {
    "Sun-Forged": {
        "keywords": ["lens", "solar", "horizon", "focus", "light", "bronze", "mirror", "furnace", "radiant", "beam", "dawn", "flare", "photonic", "sun"],
        "tone": "Direct, confident, radiant, warm, bold optimism",
        "example_idiom": "Keep your lens clear and hold the focus."
    },
    "Void-Bound": {
        "keywords": ["shadow", "twilight", "silence", "basalt", "listen", "whisper", "eclipse", "drift", "cool", "nadir", "phase", "umbral", "shroud", "chasm"],
        "tone": "Soft-spoken, contemplative, quiet wisdom, observant",
        "example_idiom": "Step softly in the twilight shadow."
    },
    "Astrolabe": {
        "keywords": ["gear", "balance", "flywheel", "ratio", "torque", "precision", "tolerance", "steam", "crank", "pinion", "clockwork", "escapement", "brass", "dial"],
        "tone": "Analytical, measured, rhythmic, engineering focus",
        "example_idiom": "Check the gear ratio before applying torque."
    },
    "Comet-Riders": {
        "keywords": ["glide", "wake", "vapor", "plume", "speed", "ice", "drift", "crest", "thruster", "sail", "harpoon", "sublimation", "frost", "slingshot"],
        "tone": "Spirited, adventurous, swift, dynamic energy",
        "example_idiom": "Catch the high vapor wake and ride the plume."
    },
    "Nebula-Weavers": {
        "keywords": ["weave", "filament", "loom", "strand", "magnetic", "silk", "gas", "glow", "tangle", "spindle", "plasma", "tapestry"],
        "tone": "Artistic, patient, interconnected, perceptive",
        "example_idiom": "Every strand in the nebula carries the tension of the whole web."
    },
    "Deep-Core Miners": {
        "keywords": ["core", "drill", "seismic", "basalt", "pressure", "piston", "tremor", "hydraulic", "forge", "fault", "strata", "heft"],
        "tone": "Grounded, resolute, steady, indomitable grit",
        "example_idiom": "Trust the bedrock under your boots and respect the pressure valve."
    },
    "Gravity-Surfers": {
        "keywords": ["singularity", "orbit", "dive", "graviton", "vector", "tide", "well", "freefall", "anchor", "curve", "momentum", "slant"],
        "tone": "Fearless, intuitive, kinetic, thrill of discovery",
        "example_idiom": "Lean into the gravitational curve and let the well slingshot you home."
    },
    "Plasma-Shepherds": {
        "keywords": ["herd", "plasma", "crook", "flare", "coronal", "lasso", "containment", "magnetic", "sparks", "field", "current", "ember"],
        "tone": "Protective, vigilant, lively, spirited stewardship",
        "example_idiom": "Keep the magnetic crook high and guide the coronal herd with a light touch."
    },
    "Chrono-Navigators": {
        "keywords": ["chronometer", "tick", "temporal", "sextant", "drift", "path", "probability", "cadence", "interval", "horizon", "course", "tachyon"],
        "tone": "Precise, visionary, calm, contemplative foresight",
        "example_idiom": "Watch the second hand align before charting the warp course."
    },
    "Bio-Alchemists": {
        "keywords": ["spore", "bloom", "chitin", "photosynthesis", "sap", "canopy", "vine", "root", "bioluminescent", "symbiosis", "nectar", "seed"],
        "tone": "Nurturing, inquisitive, organic, harmonious",
        "example_idiom": "Feed the seedling before you ask it to hold the storm wall."
    },
    "Crystal-Singers": {
        "keywords": ["chime", "harmonic", "quartz", "resonance", "pitch", "vibration", "clarity", "facet", "echo", "tuning", "sonance", "prism"],
        "tone": "Melodic, empathetic, luminous, resonant",
        "example_idiom": "When the crystal chimes true, the path opens clear."
    },
    "Tide-Wardens": {
        "keywords": ["tide", "swell", "current", "hydro", "depth", "beacon", "crest", "surge", "wake", "channel", "reef", "buoy"],
        "tone": "Vigilant, adaptable, rhythmic, oceanic focus",
        "example_idiom": "Read the rising swell before setting your rudder."
    },
    "Magnetar-Leapers": {
        "keywords": ["charge", "pole", "flux", "pulse", "arc", "leap", "polar", "repulsion", "circuit", "spark", "field", "lightning"],
        "tone": "Electrifying, brisk, daring, fast-paced",
        "example_idiom": "Match polarities on the leap, or the field will throw you into orbit."
    },
    "Aurora-Weavers": {
        "keywords": ["aurora", "shimmer", "curtain", "spectral", "emerald", "glow", "sky", "ribbon", "dazzle", "harmony", "prism", "veil"],
        "tone": "Luminous, whimsical, poetic, awe-inspiring",
        "example_idiom": "Follow the emerald curtain where the sky breathes light."
    },
    "Void-Nomads": {
        "keywords": ["starway", "caravan", "drift", "beacon", "hull", "passage", "crossroads", "wayfarer", "compass", "oasis", "haven"],
        "tone": "Worldly, resourceful, hospitable, open-hearted",
        "example_idiom": "A warm lantern in deep space turns any stranger into family."
    },
    "Solar-Artificers": {
        "keywords": ["forge", "temper", "alloy", "crucible", "optic", "refract", "furnace", "chisel", "amber", "polish", "quench"],
        "tone": "Craftsman-like, patient, disciplined, exacting pride",
        "example_idiom": "Measure three times in cold shadow before cutting in hot sun."
    },
    "Stardust-Cartographers": {
        "keywords": ["chart", "constellation", "quadrant", "meridian", "parsec", "beacon", "horizon", "survey", "atlas", "vector"],
        "tone": "Scholarly, curious, pioneering, methodical wonder",
        "example_idiom": "Every uncharted star has a story waiting for an open notebook."
    }
}

def get_faction_voice_profile(faction):
    matched_faction = "Sun-Forged"
    for k in FACTION_VOCABULARY_BANKS.keys():
        if k.lower() in str(faction).lower():
            matched_faction = k
            break
    prof = FACTION_VOCABULARY_BANKS[matched_faction]
    return {
        "dialect_name": matched_faction,
        "cadence": prof["tone"],
        "typical_idioms": [prof["example_idiom"]],
        "keywords": prof["keywords"]
    }

def analyze_character_dialogue(chapter_text, book_id=1):
    char_info = chapter_engine.get_character_info(book_id)
    faction = char_info["faction"] if char_info else "Sun-Forged"
    hero = char_info["hero"] if char_info else "Hero"

    # Match faction key
    matched_faction = "Sun-Forged"
    for k in FACTION_VOCABULARY_BANKS.keys():
        if k.lower() in faction.lower():
            matched_faction = k
            break

    profile = FACTION_VOCABULARY_BANKS[matched_faction]
    keywords = set(profile["keywords"])

    # Extract dialogue quotes
    quotes = re.findall(r'"([^"]*)"', chapter_text)
    if not quotes:
        return {
            "status": "NO_DIALOGUE_FOUND",
            "message": "No spoken dialogue quotes found in chapter text."
        }

    total_words = 0
    matched_hits = 0
    analyzed_quotes = []

    for q in quotes:
        words = re.findall(r'\b[A-Za-z]+\b', q.lower())
        total_words += len(words)
        hits = [w for w in words if w in keywords]
        matched_hits += len(hits)
        analyzed_quotes.append({
            "quote": q,
            "cultural_terms_found": hits
        })

    # Calculate cultural resonance score
    density = (matched_hits / max(1, total_words)) * 100.0
    score = min(100.0, round(density * 15.0 + 40.0, 1))

    return {
        "status": "ANALYSIS_COMPLETE",
        "book_id": book_id,
        "hero": hero,
        "faction_dialect": matched_faction,
        "cultural_authenticity_score": score,
        "dialect_tone": profile["tone"],
        "signature_idiom": profile["example_idiom"],
        "total_dialogue_quotes": len(quotes),
        "total_dialogue_words": total_words,
        "cultural_keywords_matched": matched_hits,
        "quotes": analyzed_quotes[:3]
    }

def analyze_chapter_file(file_path, book_id=1):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found."}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return analyze_character_dialogue(text, book_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linguistic Dialect & Character Voice Profiler")
    parser.add_argument("--file", help="Path to markdown chapter file")
    parser.add_argument("--book", type=int, default=1)

    args = parser.parse_args()
    if args.file:
        res = analyze_chapter_file(args.file, args.book)
    else:
        sample = '''"Watch your heat gauge, Caelum!" said Theron. "The solar beam is ready."'''
        res = analyze_character_dialogue(sample, args.book)
    print(json.dumps(res, indent=2))
