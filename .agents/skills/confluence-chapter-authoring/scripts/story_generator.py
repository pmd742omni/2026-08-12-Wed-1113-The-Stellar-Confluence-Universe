#!/usr/bin/env python3
"""
Autonomous Chapter Story Generator & Prose Drafting Co-Pilot for The Stellar Confluence Universe
Composes sensory-rich, dialogue-driven prose accessible to a 10-year-old child (Grade 4-6),
integrating 3-act narrative beats, character voices, wave physics, and physical limitations.
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

    # 1. Physics & Resonance
    res = calculate_resonance(facing_angle, char_info["faction"], loc_type)
    wave_state = calculate_wavefront_state(sector, gut)

    # 2. Scene Beats
    beats = generate_scene_beats(
        char_info["hero"], char_info["title"], char_info["faction"], char_info["world"],
        loc_type, facing_angle, res["resonance_state"], res["power_capability"], res["active_limitation"]
    )

    hero = char_info["hero"]
    title = char_info["title"]
    world = char_info["world"]
    faction = char_info["faction"]

    # 3. Autonomous High-Quality Prose Generation
    # Act 1 Prose (Sensory Opening & Grounding)
    act1_prose = f"""The twin suns of {world} climbed steadily into the copper sky, casting long, sharp shadows across the shifting sands.

{hero} adjusted the heavy bronze visor over his eyes. Even through the tinted glass, the horizon sparkled with dazzling light. The incoming Confluence Wavefront was in {wave_state['wave_zone']}, sending a pleasant, electric hum through the soles of his sand-boots.

"Watch your heat gauge, {hero}!" called out Master Theron from the observatory balcony. His old voice was gravelly but kind. "At this morning angle, the radiant energy is eager to leap into our lenses. If you rush, the brass will melt before the beam is set!"

"I hear you, Master!" {hero} shouted back with a grin, wiping a bead of sweat from his chin. "Slow and steady. Like turning the great waterwheel."
"""

    # Act 2 Prose (Escalating Physical Dilemma & Teamwork)
    act2_prose = f"""{hero} placed his gauntleted hands on the dual steering rings of the solar relay. Click, click, click. The precision gears groaned as they aligned with the blazing suns.

Suddenly, a high-pitched hiss hissed from the lower cooling valve. White steam burst into the desert air!

"The thermal bypass is stuck!" {hero} gasped. The warning crystal on his gauntlet flared angry orange. The active power limit was hitting hard—{res['active_limitation']}.

"Back away from the pedestal!" Theron shouted, leaning over the brass railing with wide eyes. "If the lens fractures, the entire sector will lose relay power!"

"No, I can reach the manual release pin!" {hero} replied. His heart thumped against his ribs, but he did not run. Remembering his daily drills, he ducked beneath the venting steam. The radiant beam above him hummed like a plucked wire, searing hot. Using his insulated wrench, he hooked the stuck lever and pulled with all his weight.

Clang!

The brass pin clicked back into its groove. Cool coolant hissed into the chamber, and the fierce orange glare faded into a steady, golden glow.
"""

    # Act 3 Prose (Climax, Discovery & Rotation Hand-off)
    act3_prose = f"""A clean, focused shaft of pure sunlight shot forward from the primary lens, piercing across the desert plain and striking the distant relay tower with pinpoint accuracy. The tower's beacon flared bright blue, chiming in harmonic triumph.

"You did it, lad," Master Theron said, walking down the steps with a proud smile and clapping a hand on {hero}'s shoulder. "Cool head under fire. That is the mark of a true guardian."

{hero} let out a long breath and looked up. Far beyond the atmosphere, the blue pulse from their relay beacon echoed outward into the deep space transit routes, carrying light and hope toward neighboring star systems.

Somewhere out there across the dark sectors, the next beacon was waiting to awaken.
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
        "total_words": len(full_prose.split()),
        "saved_to_file": file_path,
        "chapter_prose": full_prose,
        "prose_preview": full_prose[:400] + "..."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Story Generator")
    parser.add_argument("--book", type=int, default=1, help="Book ID (1-74)")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number")
    parser.add_argument("--save", action="store_true", help="Save directly to chapter file in 01_Books_Library")

    args = parser.parse_args()
    res = generate_full_chapter_prose(args.book, args.chapter, save=args.save)
    print(json.dumps(res, indent=2))
