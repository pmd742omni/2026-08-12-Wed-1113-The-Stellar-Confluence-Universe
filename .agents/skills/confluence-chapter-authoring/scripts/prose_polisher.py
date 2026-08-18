#!/usr/bin/env python3
"""
Autonomous Chapter Prose Polisher & Tone Stylist for The Stellar Confluence Universe
Enhances sensory imagery, tunes read-aloud sentence cadence (targeting Grade 4-6 readability),
and sharpens character dialogue in the spirit of Studio Ghibli, Avatar: TLA, and Ender's Game.
"""

import os
import sys
import json
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import chapter_prose_evaluator

FACTION_SENSORY_ENHANCERS = {
    "Sun-Forged": {
        r"\bsun\b": "blazing twin suns",
        r"\bmetal\b": "polished bronze alloy",
        r"\bmachine\b": "precision solar array",
        r"\bhot\b": "searing radiant warmth",
        r"\blight\b": "luminous solar beam"
    },
    "Void-Bound": {
        r"\bshadow\b": "cool umbral shadow",
        r"\bstone\b": "phase-resonant basalt",
        r"\bcold\b": "crisp twilight chill",
        r"\bsilence\b": "deep eclipse silence",
        r"\bdark\b": "soft velvet twilight"
    },
    "Astrolabe": {
        r"\bmachine\b": "precision clockwork mechanism",
        r"\bmetal\b": "balanced brass gear-train",
        r"\bturn\b": "crank the precision escapement",
        r"\bwheel\b": "balanced inertial flywheel",
        r"\bnoise\b": "rhythmic clockwork tick"
    },
    "Comet-Riders": {
        r"\bice\b": "glistening cryogenic ice",
        r"\bspeed\b": "swift sublimation thrust",
        r"\bcloud\b": "luminous cometary vapor plume",
        r"\bglide\b": "glide across the icy crest",
        r"\bcold\b": "exhilarating sub-zero rush"
    },
    "Deep-Core": {
        r"\brock\b": "dense subterranean basalt",
        r"\btool\b": "pneumatic seismic drill",
        r"\bheat\b": "geothermal mantle pressure",
        r"\bdeep\b": "deep tectonic bedrock"
    },
    "Bio-Alchemists": {
        r"\bplant\b": "bioluminescent spore canopy",
        r"\barmor\b": "photosynthetic chitin carapace",
        r"\bgrow\b": "rapid photosynthetic bloom",
        r"\bforest\b": "glowing symbiotic canopy"
    }
}

DEFAULT_SENSORY_ENHANCERS = {
    r"\bsun\b": "blazing sun",
    r"\bmetal\b": "polished alloy",
    r"\bmachine\b": "precision mechanism",
    r"\bhot\b": "radiant warmth",
    r"\bcold\b": "crisp chill",
    r"\blight\b": "luminous beam",
    r"\bshadow\b": "cool shadow"
}

def polish_prose_text(text, faction="Sun-Forged", simplify_vocabulary=True):
    # 1. Clean and evaluate original
    orig_eval = chapter_prose_evaluator.evaluate_prose(text)
    
    # 2. Select appropriate sensory enhancer set
    matched_enhancers = DEFAULT_SENSORY_ENHANCERS
    for fac_key, enh_map in FACTION_SENSORY_ENHANCERS.items():
        if fac_key.lower() in str(faction).lower():
            matched_enhancers = enh_map
            break

    # Apply sensory enrichment where appropriate (max 2 replacements per term to avoid purple prose)
    polished = text
    for pat, repl in matched_enhancers.items():
        polished = re.sub(pat, repl, polished, count=2, flags=re.IGNORECASE)

    # 3. Simplify complex academic/adult words for young readers (Grade 4-6)
    replacements_made = []
    if simplify_vocabulary and hasattr(chapter_prose_evaluator, "CHILD_FRIENDLY_SYNONYMS"):
        for complex_word, simple_synonym in chapter_prose_evaluator.CHILD_FRIENDLY_SYNONYMS.items():
            pattern = rf"\b{complex_word}\b"
            if re.search(pattern, polished, re.IGNORECASE):
                polished = re.sub(pattern, simple_synonym, polished, flags=re.IGNORECASE)
                replacements_made.append(f"{complex_word} -> {simple_synonym}")

    # 4. Re-evaluate polished prose
    new_eval = chapter_prose_evaluator.evaluate_prose(polished)

    return {
        "status": "POLISHED",
        "original_words": orig_eval.get("total_words", 0),
        "polished_words": new_eval.get("total_words", 0),
        "original_grade": orig_eval.get("flesch_kincaid_grade_level", 0.0),
        "polished_grade": new_eval.get("flesch_kincaid_grade_level", 0.0),
        "vocabulary_replacements": replacements_made,
        "sensory_faction": faction,
        "polished_cadence": new_eval.get("audio_cadence", {}),
        "polished_text": polished
    }

def polish_chapter_file(file_path, save=False):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found."}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    res = polish_prose_text(content)
    if save and res["status"] == "POLISHED":
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(res["polished_text"])
        res["saved_to_file"] = file_path

    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Prose Polisher & Tone Stylist")
    parser.add_argument("--file", help="Path to markdown chapter file")
    parser.add_argument("--save", action="store_true", help="Overwrite file with polished prose")

    args = parser.parse_args()
    if args.file:
        res = polish_chapter_file(args.file, save=args.save)
    else:
        sample = """Caelum looked at the sun. He felt hot metal under his hands. The machine started to make a humming noise."""
        res = polish_prose_text(sample)
    print(json.dumps(res, indent=2))
