#!/usr/bin/env python3
"""
Galactic Adventure & Tactical Quest Engine for The Stellar Confluence Universe
Generates child-accessible, non-violent, high-stakes exploration quests, celestial anomalies,
vehicle piloting challenges, trade convoy escorts, diplomatic mediation, and creature interactions
tailored to character rank, faction technology, active inventory, and location physics.
"""

import os
import sys
import json
import argparse
import random
from typing import Dict, Any, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_DIR), "..", "universe-state-manager", "scripts"))

import chapter_engine
import calculate_resonance
import faction_matrix
import planetary_ecology_matrix

try:
    import galactic_scale_generator
except ImportError:
    galactic_scale_generator = None

try:
    import galactic_transport_engine
except ImportError:
    galactic_transport_engine = None

try:
    import galactic_sociology_politics_engine
except ImportError:
    galactic_sociology_politics_engine = None

# 25+ Comprehensive Galactic Adventure Archetypes
EXPANDED_ADVENTURE_ARCHETYPES = [
    {
        "type": "ANCIENT_GATEWAY_CALIBRATION",
        "title": "Unsealing the Keystone Gateway",
        "objective": "Calibrate the harmonic tuning fork on the ancient subspace gateway before celestial alignment shifts.",
        "complication": "A sudden wavefront surge causes magnetic drag, jamming the lower bronze alignment gear.",
        "resolution_method": "Use physical leverage, precise timing, and acoustic dampening to ease the gear into its track.",
        "reward": "Unlocks a direct sub-light transit shortcut to neighboring star sector."
    },
    {
        "type": "COMET_TAIL_RESCUE",
        "title": "Sublimation Regatta Distress Signal",
        "objective": "Track and stabilize an unpiloted automated cargo probe caught in a high-speed cometary vapor wake.",
        "complication": "Sub-zero flash-freeze vapor threatens to ice over the primary steering thrusters.",
        "resolution_method": "Fire a heated thermal tether line and ride the gravitational curve to guide the probe into safe orbit.",
        "reward": "Recovers vital cryo-coolant canisters for the solar observatory foundries."
    },
    {
        "type": "SOLAR_FLARE_CONTAINMENT",
        "title": "Coronal Prominence Shielding",
        "objective": "Erect a focused photonic barrier to shield a vulnerable planetary research station from an incoming solar flare.",
        "complication": "Thermal exchangers approach 95% heat capacity under extreme peak facing.",
        "resolution_method": "Divert excess heat into auxiliary ground heat-sinks while maintaining steady focus on primary lens.",
        "reward": "Protects delicate scientific archives and earns High Artificer commendation."
    },
    {
        "type": "ECLIPSE_CHASM_EXPEDITION",
        "title": "Descent into the Umbral Rift",
        "objective": "Navigate deep into unmapped basalt chasms to harvest rare glowing lichen.",
        "complication": "Complete eclipse lock disables radiant lighting; navigation relies purely on tactile echoes.",
        "resolution_method": "Follow the rhythmic acoustic tapping of cold-iron guide pins along canyon walls.",
        "reward": "Acquires curative bioluminescent lichen and maps a new subterranean transit corridor."
    },
    {
        "type": "CLOCKWORK_ORRERY_SYNCHRONIZATION",
        "title": "The Great Meridian Flywheel Test",
        "objective": "Synchronize three massive orbital ring flywheels to maintain equalized day-night cycles.",
        "complication": "Centrifugal stress causes high-speed bearing vibrations that threaten gear tooth shearing.",
        "resolution_method": "Apply precision acoustic tuning to match rotation frequencies and dampen harmonic tremor.",
        "reward": "Restores smooth power distribution across equatorial habitations."
    },
    {
        "type": "GRAV_WHALE_MIGRATION_ESCORT",
        "title": "Leviathan of the Ion Drift",
        "objective": "Guide a pod of majestic deep-space Grav-Whales safely through an active asteroid mining corridor.",
        "complication": "A rogue iron meteor cluster drifts across their natural migration heading.",
        "resolution_method": "Broadcast soothing sub-acoustic chimes to nudge the pod onto a safe gravitational slingshot vector.",
        "reward": "Earns lifelong kinship of the Grav-Whales, who leave behind pure stardust crystal nodules."
    },
    {
        "type": "PHOTONIC_LIGHT_MOTH_SANCTUARY",
        "title": "The Prismatic Telescope Refraction",
        "objective": "Safely relocate a flock of curious Light-Moths nested inside the primary stellar observatory lens.",
        "complication": "Sudden bright light causes moths to flutter frantically, scattering kaleidoscopic beams across the deck.",
        "resolution_method": "Hold up a polished, warm amber prism and gently guide them toward the open desert succulent garden.",
        "reward": "Restores telescope focus, revealing an ancient star chart etched into the night sky."
    },
    {
        "type": "PHASE_STALKER_TUNNEL_GUIDE",
        "title": "The Collapsed Stratum Rescue",
        "objective": "Locate an apprentice miner trapped behind a fallen basalt rockfall in the deep core mines.",
        "complication": "Heavy seismic vibrations make standard drilling unsafe for support pillars.",
        "resolution_method": "Partner with a friendly Phase-Stalker to step through the stone wall and pass an emergency beacon.",
        "reward": "Safely retrieves the apprentice and uncovers a subterranean thermal spring."
    },
    {
        "type": "SILICON_WEAVER_PLASMA_BRIDGE",
        "title": "Weaving the Canyon Span",
        "objective": "Erect an emergency electromagnetic plasma-silk bridge across a 500-meter chasm before an ion storm arrives.",
        "complication": "High crosswinds whip through the canyon, threatening to snap unanchored silk strands.",
        "resolution_method": "Coordinate with indigenous Silicon-Weaver spiders using rhythmic pulse taps to secure anchor points.",
        "reward": "Completes the lifeline bridge and ensures safe transit for an approaching trade caravan."
    },
    {
        "type": "TACHYON_LAGOON_DIAL_RESTORATION",
        "title": "The Singing Chrono-Dials",
        "objective": "Realign submerged quartz chronometer dials in the iridescent shallows of the tide world.",
        "complication": "Wavefront shifts cause temporal water droplets to hover in place, distorting visual alignment angles.",
        "resolution_method": "Rely on the slow, rhythmic footsteps of an ancient Chrono-Tortoise to measure precise intervals.",
        "reward": "Synchronizes sector transit clocks, cutting sub-light flight drift to zero."
    },
    {
        "type": "BIOLUMINESCENT_CORAL_SANCTUARY",
        "title": "Shelter in the Abyssal Reef",
        "objective": "Establish an emergency medical outpost inside the hollow chambers of a Bioluminescent Coral Colossus.",
        "complication": "A sudden ocean swell closes outer siphon vents, trapping stale air in the upper vestibule.",
        "resolution_method": "Feed nutrient-rich sea algae to the coral core to stimulate natural photosynthetic oxygen release.",
        "reward": "Creates a permanent undersea haven for traveling ocean explorers."
    },
    {
        "type": "SINGULARITY_SLINGSHOT_CARTOGRAPHY",
        "title": "Riding the Event Horizon Curve",
        "objective": "Pilot a light scout glider around a micro-black hole accretion disk to map gravitational transit lanes.",
        "complication": "Extreme tidal shear threatens to buckle the glider's port graviton sail.",
        "resolution_method": "Feather the steering thrusters and lean cleanly into the gravitational slope with steady nerve.",
        "reward": "Maps a three-minute sub-light transit corridor that bypasses two days of deep-space cruising."
    },
    {
        "type": "SUBSPACE_BEACON_DECRYPTION",
        "title": "Echoes from the Far Outer Rim",
        "objective": "Intercept and decode a faint harmonic distress beacon emanating from a long-dormant stargate array.",
        "complication": "Cosmic background static from a nearby magnetar pulsar scrambles every fourth frequency packet.",
        "resolution_method": "Apply a triangular parity filter across three relay towers to reconstruct the audio transmission.",
        "reward": "Discovers coordinates of a hidden botanical biosphere pod floating in deep transit."
    },
    {
        "type": "SPORE_BLOOM_REMEDY_HARVEST",
        "title": "The Midnight Canopy Blossom",
        "objective": "Harvest the luminous blue pollen of the rare Star-Bloom orchid during its 15-minute annual flowering window.",
        "complication": "The orchid grows on the underside of a kilometer-high mega-canopy branch in high winds.",
        "resolution_method": "Deploy flexible chitin climbing hooks and move with quiet balance along the root walkway.",
        "reward": "Crafts a natural soothing salve that cures thermal heat fatigue across the solar observatories."
    },
    {
        "type": "CRYSTALLINE_RESONANCE_SYMPHONY",
        "title": "Tuning the Singing Spires",
        "objective": "Acoustically tune seven giant natural quartz spires before a supercharged wavefront crest shatters them.",
        "complication": "High-frequency feedback builds rapidly, ringing in the ears of the exploration team.",
        "resolution_method": "Dampen the feedback using calibrated acoustic felt pads and strike the central spire in pure harmonic pitch.",
        "reward": "Transforms the valley into a natural sub-space amplifier that boosts local communication clarity."
    },
    {
        "type": "ATMOSPHERIC_SKIMMER_THERMAL_SURF",
        "title": "The Grand Mesa Thermal Rally",
        "objective": "Pilot a Solar-Thermal Skimmer across a 300-kilometer copper canyon to deliver an emergency beacon crystal.",
        "complication": "A sudden dust squall blocks primary solar charging, requiring pure aerodynamic thermal gliding.",
        "resolution_method": "Angle the wing foils into rising basalt thermal columns and ride the cliff face updrafts.",
        "reward": "Delivers beacon in record time and earns Master Wayfarer flight wings."
    },
    {
        "type": "TRADE_CONVOY_ESCORT_MISSION",
        "title": "The Meridian Brass Convoy Defense",
        "objective": "Escort an unarmed commercial freight convoy carrying 500 tons of Precision Brass through an active debris belt.",
        "complication": "A micrometeor shower damages the lead freighter's steering thrusters, sending it drifting toward a magnetic reef.",
        "resolution_method": "Fire magnetic tow lines, sync propulsion bursts, and steer the entire convoy into the shadow of a hollow asteroid.",
        "reward": "Safely lands the cargo at Aethelgard port, earning 1000 Guild Scrip and open docking passes."
    },
    {
        "type": "DIPLOMATIC_HOSPITALITY_SUMMIT",
        "title": "The Twilight Sanctuary Accord",
        "objective": "Host a peaceful hospitality conference between Sun-Forged Artificers and Void-Bound Monks on a neutral moon.",
        "complication": "A solar flare induces static in the translation arrays, threatening diplomatic misunderstanding.",
        "resolution_method": "Present the traditional warm amber tea and polished wishing stone, demonstrating goodwill through shared custom.",
        "reward": "Signs the Bilateral Frontier Transit Treaty, de-escalating galactic tension by 15 points."
    },
    {
        "type": "BENTHIC_SEA_CRAWLER_SALVAGE",
        "title": "Abyssal Trench Archive Recovery",
        "objective": "Pilot a Bioluminescent Benthic Crawler down a 4,000-meter marine trench to recover a dropped star-chart capsule.",
        "complication": "Crushing ocean depth pressures test the sapphire dome seals while deep currents pull at the crawler's legs.",
        "resolution_method": "Equalize hydraulic ballast, activate bioluminescent floodlights, and gently scoop the capsule with the magnetic claw.",
        "reward": "Recovers ancient cartographic records showing lost interstellar transit routes."
    },
    {
        "type": "CORONAL_DRAKE_SOLAR_RESCUE",
        "title": "The Prominence Arch Navigation",
        "objective": "Follow a friendly Coronal Drake through a looping magnetic prominence to rescue a stranded research glider.",
        "complication": "Blinding solar radiance overwhelms visual sensors; pilot must fly purely on thermal acoustic cues.",
        "resolution_method": "Match the Drake's whistling thermal tone and follow its sparkling wake of ionized scales.",
        "reward": "Safely tows the research glider out of the solar corona, preserving irreplaceable stellar wind telemetry."
    },
    {
        "type": "MAGLEV_EXPRESS_SWITCHBACK_REPAIR",
        "title": "The Midnight Express Derailment Prevention",
        "objective": "Repair a damaged superconducting mag-lev track switch before the planetary express train arrives.",
        "complication": "Extreme cold has contracted the track clamp, jamming the manual alignment lever.",
        "resolution_method": "Apply a portable thermal torch with steady precision and lever the track into locking position as the train signals.",
        "reward": "Prevents derailment of 450 passengers and receives the Golden Meridian Medal of Honor."
    },
    {
        "type": "TACHYON_SAND_CHRONO_MAP",
        "title": "The Shifting Hourglass Dunes",
        "objective": "Collect undisturbed tachyon sand samples from three oscillating dunes during an exact 5-minute wavefront lull.",
        "complication": "Temporal echoes cause dune crests to shift unpredictably in forward and reverse cycles.",
        "resolution_method": "Observe the rhythmic movement of local Chrono-Tortoises and walk precisely in their calm footsteps.",
        "reward": "Gathers pristine tachyon cells for advanced slipstream navigation computers."
    },
    {
        "type": "DYSON_ACCELERATOR_CALIBRATION",
        "title": "Aligning the Relativistic Beam",
        "objective": "Calibrate the primary mirror array of a 100-gigawatt Dyson Swarm launch laser.",
        "complication": "Thermal expansion creates a 0.05-degree tilt error, which would miss the destination light-collector by a million kilometers.",
        "resolution_method": "Adjust the liquid-nitrogen cooling jacks and torque the micrometric adjustment bolts to zero tolerance.",
        "reward": "Launches the interstellar seed-convoy with absolute trajectory accuracy."
    },
    {
        "type": "LIVING_MANTA_SYMBIOSIS",
        "title": "Nurturing the Bio-Vessel Nursery",
        "objective": "Treat an ailing juvenile Bio-Chitin Manta-Craft suffering from mineral deficiency in a floating cloud archipelago.",
        "complication": "The frightened young creature hovers near high-altitude thunderstorm turbulence.",
        "resolution_method": "Approach with calm breathing, offer nutrient-rich golden succulent nectar, and gently dress its wing node.",
        "reward": "Bonds with the loyal Manta-Craft, gaining a trusted amphibious flight companion for future voyages."
    },
    {
        "type": "NEBULA_WEAVER_CHORD_EXCHANGE",
        "title": "The Cosmic Loom Symphony",
        "objective": "Weave a 10-kilometer plasma-silk communication filament across the gap between two orbital research spires.",
        "complication": "Ionized gas eddies threaten to tangle the glowing filament into a feedback knot.",
        "resolution_method": "Play an acoustic chord progression on the subspace pitch-pipe to organize the plasma charges into a stable braid.",
        "reward": "Restores inter-station data link and illuminates the night sky in brilliant multicolored auroras."
    }
]

def generate_adventure_quest(book_id: int = 1, current_gut: int = 100, quest_type: Optional[str] = None) -> Dict[str, Any]:
    """Generates an engaging, non-violent, rich adventure quest with 5-stage blueprint, transport, and sociological flavor."""
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

    # Select Archetype
    if quest_type:
        matches = [a for a in EXPANDED_ADVENTURE_ARCHETYPES if quest_type.upper() in a["type"].upper()]
        quest_base = matches[0] if matches else EXPANDED_ADVENTURE_ARCHETYPES[0]
    else:
        quest_idx = (book_id * 7 + int(current_gut) * 13) % len(EXPANDED_ADVENTURE_ARCHETYPES)
        quest_base = EXPANDED_ADVENTURE_ARCHETYPES[quest_idx]

    # Indigenous creature integration
    creature_info = None
    if galactic_scale_generator:
        creature_info = galactic_scale_generator.generate_creature_encounter(None, f"book_{book_id}_{current_gut}")

    # Transport integration
    vehicle_info = None
    if galactic_transport_engine:
        v_pref = galactic_transport_engine.get_faction_vehicle_preference(faction)
        if v_pref.get("vehicles"):
            vehicle_info = v_pref["vehicles"][0]

    # Sociological & Governance integration
    soc_profile = None
    if galactic_sociology_politics_engine:
        soc_profile = galactic_sociology_politics_engine.get_sociological_profile(faction)

    vehicle_name = vehicle_info["name"] if vehicle_info else "Standard Planetary Skimmer"
    hospitality_greeting = soc_profile["hospitality_ritual"]["dialogue_phrase"] if soc_profile else "Safe travels under the stars."

    # Generate 5-Stage Mission Blueprint
    stages = [
        {
            "stage_1_briefing": f"{hero} receives an urgent notification at {world}. Mission objective: {quest_base['objective']}",
            "stage_2_environmental_navigation": f"Boarding the {vehicle_name} to cross {planet.get('biome', 'alien terrain')} (g={planet.get('astrophysics', {}).get('surface_gravity_g', 1.0)}).",
            "stage_3_tactical_complication": f"{quest_base['complication']} (Active wavefront constraint: {res['active_limitation']}).",
            "stage_4_creature_and_cultural_interaction": f"Coordinating with {creature_info['creature_name'] if creature_info else 'local fauna'} ({creature_info['friendly_handling_protocol'] if creature_info else 'peaceful approach'}) while sharing the greeting: \"{hospitality_greeting}\".",
            "stage_5_skill_resolution": f"Deploy {fac_prof.get('signature_gear', 'signature equipment').split(',')[0]} and {quest_base['resolution_method']}"
        }
    ]

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
            "vehicle_deployed": vehicle_name,
            "environmental_hazard": f"Terrain: {planet['biome']}. (g={planet.get('astrophysics', {}).get('surface_gravity_g', 1.0)}).",
            "tactical_complication": f"{quest_base['complication']} (Active constraint: {res['active_limitation']}).",
            "creature_encounter": creature_info["creature_name"] if creature_info else "Indigenous Fauna",
            "creature_wonder": creature_info["sensory_specialty"] if creature_info else "Resonant wildlife harmony",
            "resolution_strategy": f"Deploy {fac_prof.get('signature_gear', 'signature equipment').split(',')[0]} and {quest_base['resolution_method']}",
            "mission_reward": quest_base["reward"],
            "xp_reward": 150,
            "five_stage_blueprint": stages[0]
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Adventure & Tactical Quest Engine")
    parser.add_argument("--book", type=int, default=1, help="Book ID (1-74)")
    parser.add_argument("--gut", type=int, default=100, help="Galactic Universal Time (GUT)")
    parser.add_argument("--type", help="Quest type filter")

    args = parser.parse_args()
    res = generate_adventure_quest(args.book, args.gut, args.type)
    print(json.dumps(res, indent=2))
