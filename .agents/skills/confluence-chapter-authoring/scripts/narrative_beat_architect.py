#!/usr/bin/env python3
"""
Narrative Beat Architect & 3-Act Scene Pacing Engine for The Stellar Confluence Universe
Generates structured, child-accessible, 3-act narrative blueprints grounded in active
physical limitations and celestial mechanics.
"""

import sys
import json
import argparse

def generate_scene_beats(hero, title, faction, world, loc_type, facing_angle, resonance_state, power_cap, power_limit, hazards=None):
    hazards = hazards or []
    
    # Act 1: Sensory Opening & Physical Grounding
    if "PEAK" in resonance_state:
        opening_sensory = f"Open with dazzling brilliance and intense radiant warmth across {world}. {hero} feels the humming energy of the incoming Confluence Wavefront vibrating through their equipment, but notes the heat-sink vents glowing dangerously red."
    elif "SHADOW" in resonance_state:
        opening_sensory = f"Open in the cool, silent depths or eclipse shadow of {world}. {hero} steps through dim twilight where light-beams cannot reach. Emphasize the quiet stillness, the chill in the air, and the absolute shutdown of solar lenses."
    elif "TRANSIT" in resonance_state:
        opening_sensory = f"Open along the balanced twilight horizon of {world}. {hero} works with steady hands under a gentle amber sky, where energy flows predictably and safely."
    else: # GATEWAY_SUBSPACE
        opening_sensory = f"Open in the surreal, weightless silence of the ancient subspace gateway conduit. The Confluence Wavefront is disconnected, leaving only kinetic momentum and quiet teamwork."

    # Act 2: Escalating Dilemma & Physical Problem-Solving
    dilemma_elements = []
    if hazards:
        dilemma_elements.append(f"A sudden cosmic ripple wave ({hazards[0].get('event_type', 'TURBULENCE')}) rattles the area, shaking instruments.")
    
    if "PEAK" in resonance_state:
        dilemma_elements.append(f"A critical piece of machinery or lens array begins to overheat. {hero} must quickly improvise a cooling method or vent thermal pressure before a burnout occurs.")
    elif "SHADOW" in resonance_state:
        dilemma_elements.append(f"Powered energy is completely unavailable. {hero} must rely purely on physical strength, manual mechanical pulleys, or clever stealth to overcome an obstacle.")
    elif "DEEP_SPACE" in loc_type:
        dilemma_elements.append(f"Deep-space volatility makes energy twice as wild; a minor misstep risks fracturing a hull viewport. {hero} must maintain steady breathing and precise focus.")
    else:
        dilemma_elements.append(f"A physical puzzle or unexpected mechanical jam requires {hero} to collaborate with an ally to align gears or adjust focus rings.")

    act2_text = " ".join(dilemma_elements)

    # Act 3: Climax, Discovery & Rotation Hand-off
    act3_text = f"{hero} executes a clever, non-violent physical maneuver to secure the objective. In the moment of triumph, they uncover a crucial celestial reading or dispatch a beacon pulse that echoes outward into the surrounding sectors, seamlessly setting the stage for the next book in the galactic rotation."

    return {
        "perspective_character": hero,
        "book_title": title,
        "faction": faction,
        "resonance_state": resonance_state,
        "narrative_blueprint": {
            "act_1_opening_grounding": opening_sensory,
            "act_2_escalating_dilemma": act2_text,
            "act_3_climax_discovery": act3_text
        },
        "key_themes": ["Childhood Bravery", "Physical Problem-Solving", "Wonder & Astronomy", "Teamwork & Loyalty"],
        "target_readability": "Grade 4-6 (Ages 9-12), Sensory-Rich & Jargon-Free"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 3-Act Narrative Scene Beats")
    parser.add_argument("--hero", default="Caelum Dawnrunner")
    parser.add_argument("--title", default="The Solar Crucible")
    parser.add_argument("--faction", default="Sun-Forged Hegemony")
    parser.add_argument("--world", default="Helios Prime")
    parser.add_argument("--loc", default="SURFACE")
    parser.add_argument("--facing", type=float, default=15.0)
    parser.add_argument("--res-state", default="PEAK_FACING")
    parser.add_argument("--cap", default="High-intensity solar beam output")
    parser.add_argument("--limit", default="Heat sink overheating risk")
    
    args = parser.parse_args()
    beats = generate_scene_beats(args.hero, args.title, args.faction, args.world, args.loc, args.facing, args.res_state, args.cap, args.limit)
    print(json.dumps(beats, indent=2))
