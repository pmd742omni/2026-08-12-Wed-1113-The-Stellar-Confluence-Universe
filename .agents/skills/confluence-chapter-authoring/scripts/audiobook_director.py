#!/usr/bin/env python3
"""
Audiobook Performance & Sound Design Studio Director for The Stellar Confluence Universe
Compiles written chapter prose into production-ready voice acting and sound design performance scripts
complete with ambient soundscape loop cues, character voice direction tags, and dramatic pacing pauses.
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

def generate_audiobook_script(chapter_text, book_id=1):
    char_info = chapter_engine.get_character_info(book_id)
    hero = char_info["hero"] if char_info else "Hero"
    world = char_info["world"] if char_info else "Homeworld"
    faction = char_info["faction"] if char_info else "Faction"

    # Ambient Soundscape Header based on Faction
    if "Sun" in faction:
        soundscape = f"[SOUNDSCAPE: Whistling desert wind over copper dunes; subtle 144.2 MHz crystal relay hum; warm analog acoustic guitar]"
    elif "Void" in faction:
        soundscape = f"[SOUNDSCAPE: Quiet subterranean echo; low basalt resonant chime at 128.5 MHz; gentle water dripping in eclipse shadow]"
    elif "Astrolabe" in faction:
        soundscape = f"[SOUNDSCAPE: Rhythmic clockwork gear train ticks; precision flywheel spin; distant brass steam whistle]"
    else:
        soundscape = f"[SOUNDSCAPE: Interstellar wind gliding over ice dust tail; soft vapor thruster hum]"

    lines = chapter_text.strip().split("\n")
    script_blocks = []
    script_blocks.append(f"# AUDIOBOOK RECORDING SCRIPT: Book {book_id:02d} ({char_info['title'] if char_info else ''})")
    script_blocks.append(soundscape)
    script_blocks.append("[DIRECTOR NOTE: Maintain warm, wonder-filled, courageous pacing in the style of Studio Ghibli / Avatar: TLA.]\n")

    for line in lines:
        clean = line.strip()
        if not clean or clean.startswith("#") or clean.startswith("**") or clean.startswith("---"):
            continue

        # Check for dialogue quotes
        quotes = re.findall(r'"([^"]*)"', clean)
        if quotes:
            # Process dialogue with voice acting tags
            script_line = clean
            for q in quotes:
                if hero in clean:
                    tag = f'[VOICE: {hero} (Eager, courageous, youthful)] "{q}"'
                elif "Theron" in clean or "Master" in clean:
                    tag = f'[VOICE: Master Theron (Warm, gravelly, mentoring)] "{q}"'
                else:
                    tag = f'[VOICE: Speaker (Natural, expressive)] "{q}"'
                script_line = script_line.replace(f'"{q}"', tag)
            
            # Add subtle SFX for dramatic actions
            if "steam" in clean.lower() or "hiss" in clean.lower():
                script_line = f"[FX: Thermal coolant release valve hisssss] {script_line}"
            elif "click" in clean.lower() or "gear" in clean.lower():
                script_line = f"[FX: Heavy brass gear locking in place - CLICK] {script_line}"
            elif "flare" in clean.lower() or "beacon" in clean.lower():
                script_line = f"[FX: Resonant harmonic chime ring] {script_line}"

            script_blocks.append(script_line)
            script_blocks.append("[PAUSE: 0.8s]")
        else:
            # Descriptive narration
            narration = clean
            if "twin suns" in clean.lower():
                narration = f"[FX: Subtle solar wind flare] {narration}"
            script_blocks.append(f"[NARRATOR (Warm, engaging, gentle cadence)]: {narration}")
            script_blocks.append("[PAUSE: 0.5s]")

    full_script = "\n".join(script_blocks)
    return {
        "status": "SCRIPT_COMPILED",
        "book_id": book_id,
        "hero": hero,
        "world": world,
        "soundscape_track": soundscape,
        "script_line_count": len(script_blocks),
        "production_script": full_script
    }

def process_file_to_audio_script(file_path, book_id=1):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return generate_audiobook_script(text, book_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audiobook Performance & Sound Design Director")
    parser.add_argument("--file", help="Path to markdown chapter file")
    parser.add_argument("--book", type=int, default=1)

    args = parser.parse_args()
    if args.file:
        res = process_file_to_audio_script(args.file, args.book)
    else:
        sample = """
The twin suns of Helios Prime climbed into the sky.
"Watch your heat gauge, Caelum!" called out Master Theron.
Caelum turned the wheel. The brass pin clicked into place!
"""
        res = generate_audiobook_script(sample, args.book)
    print(json.dumps(res, indent=2))
