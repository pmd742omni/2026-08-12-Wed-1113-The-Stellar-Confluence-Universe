#!/usr/bin/env python3
"""
Portable Version Registry & Ndebele Lexicon Engine for Document Now Skill
Scans progress tracking logs, auto-bootstraps missing progress folders and registry files,
maintains version_registry.json & Version_Registry.md, validates codename uniqueness,
provides 100+ categorized Ndebele vocabulary suggestions, and computes next version numbers.
"""

import os
import sys
import json
import re
import glob
import subprocess

def find_project_root():
    """Dynamically finds the project root directory by searching for .git, progress tracking, or walking up."""
    for idx, arg in enumerate(sys.argv):
        if arg == "--project-root" and idx + 1 < len(sys.argv):
            return os.path.abspath(sys.argv[idx + 1])

    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, ".git")) or os.path.exists(os.path.join(curr, "progress tracking")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
        
    return cwd

PROJECT_ROOT = find_project_root()
PROGRESS_DIR = os.path.join(PROJECT_ROOT, "progress tracking")
REGISTRY_JSON = os.path.join(PROGRESS_DIR, "version_registry.json")
REGISTRY_MD = os.path.join(PROGRESS_DIR, "Version_Registry.md")

# 100+ Curated Ndebele Vocabulary Catalog Organized Across 8 Thematic Domains
NDEBELE_DICTIONARY = [
    # 1. Foundation & Architecture (Isisekelo)
    {"codename": "Isisekelo", "meaning": "Foundation / Base", "category": "Foundation"},
    {"codename": "Inqubo", "meaning": "Process / Methodology", "category": "Foundation"},
    {"codename": "Umnyango", "meaning": "Gateway / Entrance", "category": "Foundation"},
    {"codename": "Umklamo", "meaning": "Design / Blueprint", "category": "Foundation"},
    {"codename": "Ingatsha", "meaning": "Branch / Module", "category": "Foundation"},
    {"codename": "Izidingo", "meaning": "Requirements / Needs", "category": "Foundation"},
    {"codename": "Ukuhlela", "meaning": "Planning / Architecture", "category": "Foundation"},
    {"codename": "Ukwakha", "meaning": "Building / Construction", "category": "Foundation"},
    {"codename": "Isiqalo", "meaning": "Beginning / Origin", "category": "Foundation"},
    {"codename": "Ubunjalo", "meaning": "Nature / Core Essence", "category": "Foundation"},
    {"codename": "Insika", "meaning": "Pillar / Main Support", "category": "Foundation"},
    {"codename": "Umthombo", "meaning": "Source / Origin Spring", "category": "Foundation"},
    {"codename": "Isibopho", "meaning": "Commitment / Covenant", "category": "Foundation"},

    # 2. Cosmos, Stars & Elements (Izinkanyezi / Izulu)
    {"codename": "Inkanyezi", "meaning": "Star / Shining Light", "category": "Cosmos"},
    {"codename": "Umthala", "meaning": "Milky Way / Galaxy", "category": "Cosmos"},
    {"codename": "Inyanga", "meaning": "Moon / Celestial Cycle", "category": "Cosmos"},
    {"codename": "Ilanga", "meaning": "Sun / Radiant Dawn", "category": "Cosmos"},
    {"codename": "Izulu", "meaning": "Sky / Heavens / Universe", "category": "Cosmos"},
    {"codename": "Umkhathi", "meaning": "Outer Space / Atmosphere", "category": "Cosmos"},
    {"codename": "Umnyama", "meaning": "Shadow / Deep Night", "category": "Cosmos"},
    {"codename": "Ukukhanya", "meaning": "Illumination / Clarity / Light", "category": "Cosmos"},
    {"codename": "Ukusa", "meaning": "Dawn / Daybreak", "category": "Cosmos"},
    {"codename": "Ukutshona", "meaning": "Sunset / Twilight", "category": "Cosmos"},
    {"codename": "Umoya", "meaning": "Wind / Solar Wave / Spirit", "category": "Cosmos"},
    {"codename": "Umbani", "meaning": "Lightning / Radiant Discharge", "category": "Cosmos"},
    {"codename": "Umlotha", "meaning": "Ash / Cosmic Dust", "category": "Cosmos"},

    # 3. Energy, Power & Motion (Amandla / Isivinini)
    {"codename": "Amandla", "meaning": "Power / Strength / Energy", "category": "Energy"},
    {"codename": "Isivinini", "meaning": "Velocity / High Speed", "category": "Energy"},
    {"codename": "Ukutshisa", "meaning": "Heat / Thermal Energy", "category": "Energy"},
    {"codename": "Ukubanda", "meaning": "Cold / Cryogenic State", "category": "Energy"},
    {"codename": "Isivunguvungu", "meaning": "Whirlwind / Plasma Tempest", "category": "Energy"},
    {"codename": "Umdlandla", "meaning": "Enthusiasm / Vitality Surge", "category": "Energy"},
    {"codename": "Ukuvutha", "meaning": "Blaze / Super-charged Flare", "category": "Energy"},
    {"codename": "Ukuzola", "meaning": "Calm / Harmonic Baseline", "category": "Energy"},
    {"codename": "Ukuthula", "meaning": "Peace / Silent Stasis", "category": "Energy"},
    {"codename": "Umfutho", "meaning": "Pressure / Thrust Vector", "category": "Energy"},
    {"codename": "Isidlakela", "meaning": "Mighty Impact / Kinetic Force", "category": "Energy"},
    {"codename": "Ukugxuma", "meaning": "Leap / Warp Jump", "category": "Energy"},

    # 4. Engineering, Craft & Precision (Izixhobo / Ubungcweti)
    {"codename": "Izixhobo", "meaning": "Tools / Hardware Instruments", "category": "Engineering"},
    {"codename": "Ubungcweti", "meaning": "Mastery / Craftsmanship", "category": "Engineering"},
    {"codename": "Ukonga", "meaning": "Optimization / Conservation", "category": "Engineering"},
    {"codename": "Ukunciphisa", "meaning": "Reduction / Simplification", "category": "Engineering"},
    {"codename": "Umdwebo", "meaning": "Diagram / Schematic Draft", "category": "Engineering"},
    {"codename": "Umfanekiso", "meaning": "Visualization / Optical Model", "category": "Engineering"},
    {"codename": "Ukusebenza", "meaning": "Implementation / Functionality", "category": "Engineering"},
    {"codename": "Ukusungula", "meaning": "Invention / Innovation", "category": "Engineering"},
    {"codename": "Ukulungisa", "meaning": "Refinement / Repair / Tuning", "category": "Engineering"},
    {"codename": "Isigayo", "meaning": "Gear Wheel / Mill Engine", "category": "Engineering"},
    {"codename": "Insimbi", "meaning": "Iron / Metal / Metallurgy", "category": "Engineering"},
    {"codename": "Igeja", "meaning": "Plow / Mining Drill Instrument", "category": "Engineering"},
    {"codename": "Isilinganiso", "meaning": "Measurement / Chronometer Scale", "category": "Engineering"},

    # 5. Movement, Exploration & Journey (Uhambo / Ukudabula)
    {"codename": "Uhambo", "meaning": "Journey / Interstellar Voyage", "category": "Movement"},
    {"codename": "Ukuhamba", "meaning": "Traveling / In-Transit Movement", "category": "Movement"},
    {"codename": "Ukudabula", "meaning": "Traversing / Navigating Deep Space", "category": "Movement"},
    {"codename": "Indlela", "meaning": "Path / Route / Celestial Trajectory", "category": "Movement"},
    {"codename": "Isikepe", "meaning": "Ship / Star Vessel", "category": "Movement"},
    {"codename": "Isiphephetha", "meaning": "Sail / Solar Thruster", "category": "Movement"},
    {"codename": "Ukufika", "meaning": "Arrival / Reaching Orbital Destination", "category": "Movement"},
    {"codename": "Ukundiza", "meaning": "Flight / Orbiting", "category": "Movement"},
    {"codename": "Ukujika", "meaning": "Turning / Vector Reorientation", "category": "Movement"},
    {"codename": "Inqola", "meaning": "Chariot / Spacecraft Skiff", "category": "Movement"},
    {"codename": "Umgwaqo", "meaning": "Highway / Subspace Conduit", "category": "Movement"},
    {"codename": "Ukugijima", "meaning": "Running / Rapid Acceleration", "category": "Movement"},

    # 6. Guard, Shield & Safety (Isihlangu / Ukuphepha)
    {"codename": "Qaphela", "meaning": "Caution / Vigilance", "category": "Security"},
    {"codename": "Ukuphepha", "meaning": "Safety / Security Protection", "category": "Security"},
    {"codename": "Isihlangu", "meaning": "Shield / Deflector Barrier", "category": "Security"},
    {"codename": "Umlindi", "meaning": "Sentinel / Watchman / Warden", "category": "Security"},
    {"codename": "Inqaba", "meaning": "Fortress / Orbital Stronghold", "category": "Security"},
    {"codename": "Ukulinda", "meaning": "Guarding / Station Keeping", "category": "Security"},
    {"codename": "Ukulonda", "meaning": "Preserving / Safe Custody", "category": "Security"},
    {"codename": "Ukucinisa", "meaning": "Strengthening / Robustness", "category": "Security"},
    {"codename": "Ukuvikela", "meaning": "Defense / Armor Ward", "category": "Security"},
    {"codename": "Inkemba", "meaning": "Sword / Radiant Blade", "category": "Security"},
    {"codename": "Umkhonto", "meaning": "Spear / Projectile Javelin", "category": "Security"},
    {"codename": "Ukuma", "meaning": "Standing Firm / Resilience", "category": "Security"},

    # 7. Harmony, Network & Integration (Ukuhlangana / Ukuxhumana)
    {"codename": "Ukuxhumana", "meaning": "Networking / Connectivity / Comms", "category": "Harmony"},
    {"codename": "Ukuhlanganisa", "meaning": "Integration / Harmonization / Confluence", "category": "Harmony"},
    {"codename": "Ubunye", "meaning": "Unity / Galactic Accord", "category": "Harmony"},
    {"codename": "Umphakathi", "meaning": "Community / Faction Council", "category": "Harmony"},
    {"codename": "Isivumelwano", "meaning": "Treaty / Compact / Pact", "category": "Harmony"},
    {"codename": "Ukudlulisa", "meaning": "Transmission / Relay Synchronization", "category": "Harmony"},
    {"codename": "Ukuthembana", "meaning": "Mutual Trust / Alliance", "category": "Harmony"},
    {"codename": "Uzwano", "meaning": "Mutual Understanding / Resonance", "category": "Harmony"},
    {"codename": "Ubudlelwano", "meaning": "Partnership / Fellowship", "category": "Harmony"},
    {"codename": "Ukubambisana", "meaning": "Cooperation / Teamwork", "category": "Harmony"},
    {"codename": "Ukuvumelana", "meaning": "Agreement / Accord", "category": "Harmony"},

    # 8. Wisdom, Knowledge & Lore (Ukwazi / Isiphetho)
    {"codename": "Ukwazi", "meaning": "Knowledge / Intel / Awareness", "category": "Wisdom"},
    {"codename": "Ukuhlakanipha", "meaning": "Wisdom / Insight / Strategic Acumen", "category": "Wisdom"},
    {"codename": "Ukuhlola", "meaning": "Testing / Evaluation / Diagnostic", "category": "Wisdom"},
    {"codename": "Ukuqinisekisa", "meaning": "Verification / Proof / Validation", "category": "Wisdom"},
    {"codename": "Umbiko", "meaning": "Report / Synopsis / Chronicles", "category": "Wisdom"},
    {"codename": "Ukubuka", "meaning": "Observation / Telescopic Survey", "category": "Wisdom"},
    {"codename": "Ukufunda", "meaning": "Learning / Study / Ephemeris Charting", "category": "Wisdom"},
    {"codename": "Isixwayiso", "meaning": "Warning / Anomaly Alert", "category": "Wisdom"},
    {"codename": "Ukuthuthuka", "meaning": "Evolution / Progress / Mastery", "category": "Wisdom"},
    {"codename": "Ukwanelisa", "meaning": "Fulfillment / Completion / Climax", "category": "Wisdom"},
    {"codename": "Isiphetho", "meaning": "Destiny / Culmination / Final Convergence", "category": "Wisdom"}
]

def scan_progress_files():
    """Scans all markdown files in progress tracking/ to extract version records."""
    entries = []
    if not os.path.exists(PROGRESS_DIR):
        return entries

    files = glob.glob(os.path.join(PROGRESS_DIR, "*.md"))
    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        if filename.startswith("Version_Registry") or filename.startswith("version_registry"):
            continue
            
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        version_match = re.search(r"##\s+Version\s+([\d\.]+)\s+[\(]?([A-Za-z0-9_-]+)[\)]?", content, re.IGNORECASE)
        date_match = re.search(r"##\s+Date\s+&\s+Time\s*\n+([^\n]+)", content, re.IGNORECASE)
        codename_match = re.search(r"\*\s+\*\*Codename\*\*:\s*([A-Za-z0-9_-]+)(?:\s*\(([^\)]+)\))?", content, re.IGNORECASE)

        if version_match:
            ver_num = version_match.group(1).strip()
            codename = version_match.group(2).strip()
            date_str = date_match.group(1).strip() if date_match else "N/A"
            meaning = codename_match.group(2).strip() if codename_match and codename_match.group(2) else ""

            entries.append({
                "version": ver_num,
                "codename": codename,
                "meaning": meaning,
                "date": date_str,
                "file": filename
            })

    return entries

def parse_semver(ver_str):
    try:
        parts = [int(p) for p in ver_str.split(".")]
        while len(parts) < 3:
            parts.append(0)
        return parts
    except Exception:
        return [0, 0, 0]

def load_registry():
    """Loads registry from JSON file or rescans if missing."""
    scanned = scan_progress_files()
    
    if os.path.exists(REGISTRY_JSON):
        try:
            with open(REGISTRY_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing_vers = {item["version"]: item for item in data}
                for item in scanned:
                    existing_vers[item["version"]] = item
                data = sorted(existing_vers.values(), key=lambda x: parse_semver(x["version"]))
                return data
        except Exception:
            pass
            
    scanned = sorted(scanned, key=lambda x: parse_semver(x["version"]))
    save_registry(scanned)
    return scanned

def save_registry(entries):
    """Saves registry entries to version_registry.json and Version_Registry.md."""
    if not os.path.exists(PROGRESS_DIR):
        os.makedirs(PROGRESS_DIR, exist_ok=True)

    with open(REGISTRY_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    md_content = "# Version and Codename Registry\n\n"
    md_content += "| Version | Ndebele Codename | Meaning / Translation | Date & Time | Progress File |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- |\n"
    for item in entries:
        file_link = f"[{item['file']}](./{item['file']})"
        md_content += f"| **{item['version']}** | `{item['codename']}` | {item.get('meaning', 'N/A')} | {item['date']} | {file_link} |\n"

    with open(REGISTRY_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

def check_codename_unique(proposed_codename):
    """Checks if a proposed codename is unique across all registered versions."""
    registry = load_registry()
    proposed_clean = proposed_codename.strip().lower()
    
    for item in registry:
        if item["codename"].strip().lower() == proposed_clean:
            return {
                "unique": False,
                "message": f"CONFLICT: Codename '{proposed_codename}' was already used in Version {item['version']} ({item['file']})!",
                "used_in": item
            }
            
    return {
        "unique": True,
        "message": f"SUCCESS: Codename '{proposed_codename}' is unique and available."
    }

def suggest_codenames(count=5, category=None, search=None):
    """Suggests unused Ndebele codenames filtered by category or search query."""
    registry = load_registry()
    used_clean = {item["codename"].strip().lower() for item in registry}
    
    suggestions = []
    for entry in NDEBELE_DICTIONARY:
        if entry["codename"].strip().lower() in used_clean:
            continue
        if category and entry.get("category", "").lower() != category.lower():
            continue
        if search and (search.lower() not in entry["codename"].lower() and search.lower() not in entry["meaning"].lower()):
            continue
            
        suggestions.append(entry)
        if len(suggestions) >= count:
            break
            
    return suggestions

def get_next_version():
    """Calculates the next version number string."""
    registry = load_registry()
    if not registry:
        return "1.0.0"
        
    latest = registry[-1]["version"]
    parts = parse_semver(latest)
    parts[-1] += 1
    return f"{parts[0]}.{parts[1]}.{parts[2]}"

def bootstrap_workspace():
    """Ensures progress tracking directory and registry files exist."""
    created_dir = False
    if not os.path.exists(PROGRESS_DIR):
        os.makedirs(PROGRESS_DIR, exist_ok=True)
        created_dir = True
        
    registry = load_registry()
    
    git_initialized = False
    try:
        res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=PROJECT_ROOT, capture_output=True, text=True)
        if res.returncode == 0 and "true" in res.stdout:
            git_initialized = True
    except Exception:
        pass
        
    return {
        "project_root": PROJECT_ROOT,
        "progress_dir": PROGRESS_DIR,
        "created_progress_dir": created_dir,
        "registry_count": len(registry),
        "total_dictionary_terms": len(NDEBELE_DICTIONARY),
        "next_version": get_next_version() if registry else "1.0.0",
        "suggested_codename": suggest_codenames(1)[0] if suggest_codenames(1) else {"codename": "Isisekelo", "meaning": "Foundation"},
        "git_initialized": git_initialized
    }

def register_version(ver_num, codename, meaning, date_str, filename):
    """Registers a new version entry into the registry."""
    check_res = check_codename_unique(codename)
    if not check_res["unique"]:
        print(json.dumps(check_res, indent=2))
        sys.exit(1)
        
    registry = load_registry()
    new_entry = {
        "version": ver_num,
        "codename": codename,
        "meaning": meaning,
        "date": date_str,
        "file": filename
    }
    registry.append(new_entry)
    save_registry(registry)
    return {"status": "registered", "entry": new_entry}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python version_registry.py [bootstrap|list|check <name>|suggest [--category <cat>] [--search <query>] [--count <n>]|next-version|register <ver> <name> <meaning> <date> <file>]"}, indent=2))
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "bootstrap":
        print(json.dumps(bootstrap_workspace(), indent=2))
    elif cmd == "list":
        print(json.dumps(load_registry(), indent=2))
    elif cmd == "check" and len(sys.argv) >= 3:
        print(json.dumps(check_codename_unique(sys.argv[2]), indent=2))
    elif cmd == "suggest":
        cat = None
        srch = None
        cnt = 5
        for i, a in enumerate(sys.argv[2:]):
            if a == "--category" and i + 3 < len(sys.argv):
                cat = sys.argv[i + 3]
            elif a == "--search" and i + 3 < len(sys.argv):
                srch = sys.argv[i + 3]
            elif a == "--count" and i + 3 < len(sys.argv) and sys.argv[i + 3].isdigit():
                cnt = int(sys.argv[i + 3])
            elif a.isdigit() and cnt == 5:
                cnt = int(a)
        print(json.dumps(suggest_codenames(count=cnt, category=cat, search=srch), indent=2))
    elif cmd == "next-version":
        print(json.dumps({"next_version": get_next_version()}, indent=2))
    elif cmd == "register" and len(sys.argv) >= 6:
        ver = sys.argv[2]
        name = sys.argv[3]
        meaning = sys.argv[4]
        date_str = sys.argv[5]
        file_name = sys.argv[6] if len(sys.argv) >= 7 else "N/A"
        print(json.dumps(register_version(ver, name, meaning, date_str, file_name), indent=2))
    else:
        print(json.dumps({"error": f"Unknown command or invalid arguments for '{cmd}'"}, indent=2))
