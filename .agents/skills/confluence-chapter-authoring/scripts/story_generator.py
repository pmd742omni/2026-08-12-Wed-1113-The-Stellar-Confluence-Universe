#!/usr/bin/env python3
"""
Autonomous Multi-Faction Chapter Story Generator for The Stellar Confluence Universe
Composes sensory-rich, dialogue-driven prose accessible to a 10-year-old child (Grade 4-6),
dynamically synthesizing character identity, mentors, planetary biomes, alien creature interactions,
interstellar cultures, vehicle transport physics, economic trade contexts, governance models,
active relics, and celestial wave physics across all 74 storylines.
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

from calculate_resonance import calculate_resonance
from narrative_beat_architect import generate_scene_beats, get_chapter_arc_info, PLOT_STYLES
from confluence_wave_physics import calculate_wavefront_state
import chapter_engine
import character_mesh_graph
import planetary_ecology_matrix
import faction_matrix
import character_voice_profiler
import artifact_ledger_engine
import character_mastery_engine

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

try:
    import galactic_trade_economy
except ImportError:
    galactic_trade_economy = None

# Culinary and Comfort Hospitality Treats by Faction
FACTION_HOSPITALITY_TREATS = {
    "Sun-Forged": ("warm amber tea with golden honey", "toasted cinnamon sun-cakes"),
    "Void-Bound": ("steaming midnight herb infusion", "crisp basalt wafer crisps"),
    "Astrolabe": ("hot spiced cider with nutmeg", "glazed sweet gear-biscuits"),
    "Comet-Riders": ("frosted mint berry brew", "crystallized sugar snow-flakes"),
    "Nebula-Weavers": ("lavender cloud-mist tea", "spun sugar plasma-threads"),
    "Deep-Core Miners": ("rich roasted barley broth", "warm iron-crust hazelnut bread"),
    "Gravity-Surfers": ("sparkling citrus tonic", "crunchy star-fruit bites"),
    "Plasma-Shepherds": ("golden chamomile tisane", "spiced solar-berry scones"),
    "Chrono-Navigators": ("slow-steeped vanilla rooibos", "hourglass almond shortbread"),
    "Bio-Alchemists": ("sweet nectar flower-dew", "dried golden succulent figs"),
    "Crystal-Singers": ("chilled quartz-filtered springwater", "singing candy prisms"),
    "Tide-Wardens": ("kelp-mint sea tea", "toasted ocean grain biscuits"),
    "Magnetar-Leapers": ("fizzy blackberry spark-juice", "popped star-corn with stardust salt")
}

# 20-Chapter Specific Title Generator Matrix
CHAPTER_TITLE_TEMPLATES = {
    1: ["The Rookie Flight & The Golden Horizon", "First Sparks Over {world}", "The Copper Dawn Launch"],
    2: ["The Creature in the Workshop", "Playful Whistles & Polished Lenses", "The Secret of the {creature}"],
    3: ["The Shadow Gale & The Basalt Path", "Storm of Glass & Amber", "The Cold-Iron Guide Pins"],
    4: ["The Meridian Trial", "Wings of the Wayfarer", "The Elder's Blessing"],
    5: ["Ascending the Great Skyhook", "Above the Cloud Sea", "The Blue Curve of Orbit"],
    6: ["Slingshot Through the Asteroids", "The Distant SOS", "The Magnetic Tow Line"],
    7: ["The Lanterns of the Neutral Port", "Tea with Strangers", "The Wishing Stone Exchange"],
    8: ["Riding the Coronal Prominence", "The Solar Wind Regatta", "Feathering the Photonic Sail"],
    9: ["The Sunken Clockwork Orrery", "Vaults of the First Artificers", "The Stone Starmap"],
    10: ["The Great Wavefront Surge", "When the Dynamos Stalled", "The Manual Flywheel Hold"],
    11: ["Song of the Keystone", "Awakening the Sleeping Prism", "The Whisper in the Quartz"],
    12: ["The Master's Anvil", "The Chain of Golden Rings", "Promotion to Master Artisan"],
    13: ["Beyond the Keystone Gate", "The Weightless Subspace Conduit", "Uncharted Starway"],
    14: ["Dance of the Grav-Whales", "The Dark Drift Leviathan", "Chimes for the Lost Calf"],
    15: ["The Hand Across the Stars", "Two Fleets, One Heart", "The Interstellar Fellowship"],
    16: ["Lighthouse of the Pulsar", "The Emerald Shieldwall", "Holding the Navigational Beam"],
    17: ["The Sprint to the Meridian Hub", "Race Against the Clockwork", "The Multi-Body Slingshot"],
    18: ["The Harmonizing of All Worlds", "The Choir of 74 Relays", "The Golden Chord"],
    19: ["The Zenith Wave Crest", "Light Across Trillions of Stars", "The Triumph of Harmony"],
    20: ["The Feast of Boundless Horizons", "Toasts by Lantern Light", "The Endless Voyage Ahead"]
}

def get_location_for_chapter(world: str, loc_type: str, sector: str, chapter_num: int) -> Dict[str, str]:
    """Dynamically moves characters across interplanetary and interstellar locations as chapters progress."""
    chap = max(1, min(20, int(chapter_num)))
    if chap <= 4:
        return {"world": world, "loc_type": loc_type, "sector": sector, "desc": f"the familiar terrain and workshops of {world}"}
    elif chap <= 8:
        return {"world": f"Orbital Skyhook of {world}", "loc_type": "ORBITAL", "sector": sector, "desc": f"the orbital cycler docks high above {world}"}
    elif chap <= 12:
        return {"world": f"Ancient Keystone Ruins ({world} Sector)", "loc_type": "SURFACE", "sector": sector, "desc": f"the ancient subterranean ruins in Sector {sector}"}
    elif chap <= 16:
        return {"world": f"Keystone Subspace Transit Gateway", "loc_type": "GATEWAY_SUBSPACE", "sector": sector, "desc": "the weightless, glowing subspace transit corridor"}
    else:
        return {"world": "The Grand Galactic Confluence Hub", "loc_type": "ORBITAL", "sector": "[0, 0, 0]", "desc": "the glittering Grand Confluence Hub connecting all 74 star sectors"}

def get_character_rank_for_chapter(chapter_num: int) -> str:
    chap = max(1, min(20, int(chapter_num)))
    if chap <= 4:
        return "Apprentice Scout"
    elif chap <= 11:
        return "Wayfarer Guide"
    elif chap <= 19:
        return "Master Artisan"
    else:
        return "High Artificer"

def generate_full_chapter_prose(book_id: int, chapter_num: int, save: bool = False, plot_style: Optional[str] = None) -> Dict[str, Any]:
    """
    Synthesizes an expansive, multi-scene, sensory-rich chapter adhering strictly to Grade 4-6 readability,
    scientific authenticity, lively character interactions, cute creature moments, and 20-chapter story arcs.
    """
    book_id = int(book_id)
    chapter_num = int(chapter_num)
    
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        return {"error": f"Book {book_id} not found in registry"}

    clock_info = chapter_engine.get_clockwork_state(book_id)
    facing_angle = clock_info["facing_angle"] if clock_info else 15.0
    sector = clock_info["sector"] if clock_info else char_info["sector"]
    gut = clock_info["gut"] if clock_info else 100

    hero = char_info["hero"]
    title = char_info["title"]
    homeworld = char_info["world"]
    faction = char_info["faction"]
    
    # Progressive location and rank
    loc_data = get_location_for_chapter(homeworld, char_info["loc_type"], sector, chapter_num)
    active_world = loc_data["world"]
    active_loc_type = loc_data["loc_type"]
    active_rank = get_character_rank_for_chapter(chapter_num)

    # 1. Physics & Resonance
    res = calculate_resonance(facing_angle, faction, active_loc_type)
    wave_state = calculate_wavefront_state(sector, gut)

    # 2. Character Mesh & Mentor
    mesh_info = character_mesh_graph.get_character_mesh(book_id)["mesh"]
    raw_mentor = mesh_info.get("mentor", f"Master Elder of {homeworld}")
    mentor_display = raw_mentor.split("(")[0].strip()
    mentor_title = mentor_display if mentor_display.startswith("Master") or mentor_display.startswith("Elder") or mentor_display.startswith("Brother") or mentor_display.startswith("Matron") or mentor_display.startswith("Captain") or mentor_display.startswith("Commander") or mentor_display.startswith("High") or mentor_display.startswith("Forge") else f"Elder {mentor_display}"
    
    hero_first_name = hero.split()[0]
    planet = planetary_ecology_matrix.get_planetary_profile(homeworld)
    fac_profile = faction_matrix.get_faction_profile(faction)["profile"]
    voice_profile = character_voice_profiler.get_faction_voice_profile(faction)

    signature_gear = fac_profile.get("signature_gear", "Resonant Gear").split(",")[0].strip()
    idiom = voice_profile.get("typical_idioms", ["Hold steady and trust the alignment."])[0]
    biome_desc = planet.get("biome", "Dramatic alien terrain")
    gravity_g = planet.get("astrophysics", {}).get("surface_gravity_g", 1.0)
    stellar_type = planet.get("astrophysics", {}).get("stellar_type", "Primary Star").split("(")[0].strip()

    # 3. Transport Vehicle Integration
    vehicle_name = "Solar-Thermal Atmospheric Skimmer"
    vehicle_vibe = "panoramic brass canopy, rhythmic hum of warm air intakes, and smooth magnetic rudder sticks"
    if galactic_transport_engine:
        v_pref = galactic_transport_engine.get_faction_vehicle_preference(faction)
        if v_pref.get("vehicles"):
            v_obj = v_pref["vehicles"][0]
            vehicle_name = v_obj.get("name", vehicle_name)
            vehicle_vibe = v_obj.get("cockpit_vibe", vehicle_vibe).rstrip(".")

    # 4. Sociological & Cultural Traditions & Hospitality
    cultural_ritual = "Offering a warm drink and a polished wishing stone"
    hospitality_greeting = "May your path be steady under the turning stars."
    governance_title = "The Regional Artificer Council"
    if galactic_sociology_politics_engine:
        soc_prof = galactic_sociology_politics_engine.get_sociological_profile(faction)
        if soc_prof:
            cultural_ritual = soc_prof.get("hospitality_ritual", {}).get("name", cultural_ritual)
            hospitality_greeting = soc_prof.get("hospitality_ritual", {}).get("dialogue_phrase", hospitality_greeting)
            governance_title = soc_prof.get("governance_model", governance_title)

    # Hospitality snack
    treat_key = "Sun-Forged"
    for k in FACTION_HOSPITALITY_TREATS.keys():
        if k.lower() in faction.lower():
            treat_key = k
            break
    drink_name, snack_name = FACTION_HOSPITALITY_TREATS[treat_key]

    # 5. Indigenous Creature Encounter
    creature_name = "Photonic Light-Moth"
    creature_wonder = "its crystal wings shimmer with bright golden sparks"
    creature_handling = "Hold up a polished amber prism and whistle a soft harmonic tone"
    if galactic_scale_generator:
        c_enc = galactic_scale_generator.generate_creature_encounter(None, f"story_{book_id}_{chapter_num}")
        if c_enc:
            creature_name = c_enc["creature_name"].split("(")[0].strip()
            creature_wonder = c_enc["sensory_specialty"].lower().rstrip(".")
            creature_handling = c_enc["friendly_handling_protocol"].rstrip(".")

    # 6. Chapter Title & 20-Chapter Arc Info
    arc_info = get_chapter_arc_info(chapter_num)
    title_choices = CHAPTER_TITLE_TEMPLATES.get(chapter_num, ["A New Dawn in the Stars"])
    chosen_title_suffix = title_choices[(book_id) % len(title_choices)].replace("{world}", homeworld).replace("{creature}", creature_name)
    chapter_display_title = f"Chapter {chapter_num:02d}: {chosen_title_suffix}"
    rank_article = "an" if active_rank.startswith("A") or active_rank.startswith("E") or active_rank.startswith("I") or active_rank.startswith("O") or active_rank.startswith("U") else "a"

    # 7. Multi-Scene Narrative Generation (4 Engaging Scenes)
    
    # --- SCENE 1: Morning Light, Warm Hospitality & Gentle Banter ---
    scene_1 = f"""The golden light of {stellar_type} broke across the horizon of {active_world}, casting long, gentle shadows over {biome_desc.lower()}. Inside the observation workshop, the air smelled wonderfully of {drink_name} and fresh {snack_name}.

{hero}, now serving proudly as {rank_article} **{active_rank}**, tightened the brass fasteners on his flight tunic. On the workbench beside him, a curious young {creature_name} perched near the tool rack. It let out a cheerful, trilling chirp as {creature_wonder}.

"Don't let our little friend get into the spare copper bolts, {hero_first_name}!" chuckled {mentor_title}, setting down two steaming mugs with a warm, wrinkled smile. "Under the guidance of {governance_title}, a good breakfast comes before any great flight. Remember what our elders teach: *{idiom}*"

"No worries, {mentor_title}!" {hero_first_name} grinned back, feeding the little creature a small crumb of sweet bread. The creature chirped happily and nudged {hero_first_name}'s thumb. "{hospitality_greeting} Today's route looks clear across Sector {sector}."

"Clear, but the Confluence Wavefront is in {wave_state['wave_zone']}," {mentor_title} noted, tapping the brass barometer dial. "Keep your eyes sharp and your hands gentle on the steering yoke."
"""

    # --- SCENE 2: The Expedition & The Unexpected Astronomical Challenge ---
    scene_2 = f"""Climbing aboard the {vehicle_name}, {hero_first_name} settled into the pilot's seat. The cockpit felt welcoming, surrounded by {vehicle_vibe}. With a smooth push of the primary throttle lever, the magnetic landing skids unlocked, and the craft leaped gracefully into the sky.

Beneath the panoramic canopy, {loc_data['desc']} stretched out in breathtaking splendor. At {gravity_g}g gravity, every glide felt buoyant and clean.

Suddenly, a resonant chime echoed from the main instrument console! The wavefront shifted into {res['resonance_state']} at {facing_angle:.1f}° facing angle.

The active physical constraint asserted itself immediately: **{res['active_limitation']}**!

"{mentor_title}!" {hero_first_name} called through the comm-link, adjusting the control trim as the craft vibrated with a deep harmonic hum. "The primary indicator needle is oscillating! {arc_info['dilemma']}"

"Steady, {hero_first_name}!" {mentor_title}'s calm voice crackled back through the speaker. "Do not fight the kinetic pull. Breathe, observe the flow, and trust your training!"
"""

    # --- SCENE 3: Creative, Non-Violent Breakthrough & Teamwork ---
    scene_3 = f"""{hero_first_name} took a deep, steadying breath. Panicking never solved a gear jam or a solar flare. 

Beside the instrument pod, the little {creature_name} fluttered its wings, tilting its head toward the lower bypass housing. It remembered the gentle handling protocol ({creature_handling.lower()}) and pointed its sparkling antennae directly at the harmonic dampener.

"Of course!" {hero_first_name} realized with a bright spark of insight. "The natural magnetic resonance is creating a bypass pathway!"

Working with calm, measured precision, {hero_first_name} drew his {signature_gear.lower()} and gently adjusted the auxiliary relief valve by zero-point-two millimeters. {arc_info['resolution']}

*Click-clack-hum.*

The rattling vibration instantly melted away. The warning glare smoothed into a harmonious, steady emerald glow. The {vehicle_name} leveled off, gliding through the sparkling celestial corridor as smoothly as a river pebble.
"""

    # --- SCENE 4: Triumph, Celebration & The Expanding Horizon ---
    scene_4 = f"""A brilliant, focused beacon pulse beamed upward from the array, striking the sector transit buoy with flawless accuracy. Across Sector {sector}, the green navigation lights blinked in joyful sequence, opening safe passage for traveling starships and friendly convoys.

"Magnificent flying, {hero_first_name}!" {mentor_title}'s proud cheer rang through the cockpit comms. "You handled that with patience, courage, and true craftsmanship. The entire council will celebrate tonight!"

{hero_first_name} let out a joyful laugh, reaching down to gently stroke the soft crest of the {creature_name}. Below them, the starlit horizon stretched endless and bright, full of mysteries waiting to be explored.

As {active_rank}, {hero_first_name} knew this was only one step on a grand journey spanning trillions of worlds across the great Stellar Confluence.

Across the vast cosmos, the next storyline in the grand rotation was ready to awaken.
"""

    full_prose = f"""# Book {book_id:02d}: {title}
## {chapter_display_title}

**Galactic Universal Time (GUT)**: {gut}
**Perspective Character**: {hero} ({active_rank}) | **Faction**: {faction}
**Current Location**: {active_world} (`{active_loc_type}` | Sector `{sector}`)
**Resonance State**: `{res['resonance_state']}` ({facing_angle:.1f}° Facing Alignment)
**Confluence Wave Intensity**: `{wave_state['wave_intensity_factor']}` ({wave_state['wave_zone']})
**Primary Transport**: `{vehicle_name}`
**Governance & Cultural Accord**: `{governance_title}`
**Story Arc Phase**: `{arc_info['phase']}`

---

{scene_1}

{scene_2}

{scene_3}

{scene_4}
"""

    file_path = None
    if save:
        book_folder = chapter_engine.get_book_dir(book_id)
        chapter_file = os.path.join(book_folder, f"Book_{book_id:02d}_Chapter_{chapter_num:02d}.md")
        os.makedirs(book_folder, exist_ok=True)
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(full_prose)
        file_path = chapter_file

    return {
        "status": "drafted",
        "book_id": book_id,
        "chapter_num": chapter_num,
        "chapter_title": chosen_title_suffix,
        "hero": hero,
        "rank": active_rank,
        "title": title,
        "faction": faction,
        "world": active_world,
        "mentor": mentor_title,
        "vehicle_deployed": vehicle_name,
        "phase": arc_info["phase"],
        "plot_style": plot_style or "EXPLORATION_DISCOVERY",
        "creature_encounter": creature_name,
        "total_words": len(full_prose.split()),
        "saved_to_file": file_path,
        "chapter_prose": full_prose,
        "prose_preview": full_prose[:400] + "..."
    }

def generate_dual_layer_annotated_chapter(book_id: int, chapter_num: int = 1, plot_style: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a dual-layer story artifact:
    - Layer 1: Sensory-rich, warm, non-violent story accessible to a 10-year-old child (Grade 4-6).
    - Layer 2: Deep intellectual companion breakdown explaining astrophysics, propulsion kinetics,
      macroeconomics, and civic philosophy for smart readers and students.
    """
    draft = generate_full_chapter_prose(book_id, chapter_num, save=False, plot_style=plot_style)
    if "error" in draft:
        return draft

    char_info = chapter_engine.get_character_info(book_id)
    clock_info = chapter_engine.get_clockwork_state(book_id)
    facing_angle = clock_info["facing_angle"] if clock_info else 15.0
    loc_type = clock_info["loc_type"] if clock_info else char_info["loc_type"]
    sector = clock_info["sector"] if clock_info else char_info["sector"]

    planet = planetary_ecology_matrix.get_planetary_profile(char_info["world"])
    res = calculate_resonance(facing_angle, draft["faction"], loc_type)
    wave_state = calculate_wavefront_state(sector, clock_info["gut"] if clock_info else 100)

    # Transport profile
    v_profile = None
    if galactic_transport_engine:
        v_profile = galactic_transport_engine.get_vehicle_profile(draft["vehicle_deployed"])

    # Sociological profile
    soc_profile = None
    if galactic_sociology_politics_engine:
        soc_profile = galactic_sociology_politics_engine.get_sociological_profile(draft["faction"])

    companion_breakdown = {
        "layer_1_child_wonder_summary": f"In this chapter, {draft['hero']} ({draft['rank']}) demonstrates courage, steady focus, and kindness alongside {draft['creature_encounter']} and mentor {draft['mentor']}.",
        "layer_2_astrophysics_and_kinetics": {
            "stellar_and_planetary_physics": f"World {char_info['world']} operates with {planet.get('astrophysics', {}).get('surface_gravity_g', 1.0)}g surface gravity under a {planet.get('astrophysics', {}).get('stellar_type', 'G-type')} star.",
            "confluence_wavefront_mechanics": f"Facing angle of {facing_angle:.1f}° places the hero in {res['resonance_state']} with a wavefront intensity factor of {wave_state['wave_intensity_factor']}.",
            "propulsion_physics": v_profile.get("intuitive_explanation", "Photonic and kinetic momentum.") if v_profile else "Kinetic propulsion."
        },
        "layer_3_macroeconomics_and_trade": {
            "export_surplus": planet.get("key_exports", ["Solarite Ore", "Precision Tech"]),
            "market_role": f"{char_info['world']} acts as a primary supply hub connecting to interstellar trade lanes."
        },
        "layer_4_civics_and_philosophy": {
            "governance_model": soc_profile.get("governance_model", "Artificer Council") if soc_profile else "Regional Council",
            "hospitality_and_ethics": soc_profile.get("hospitality_ritual", {}).get("name", "Welcoming tea and peaceful fellowship") if soc_profile else "Hospitality greeting"
        }
    }

    return {
        "status": "DUAL_LAYER_CHAPTER_GENERATED",
        "book_id": book_id,
        "chapter_num": chapter_num,
        "hero": draft["hero"],
        "title": draft["title"],
        "story_prose_layer_1": draft["chapter_prose"],
        "intellectual_companion_layer_2": companion_breakdown
    }

def generate_model_authoring_brief(book_id: int, chapter_num: int = 1, gut: Optional[int] = None) -> Dict[str, Any]:
    """Generates a complete, high-context authoring brief for LLM / subagent chapter writing."""
    import model_prompt_architect
    return model_prompt_architect.build_model_authoring_context(book_id, chapter_num, gut)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Multi-Faction Chapter Story Generator")
    parser.add_argument("--book-id", type=int, default=1, help="Book ID (1-74)")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number")
    parser.add_argument("--save", action="store_true", help="Save chapter markdown to library")
    parser.add_argument("--style", help="Plot style: EXPLORATION_DISCOVERY, HIGH_STAKES_RESCUE, CREATURE_ALLIANCE, ENGINEERING_EMERGENCY")
    parser.add_argument("--dual-layer", action="store_true", help="Generate dual-layer story and educational companion breakdown")

    args = parser.parse_args()
    if args.dual_layer:
        res = generate_dual_layer_annotated_chapter(args.book_id, args.chapter, plot_style=args.style)
    else:
        res = generate_full_chapter_prose(args.book_id, args.chapter, save=args.save, plot_style=args.style)
    print(json.dumps(res, indent=2))

