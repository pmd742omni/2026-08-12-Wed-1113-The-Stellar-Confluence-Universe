#!/usr/bin/env python3
"""
Model Prompt Architect for The Stellar Confluence Universe
Extracts real-time 3D celestial ephemeris, wavefront resonance, power constraints,
transport kinetics, character mastery, and geopolitical tension to construct
optimal, high-context authoring prompts for LLMs and Subagents.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))

PROJECT_ROOT = find_project_root()
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

import chapter_engine
import narrative_beat_architect
import character_voice_profiler
import galactic_transport_engine
import galactic_sociology_politics_engine
import galactic_tension_tracker
import character_mastery_engine
import resonance_artifact_engine
import sensory_audio_director

def build_model_authoring_context(book_id: int, chapter_num: int = 1, gut: Optional[int] = None) -> Dict[str, Any]:
    """
    Constructs a comprehensive, high-fidelity world state context for LLM / subagent chapter authoring.
    """
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        raise ValueError(f"Book ID {book_id} not found in registry.")

    rot = chapter_engine.read_rotation_tracker()
    active_gut = gut if gut is not None else rot.get("current_gut", 100)

    hero = char_info["hero"]
    faction = char_info["faction"]
    title = char_info["title"]
    homeworld = char_info["world"]
    sector = char_info["sector"]

    # 1. Macro Arc & Narrative Phase
    arc_info = narrative_beat_architect.get_chapter_arc_info(chapter_num)
    ranks = ["Apprentice Scout", "Wayfarer Guide", "Master Artisan", "High Artificer"]
    active_rank = ranks[min(3, (chapter_num - 1) // 5)]

    # 2. Dynamic Location & Celestial Biome
    loc_progression = [
        {"type": "SURFACE", "world": homeworld, "desc": f"Planetary surface and primary workshop base on {homeworld}"},
        {"type": "ORBITAL", "world": f"{homeworld} Skyhook & Orbital Yards", "desc": f"High orbital staging platforms and docking elevators overlooking {homeworld}"},
        {"type": "DEEP_SPACE_TRANSIT", "world": f"Sector {sector} Deep-Space Relics", "desc": f"Ancient crystalline star-orreries and drifting keystone ruins in deep space"},
        {"type": "GATEWAY_SUBSPACE", "world": "Keystone Subspace Stargate", "desc": "Interstellar wormhole transit corridor with neutral spatial baseline"},
        {"type": "ORBITAL", "world": "The Grand Galactic Confluence Hub", "desc": "The colossal central meridian station unifying all 74 star sectors"}
    ]
    loc_idx = min(4, (chapter_num - 1) // 4)
    active_loc = loc_progression[loc_idx]

    # 3. Wavefront Angle & Physical Constraints
    facing_angle = round((active_gut * 15.0 + book_id * 7.5) % 180.0, 1)
    if facing_angle <= 30.0:
        res_state = "PEAK_FACING (Zenith)"
        power_desc = "SUPERCHARGED RADIANCE: Maximum energy beam output and solar power generation."
        constraint_desc = "OVERHEAT DANGER: Heat exchangers reach critical thermal runaway; thermal venting is mandatory to prevent system meltdown."
    elif facing_angle >= 150.0:
        res_state = "SHADOW_FACING (Nadir)"
        power_desc = "APEX SHADOW PHASE: Complete phase-shifting and rock/hull permeability."
        constraint_desc = "FROST EXHAUSTION & MECHANICAL DRAG: Zero beam generation; extreme cold and manual mechanical flywheels required."
    else:
        res_state = "TRANSIT_FACING (Twilight)"
        power_desc = "HARMONIC BASELINE: Stable, balanced radiant and shadow output."
        constraint_desc = "MOMENTUM CONSERVATION: Requires smooth gear synchronization and steady angular velocity management."

    # 4. Transport & Mobility
    vehicle_info = galactic_transport_engine.get_faction_vehicle_preference(faction)
    vehicle_name = vehicle_info.get("primary_vehicle", "Solar-Thermal Atmospheric Skimmer")
    vehicle_prof = galactic_transport_engine.get_vehicle_profile(vehicle_name) or {}

    # 5. Geopolitical Friction & Civic Traditions
    gov_model = galactic_sociology_politics_engine.get_governance_model(faction)
    soc_prof = galactic_sociology_politics_engine.get_sociological_profile(faction)

    # 6. Character Mastery & Voice
    voice_prof = next((v for k, v in character_voice_profiler.FACTION_VOCABULARY_BANKS.items() if k.lower() in faction.lower()), {
        "keywords": ["star", "beacon", "relay", "journey"],
        "tone": "Courageous, observant, collaborative",
        "example_idiom": "Follow the beacon through the dark."
    })

    # 7. Culinary & Hospitality Anchors
    HOSPITALITY_MAP = {
        "Sun-Forged": ("warm amber tea with golden honey", "fresh toasted cinnamon sun-cakes"),
        "Void-Bound": ("dark twilight berry infusion", "crisp phase-basalt wafers"),
        "Astrolabe": ("hot spiced chicory brew", "sweet brass-pressed gear-biscuits"),
        "Comet-Rider": ("steaming peppermint broth", "crystallized glacier-sugar flakes"),
        "Nebula-Weaver": ("glowing violet stardust cordial", "spun-sugar nebula crisps"),
        "Deep-Core": ("rich roasted chicory roast", "dense toasted oat-iron cakes"),
        "Plasma-Shepherd": ("simmering sun-pepper cider", "golden maize skillet bread"),
        "Chrono-Navigator": ("lavender chamomile tea", "honey-glazed thyme cookies"),
        "Bio-Alchemist": ("effervescent citrus bloom nectar", "candied luminescent berries"),
        "Crystal-Singer": ("pure distilled mineral spring water", "prismatic rock-sugar prisms"),
        "Tide-Warden": ("kelp-mint sea infusion", "crisp salted kelp wafers"),
        "Magnetar-Leaper": ("electrified ginger spark tea", "roasted spiced pulse-nuts"),
    }
    treat_pair = next((v for k, v in HOSPITALITY_MAP.items() if k.lower() in faction.lower()), ("warm spiced tea", "fresh hearth bread"))

    # 8. High-Stakes Mature Narrative Dilemma
    dilemma_descriptions = [
        f"A critical atmospheric thermal spike threatens to melt the skimmer's cooling manifold during a high-speed orbital vector trial.",
        f"A localized magnetic storm destabilizes the skyhook elevators, leaving an unanchored freight pod falling toward the planetary atmosphere.",
        f"Ancient resonance glyphs in a sunken star-orrery begin overloading, risking a sector-wide subspace navigation blackout.",
        f"An unexpected gravitational shear near a subspace keystone stargate threatens to tear traveling convoys from their transit corridors.",
        f"The incoming crest of the Great Confluence Wavefront arrives, demanding all 74 star sectors synchronize their beacon relays simultaneously."
    ]
    active_dilemma = dilemma_descriptions[loc_idx]

    return {
        "book_id": book_id,
        "chapter_num": chapter_num,
        "title": title,
        "hero": hero,
        "rank": active_rank,
        "faction": faction,
        "gut": active_gut,
        "sector": sector,
        "location": active_loc,
        "wavefront_facing_angle": facing_angle,
        "resonance_state": res_state,
        "power_capabilities": power_desc,
        "active_physical_constraint": constraint_desc,
        "vehicle_deployed": {
            "name": vehicle_name,
            "propulsion": vehicle_prof.get("propulsion_type", "Solar-Thermal Kinetic"),
            "cockpit": vehicle_prof.get("cockpit_experience", "Panoramic brass canopy with magnetic rudders")
        },
        "governance_model": gov_model.get("name", "Artificer Council"),
        "culinary_hospitality": {"drink": treat_pair[0], "food": treat_pair[1]},
        "macro_arc": arc_info,
        "dramatic_dilemma": active_dilemma,
        "voice_profile": voice_prof
    }

def generate_model_authoring_prompt(book_id: int, chapter_num: int = 1, gut: Optional[int] = None) -> str:
    """
    Renders a complete, markdown-formatted master prompt for LLMs or Subagents to author
    rich, organic, thematically mature chapter prose with Grade 4-6 vocabulary accessibility.
    """
    ctx = build_model_authoring_context(book_id, chapter_num, gut)
    
    prompt = f"""# MISSION BRIEF: Chapter Authoring for The Stellar Confluence Universe

You are the Master Storyteller for **The Stellar Confluence Universe**.
Author the complete, immersive narrative prose for **Book {ctx['book_id']:02d}: {ctx['title']} — Chapter {ctx['chapter_num']:02d}**.

---

## 1. NARRATIVE STANDARD & TONE GUIDELINES
- **Thematically Mature & High-Stakes Sci-Fi**: The story is **dramatic, intelligent, thrilling, and emotionally profound** (in the spirit of *Ender's Game*, *Dune*, *The Expanse*, *Battlestar Galactica*, and *Princess Mononoke*). Characters experience genuine physical peril, engineering crises, survival tension, moral choices, and deep interpersonal bonds. Do NOT make the storytelling childish, sanitized, or simplistic.
- **Clean & Accessible Vocabulary (Grade 4–6 Readability)**: While themes and concepts are mature, the **vocabulary must be crisp, sensory, and accessible** (Grade 4–6 reading level / plain English). Write short, active, punchy sentences (Average Sentence Length ~10–12 words). Avoid convoluted technobabble, academic obscurity, and purple prose so that readers can visualize complex astronomy effortlessly.
- **Organic Storytelling**: Write full, living narrative scenes (~800–1,200 words) with authentic dialogue, mentor-apprentice camaraderie, tactile physics, sensory comfort, and non-weaponized problem-solving.

---

## 2. REAL-TIME CELESTIAL & UNIVERSE STATE
- **Perspective Hero**: **{ctx['hero']}** (Rank: **{ctx['rank']}**)
- **Faction**: **{ctx['faction']}** (Governance: *{ctx['governance_model']}*)
- **Current Location**: **{ctx['location']['world']}** (`{ctx['location']['type']}` | Sector `{ctx['sector']}`)
- **Galactic Universal Time (GUT)**: `{ctx['gut']}`
- **Confluence Wavefront Orientation**: `{ctx['wavefront_facing_angle']}°` Facing Alignment ($\theta$)
- **Resonance State**: `{ctx['resonance_state']}`
  - *Power Capability*: {ctx['power_capabilities']}
  - *Physical Constraint / Hazard*: **{ctx['active_physical_constraint']}**
- **Primary Transport**: `{ctx['vehicle_deployed']['name']}` ({ctx['vehicle_deployed']['propulsion']})
- **Hospitality Treats**: {ctx['culinary_hospitality']['drink']} & {ctx['culinary_hospitality']['food']}

---

## 3. DRAMATIC PLOT BLUEPRINT & SCENE STRUCTURE (4 BEATS)
- **Act I (Opening & Everyday Life)**: Establish the setting at {ctx['location']['world']}, enjoying {ctx['culinary_hospitality']['drink']} and {ctx['culinary_hospitality']['food']} in the workshop/staging bay while preparing for the day's flight. Warm, natural dialogue with mentor or crew.
- **Act II (Departure & Environmental Shift)**: Launch the {ctx['vehicle_deployed']['name']}. Describe the physical sensations of flight, celestial gravity, and the panoramic view. The wavefront resonance shifts to {ctx['wavefront_facing_angle']}°.
- **Act III (The High-Stakes Crisis)**: **{ctx['dramatic_dilemma']}**. The active constraint ({ctx['active_physical_constraint']}) strikes! Alarms flash, instruments vibrate, and real survival pressure hits.
- **Act IV (Insight & Triumph)**: Working through patience, keen observation of physical laws, teamwork, and calm precision, {ctx['hero']} solves the crisis without violence. A brilliant beacon pulse is aligned, securing safe passage.

---

## 4. OUTPUT FORMAT
Output the complete chapter with standard frontmatter:

```markdown
# Book {ctx['book_id']:02d}: {ctx['title']}
## Chapter {ctx['chapter_num']:02d}: [Creative Chapter Title]

**Galactic Universal Time (GUT)**: {ctx['gut']}
**Perspective Character**: {ctx['hero']} ({ctx['rank']}) | **Faction**: {ctx['faction']}
**Current Location**: {ctx['location']['world']} (`{ctx['location']['type']}` | Sector `{ctx['sector']}`)
**Resonance State**: `{ctx['resonance_state']}` ({ctx['wavefront_facing_angle']}° Facing Alignment)
**Primary Transport**: `{ctx['vehicle_deployed']['name']}`
**Story Arc Phase**: `{ctx['macro_arc']['phase']}`

---

[Write complete 4-scene narrative prose here (~800–1,200 words)...]
```
"""
    return prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Prompt Architect for The Stellar Confluence Universe")
    parser.add_argument("--book-id", type=int, default=1, help="Book ID number (1-74)")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number (1-20)")
    parser.add_argument("--gut", type=int, help="Galactic Universal Time timestamp")
    parser.add_argument("--json", action="store_true", help="Output raw context dictionary as JSON")

    args = parser.parse_args()
    if args.json:
        ctx = build_model_authoring_context(args.book_id, args.chapter, args.gut)
        print(json.dumps(ctx, indent=2))
    else:
        prompt_str = generate_model_authoring_prompt(args.book_id, args.chapter, args.gut)
        print(prompt_str)
