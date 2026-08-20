#!/usr/bin/env python3
"""
Centralized Core Foundation for The Stellar Confluence Universe Agent Engine
Provides unified project paths, state IO, ANSI formatting, and terminal dashboards.
"""

import os
import sys
import json
import re
import math
from typing import Dict, Any, List, Optional

def find_project_root() -> str:
    """Dynamically finds the project root directory by searching for 00_System_State, .git, or walking up."""
    for idx, arg in enumerate(sys.argv):
        if arg == "--project-root" and idx + 1 < len(sys.argv):
            return os.path.abspath(sys.argv[idx + 1])

    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, "00_System_State")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent

    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(this_dir))

PROJECT_ROOT = find_project_root()
AGENTS_DIR = os.path.join(PROJECT_ROOT, ".agents")
SKILLS_DIR = os.path.join(AGENTS_DIR, "skills")
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
BOOKS_LIB_DIR = os.path.join(PROJECT_ROOT, "01_Books_Library")
PROGRESS_DIR = os.path.join(PROJECT_ROOT, "progress tracking")

# Standard State File Paths
ROTATION_TRACKER_MD = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
CHARACTER_REGISTRY_MD = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
COSMIC_CLOCKWORK_MD = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")
COSMIC_EVENTS_JSON = os.path.join(SYSTEM_STATE_DIR, "cosmic_events.json")
CHARACTER_ARCS_JSON = os.path.join(SYSTEM_STATE_DIR, "character_arcs.json")
CHARACTER_MASTERY_JSON = os.path.join(SYSTEM_STATE_DIR, "character_mastery.json")
GALACTIC_TENSION_JSON = os.path.join(SYSTEM_STATE_DIR, "galactic_tension.json")
GALACTIC_ECONOMY_JSON = os.path.join(SYSTEM_STATE_DIR, "galactic_economy.json")
TRANSIT_MISSIONS_JSON = os.path.join(SYSTEM_STATE_DIR, "transit_missions.json")
ARTIFACT_LEDGER_JSON = os.path.join(SYSTEM_STATE_DIR, "artifact_ledger.json")
DASHBOARD_HTML = os.path.join(SYSTEM_STATE_DIR, "universe_dashboard.html")

# ANSI Color Codes for Rich Terminal Presentation
class TermColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Foreground
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

def colorize(text: str, *colors: str) -> str:
    """Applies ANSI colors to text if supported, otherwise returns plain text."""
    if os.environ.get("NO_COLOR"):
        return text
    return f"{''.join(colors)}{text}{TermColor.RESET}"

def slugify(text: str) -> str:
    """Converts a title or string to a standard file-system slug."""
    clean = re.sub(r"[^\w\s-]", "", text).strip()
    return re.sub(r"[-\s]+", "_", clean)

def ensure_sys_path():
    """Injects all skill script directories into sys.path."""
    skill_names = [
        "document-now",
        "confluence-chapter-authoring",
        "universe-state-manager",
        "prompt-response-flow",
        "world-engine-audit"
    ]
    for s in skill_names:
        p = os.path.join(SKILLS_DIR, s, "scripts")
        if p not in sys.path:
            sys.path.insert(0, p)
    if AGENTS_DIR not in sys.path:
        sys.path.insert(0, AGENTS_DIR)
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

ensure_sys_path()

# Safe JSON IO
def read_json_safe(file_path: str, default: Any = None) -> Any:
    """Safely reads and parses a JSON file, returning default on failure."""
    if not os.path.exists(file_path):
        return default if default is not None else {}
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def write_json_safe(file_path: str, data: Any, indent: int = 2) -> bool:
    """Safely writes data to a JSON file, creating parent directories if needed."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception:
        return False

# State Loaders
def get_rotation_state() -> Dict[str, Any]:
    """Reads current rotation tracker state."""
    state = {"active_book_index": 1, "active_chapter_number": 1, "current_gut": 100, "next_book_index": 2, "next_chapter_number": 1}
    if not os.path.exists(ROTATION_TRACKER_MD):
        return state
    with open(ROTATION_TRACKER_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    m_book = re.search(r"Active Book #:\s*(\d+)", content)
    m_chap = re.search(r"Active Chapter #:\s*(\d+)", content)
    m_gut = re.search(r"Current GUT:\s*(\d+)", content)
    m_next_b = re.search(r"Next Book In Queue:\s*Book\s+(\d+)", content)
    m_next_c = re.search(r"Next Chapter In Queue:\s*Chapter\s+(\d+)", content)
    
    if m_book: state["active_book_index"] = int(m_book.group(1))
    if m_chap: state["active_chapter_number"] = int(m_chap.group(1))
    if m_gut: state["current_gut"] = int(m_gut.group(1))
    if m_next_b: state["next_book_index"] = int(m_next_b.group(1))
    if m_next_c: state["next_chapter_number"] = int(m_next_c.group(1))
    return state

# Memory Cache for Fast State Lookups
_STATE_CACHE: Dict[str, Any] = {}

def get_all_characters(reload: bool = False) -> List[Dict[str, Any]]:
    """Retrieves all 74 characters from character_registry.md with caching."""
    if not reload and "all_characters" in _STATE_CACHE:
        return _STATE_CACHE["all_characters"]
    
    if not os.path.exists(CHARACTER_REGISTRY_MD):
        return []
    with open(CHARACTER_REGISTRY_MD, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    characters = []
    pattern = r"\|\s*\*\*Book\s+(\d+)\*\*\s*\|\s*([^\|]+)\s*\|\s*`?([^\|`]+)`?\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*`?([^\|`]+)`?\s*\|\s*`?([^\|`]+)`?\s*\|"
    for match in re.finditer(pattern, content):
        characters.append({
            "book_id": int(match.group(1)),
            "title": match.group(2).strip(),
            "hero": match.group(3).strip(),
            "faction": match.group(4).strip(),
            "world": match.group(5).strip(),
            "loc_type": match.group(6).strip().upper(),
            "sector": match.group(7).strip()
        })
    _STATE_CACHE["all_characters"] = characters
    return characters

def get_character_info(book_index: int) -> Optional[Dict[str, Any]]:
    """Retrieves character info from character_registry.md."""
    chars = get_all_characters()
    for c in chars:
        if c["book_id"] == book_index:
            return c
    return None

def get_clockwork_info(book_index: int) -> Optional[Dict[str, Any]]:
    """Retrieves clockwork facing and resonance info from cosmic_clockwork.md."""
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

def generate_book_dossier(book_id: int) -> Dict[str, Any]:
    """Generates a complete 360-degree dossier for any book storyline (1-74)."""
    char = get_character_info(book_id) or {
        "book_id": book_id,
        "title": f"Storyline {book_id:02d}",
        "hero": f"Hero {book_id:02d}",
        "faction": "Independent Star-Farer",
        "world": "Deep Space Station",
        "loc_type": "SURFACE",
        "sector": "[0, 0, 0]"
    }
    clock = get_clockwork_info(book_id) or {
        "gut": 100,
        "facing_angle": 0.0,
        "resonance_state": "PEAK_FACING",
        "power_limit_desc": "Standard output"
    }

    # Character Arc data
    arcs_raw = read_json_safe(CHARACTER_ARCS_JSON, {})
    arc_data = arcs_raw.get(f"Book_{book_id:02d}", arcs_raw.get(str(book_id), {}))
    inventory = arc_data.get("inventory", [])
    wounds = arc_data.get("wounds_or_conditions", arc_data.get("conditions", []))
    milestones = arc_data.get("milestones", [])

    # Mastery data
    mastery_raw = read_json_safe(CHARACTER_MASTERY_JSON, {})
    m_data = mastery_raw.get(f"Book_{book_id:02d}", mastery_raw.get(str(book_id), {}))
    mastery_rank = m_data.get("rank", "Novice")
    mastery_xp = m_data.get("xp", 0)
    mastery_level = m_data.get("level", 1)
    skills = m_data.get("unlocked_skills", [])

    # Active Transits
    transit_raw = read_json_safe(TRANSIT_MISSIONS_JSON, {})
    transit_list = list(transit_raw.values()) if isinstance(transit_raw, dict) else (transit_raw if isinstance(transit_raw, list) else [])
    active_transit = next((t for t in transit_list if isinstance(t, dict) and t.get("book_id") == book_id and t.get("status") == "IN_TRANSIT"), None)

    # Relics
    art_raw = read_json_safe(ARTIFACT_LEDGER_JSON, {})
    art_list = art_raw.get("master_artifacts", list(art_raw.values()) if isinstance(art_raw, dict) else (art_raw if isinstance(art_raw, list) else []))
    held_relics = [
        a for a in art_list if isinstance(a, dict) and (
            a.get("current_custody") == f"Book {book_id:02d}" or
            a.get("current_bearer_book") == book_id
        )
    ]

    # Chapter Manuscript status
    book_slug = f"Book_{book_id:02d}_{slugify(char['title'])}"
    book_dir = os.path.join(BOOKS_LIB_DIR, book_slug)
    chapters_written = 0
    if os.path.exists(book_dir):
        chapters_written = len([f for f in os.listdir(book_dir) if f.startswith("Book_") and f.endswith(".md")])

    return {
        "book_id": book_id,
        "title": char["title"],
        "hero": char["hero"],
        "faction": char["faction"],
        "homeworld": char["world"],
        "location_type": char["loc_type"],
        "sector_coords": char["sector"],
        "facing_angle": clock.get("facing_angle", 0.0),
        "resonance_state": clock.get("resonance_state", "PEAK_FACING"),
        "power_dynamics": clock.get("power_limit_desc", "Standard"),
        "mastery": {
            "rank": mastery_rank,
            "level": mastery_level,
            "xp": mastery_xp,
            "unlocked_skills": skills
        },
        "arc": {
            "inventory": inventory,
            "wounds_or_conditions": wounds,
            "milestones": milestones
        },
        "active_transit": active_transit,
        "relics": held_relics,
        "chapters_written_count": chapters_written
    }

def format_book_dossier_terminal(book_id: int) -> str:
    """Renders a styled ASCII dossier card for a storyline."""
    dossier = generate_book_dossier(book_id)
    w = 78
    sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
    sub_sep = colorize("-" * w, TermColor.DIM)

    lines = [
        "",
        sep,
        colorize(f"   *  STORYLINE DOSSIER: BOOK {dossier['book_id']:02d}  *   {dossier['title'].upper()}", TermColor.BOLD, TermColor.BRIGHT_YELLOW),
        sep,
        f" {colorize('Protagonist:', TermColor.BOLD)} {colorize(dossier['hero'], TermColor.BRIGHT_WHITE)}   |   {colorize('Faction:', TermColor.BOLD)} {dossier['faction']}",
        f" {colorize('Homeworld:', TermColor.BOLD)} {dossier['homeworld']} ({dossier['location_type']} | Sector {dossier['sector_coords']})",
        f" {colorize('Wavefront State:', TermColor.BOLD)} {colorize(dossier['resonance_state'], TermColor.BRIGHT_MAGENTA)} ({dossier['facing_angle']:.1f}° Facing)",
        f" {colorize('Power Dynamics:', TermColor.DIM)} {dossier['power_dynamics']}",
        sub_sep,
        f" {colorize('CHARACTER PROGRESSION & MASTERY:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}",
        f"   - {colorize('Mastery Rank:', TermColor.DIM)} {colorize(dossier['mastery']['rank'], TermColor.BRIGHT_GREEN)} (Lvl {dossier['mastery']['level']} | {dossier['mastery']['xp']} XP)",
        f"   - {colorize('Unlocked Skills:', TermColor.DIM)} {', '.join(dossier['mastery']['unlocked_skills']) if dossier['mastery']['unlocked_skills'] else 'None unlocked'}",
        f"   - {colorize('Inventory Items:', TermColor.DIM)} {len(dossier['arc']['inventory'])} items ({', '.join([i.get('name', i.get('item', str(i))) if isinstance(i, dict) else str(i) for i in dossier['arc']['inventory'][:3]]) if dossier['arc']['inventory'] else 'Standard Kit'})",
        f"   - {colorize('Active Wounds/Conditions:', TermColor.DIM)} {', '.join(dossier['arc']['wounds_or_conditions']) if dossier['arc']['wounds_or_conditions'] else 'In peak physical health'}",
        sub_sep,
        f" {colorize('SPACEFLIGHT & RELIC STATUS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}"
    ]

    if dossier["active_transit"]:
        tr = dossier["active_transit"]
        lines.append(f"   - {colorize('Starship Flight:', TermColor.DIM)} {colorize('IN TRANSIT', TermColor.BRIGHT_YELLOW)} from {tr.get('origin_coords')} to {tr.get('dest_coords')} (ETA: GUT {tr.get('eta_gut')})")
    else:
        lines.append(f"   - {colorize('Starship Flight:', TermColor.DIM)} Stationed at {dossier['homeworld']}")

    if dossier["relics"]:
        for r in dossier["relics"]:
            lines.append(f"   - {colorize('Held Master Relic:', TermColor.DIM)} {colorize(r.get('name'), TermColor.BRIGHT_YELLOW)} ({r.get('relic_type')})")
    else:
        lines.append(f"   - {colorize('Held Master Relic:', TermColor.DIM)} No legendary relic registered in active custody")

    lines.extend([
        f"   - {colorize('Manuscript Chapters Written:', TermColor.DIM)} {dossier['chapters_written_count']} chapter(s)",
        sep,
        ""
    ])
    return "\n".join(lines)

def search_universe(query: str) -> Dict[str, Any]:
    """Performs a global search across all 74 storylines, characters, factions, worlds, relics, items, creatures, and biomes."""
    q = query.lower().strip()
    chars = get_all_characters()
    
    matched_books = []
    for c in chars:
        if (q in str(c["book_id"]) or 
            q in c["title"].lower() or 
            q in c["hero"].lower() or 
            q in c["faction"].lower() or 
            q in c["world"].lower() or 
            q in c["sector"].lower()):
            matched_books.append(c)

    # Search Relics
    art_raw = read_json_safe(ARTIFACT_LEDGER_JSON, {})
    art_list = art_raw.get("master_artifacts", list(art_raw.values()) if isinstance(art_raw, dict) else (art_raw if isinstance(art_raw, list) else []))
    matched_relics = [
        r for r in art_list
        if isinstance(r, dict) and (
            q in r.get("name", "").lower() or
            q in r.get("relic_type", "").lower() or
            q in r.get("current_custody", "").lower() or
            q in r.get("current_bearer_hero", "").lower() or
            q in r.get("origin_world", "").lower() or
            q in r.get("energy_type", "").lower() or
            q in r.get("power_effect", "").lower()
        )
    ]

    # Search Active Transits
    transit_raw = read_json_safe(TRANSIT_MISSIONS_JSON, {})
    transit_list = list(transit_raw.values()) if isinstance(transit_raw, dict) else (transit_raw if isinstance(transit_raw, list) else [])
    matched_transits = [
        t for t in transit_list
        if isinstance(t, dict) and (q in str(t.get("book_id", "")) or q in str(t.get("waypoint_name", "")).lower() or q in str(t.get("origin_coords", "")) or q in str(t.get("dest_coords", "")))
    ]

    # Search Character Inventories
    arcs_raw = read_json_safe(CHARACTER_ARCS_JSON, {})
    matched_items = []
    for b_key, b_arc in arcs_raw.items():
        if isinstance(b_arc, dict):
            for itm in b_arc.get("inventory", []):
                itm_name = itm.get("name", itm.get("item", str(itm))) if isinstance(itm, dict) else str(itm)
                if q in itm_name.lower():
                    matched_items.append({"book": b_key, "item": itm})

    # Search Xenobiology Creatures & Biomes
    matched_creatures = []
    try:
        import galactic_scale_generator
        for c in galactic_scale_generator.ALIEN_CREATURE_CATALOG:
            if (q in c["species_name"].lower() or 
                q in c["biome_niche"].lower() or 
                q in c["sensory_capability"].lower() or
                q in c["temperament"].lower()):
                matched_creatures.append(c)
    except Exception:
        pass

    # Search Galactic Transport Vehicles
    matched_vehicles = []
    try:
        import galactic_transport_engine
        for v in galactic_transport_engine.get_all_vehicles():
            if (q in v.get("vehicle_id", "").lower() or
                q in v.get("name", "").lower() or
                q in v.get("propulsion_type", "").lower() or
                q in v.get("cockpit_vibe", "").lower()):
                matched_vehicles.append(v)
    except Exception:
        pass

    # Search Governance Models & Politics
    matched_governance = []
    try:
        import galactic_sociology_politics_engine
        for g in galactic_sociology_politics_engine.GOVERNANCE_ARCHETYPES:
            if (q in g.get("model_id", "").lower() or
                q in g.get("name", "").lower() or
                q in g.get("legal_charter", "").lower() or
                q in g.get("leadership_structure", "").lower()):
                matched_governance.append(g)
    except Exception:
        pass

    # Search Commodities
    matched_commodities = []
    try:
        import galactic_trade_economy
        eco_m = galactic_trade_economy.get_market_prices().get("market", {})
        for comm_name, comm_data in eco_m.items():
            if q in comm_name.lower() or q in comm_data.get("description", "").lower() or q in comm_data.get("category", "").lower():
                matched_commodities.append({"name": comm_name, **comm_data})
    except Exception:
        pass

    # Search Cosmic Anomalies
    matched_anomalies = []
    try:
        import galactic_scale_generator
        for a in getattr(galactic_scale_generator, "COSMIC_ANOMALIES_CATALOG", []):
            if q in a.get("name", "").lower() or q in a.get("anomaly_id", "").lower() or q in a.get("scientific_basis", "").lower():
                matched_anomalies.append(a)
    except Exception:
        pass

    # Search Culinary Traditions
    matched_culinary = []
    try:
        import galactic_sociology_politics_engine
        for c in galactic_sociology_politics_engine.SOCIOLOGICAL_SYSTEMS.get("culinary_traditions", []):
            if q in c.get("name", "").lower() or q in c.get("description", "").lower():
                matched_culinary.append(c)
    except Exception:
        pass

    return {
        "query": query,
        "total_results": len(matched_books) + len(matched_relics) + len(matched_transits) + len(matched_items) + len(matched_creatures) + len(matched_vehicles) + len(matched_governance) + len(matched_commodities) + len(matched_anomalies) + len(matched_culinary),
        "matched_storylines": matched_books,
        "matched_relics": matched_relics,
        "matched_transits": matched_transits,
        "matched_inventory_items": matched_items,
        "matched_creatures": matched_creatures,
        "matched_vehicles": matched_vehicles,
        "matched_governance": matched_governance,
        "matched_commodities": matched_commodities,
        "matched_anomalies": matched_anomalies,
        "matched_culinary": matched_culinary
    }

# Ensure standard output uses UTF-8 if available
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def generate_terminal_overview() -> str:
    """Generates a rich, styled ASCII galactic status board for terminal display."""
    rot = get_rotation_state()
    active_b = rot["active_book_index"]
    active_c = rot["active_chapter_number"]
    curr_gut = rot["current_gut"]
    next_b = rot["next_book_index"]
    next_c = rot["next_chapter_number"]

    char = get_character_info(active_b) or {"title": "Unknown", "hero": "Unknown", "faction": "Unknown", "world": "Unknown", "loc_type": "SURFACE", "sector": "[0, 0, 0]"}
    clock = get_clockwork_info(active_b) or {"facing_angle": 0.0, "resonance_state": "PEAK_FACING", "power_limit_desc": "Baseline"}

    # Load active hazards
    events_raw = read_json_safe(COSMIC_EVENTS_JSON, [])
    events_list = events_raw if isinstance(events_raw, list) else events_raw.get("events", [])
    active_hazards = [
        e for e in events_list
        if isinstance(e, dict) and e.get("active", True) and e.get("start_gut", 0) <= curr_gut <= (e.get("expiry_gut") or e.get("end_gut") or 99999)
    ]

    # Load active transit missions
    transit_raw = read_json_safe(TRANSIT_MISSIONS_JSON, {})
    transit_list = list(transit_raw.values()) if isinstance(transit_raw, dict) else (transit_raw if isinstance(transit_raw, list) else [])
    active_transits = [m for m in transit_list if isinstance(m, dict) and m.get("status") == "IN_TRANSIT"]

    # Load top tensions
    tension_raw = read_json_safe(GALACTIC_TENSION_JSON, {})
    tension_list = list(tension_raw.values()) if isinstance(tension_raw, dict) else (tension_raw.get("faction_pairs", []) if isinstance(tension_raw, dict) else tension_raw)
    tensions = sorted([t for t in tension_list if isinstance(t, dict)], key=lambda x: x.get("tension_index", 0), reverse=True)[:3]

    # Load recent diary entries
    diary_entries = []
    if os.path.exists(DIARY_MD):
        with open(DIARY_MD, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.startswith("| GUT")]
            diary_entries = lines[-3:]

    # Build ASCII Frame
    w = 78
    sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
    sub_sep = colorize("-" * w, TermColor.DIM)
    
    lines = [
        "",
        sep,
        colorize("   *  THE STELLAR CONFLUENCE UNIVERSE  *   GALACTIC STATUS BOARD", TermColor.BOLD, TermColor.BRIGHT_YELLOW),
        sep,
        f" {colorize('Galactic Universal Time (GUT):', TermColor.BOLD)} {colorize(str(curr_gut), TermColor.BRIGHT_GREEN)}   |   {colorize('Active Rotation:', TermColor.BOLD)} {colorize(f'Book {active_b:02d}, Ch {active_c:02d}', TermColor.BRIGHT_CYAN)}   |   {colorize('Next Queue:', TermColor.BOLD)} Book {next_b:02d}, Ch {next_c:02d}",
        sub_sep,
        f" {colorize('ACTIVE STORYLINE:', TermColor.BOLD, TermColor.BRIGHT_WHITE)} Book {active_b:02d}: {colorize(char['title'], TermColor.BRIGHT_YELLOW)}",
        f"   - {colorize('Protagonist:', TermColor.DIM)} {colorize(char['hero'], TermColor.BRIGHT_WHITE)}   |   {colorize('Faction:', TermColor.DIM)} {char['faction']}",
        f"   - {colorize('Current Location:', TermColor.DIM)} {char['world']} ({char['loc_type']} | Sector {char['sector']})",
        f"   - {colorize('Wavefront Resonance:', TermColor.DIM)} {colorize(clock['resonance_state'], TermColor.BRIGHT_MAGENTA)} ({clock['facing_angle']:.1f} deg Facing Alignment)",
        f"   - {colorize('Power Dynamics:', TermColor.DIM)} {clock['power_limit_desc']}",
        sub_sep,
        f" {colorize('GALACTIC SITUATION & CROSS-BOOK RIPPLES:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}",
        f"   - {colorize('Active Environmental Hazards:', TermColor.DIM)} {len(active_hazards)} registered"
    ]

    for h in active_hazards[:2]:
        lines.append(f"     |-- [{h.get('event_type')}] Sector {h.get('origin_sector')} (Radius: {h.get('blast_radius')}) -> {h.get('description')[:45]}")

    lines.append(f"   - {colorize('Starship Transit Missions:', TermColor.DIM)} {len(active_transits)} en route")
    for t in active_transits[:2]:
        lines.append(f"     |-- Book {t.get('book_id'):02d}: {t.get('origin_coords')} -> {t.get('dest_coords')} (ETA: GUT {t.get('eta_gut')})")

    lines.append(f"   - {colorize('Highest Geopolitical Friction:', TermColor.DIM)}")
    for tp in tensions[:2]:
        t_idx = tp.get("tension_index", 0)
        t_state = tp.get("diplomatic_state") or tp.get("state", "UNKNOWN")
        t_color = TermColor.BRIGHT_RED if t_idx >= 80 else TermColor.BRIGHT_YELLOW
        t_label = f"{t_idx}/100 [{t_state}]"
        lines.append(f"     |-- {tp.get('faction_a')} vs {tp.get('faction_b')}: {colorize(t_label, t_color)}")

    if diary_entries:
        lines.append(sub_sep)
        lines.append(f" {colorize('RECENT CHRONICLE ENTRIES (DIARY):', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
        for d in diary_entries:
            parts = [p.strip() for p in d.split("|")[1:-1]]
            if len(parts) >= 5:
                lines.append(f"   - {colorize(parts[0], TermColor.BRIGHT_GREEN)} | {parts[1]} {parts[2]} ({parts[3]}): {parts[4][:40]}...")

    lines.extend([
        sep,
        f" {colorize('Hub Quick Commands:', TermColor.DIM)} 'hub.py author prepare' | 'hub.py cosmos explore' | 'hub.py doctor'",
        sep,
        ""
    ])
    return "\n".join(lines)
