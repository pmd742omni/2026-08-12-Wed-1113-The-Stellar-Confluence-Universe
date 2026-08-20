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
from narrative_beat_architect import generate_scene_beats, PLOT_STYLES
from confluence_wave_physics import calculate_wavefront_state
import chapter_engine
import character_mesh_graph
import planetary_ecology_matrix
import faction_matrix
import character_voice_profiler
import artifact_ledger_engine

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

def generate_full_chapter_prose(book_id: int, chapter_num: int, save: bool = False, plot_style: Optional[str] = None) -> Dict[str, Any]:
    """
    Synthesizes a complete, beautifully written chapter adhering strictly to Grade 4-6 readability,
    scientific authenticity, celestial mechanics, vehicle transport, and sociological richness.
    """
    book_id = int(book_id)
    chapter_num = int(chapter_num)
    
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        return {"error": f"Book {book_id} not found in registry"}

    clock_info = chapter_engine.get_clockwork_state(book_id)
    facing_angle = clock_info["facing_angle"] if clock_info else 15.0
    loc_type = clock_info["loc_type"] if clock_info else char_info["loc_type"]
    sector = clock_info["sector"] if clock_info else char_info["sector"]
    gut = clock_info["gut"] if clock_info else 100

    hero = char_info["hero"]
    title = char_info["title"]
    world = char_info["world"]
    faction = char_info["faction"]

    # 1. Physics & Resonance
    res = calculate_resonance(facing_angle, faction, loc_type)
    wave_state = calculate_wavefront_state(sector, gut)

    # 2. Universe State & Ecology
    mesh_info = character_mesh_graph.get_character_mesh(book_id)["mesh"]
    mentor = mesh_info.get("mentor", f"Master Elder of {world}")
    planet = planetary_ecology_matrix.get_planetary_profile(world)
    fac_profile = faction_matrix.get_faction_profile(faction)["profile"]
    voice_profile = character_voice_profiler.get_faction_voice_profile(faction)

    signature_gear = fac_profile.get("signature_gear", "Resonant Gear").split(",")[0].strip()
    idiom = voice_profile.get("typical_idioms", ["Hold steady and trust the alignment."])[0]
    biome_desc = planet.get("biome", "Dramatic alien terrain")
    gravity_g = planet.get("astrophysics", {}).get("surface_gravity_g", 1.0)
    stellar_type = planet.get("astrophysics", {}).get("stellar_type", "Primary Star")

    # 3. Transport Vehicle Integration
    vehicle_name = "Solar-Thermal Atmospheric Skimmer"
    vehicle_vibe = "smooth magnetic rudder sticks and panoramic brass canopy"
    if galactic_transport_engine:
        v_pref = galactic_transport_engine.get_faction_vehicle_preference(faction)
        if v_pref.get("vehicles"):
            v_obj = v_pref["vehicles"][0]
            vehicle_name = v_obj.get("name", vehicle_name)
            vehicle_vibe = v_obj.get("cockpit_vibe", vehicle_vibe).split(",")[0].strip()

    # 4. Sociological & Cultural Traditions
    cultural_ritual = "Offering a warm drink and a polished wishing stone"
    hospitality_greeting = "May your path be steady under the turning stars."
    governance_title = "The Regional Artificer Council"
    if galactic_sociology_politics_engine:
        soc_prof = galactic_sociology_politics_engine.get_sociological_profile(faction)
        if soc_prof:
            cultural_ritual = soc_prof.get("hospitality_ritual", {}).get("name", cultural_ritual)
            hospitality_greeting = soc_prof.get("hospitality_ritual", {}).get("dialogue_phrase", hospitality_greeting)
            governance_title = soc_prof.get("governance_model", governance_title)

    # 5. Indigenous Creature
    creature_name = "Photonic Light-Moth"
    creature_wonder = "Prismatic crystal wings reflect sunlight into protective halos"
    creature_handling = "Hold up a polished amber prism and speak in gentle tones"
    if galactic_scale_generator:
        c_enc = galactic_scale_generator.generate_creature_encounter(None, f"story_{book_id}_{chapter_num}")
        if c_enc:
            creature_name = c_enc["creature_name"].split("(")[0].strip()
            creature_wonder = c_enc["sensory_specialty"]
            creature_handling = c_enc["friendly_handling_protocol"]

    # Select dynamic plot style
    style_choices = list(PLOT_STYLES.keys())
    chosen_style = plot_style.upper() if (plot_style and plot_style.upper() in PLOT_STYLES) else style_choices[(book_id * 3 + chapter_num) % len(style_choices)]

    # --- Act 1: Sensory Opening, Vehicle Grounding & Cultural Warmth ---
    if "Sun" in faction:
        act1_prose = f"""The blazing twin suns of {world} climbed steadily into the copper sky, casting long, sharp shadows across {biome_desc.lower()}.
{hero} stepped onto the boarding ramp of the {vehicle_name}. The controls gleamed with {vehicle_vibe}. Even through the tinted glass, the horizon sparkled with dazzling light. The incoming Confluence Wavefront was in {wave_state['wave_zone']}, sending a pleasant, electric hum through the soles of his boots. Nearby, a gentle {creature_name} glided through the warm morning breeze, its wings shimmering as {creature_wonder.lower()}.
"Watch your heat gauge, {hero}!" called out {mentor} from the observatory balcony. His old voice was gravelly but kind as he raised a cup of warm tea. "Under {governance_title}, we honor every visitor with patience. Remember: {idiom}"
"I hear you, Master!" {hero} shouted back with a grin, wiping a bead of sweat from his chin. "{hospitality_greeting}"
"""
    elif "Void" in faction:
        act1_prose = f"""A deep, soothing twilight hung over {world}, where {biome_desc.lower()} stretched into the cool quiet of the canyon.
{hero} adjusted the controls of the {vehicle_name}, enjoying the {vehicle_vibe}. The air was still and crisp, carrying the soft scent of nocturnal lichen. Across Sector {sector}, the Confluence Wavefront brushed the atmosphere in {wave_state['wave_zone']}, silencing stray echoes. From a high stone ledge, a watchful {creature_name} looked down with curious, glowing eyes.
"Listen to the stone, {hero}," whispered {mentor}, stepping gracefully from the shadows of the sanctuary. Her eyes reflected the gentle bioluminescence of the cavern. "In the nadir shadow, patience is our greatest shield. {idiom}"
"I am listening, Elder," {hero} replied softly, feeling the steady coolness of the phase-stone beneath their fingertips. "{hospitality_greeting}"
"""
    elif "Astrolabe" in faction:
        act1_prose = f"""Rhythmic clicks and hums echoed across the brass towers of {world}, where {biome_desc.lower()} gleamed under the filtered orbital mist.
{hero} calibrated the precision calipers inside the cockpit of the {vehicle_name}, surrounded by {vehicle_vibe}. Every counterweight was balanced, and the massive meridian flywheels turned with clockwork grace. The incoming Confluence Wavefront hovered in {wave_state['wave_zone']}, vibrating through the bronze floorplates while a playful {creature_name} fluttered around the steam vents.
"Check your tolerance levels, {hero}!" shouted {mentor} over the hiss of a steam valve. "Centrifugal momentum builds fast during harmonic transit. {idiom}"
"Tolerance is locked at zero-point-two microns, Chief!" {hero} called back with a proud smile. "{hospitality_greeting}"
"""
    elif "Comet" in faction:
        act1_prose = f"""A shimmering tail of ionized dust and blue vapor arched across the sky of {world}, illuminating {biome_desc.lower()}.
{hero} tightened the thermal straps on the {vehicle_name}, feeling the {vehicle_vibe}. At {gravity_g}g surface gravity, every step was a buoyant glide over the ice. The Confluence Wavefront surged in {wave_state['wave_zone']}, charging the sublimation thrusters with crackling static as a swift {creature_name} leaped alongside in tandem glide.
"Keep your eyes on the vapor ridge, {hero}!" called out {mentor} through the comm-bead, his voice full of excitement. "{idiom}"
"Vapor trail locked!" {hero} shouted into the wind, sliding effortlessly over the glistening frost crest. "{hospitality_greeting}"
"""
    else: # Expansion Factions
        act1_prose = f"""Vivid celestial light bathed the horizon of {world}, reflecting across {biome_desc.lower()} under {stellar_type}.
{hero} checked the instruments of the {vehicle_name}, noting the {vehicle_vibe}. Around them, the unique natural harmony of their homeworld hummed in rhythm with the Confluence Wavefront in {wave_state['wave_zone']}. A native {creature_name} moved calmly nearby, responding to the shifting energy with tranquil grace.
"{hero}, maintain steady focus on the primary array," called out {mentor}, watching with supportive guidance. "Our elders always say: {idiom}"
"Ready on all channels!" {hero} responded with cheerful determination. "{hospitality_greeting}"
"""

    # --- Act 2: Dynamic Complication, Transport Kinetics & Creative Ingenuity ---
    if chosen_style == "EXPLORATION_DISCOVERY":
        act2_prose = f"""{hero} placed gauntleted hands onto the survey array of the {vehicle_name}. A set of strange harmonic coordinates flickered onto the brass dials, pointing toward an uncharted ridge across the sector.
Suddenly, a warning chime rang out! The active power limit asserted itself—{res['active_limitation']}.
"The navigational compass is oscillating wildly!" {hero} called out, steadying the steering yoke.
"Take your time and observe the terrain!" {mentor} advised calmly through the comms. "Remember our people's custom of {cultural_ritual.lower()}. Nature always reveals the balance."
Noticing the {creature_name} moving safely along an unmapped stone shelf, {hero} realized the creature was using natural magnetic pathways to bypass the interference. Moving with gentle patience ({creature_handling.lower()}), {hero} adjusted the vehicle's alignment to match the creature's glide path.
Click!
The erratic frequency smoothed into a crystal-clear harmonic signal, revealing a safe transit corridor across the planetary expanse.
"""
    elif chosen_style == "HIGH_STAKES_RESCUE":
        act2_prose = f"""An emergency distress ping echoed through the cockpit comms! A sub-light cargo probe's stabilizer had jammed in the high atmospheric jet stream, drifting dangerously close to a jagged crystal spire.
{hero} fired the steering verniers of the {vehicle_name}, angling into the wind. But as the wavefront shifted, the active constraint took hold: {res['active_limitation']}.
"Thruster output is bottlenecked!" {hero} gasped, watching the telemetry gauge drop.
"Do not force the engine!" {mentor} shouted through the link. "Use the planet's gravity curve and keep your hands steady!"
Drawing a deep, calm breath, {hero} relied on kinetic momentum. Spotting a helpful thermal updraft signaled by a passing {creature_name}, {hero} launched an insulated grappling line. With a firm, practiced tug, {hero} snagged the probe's tow-ring and swung it into safe, open airspace.
The rescue was complete, and the recovered cargo beacon glowed a steady, reassuring green.
"""
    elif chosen_style == "CREATURE_ALLIANCE":
        act2_prose = f"""A sudden tremor rippled across {world}. A young {creature_name} had wandered onto the primary power conduit platform, its natural electromagnetic field unintentionally drawing sparks from the collector coils.
"Stand clear, {hero}!" {mentor} warned. "If you startle it during a wavefront surge, the power limit will trigger—{res['active_limitation']}!"
"I won't startle it," {hero} said softly. "It's just disoriented by the static build-up."
Lowering the heavy visor and powering down the vehicle's loud intake fan, {hero} stepped onto the platform. {hero} remembered the ancient guidance: {creature_handling}. Slowly, {hero} whistled a soft, harmonic tone matching the creature's breathing rhythm.
The {creature_name} tilted its head, calmed by {hero}'s peaceful presence, and gently stepped away from the energized coils back into the safety of the sanctuary gardens.
"""
    else: # ENGINEERING_EMERGENCY / RELIC_DECIPHERING
        act2_prose = f"""{hero} placed gauntleted hands onto the primary control housing. Click, click, click. The precision linkages of the {signature_gear.lower()} hummed as they aligned with the celestial coordinates.
Suddenly, a warning chime rang out! A sharp tremor vibrated through the casing. The active power limit was asserting itself—{res['active_limitation']}.
"The bypass valve is resisting!" {hero} gasped, watching the indicator needle jump into the warning zone.
"Step back and assess!" {mentor} called out urgently, leaning forward with watchful eyes. "If that circuit overloads, the entire sector relay will trip offline!"
"No, I can steady it manually!" {hero} replied. Drawing a calm, deep breath, {hero} ducked beneath the venting exhaust. Using an insulated wrench and pure physical focus, {hero} hooked the stuck release lever and eased it back into its guide groove with practiced care.
Clack!
The latch locked securely into position. The fluctuating gauge settled, and the warning glare smoothed into a harmonious, steady glow.
"""

    # --- Act 3: Climax, Discovery & Rotation Hand-off ---
    act3_prose = f"""A brilliant, focused pulse of resonant energy surged through the primary array of {world}, piercing cleanly into the atmosphere and striking the orbital relay waypoint with absolute accuracy. The distant beacon chimed in triumphant harmony, signaling a green status across Sector {sector}.
"Splendid work, {hero}," {mentor} said with a warm smile, clapping a proud hand over {hero}'s shoulder. "A steady hand, kind heart, and brave mind make all the difference in the galaxy."
{hero} let out a long breath of relief and gazed up at the sky. Far beyond the cloud tops, the blue carrier pulse echoed into the deep space transit routes, linking their homeworld to neighboring star systems.
Across the vast reaches of the galaxy, the next storyline in the grand rotation was ready to awaken.
"""

    full_prose = f"""# Book {book_id:02d}: {title}
## Chapter {chapter_num:02d}

**Galactic Universal Time (GUT)**: {gut}
**Perspective Character**: {hero} | **Faction**: {faction}
**Location**: {world} (`{loc_type}` | Sector `{sector}`)
**Resonance State**: `{res['resonance_state']}` ({facing_angle:.1f}° Facing Alignment)
**Confluence Wave Intensity**: `{wave_state['wave_intensity_factor']}` ({wave_state['wave_zone']})
**Primary Transport**: `{vehicle_name}`
**Governance & Cultural Accord**: `{governance_title}`
**Narrative Plot Style**: `{chosen_style}`

---

{act1_prose}

{act2_prose}

{act3_prose}
"""

    file_path = None
    if save:
        title_slug = chapter_engine.slugify(title)
        book_folder = os.path.join(chapter_engine.BOOKS_LIB_DIR, f"Book_{book_id:02d}_{title_slug}")
        chapter_file = os.path.join(book_folder, f"Book_{book_id:02d}_Chapter_{chapter_num:02d}.md")
        os.makedirs(book_folder, exist_ok=True)
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(full_prose)
        file_path = chapter_file

    return {
        "status": "drafted",
        "book_id": book_id,
        "chapter_num": chapter_num,
        "hero": hero,
        "title": title,
        "faction": faction,
        "world": world,
        "mentor": mentor,
        "vehicle_deployed": vehicle_name,
        "plot_style": chosen_style,
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
    - Layer 2: Deep intellectual companion breakdown explaining the astrophysics, propulsion kinetics,
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

    planet = planetary_ecology_matrix.get_planetary_profile(draft["world"])
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
        "layer_1_child_wonder_summary": f"In this chapter, {draft['hero']} demonstrates courage, steady focus, and kindness by solving an emergency alongside {draft['creature_encounter']} and their mentor {draft['mentor']}.",
        "layer_2_astrophysics_and_kinetics": {
            "stellar_and_planetary_physics": f"World {draft['world']} operates with {planet.get('astrophysics', {}).get('surface_gravity_g', 1.0)}g surface gravity and a {planet.get('astrophysics', {}).get('diurnal_cycle_gut', 24)} GUT day-night cycle under a {planet.get('astrophysics', {}).get('stellar_type', 'G-type')} star.",
            "confluence_wavefront_mechanics": f"Facing angle of {facing_angle:.1f}° places the hero in {res['resonance_state']} with a wavefront intensity factor of {wave_state['wave_intensity_factor']}.",
            "propulsion_physics": v_profile.get("intuitive_explanation", "Photonic and kinetic momentum.") if v_profile else "Kinetic propulsion."
        },
        "layer_3_macroeconomics_and_trade": {
            "export_surplus": planet.get("key_exports", ["Solarite Ore", "Precision Tech"]),
            "market_role": f"{draft['world']} acts as a primary supply hub, connecting to interstellar trade lanes via commercial convoys."
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

