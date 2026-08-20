#!/usr/bin/env python3
"""
Narrative Beat Architect & 3-Act Scene Pacing Engine for The Stellar Confluence Universe
Generates structured, child-accessible, 3-act narrative blueprints grounded in active
physical limitations, celestial mechanics, alien creature encounters, and diverse plot styles.
"""

import sys
import json
import argparse
import random

PLOT_STYLES = {
    "EXPLORATION_DISCOVERY": {
        "theme": "Wonder, astronomical cartography, and unmapping uncharted sectors",
        "dilemma": "An unexpected celestial phenomenon or hidden ancient ruin presents an astronomical puzzle.",
        "resolution": "Using keen observation, scientific curiosity, and sensory clues to map a safe path forward."
    },
    "HIGH_STAKES_RESCUE": {
        "theme": "Bravery, loyalty, and aiding travelers in physical distress",
        "dilemma": "A teammate, cargo probe, or traveler is stranded by environmental turbulence or mechanical failure.",
        "resolution": "Coordinated teamwork, physical courage, and improvised tether lines to bring everyone to safety."
    },
    "RELIC_DECIPHERING": {
        "theme": "Ancient cosmic wisdom, tactile puzzle-solving, and relic alignment",
        "dilemma": "An ancient master relic requires precise acoustic or optical resonance tuning before wave shift.",
        "resolution": "Patience, gentle calibration, and following harmonic cues to unlock the relic's dormant knowledge."
    },
    "CREATURE_ALLIANCE": {
        "theme": "Symbiosis, kindness to alien fauna, and mutual understanding",
        "dilemma": "A magnificent indigenous creature is agitated by wavefront static or separated from its habitat.",
        "resolution": "Approaching with gentle, non-threatening gestures and offering comfort to form an unbreakable bond."
    },
    "ENGINEERING_EMERGENCY": {
        "theme": "Ingenuity, hands-on mechanical repair, and physical physics mastery",
        "dilemma": "A crucial gear train, thermal heat-sink, or orbital gyro experiences sudden friction overload.",
        "resolution": "Rapid physical lever intervention, manual flywheel damping, and teamwork under pressure."
    },
    "DIPLOMATIC_FIRST_CONTACT": {
        "theme": "Empathy, cultural hospitality, and peaceful conflict resolution",
        "dilemma": "Two neighboring factions or enclaves misunderstand each other's signals during a tense transit pass.",
        "resolution": "Offering the traditional hospitality gift and finding common harmonic ground to establish friendship."
    }
}

def generate_scene_beats(hero, title, faction, world, loc_type, facing_angle, resonance_state, power_cap, power_limit, hazards=None, plot_style=None, creature_name=None):
    hazards = hazards or []
    style_key = plot_style.upper() if (plot_style and plot_style.upper() in PLOT_STYLES) else "ENGINEERING_EMERGENCY"
    style_info = PLOT_STYLES.get(style_key, PLOT_STYLES["ENGINEERING_EMERGENCY"])
    
    # Act 1: Sensory Opening & Physical Grounding
    if "PEAK" in resonance_state:
        opening_sensory = f"Open with dazzling brilliance and intense radiant warmth across {world}. {hero} feels the humming energy of the incoming Confluence Wavefront vibrating through their equipment, but notes the heat-sink vents glowing dangerously red."
    elif "SHADOW" in resonance_state:
        opening_sensory = f"Open in the cool, silent depths or eclipse shadow of {world}. {hero} steps through dim twilight where light-beams cannot reach. Emphasize the quiet stillness, the chill in the air, and the absolute shutdown of solar lenses."
    elif "TRANSIT" in resonance_state:
        opening_sensory = f"Open along the balanced twilight horizon of {world}. {hero} works with steady hands under a gentle amber sky, where energy flows predictably and safely."
    else: # GATEWAY_SUBSPACE
        opening_sensory = f"Open in the surreal, weightless silence of the ancient subspace gateway conduit. The Confluence Wavefront is disconnected, leaving only kinetic momentum and quiet teamwork."

    if creature_name:
        opening_sensory += f" In the distance, a gentle {creature_name} moves peacefully across its native habitat."

    # Act 2: Escalating Dilemma & Physical Problem-Solving
    dilemma_elements = []
    if hazards:
        dilemma_elements.append(f"A sudden cosmic ripple wave ({hazards[0].get('event_type', 'TURBULENCE')}) rattles the area, shaking instruments.")
    
    dilemma_elements.append(f"Plot Tension ({style_key}): {style_info['dilemma']}")

    if "PEAK" in resonance_state:
        dilemma_elements.append(f"The active constraint triggers: {power_limit}. A critical piece of machinery or lens array begins to overheat.")
    elif "SHADOW" in resonance_state:
        dilemma_elements.append(f"The active constraint triggers: {power_limit}. Direct radiant energy is completely locked, requiring physical grit and tactile guidance.")
    elif "DEEP_SPACE" in loc_type:
        dilemma_elements.append(f"Deep-space volatility doubles kinetic energy surges; a minor misstep risks fracturing a hull viewport.")
    else:
        dilemma_elements.append(f"Active constraint ({power_limit}) demands precise physical teamwork and calibrated gear operation.")

    act2_text = " ".join(dilemma_elements)

    # Act 3: Climax, Discovery & Rotation Hand-off
    act3_text = f"{hero} executes a clever, non-violent physical maneuver ({style_info['resolution']}). In the moment of triumph, they secure the objective, uncover a crucial celestial reading or dispatch a beacon pulse that echoes outward across Sector transit routes, seamlessly setting the stage for the next book in the grand galactic rotation."

    return {
        "perspective_character": hero,
        "book_title": title,
        "faction": faction,
        "resonance_state": resonance_state,
        "plot_style": style_key,
        "narrative_blueprint": {
            "act_1_opening_grounding": opening_sensory,
            "act_2_escalating_dilemma": act2_text,
            "act_3_climax_discovery": act3_text
        },
        "key_themes": ["Childhood Bravery", "Physical Problem-Solving", "Wonder & Astronomy", "Teamwork & Loyalty", style_info["theme"]],
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
    parser.add_argument("--style", default="EXPLORATION_DISCOVERY")
    parser.add_argument("--creature", help="Optional creature name")
    
    args = parser.parse_args()
    beats = generate_scene_beats(args.hero, args.title, args.faction, args.world, args.loc, args.facing, args.res_state, args.cap, args.limit, plot_style=args.style, creature_name=args.creature)
    print(json.dumps(beats, indent=2))
