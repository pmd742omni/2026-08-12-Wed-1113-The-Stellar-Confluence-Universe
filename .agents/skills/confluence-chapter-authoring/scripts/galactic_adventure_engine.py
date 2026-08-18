#!/usr/bin/env python3
"""
Galactic Adventure & Tactical Quest Engine for The Stellar Confluence Universe
Generates child-accessible, non-violent, high-stakes exploration quests, celestial anomalies,
and cooperative sector challenges tailored to character rank, faction technology, and location.
"""

import os
import sys
import json
import argparse
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_DIR), "..", "universe-state-manager", "scripts"))

import chapter_engine
import calculate_resonance
import faction_matrix
import planetary_ecology_matrix

ADVENTURE_ARCHETYPES = [
    {
        "type": "ANCIENT_GATEWAY_CALIBRATION",
        "title": "Unsealing the Keystone Gateway",
        "objective": "Calibrate the harmonic tuning fork on the ancient subspace gateway before the celestial alignment shifts.",
        "complication": "A sudden wavefront surge causes magnetic drag, jamming the lower bronze alignment gear.",
        "resolution_method": "Use physical leverage and synchronized timing with an allied relay beacon to free the gear.",
        "reward": "Unlocks a direct sub-light transit shortcut to neighboring star sector."
    },
    {
        "type": "COMET_TAIL_RESCUE",
        "title": "Sublimation Regatta Distress Signal",
        "objective": "Track and stabilize an unpiloted automated cargo probe caught in a high-speed cometary vapor wake.",
        "complication": "Sub-zero flash-freeze vapor threatens to ice over the primary steering thrusters.",
        "resolution_method": "Fire a heated tether line and ride the gravitational curve to guide the probe into safe orbit.",
        "reward": "Recovers vital cryo-coolant canisters for the solar observatory foundries."
    },
    {
        "type": "SOLAR_FLARE_CONTAINMENT",
        "title": "Coronal Prominence Shielding",
        "objective": "Erect a focused photonic barrier to shield a vulnerable planetary research station from an incoming solar flare.",
        "complication": "Thermal exchangers approach 95% heat capacity under extreme peak facing.",
        "resolution_method": "Divert excess heat into auxiliary ground heat-sinks while maintaining steady focus on the primary lens.",
        "reward": "Protects delicate scientific archives and earns High Artificer commendation."
    },
    {
        "type": "ECLIPSE_CHASM_EXPEDITION",
        "title": "Descent into the Umbral Rift",
        "objective": "Navigate deep into the unmapped basalt chasms of Nadir Prime to harvest rare glowing lichen.",
        "complication": "Complete eclipse lock disables all radiant lighting; navigation relies purely on tactile echoes.",
        "resolution_method": "Follow the rhythmic acoustic tapping of cold-iron guide pins along the canyon walls.",
        "reward": "Acquires curative bioluminescent lichen and maps a new subterranean transit corridor."
    },
    {
        "type": "CLOCKWORK_ORRERY_SYNCHRONIZATION",
        "title": "The Great Meridian Flywheel Test",
        "objective": "Synchronize three massive orbital ring flywheels to maintain equalized day-night cycles.",
        "complication": "Centrifugal stress causes high-speed bearing vibrations that threaten gear tooth shearing.",
        "resolution_method": "Apply precision acoustic tuning to match the rotation frequencies and dampen the harmonic tremor.",
        "reward": "Restores smooth power distribution across the entire equatorial habitations."
    }
]

def generate_adventure_quest(book_id=1, current_gut=100):
    book_id = int(book_id)
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        return {"error": f"Book {book_id} not found."}

    hero = char_info["hero"]
    faction = char_info["faction"]
    world = char_info["world"]
    loc_type = char_info["loc_type"]
    sector = char_info["sector"]

    clock = chapter_engine.get_clockwork_state(book_id)
    facing = clock.get("facing_angle", 15.0) if clock else 15.0
    res = calculate_resonance.calculate_resonance(facing, faction, loc_type)
    planet = planetary_ecology_matrix.get_planetary_profile(world)
    fac_prof = faction_matrix.get_faction_profile(faction)["profile"]

    # Select thematic quest
    quest_idx = (book_id + int(current_gut)) % len(ADVENTURE_ARCHETYPES)
    quest_base = ADVENTURE_ARCHETYPES[quest_idx]

    return {
        "status": "QUEST_GENERATED",
        "book_id": book_id,
        "hero": hero,
        "faction": faction,
        "location": f"{world} ({loc_type} | Sector {sector})",
        "facing_angle_deg": facing,
        "resonance_state": res["resonance_state"],
        "active_limitation": res["active_limitation"],
        "quest_details": {
            "title": f"Book {book_id:02d} Quest: {quest_base['title']}",
            "type": quest_base["type"],
            "objective": f"{hero} must {quest_base['objective']} at {world}.",
            "environmental_hazard": f"Terrain: {planet['biome']}. Astrophysics: {planet['astrophysics']['stellar_type']} (g={planet['astrophysics']['surface_gravity_g']}).",
            "tactical_complication": f"{quest_base['complication']} (Active constraint: {res['active_limitation']}).",
            "resolution_strategy": f"Deploy {fac_prof.get('signature_gear', 'signature equipment').split(',')[0]} and {quest_base['resolution_method']}",
            "mission_reward": quest_base["reward"]
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Adventure & Tactical Quest Engine")
    parser.add_argument("--book", type=int, default=1, help="Book ID (1-74)")
    parser.add_argument("--gut", type=int, default=100, help="Galactic Universal Time (GUT)")

    args = parser.parse_args()
    res = generate_adventure_quest(args.book, args.gut)
    print(json.dumps(res, indent=2))
