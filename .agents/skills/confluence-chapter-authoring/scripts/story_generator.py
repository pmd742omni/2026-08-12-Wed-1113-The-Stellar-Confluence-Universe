#!/usr/bin/env python3
"""
Autonomous Multi-Faction Chapter Story Generator for The Stellar Confluence Universe
Composes sensory-rich, dialogue-driven prose accessible to a 10-year-old child (Grade 4-6),
dynamically synthesizing character identity, mentors, planetary biomes, faction mechanics,
active relics, and celestial wave physics across all 74 storylines.
"""

import os
import sys
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(os.path.dirname(SCRIPT_DIR), "..", "universe-state-manager", "scripts"))

from calculate_resonance import calculate_resonance
from narrative_beat_architect import generate_scene_beats
from confluence_wave_physics import calculate_wavefront_state
import chapter_engine
import character_mesh_graph
import planetary_ecology_matrix
import faction_matrix
import character_voice_profiler
import artifact_ledger_engine

def generate_full_chapter_prose(book_id, chapter_num, save=False):
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

    # 2. Rich Universe State Integration
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

    # 3. Dynamic 3-Act Prose Generation Tailored to Faction & Environment
    # Act 1: Sensory Opening & Grounding
    if "Sun" in faction:
        act1_prose = f"""The blazing twin suns of {world} climbed steadily into the copper sky, casting long, sharp shadows across {biome_desc.lower()}.

{hero} adjusted the heavy bronze visor over his eyes. Even through the tinted glass, the horizon sparkled with dazzling light. The incoming Confluence Wavefront was in {wave_state['wave_zone']}, sending a pleasant, electric hum through the soles of his boots.

"Watch your heat gauge, {hero}!" called out {mentor} from the observatory balcony. His old voice was gravelly but kind. "At this morning angle, the radiant energy is eager to leap into our {signature_gear.lower()}. Remember: {idiom}"

"I hear you, Master!" {hero} shouted back with a grin, wiping a bead of sweat from his chin. "Slow and steady. Like turning the great waterwheel."
"""
    elif "Void" in faction:
        act1_prose = f"""A deep, soothing twilight hung over {world}, where {biome_desc.lower()} stretched into the cool quiet of the canyon.

{hero} adjusted the obsidian folds of the {signature_gear.lower()}. The air was still and crisp, carrying the soft scent of nocturnal lichen. Across Sector {sector}, the Confluence Wavefront brushed the atmosphere in {wave_state['wave_zone']}, silencing stray echoes.

"Listen to the stone, {hero}," whispered {mentor}, stepping gracefully from the shadows. Her eyes reflected the gentle bioluminescence of the cavern. "In the nadir shadow, patience is our greatest shield. {idiom}"

"I am listening, Elder," {hero} replied softly, feeling the steady coolness of the phase-stone beneath their fingertips. "The twilight is clear."
"""
    elif "Astrolabe" in faction:
        act1_prose = f"""Rhythmic clicks and hums echoed across the brass towers of {world}, where {biome_desc.lower()} gleamed under the filtered orbital mist.

{hero} calibrated the precision calipers of the {signature_gear.lower()}. Every counterweight was balanced, and the massive meridian flywheels turned with clockwork grace. The incoming Confluence Wavefront hovered in {wave_state['wave_zone']}, vibrating through the bronze floorplates.

"Check your tolerance levels, {hero}!" shouted {mentor} over the hiss of a steam valve. "Centrifugal momentum builds fast during harmonic transit. {idiom}"

"Tolerance is locked at zero-point-two microns, Chief!" {hero} called back, checking the spring tension dial with a satisfied nod.
"""
    elif "Comet" in faction:
        act1_prose = f"""A shimmering tail of ionized dust and blue vapor arched across the sky of {world}, illuminating {biome_desc.lower()}.

{hero} tightened the thermal straps on the {signature_gear.lower()}. At {gravity_g}g surface gravity, every step was a buoyant glide over the ice. The Confluence Wavefront surged in {wave_state['wave_zone']}, charging the sublimation thrusters with crackling static.

"Keep your eyes on the vapor ridge, {hero}!" called out {mentor} through the comm-bead, his voice full of excitement. "{idiom}"

"Vapor trail locked!" {hero} shouted into the wind, sliding effortlessly over the glistening frost crest.
"""
    else: # Expansion Factions (Nebula-Weavers, Deep-Core, Plasma-Shepherds, Bio-Alchemists, etc.)
        act1_prose = f"""Vivid celestial light bathed the horizon of {world}, reflecting across {biome_desc.lower()} under {stellar_type}.

{hero} secured the straps on the {signature_gear.lower()}. Around them, the unique natural harmony of their homeworld hummed in rhythm with the Confluence Wavefront in {wave_state['wave_zone']}.

"{hero}, maintain steady focus on the primary array," called out {mentor}, watching with supportive guidance. "Our elders always say: {idiom}"

"Ready on all channels!" {hero} responded with cheerful determination, stepping forward to meet the challenge.
"""

    # Act 2: Escalating Physical Dilemma & Teamwork
    act2_prose = f"""{hero} placed gauntleted hands onto the primary control housing. Click, click, click. The precision linkages hummed as they aligned with the celestial coordinates.

Suddenly, a warning chime rang out! A sharp tremor vibrated through the casing. The active power limit was asserting itself—{res['active_limitation']}.

"The bypass channel is resisting!" {hero} gasped, watching the indicator needle jump into the warning zone.

"Step back and assess!" {mentor} called out urgently, leaning forward with watchful eyes. "If that circuit overloads, the entire sector relay will trip offline!"

"No, I can steady it manually!" {hero} replied. Drawing a calm, deep breath, {hero} ducked beneath the venting exhaust. Using an insulated wrench and pure physical focus, {hero} hooked the stuck release lever and eased it back into its guide groove with practiced care.

Clack!

The latch locked securely into position. The fluctuating gauge settled, and the warning glare smoothed into a harmonious, steady glow.
"""

    # Act 3: Climax, Discovery & Rotation Hand-off
    act3_prose = f"""A brilliant, focused pulse of resonant energy surged through the primary array of {world}, piercing cleanly into the atmosphere and striking the orbital relay waypoint with absolute accuracy. The distant beacon chimed in triumphant harmony, signaling a green status across Sector {sector}.

"Splendid work, {hero}," {mentor} said with a warm smile, clapping a proud hand over {hero}'s shoulder. "A steady hand and brave heart make all the difference."

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
        "total_words": len(full_prose.split()),
        "saved_to_file": file_path,
        "chapter_prose": full_prose,
        "prose_preview": full_prose[:400] + "..."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Multi-Faction Story Generator")
    parser.add_argument("--book", type=int, default=1, help="Book ID (1-74)")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number")
    parser.add_argument("--save", action="store_true", help="Save directly to chapter file in 01_Books_Library")

    args = parser.parse_args()
    res = generate_full_chapter_prose(args.book, args.chapter, save=args.save)
    print(json.dumps(res, indent=2))
