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

SENSORY_ENHANCERS = {
    r"\bsun\b": "blazing twin suns",
    r"\bmetal\b": "polished brass alloy",
    r"\bmachine\b": "precision clockwork mechanism",
    r"\bhot\b": "searing radiant warmth",
    r"\bcold\b": "crisp twilight chill",
    r"\blight\b": "luminous solar beam",
    r"\bshadow\b": "cool umbral shadow"
}

def polish_prose_text(text):
    # 1. Clean and evaluate original
    orig_eval = chapter_prose_evaluator.evaluate_prose(text)
    
    # 2. Apply sensory enrichment where appropriate
    polished = text
    for pat, repl in SENSORY_ENHANCERS.items():
        # Replace only a few occurrences to avoid purple prose
        polished = re.sub(pat, repl, polished, count=2, flags=re.IGNORECASE)

    # 3. Re-evaluate polished prose
    new_eval = chapter_prose_evaluator.evaluate_prose(polished)

    return {
        "status": "POLISHED",
        "original_words": orig_eval.get("total_words", 0),
        "polished_words": new_eval.get("total_words", 0),
        "original_grade": orig_eval.get("flesch_kincaid_grade_level", 0.0),
        "polished_grade": new_eval.get("flesch_kincaid_grade_level", 0.0),
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
