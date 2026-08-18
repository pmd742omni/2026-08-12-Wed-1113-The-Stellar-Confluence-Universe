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
        "keywords": ["lens", "solar", "horizon", "focus", "light", "bronze", "mirror", "furnace", "radiant", "beam", "dawn"],
        "tone": "Direct, confident, radiant, warm, bold optimism",
        "example_idiom": "Keep your lens clear and hold the focus."
    },
    "Void-Bound": {
        "keywords": ["shadow", "twilight", "silence", "basalt", "listen", "whisper", "eclipse", "drift", "cool", "nadir", "phase"],
        "tone": "Soft-spoken, contemplative, quiet wisdom, observant",
        "example_idiom": "Step softly in the twilight shadow."
    },
    "Astrolabe": {
        "keywords": ["gear", "balance", "flywheel", "ratio", "torque", "precision", "tolerance", "steam", "crank", "pinion", "clockwork"],
        "tone": "Analytical, measured, rhythmic, engineering focus",
        "example_idiom": "Check the gear ratio before applying torque."
    },
    "Comet-Riders": {
        "keywords": ["glide", "wake", "vapor", "plume", "speed", "ice", "drift", "crest", "thruster", "sail", "harpoon"],
        "tone": "Spirited, adventurous, swift, dynamic energy",
        "example_idiom": "Catch the high vapor wake and ride the plume."
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
    # Expected density ~ 3-8%
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
