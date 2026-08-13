#!/usr/bin/env python3
"""
Sensory Soundscape & Visual Palette Director for The Stellar Confluence Universe
Extracts audio soundscape cues, onomatopoeia, visual color palettes, and lighting cues
from chapter prose to craft Grade 4-6 child-oriented sensory performance scripts.
"""

import sys
import json
import re

SENSORY_PATTERNS = {
    "AUDIO_ONOMATOPOEIA": [r"\bclack\b", r"\bwhir+\b", r"\bhiss\b", r"\bhum\b", r"\bboom\b", r"\bsnap\b", r"\bchime\b", r"\brumble\b", r"\bcrackle\b"],
    "VISUAL_PALETTE": [r"\bgolden\b", r"\bbronze\b", r"\bamber\b", r"\bcopper\b", r"\bazure\b", r"\bviolet\b", r"\bshadowy\b", r"\bdazzling\b", r"\bcrimson\b"],
    "TACTILE_SENSATIONS": [r"\bwarmth\b", r"\bcold\b", r"\bheat\b", r"\bfrost\b", r"\bsweat\b", r"\bbreeze\b", r"\bvibration\b", r"\btingle\b"]
}

def analyze_soundscape(prose_text):
    """Analyzes prose for sensory soundscapes and generates production audio/visual cues."""
    found_audio = []
    found_visual = []
    found_tactile = []
    
    words = prose_text.lower()
    for pat in SENSORY_PATTERNS["AUDIO_ONOMATOPOEIA"]:
        matches = re.findall(pat, words)
        if matches:
            found_audio.extend(matches)
            
    for pat in SENSORY_PATTERNS["VISUAL_PALETTE"]:
        matches = re.findall(pat, words)
        if matches:
            found_visual.extend(matches)
            
    for pat in SENSORY_PATTERNS["TACTILE_SENSATIONS"]:
        matches = re.findall(pat, words)
        if matches:
            found_tactile.extend(matches)

    unique_audio = list(set(found_audio))
    unique_visual = list(set(found_visual))
    unique_tactile = list(set(found_tactile))

    # Determine dominant lighting vibe
    if "golden" in unique_visual or "bronze" in unique_visual or "dazzling" in unique_visual:
        color_vibe = "SOLAR_GOLDEN_HOUR"
    elif "shadowy" in unique_visual or "violet" in unique_visual:
        color_vibe = "ECLIPSE_PURPLE_SHADOW"
    else:
        color_vibe = "HARMONIC_AMORTIZED_LIGHT"

    soundscape_cues = []
    if unique_audio:
        soundscape_cues.append(f"FX: Layer background ambient loop with {', '.join(unique_audio[:3])} effects.")
    else:
        soundscape_cues.append("FX: Low cosmic solar hum baseline.")

    return {
        "status": "ANALYZED",
        "audio_cues_detected": unique_audio,
        "visual_palette_detected": unique_visual,
        "tactile_sensation_count": len(unique_tactile),
        "recommended_color_vibe": color_vibe,
        "soundscape_cues": soundscape_cues,
        "sensory_richness_score": round(min(10.0, (len(unique_audio)*2.5 + len(unique_visual)*1.5 + len(unique_tactile)*1.0)), 1)
    }

if __name__ == "__main__":
    sample = sys.argv[1] if len(sys.argv) > 1 else "The golden solar lens hummed with a dazzling beam while a low clack echoed."
    print(json.dumps(analyze_soundscape(sample), indent=2))
