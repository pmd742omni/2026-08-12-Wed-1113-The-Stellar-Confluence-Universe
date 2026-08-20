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

# 20-Chapter Progressive Story Arc Blueprint
CHAPTER_ARC_BLUEPRINTS = {
    1: {
        "phase": "Phase 1: Apprenticeship & Discovery",
        "chapter_type": "APPRENTICE_FIRST_FLIGHT",
        "title_prefix": "The Rookie Flight & The Strange Signal",
        "theme": "Wonder, astronomical curiosity, and first flight trial",
        "dilemma": "A mysterious harmonic pulse ripples through the primary sensors during a routine trial flight.",
        "resolution": "Coordinating with mentor guidance and gentle rudder feathering to trace the signal to its source."
    },
    2: {
        "phase": "Phase 1: Apprenticeship & Discovery",
        "chapter_type": "CREATURE_BOND_AND_WORKSHOP",
        "title_prefix": "Creature Bonds & The Workshop Mishap",
        "theme": "Symbiosis, patience, and non-threatening kindness",
        "dilemma": "A curious indigenous creature wanders into the workshop, attracted to vibrating energy coils.",
        "resolution": "Sharing a soothing hospitality snack, calming the creature, and learning a clever trick from its movement."
    },
    3: {
        "phase": "Phase 1: Apprenticeship & Discovery",
        "chapter_type": "ECLIPSE_STORM_COURAGE",
        "title_prefix": "The Sudden Eclipse & The Shadow Gale",
        "theme": "Childhood courage, sensory navigation, and trusting physical tools",
        "dilemma": "A localized celestial shadow-shift disables radiant sensors during an environmental gale.",
        "resolution": "Switching to tactile acoustic pins and steady manual levers to shelter the observation post."
    },
    4: {
        "phase": "Phase 1: Apprenticeship & Discovery",
        "chapter_type": "MERIDIAN_RANK_TRIAL",
        "title_prefix": "The Meridian Trial & The Wayfarer Wings",
        "theme": "Earning rank, responsibility, and community honor",
        "dilemma": "The elder council sets an intricate calibration challenge across the sector boundary.",
        "resolution": "Combining everything learned to earn promotion from Apprentice Scout to Wayfarer Guide."
    },
    5: {
        "phase": "Phase 2: Planetary Frontier & System Transit",
        "chapter_type": "ORBITAL_SKYHOOK_ASCENT",
        "title_prefix": "Ascending the Skyhook & The Blue Horizon",
        "theme": "Awe of spaceflight, zero-gravity wonder, and expanding horizons",
        "dilemma": "Riding the orbital skyhook elevator when high-altitude wind shear threatens carriage stability.",
        "resolution": "Adjusting magnetic counterweights to smoothly glide above the atmosphere into orbital cycler docks."
    },
    6: {
        "phase": "Phase 2: Planetary Frontier & System Transit",
        "chapter_type": "ASTEROID_BELT_RESCUE",
        "title_prefix": "The Asteroid Slingshot & The Distress Ping",
        "theme": "Bravery, quick thinking, and assisting travelers",
        "dilemma": "An unpiloted automated supply skiff loses its stabilizer in a tumbling asteroid belt.",
        "resolution": "Piloting an ingenious gravitational slingshot maneuver to snag the skiff and tow it to safety."
    },
    7: {
        "phase": "Phase 2: Planetary Frontier & System Transit",
        "chapter_type": "CROSS_FACTION_BAZAAR",
        "title_prefix": "The Neutral Haven & The Lantern Greeting",
        "theme": "Cultural empathy, hospitality tea, and peaceful fellowship",
        "dilemma": "A misunderstanding between visiting merchants threatens to close the shared water docks.",
        "resolution": "Offering the traditional warm hospitality tea and wishing stone, building an unexpected friendship."
    },
    8: {
        "phase": "Phase 2: Planetary Frontier & System Transit",
        "chapter_type": "CORONAL_REEF_PASSAGE",
        "title_prefix": "Riding the Coronal Reef",
        "theme": "Precision transport piloting and thermodynamic balance",
        "dilemma": "Intense plasma turbulence in the magnetic reef forces engine heat exchangers toward critical limits.",
        "resolution": "Feathering solar sails along cooler magnetic field lines with smooth kinetic finesse."
    },
    9: {
        "phase": "Phase 3: Ancient Keystone & Relic Awakening",
        "chapter_type": "ANCIENT_STAR_ORRERY_RUIN",
        "title_prefix": "The Sunken Star-Orrery of the Ancients",
        "theme": "Archeo-astronomy, forgotten history, and tactile puzzle-solving",
        "dilemma": "Exploring long-dormant subterranean ruins where an ancient celestial clockwork is locked in stone.",
        "resolution": "Matching acoustic tones to unlock the bronze tumblers, revealing a dormant starmap."
    },
    10: {
        "phase": "Phase 3: Ancient Keystone & Relic Awakening",
        "chapter_type": "WAVEFRONT_SURGE_CRISIS",
        "title_prefix": "The Wavefront Surge & The Stalled Core",
        "theme": "High-stakes resilience and physical grit under pressure",
        "dilemma": "A massive wave shift triggers extreme power constraints, threatening to disconnect the planetary grid.",
        "resolution": "Manually anchoring the flywheel governor with a heavy wrench, preventing an emergency blackout."
    },
    11: {
        "phase": "Phase 3: Ancient Keystone & Relic Awakening",
        "chapter_type": "WHISPERING_KEYSTONE_UNLOCKED",
        "title_prefix": "The Whispering Keystone Deciphered",
        "theme": "Ancient wisdom, creature intuition, and harmonious insight",
        "dilemma": "An ancient resonance keystone will not activate without the precise vibrational frequency.",
        "resolution": "Listening to the gentle song of a loyal creature companion, matching its pitch to awaken the keystone."
    },
    12: {
        "phase": "Phase 3: Ancient Keystone & Relic Awakening",
        "chapter_type": "GUILD_MASTER_BLESSING",
        "title_prefix": "The Master's Blessing & The Unbroken Chain",
        "theme": "Promotion to Master Artisan, leadership, and inspiring younger apprentices",
        "dilemma": "A critical repair demands teaching and trusting newer apprentices while coordinating the sector network.",
        "resolution": "Guiding the team with calm encouragement, receiving promotion to Master Artisan."
    },
    13: {
        "phase": "Phase 4: Interstellar Gateway & Deep Cosmos",
        "chapter_type": "SUBSPACE_KEYSTONE_GATEWAY",
        "title_prefix": "Passing Through the Keystone Gateway",
        "theme": "Interstellar journey, subspace wonder, and boundless courage",
        "dilemma": "Entering an ancient subspace stargate into uncharted sectors where standard radio cannot reach.",
        "resolution": "Navigating the serene, weightless conduit using inertial compasses and unwavering trust."
    },
    14: {
        "phase": "Phase 4: Interstellar Gateway & Deep Cosmos",
        "chapter_type": "GRAV_WHALE_MIGRATION_ESCORT",
        "title_prefix": "The Leviathan's Song in the Dark Drift",
        "theme": "Cosmic majesty, environmental stewardship, and deep-space companionship",
        "dilemma": "A young Grav-Whale calf is disoriented by cosmic static from an approaching comet wake.",
        "resolution": "Broadcasting gentle harmonic sub-chimes, swimming alongside the leviathan to guide it back to the pod."
    },
    15: {
        "phase": "Phase 4: Interstellar Gateway & Deep Cosmos",
        "chapter_type": "CROSS_SECTOR_FELLOWSHIP",
        "title_prefix": "The Hand Across the Stars",
        "theme": "Inter-faction alliance, collaborative ingenuity, and mutual respect",
        "dilemma": "A neighboring sector's flagship experiences a catastrophic bearing freeze during transit.",
        "resolution": "Combining different faction technologies in brilliant synergy to restore full mobility."
    },
    16: {
        "phase": "Phase 4: Interstellar Gateway & Deep Cosmos",
        "chapter_type": "PULSAR_RELAY_STATIC_SHIELD",
        "title_prefix": "Shielding the Pulsar Beacon",
        "theme": "Defending communication, fortitude, and astronomical precision",
        "dilemma": "A relativistic magnetar flare threatens to overwhelm the interstellar navigational beacon.",
        "resolution": "Erecting an angled photonic deflection grid to preserve the vital stellar lighthouse."
    },
    17: {
        "phase": "Phase 5: Grand Climax & Cosmic Harmony",
        "chapter_type": "RACE_TO_THE_MERIDIAN_HUB",
        "title_prefix": "The Grand S-Curve Sprint",
        "theme": "Peak piloting skill, teamwork, and high-velocity excitement",
        "dilemma": "A tight countdown to reach the central sector hub before ephemeris alignment shifts.",
        "resolution": "Executing a flawless multi-body slingshot maneuver, arriving at the hub with seconds to spare."
    },
    18: {
        "phase": "Phase 5: Grand Climax & Cosmic Harmony",
        "chapter_type": "SONG_OF_THE_CONFLUENCE",
        "title_prefix": "The Harmonizing of the Spheres",
        "theme": "Uniting all elements, deep scientific wonder, and cosmic beauty",
        "dilemma": "All 74 sector relays must be tuned into exact resonance simultaneously.",
        "resolution": "Striking the primary keystone with absolute calm, sending a ripple of pure harmony across the stars."
    },
    19: {
        "phase": "Phase 5: Grand Climax & Cosmic Harmony",
        "chapter_type": "THE_ZENITH_WAVE_CREST",
        "title_prefix": "The Golden Crest of the Confluence",
        "theme": "The supreme climax, non-violent victory, and celestial triumph",
        "dilemma": "The greatest wavefront surge in a century reaches its zenith peak facing.",
        "resolution": "Channeling the energy harmlessly through ancient orbital rings, lighting up the sky in iridescent auroras."
    },
    20: {
        "phase": "Phase 5: Grand Climax & Cosmic Harmony",
        "chapter_type": "FESTIVAL_OF_BOUNDLESS_HORIZONS",
        "title_prefix": "The Feast of Lanterns & The Boundless Horizon",
        "theme": "High Artificer celebration, enduring legacy, and looking to the future",
        "dilemma": "Preparing to pass wisdom to the next generation of apprentices while charting new voyages.",
        "resolution": "Sharing warm tea and stardust bread at the grand feast, promoted to High Artificer, ready for the next galaxy."
    }
}

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

def get_chapter_arc_info(chapter_num: int):
    chap = max(1, min(20, int(chapter_num)))
    return CHAPTER_ARC_BLUEPRINTS.get(chap, CHAPTER_ARC_BLUEPRINTS[1])

def generate_scene_beats(hero, title, faction, world, loc_type, facing_angle, resonance_state, power_cap, power_limit, hazards=None, plot_style=None, creature_name=None, chapter_num=1):
    hazards = hazards or []
    arc_info = get_chapter_arc_info(chapter_num)
    
    style_key = plot_style.upper() if (plot_style and plot_style.upper() in PLOT_STYLES) else arc_info["chapter_type"]
    style_info = PLOT_STYLES.get(style_key, {
        "theme": arc_info["theme"],
        "dilemma": arc_info["dilemma"],
        "resolution": arc_info["resolution"]
    })
    
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
        opening_sensory += f" Nearby, an affectionate and gentle {creature_name} chirps and stays close by {hero}'s side."

    # Act 2: Escalating Dilemma & Physical Problem-Solving
    dilemma_elements = []
    if hazards:
        dilemma_elements.append(f"A sudden cosmic ripple wave ({hazards[0].get('event_type', 'TURBULENCE')}) rattles the area, shaking instruments.")
    
    dilemma_elements.append(f"Story Arc Focus (Chapter {chapter_num:02d} - {arc_info['phase']}): {style_info['dilemma']}")

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
    act3_text = f"{hero} executes a clever, non-violent physical maneuver ({style_info['resolution']}). In the moment of triumph, they secure the objective, uncover a crucial celestial reading or dispatch a beacon pulse that echoes outward across Sector transit routes, advancing their legacy and setting the stage for the next book in the grand galactic rotation."

    return {
        "perspective_character": hero,
        "book_title": title,
        "faction": faction,
        "chapter_number": chapter_num,
        "chapter_title_prefix": arc_info["title_prefix"],
        "phase": arc_info["phase"],
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
    parser.add_argument("--style", default=None)
    parser.add_argument("--chapter", type=int, default=1)
    parser.add_argument("--creature", help="Optional creature name")
    
    args = parser.parse_args()
    beats = generate_scene_beats(args.hero, args.title, args.faction, args.world, args.loc, args.facing, args.res_state, args.cap, args.limit, plot_style=args.style, creature_name=args.creature, chapter_num=args.chapter)
    print(json.dumps(beats, indent=2))

