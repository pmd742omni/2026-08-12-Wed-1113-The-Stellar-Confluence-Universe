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

    # Dynamic Dialogue Generation based on Faction Mechanics & Archetypes
    import faction_matrix
    import character_voice_profiler

    prof_a = faction_matrix.get_faction_profile(fac_a)["profile"]
    prof_b = faction_matrix.get_faction_profile(fac_b)["profile"]
    voice_a = character_voice_profiler.get_faction_voice_profile(fac_a)
    voice_b = character_voice_profiler.get_faction_voice_profile(fac_b)

    gear_a = prof_a.get("signature_gear", "Resonant Gear").split(",")[0]
    gear_b = prof_b.get("signature_gear", "Resonant Gear").split(",")[0]
    idiom_a = voice_a.get("typical_idioms", ["Hold the focus."])[0]
    idiom_b = voice_b.get("typical_idioms", ["Check the balance."])[0]

    if "Sun" in fac_a and "Void" in fac_b:
        dialogue = [
            {"speaker": hero_a, "text": f"{world_a} relay station online! {hero_b}, are you receiving my light-pulse across the twilight gap?"},
            {"speaker": hero_b, "text": f"Loud and clear, {hero_a}. But dim that beam down half a notch. You are dazzling every sensor in my shadow canopy."},
            {"speaker": hero_a, "text": f"Sorry! The Confluence Wavefront is peaking at high zenith today. Everything in the solar array wants to run at full blast."},
            {"speaker": hero_b, "text": f"And over here in the eclipse shadow, my basalt phase-rings are dead quiet. If we link our frequencies, your heat can warm my power cells while my cold buffers your thermal vents."},
            {"speaker": hero_a, "text": f"A balanced bridge. Brilliant! Locking in frequency 144.2 MHz right now."}
        ]
        narrative_summary = f"{hero_a} and {hero_b} balance their opposing radiant and shadow extremes through a shared subspace relay link, achieving stable harmonic equilibrium."
    elif "Astrolabe" in fac_a or "Astrolabe" in fac_b:
        eng_hero = hero_a if "Astrolabe" in fac_a else hero_b
        oth_hero = hero_b if "Astrolabe" in fac_a else hero_a
        eng_fac = fac_a if "Astrolabe" in fac_a else fac_b
        oth_fac = fac_b if "Astrolabe" in fac_a else fac_a
        dialogue = [
            {"speaker": eng_hero, "text": f"Telemetry incoming from {oth_hero}. Your sector signal has an uncalibrated harmonic wobble."},
            {"speaker": oth_hero, "text": f"That's our {gear_a if oth_hero == hero_a else gear_b} adjusting to the local wavefront turbulence."},
            {"speaker": eng_hero, "text": f"Hold torque! {idiom_a if eng_hero == hero_a else idiom_b} Let me tune our clockwork escapement to dampen your vibrational drag."},
            {"speaker": oth_hero, "text": f"Dampers locked. The wobble vanished instantly. Clean readings across the whole array!"},
            {"speaker": eng_hero, "text": f"Clockwork precision never fails. Relay channels synchronized."}
        ]
        narrative_summary = f"{eng_hero} ({eng_fac}) uses precision gear alignment to stabilize the fluctuating transmission from {oth_hero} ({oth_fac}), ensuring safe sector synchronization."
    else:
        dialogue = [
            {"speaker": hero_a, "text": f"Calling Sector station {world_b}, this is {hero_a} transmitting from {world_a}."},
            {"speaker": hero_b, "text": f"Carrier wave received, {hero_a}. Our {gear_b} picked up your beacon pulse over the ambient noise."},
            {"speaker": hero_a, "text": f"We are tracking incoming wavefront oscillations in this sector. As our elders say, '{idiom_a}'"},
            {"speaker": hero_b, "text": f"Acknowledged. We're matching your frequency. Together our arrays can maintain a stable navigational corridor."},
            {"speaker": hero_a, "text": f"All telemetry locked and verified. Safe travels across the star lanes, {hero_b}!"}
        ]
        narrative_summary = f"{hero_a} ({fac_a}) and {hero_b} ({fac_b}) coordinate cross-sector telemetry and align equipment, bridging faction boundaries through practical cooperation."

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
