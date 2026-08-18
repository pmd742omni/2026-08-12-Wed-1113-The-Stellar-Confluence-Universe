#!/usr/bin/env python3
"""
Unified Chapter Engine & Authoring Orchestrator for The Stellar Confluence Universe
Automates the full pipeline: state auditing, hazard detection, resonance calculation,
3-act narrative beat architecture, ephemeris propagation, and rotation advancement.
"""

import os
import sys
import json
import re
import argparse

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
    return cwd

PROJECT_ROOT = find_project_root()
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
BOOKS_LIB_DIR = os.path.join(PROJECT_ROOT, "01_Books_Library")
ROTATION_TRACKER_MD = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
CHARACTER_REGISTRY_MD = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
COSMIC_CLOCKWORK_MD = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")

# Ensure helper scripts are importable
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")
sys.path.insert(0, os.path.join(SKILLS_DIR, "confluence-chapter-authoring", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

from advance_rotation import read_rotation_tracker, advance_rotation, write_rotation_tracker
from calculate_resonance import calculate_resonance
from cosmic_event_bus import check_hazards
from cosmic_ephemeris_engine import propagate_ephemeris
from narrative_beat_architect import generate_scene_beats
import character_voice_profiler
import chapter_prose_evaluator
import character_mastery_engine
import galactic_tension_tracker

def slugify(text):
    clean = re.sub(r"[^\w\s-]", "", text).strip()
    return re.sub(r"[-\s]+", "_", clean)

def get_character_info(book_index):
    if not os.path.exists(CHARACTER_REGISTRY_MD):
        return None
    with open(CHARACTER_REGISTRY_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    pattern = rf"\|\s*\*\*Book\s+{book_index:02d}\*\*\s*\|\s*([^\|]+)\s*\|\s*`?([^\|`]+)`?\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*`?([^\|`]+)`?\s*\|\s*`?([^\|`]+)`?\s*\|"
    match = re.search(pattern, content, re.IGNORECASE)
    if not match:
        return None

    return {
        "book_id": book_index,
        "title": match.group(1).strip(),
        "hero": match.group(2).strip(),
        "faction": match.group(3).strip(),
        "world": match.group(4).strip(),
        "loc_type": match.group(5).strip().upper(),
        "sector": match.group(6).strip()
    }

def get_clockwork_state(book_index):
    if not os.path.exists(COSMIC_CLOCKWORK_MD):
        return None
    with open(COSMIC_CLOCKWORK_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    pattern = rf"\|\s*(\d+)\s*\|\s*Book\s+{book_index:02d}\s*\|\s*([^\|]+)\s*\|\s*`?([^\|`]+)`?\s*\|\s*`?([^\|`]+)`?\s*\|\s*([\d\.]+)°\s*\|\s*`?([^\|`]+)`?\s*\|\s*([^\|]+)\s*\|"
    match = re.search(pattern, content, re.IGNORECASE)
    if not match:
        return None

    return {
        "gut": int(match.group(1)),
        "hero": match.group(2).strip(),
        "loc_type": match.group(3).strip().upper(),
        "sector": match.group(4).strip(),
        "facing_angle": float(match.group(5)),
        "resonance_state": match.group(6).strip(),
        "power_limit_desc": match.group(7).strip()
    }

def prepare_next_chapter_stub():
    """Audits system state, generates 3-act scene blueprint, retrieves dialect guidelines, and scaffolds chapter stub."""
    rot = read_rotation_tracker()
    active_book = rot["active_book_index"]
    active_chap = rot["active_chapter_number"]
    curr_gut = rot["current_gut"]

    char_info = get_character_info(active_book)
    if not char_info:
        return {"error": f"Book {active_book} not found in character_registry.md"}

    clock_info = get_clockwork_state(active_book)
    facing_angle = clock_info["facing_angle"] if clock_info else 0.0
    loc_type = clock_info["loc_type"] if clock_info else char_info["loc_type"]
    sector = clock_info["sector"] if clock_info else char_info["sector"]

    # Check active hazards
    hazards = check_hazards(sector, curr_gut)

    # Compute resonance & constraints
    res = calculate_resonance(facing_angle, char_info["faction"], loc_type)

    # Generate 3-Act Scene Beats Blueprint
    beats = generate_scene_beats(
        char_info["hero"], char_info["title"], char_info["faction"], char_info["world"],
        loc_type, facing_angle, res["resonance_state"], res["power_capability"], res["active_limitation"], hazards["hazards"]
    )

    # Dialect and Cultural Voice Profile
    voice_profile = character_voice_profiler.get_faction_voice_profile(char_info["faction"])

    # Format paths
    title_slug = slugify(char_info["title"])
    book_folder = os.path.join(BOOKS_LIB_DIR, f"Book_{active_book:02d}_{title_slug}")
    chapter_file = os.path.join(book_folder, f"Book_{active_book:02d}_Chapter_{active_chap:02d}.md")
    os.makedirs(book_folder, exist_ok=True)

    # Generate Chapter Stub Markdown with Scene Blueprint & Voice Guidelines
    hazard_section = ""
    if hazards["active_hazard_count"] > 0:
        hazard_section = "\n**Active Environmental Anomalies**:\n"
        for h in hazards["hazards"]:
            hazard_section += f"- *{h['event_type']}* ({h['source_book']}): {h['description']} (Distance: {h['distance_units']} sectors)\n"

    stub_content = f"""# Book {active_book:02d}: {char_info['title']}
## Chapter {active_chap:02d}

**Galactic Universal Time (GUT)**: {curr_gut}
**Perspective Character**: {char_info['hero']} | **Faction**: {char_info['faction']}
**Location**: {char_info['world']} (`{loc_type}` | Sector `{sector}`)
**Resonance State**: `{res['resonance_state']}` ({facing_angle:.1f}° Facing Alignment)
**Power Capabilities**: {res['power_capability']}
**Active Constraints**: {res['active_limitation']}{hazard_section}

<!-- NARRATIVE SCENE BLUEPRINT (3-ACT PACING) -->
<!-- 
Act 1 (Sensory Opening): {beats['narrative_blueprint']['act_1_opening_grounding']}
Act 2 (Physical Dilemma): {beats['narrative_blueprint']['act_2_escalating_dilemma']}
Act 3 (Climax & Rotation Hand-off): {beats['narrative_blueprint']['act_3_climax_discovery']}
-->

<!-- FACTION DIALECT & VOCAL CADENCE GUIDELINES -->
<!--
Dialect: {voice_profile.get('dialect_name', char_info['faction'])}
Tone / Rhythm: {voice_profile.get('cadence', 'Balanced read-aloud pacing')}
Idiom Tendencies: {', '.join(voice_profile.get('typical_idioms', []))}
-->

---

[Draft chapter prose here with Grade 4-6 readability, high emotional stakes, sensory immersion, and bravery...]
"""

    if not os.path.exists(chapter_file):
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write(stub_content)
        created = True
    else:
        created = False

    return {
        "status": "ready",
        "active_book": active_book,
        "active_chapter": active_chap,
        "current_gut": curr_gut,
        "title": char_info["title"],
        "hero": char_info["hero"],
        "faction": char_info["faction"],
        "loc_type": loc_type,
        "sector": sector,
        "facing_angle": facing_angle,
        "resonance_state": res["resonance_state"],
        "power_capability": res["power_capability"],
        "active_limitation": res["active_limitation"],
        "scene_blueprint": beats["narrative_blueprint"],
        "voice_guidelines": voice_profile,
        "active_hazards": hazards["hazards"],
        "chapter_file_path": chapter_file,
        "chapter_stub_created": created
    }

def complete_chapter_generation(synopsis, gut_increment=1):
    """Marks current chapter complete, evaluates prose, awards mastery XP, appends to diary, propagates ephemeris, and advances rotation."""
    rot = read_rotation_tracker()
    active_book = rot["active_book_index"]
    active_chap = rot["active_chapter_number"]
    curr_gut = rot["current_gut"]

    char_info = get_character_info(active_book)
    title = char_info["title"] if char_info else f"Book {active_book}"
    hero = char_info["hero"] if char_info else "Hero"

    title_slug = slugify(title)
    chapter_file = os.path.join(BOOKS_LIB_DIR, f"Book_{active_book:02d}_{title_slug}", f"Book_{active_book:02d}_Chapter_{active_chap:02d}.md")
    
    prose_eval = None
    if os.path.exists(chapter_file):
        try:
            prose_eval = chapter_prose_evaluator.evaluate_file(chapter_file)
        except Exception:
            pass

    # Award character experience
    xp_award = None
    try:
        xp_award = character_mastery_engine.award_experience(
            active_book, 100, f"Completed Book {active_book} Chapter {active_chap}: {synopsis[:40]}",
            active_chap, curr_gut
        )
    except Exception:
        pass

    # 1. Append to diary
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    diary_entry = f"| GUT {curr_gut} | Book {active_book:02d} ({title}) | Ch {active_chap:02d} | {hero} | {synopsis.strip()} |\n"
    header_needed = not os.path.exists(DIARY_MD)
    with open(DIARY_MD, "a", encoding="utf-8") as f:
        if header_needed:
            f.write("# The Stellar Confluence Universe: Diary of Completed Chapters\n\n")
            f.write("| GUT | Book | Chapter | Character | Synopsis / Action Summary |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        f.write(diary_entry)

    # 2. Advance ephemeris across all characters
    target_gut = curr_gut + gut_increment
    propagate_ephemeris(curr_gut, target_gut, save=True)

    # 3. Advance rotation tracker
    next_rot = advance_rotation(gut_increment=gut_increment, save=True)

    return {
        "status": "completed",
        "completed_book": active_book,
        "completed_chapter": active_chap,
        "completed_gut": curr_gut,
        "synopsis": synopsis,
        "prose_evaluation": prose_eval,
        "mastery_xp_award": xp_award,
        "next_rotation_state": next_rot["new_state"],
        "diary_logged": True,
        "ephemeris_propagated": True
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified Chapter Authoring Engine")
    subparsers = parser.add_subparsers(dest="command")

    # Prepare command
    subparsers.add_parser("prepare", help="Prepare chapter stub and audit physical constraints")

    # Complete command
    comp_p = subparsers.add_parser("complete", help="Complete chapter, log diary, propagate ephemeris, and advance queue")
    comp_p.add_argument("--synopsis", required=True, help="1-2 sentence summary of completed chapter")
    comp_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance (default: 1)")

    args = parser.parse_args()

    if args.command == "prepare":
        res = prepare_next_chapter_stub()
        print(json.dumps(res, indent=2))
    elif args.command == "complete":
        res = complete_chapter_generation(args.synopsis, args.gut_delta)
        print(json.dumps(res, indent=2))
    else:
        res = prepare_next_chapter_stub()
        print(json.dumps(res, indent=2))

