#!/usr/bin/env python3
"""
Dual-Hero Cross-Book Encounter & Multi-Character Dialogue Simulator
Simulates shared scenes and authentic dialogue exchanges between interacting protagonists
from different storylines, contrasting their faction philosophies and solving joint physical dilemmas.
"""

import os
import sys
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

import chapter_engine
import character_mesh_graph
import faction_diplomacy_engine

def simulate_cross_encounter(book_a, book_b, encounter_type="SUBSPACE_COMMS"):
    char_a = chapter_engine.get_character_info(book_a)
    char_b = chapter_engine.get_character_info(book_b)

    if not char_a or not char_b:
        return {"error": f"Invalid book IDs ({book_a}, {book_b})"}

    hero_a, fac_a, world_a = char_a["hero"], char_a["faction"], char_a["world"]
    hero_b, fac_b, world_b = char_b["hero"], char_b["faction"], char_b["world"]

    dip = faction_diplomacy_engine.get_diplomatic_relation(fac_a, fac_b)
    stance = dip["stance"]
    tension = dip["tension_index"]

    # Dialogue Scripting based on Faction Chemistry
    if "Sun" in fac_a and "Void" in fac_b:
        dialogue = [
            {"speaker": hero_a, "text": f"Helios Relay station online! Vespera, are you receiving my light-pulse across the twilight gap?"},
            {"speaker": hero_b, "text": f"Loud and clear, Caelum. But dim that beam down half a notch. You are dazzling every sensor in my shadow canopy."},
            {"speaker": hero_a, "text": f"Sorry! The Confluence Wavefront is peaking at high zenith today. Everything in the solar array wants to run at full blast."},
            {"speaker": hero_b, "text": f"And over here in the eclipse shadow, my basalt phase-rings are dead quiet. If we link our frequencies, your heat can warm my power cells while my cold buffers your thermal vents."},
            {"speaker": hero_a, "text": f"A balanced bridge. Brilliant! Locking in frequency 144.2 MHz right now."}
        ]
        narrative_summary = f"Caelum ({hero_a}) and Vespera ({hero_b}) balance their opposing radiant and shadow extremes through a shared subspace relay link, achieving stable harmonic equilibrium."
    else:
        dialogue = [
            {"speaker": hero_a, "text": f"Relay channel established. Greetings from {world_a}."},
            {"speaker": hero_b, "text": f"Receiving your carrier wave on {world_b}. All telemetry coordinates align with the Confluence Wavefront."},
            {"speaker": hero_a, "text": f"Let's synchronize our sector clocks before the next orbital transit window closes."},
            {"speaker": hero_b, "text": f"Agreed. Transmitting telemetry burst now."}
        ]
        narrative_summary = f"{hero_a} and {hero_b} coordinate cross-sector telemetry, bridging faction boundaries through practical cooperation."

    return {
        "encounter_type": encounter_type,
        "protagonists": [
            {"book_id": book_a, "hero": hero_a, "faction": fac_a, "world": world_a},
            {"book_id": book_b, "hero": hero_b, "faction": fac_b, "world": world_b}
        ],
        "diplomatic_context": {
            "stance": stance,
            "tension_index": tension,
            "treaty": dip.get("historic_treaty", "None")
        },
        "dialogue_script": dialogue,
        "narrative_scene_summary": narrative_summary
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cross-Book Encounter Simulator")
    parser.add_argument("--book-a", type=int, default=1, help="First book protagonist ID")
    parser.add_argument("--book-b", type=int, default=11, help="Second book protagonist ID")
    parser.add_argument("--type", default="SUBSPACE_COMMS", help="Encounter type (SUBSPACE_COMMS, PHYSICAL_PROXIMITY)")

    args = parser.parse_args()
    res = simulate_cross_encounter(args.book_a, args.book_b, args.type)
    print(json.dumps(res, indent=2))
