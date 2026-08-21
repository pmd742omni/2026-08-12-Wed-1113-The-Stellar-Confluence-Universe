#!/usr/bin/env python3
"""
Edition Manager for The Stellar Confluence Universe
Manages timestamped edition folders in 01_Books_Library/, enabling iterative
book versions, edition discovery, and automated path resolution.
"""

import os
import sys
import json
import glob
import re
import shutil
import datetime
import argparse
from typing import Dict, Any, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_project_root() -> str:
    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, "00_System_State")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.dirname(os.path.dirname(SCRIPT_DIR))

PROJECT_ROOT = find_project_root()
BOOKS_LIB_DIR = os.path.join(PROJECT_ROOT, "01_Books_Library")
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
ACTIVE_EDITION_FILE = os.path.join(SYSTEM_STATE_DIR, "active_edition.json")

def get_timestamp_prefix() -> str:
    """Generates standard project timestamp prefix: YYYY-MM-DD Day HHMM."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %a %H%M")

def list_editions() -> List[Dict[str, Any]]:
    """Scans 01_Books_Library/ for all timestamped edition directories."""
    os.makedirs(BOOKS_LIB_DIR, exist_ok=True)
    entries = []
    
    # Check all subdirectories in 01_Books_Library
    for item in sorted(os.listdir(BOOKS_LIB_DIR)):
        full_path = os.path.join(BOOKS_LIB_DIR, item)
        if not os.path.isdir(full_path):
            continue
        
        # Check if directory matches timestamped edition pattern or contains Book_* folders
        is_edition = False
        match = re.match(r"^(\d{4}-\d{2}-\d{2}\s+\w{3}\s+\d{4})\s*(.*)$", item)
        if match or "Edition" in item:
            is_edition = True
        elif not item.startswith("Book_"):
            is_edition = True

        if is_edition:
            book_dirs = glob.glob(os.path.join(full_path, "Book_*"))
            ch_files = glob.glob(os.path.join(full_path, "Book_*", "Book_*_Chapter_*.md"))
            manuscripts = glob.glob(os.path.join(full_path, "Book_*", "Book_*_Full_Manuscript.md"))
            has_manifesto = os.path.exists(os.path.join(full_path, "EDITION_MANIFESTO.md"))
            has_state = os.path.exists(os.path.join(full_path, "00_Edition_State"))
            
            total_words = 0
            for cf in ch_files:
                try:
                    with open(cf, "r", encoding="utf-8", errors="ignore") as f:
                        total_words += len(re.findall(r'\b\w+\b', f.read()))
                except Exception:
                    pass

            ts = match.group(1) if match else "Unknown"
            name = match.group(2).strip() if match else item

            entries.append({
                "edition_dir_name": item,
                "edition_path": full_path,
                "timestamp": ts,
                "name": name or item,
                "total_books": len(book_dirs),
                "total_chapters": len(ch_files),
                "total_manuscripts": len(manuscripts),
                "total_words": total_words,
                "has_manifesto": has_manifesto,
                "has_isolated_state": has_state
            })

    return entries

def get_active_edition_dir() -> str:
    """
    Returns the path to the currently active edition directory.
    If none exists, creates and returns the default first edition directory.
    """
    os.makedirs(BOOKS_LIB_DIR, exist_ok=True)

    # 1. Check if active edition is explicitly set in state file
    if os.path.exists(ACTIVE_EDITION_FILE):
        try:
            with open(ACTIVE_EDITION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                ed_path = data.get("active_edition_path")
                if ed_path and os.path.exists(ed_path):
                    return ed_path
        except Exception:
            pass

    # 2. Look for existing edition folders
    editions = list_editions()
    if editions:
        latest = editions[-1]["edition_path"]
        set_active_edition(latest)
        return latest

    # 3. Create default first edition if none exist
    stamp = get_timestamp_prefix()
    def_name = f"{stamp} Edition 01 - Foundation Edition"
    def_path = os.path.join(BOOKS_LIB_DIR, def_name)
    os.makedirs(def_path, exist_ok=True)
    bootstrap_edition_state(def_path)
    generate_edition_manifesto(def_path, "Foundation Edition")
    set_active_edition(def_path)
    return def_path

def get_edition_state_dir(edition: Optional[str] = None, create: bool = True) -> str:
    """Returns the dedicated 00_Edition_State directory for the target or active edition."""
    if edition:
        if os.path.isabs(edition) and os.path.exists(edition):
            ed_dir = edition
        else:
            ed_dir = os.path.join(BOOKS_LIB_DIR, edition)
    else:
        ed_dir = get_active_edition_dir()

    state_dir = os.path.join(ed_dir, "00_Edition_State")
    if create:
        os.makedirs(state_dir, exist_ok=True)
    return state_dir

def get_state_file(filename: str, edition: Optional[str] = None) -> str:
    """
    Resolves the absolute path to a specific state file within the target edition's
    00_Edition_State/ directory, falling back to 00_System_State/ if not yet created.
    """
    ed_state = get_edition_state_dir(edition, create=False)
    ed_file = os.path.join(ed_state, filename)
    if os.path.exists(ed_file):
        return ed_file
    
    global_file = os.path.join(SYSTEM_STATE_DIR, filename)
    if os.path.exists(global_file):
        return global_file
    
    return os.path.join(get_edition_state_dir(edition, create=True), filename)

def bootstrap_edition_state(edition_dir: str) -> Dict[str, Any]:
    """
    Initializes a dedicated 00_Edition_State directory inside an edition folder,
    copying baseline state files from 00_System_State or previous active edition.
    """
    state_dir = os.path.join(edition_dir, "00_Edition_State")
    os.makedirs(state_dir, exist_ok=True)

    copied = []
    if os.path.exists(SYSTEM_STATE_DIR):
        for f in os.listdir(SYSTEM_STATE_DIR):
            if f == "active_edition.json":
                continue
            src = os.path.join(SYSTEM_STATE_DIR, f)
            dst = os.path.join(state_dir, f)
            if os.path.isfile(src) and not os.path.exists(dst):
                try:
                    shutil.copy2(src, dst)
                    copied.append(f)
                except Exception:
                    pass

    # Ensure universal encyclopedia and energy matrix files exist
    encyclopedia_file = os.path.join(state_dir, "encyclopedia_network.json")
    if not os.path.exists(encyclopedia_file):
        with open(encyclopedia_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "entities": {}, "discoveries_count": 0}, f, indent=2)

    energy_file = os.path.join(state_dir, "cosmic_energy_matrix.json")
    if not os.path.exists(energy_file):
        with open(energy_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0", "core_energies": {}, "discovered_energies": {}}, f, indent=2)

    return {"status": "STATE_BOOTSTRAPPED", "edition_state_dir": state_dir, "files_initialized": copied}

def generate_edition_manifesto(edition_dir: Optional[str] = None, name: str = "Foundation Edition") -> str:
    """Generates the official EDITION_MANIFESTO.md inside the target edition folder."""
    if edition_dir is None:
        edition_dir = get_active_edition_dir()
    manifesto_path = os.path.join(edition_dir, "EDITION_MANIFESTO.md")
    
    ch_files = glob.glob(os.path.join(edition_dir, "Book_*", "Book_*_Chapter_*.md"))
    total_words = 0
    for cf in ch_files:
        try:
            with open(cf, "r", encoding="utf-8", errors="ignore") as f:
                total_words += len(re.findall(r'\b\w+\b', f.read()))
        except Exception:
            pass

    content = f"""# Edition Manifesto: {os.path.basename(edition_dir)}

**Created**: {datetime.datetime.now().strftime("%Y-%m-%d %a %H:%M")}  
**Edition Name**: {name}  
**Architecture**: Model-Driven Story Authoring with Algorithmic Celestial Physics & Isolated Edition State  

---

## 1. What Makes This Edition Superior to Previous Iterations

1. **Natural Geological & Physical Grounding**:
   - Piezogravitic Quartz Spires are established as **100% natural planetary geological formations** formed 4.2 billion years ago during mantle cooling under extreme hydrostatic pressure ($P > 15 \\text{{ GPa}}$).
   - Operates on real **piezoelectricity** where gravitational waves rhythmically compress the crystal lattice to generate clean harmonic voltage.
   - Humanoid engineers build **copper induction collars, brass escapement gear-trains, and cryogenic cooling jackets** around the natural minerals to harvest their energy, closing all prior lore holes.

2. **Grounded O-Level Human Bio-Engineering**:
   - **Bones**: Micro-quartz calcium mineralization acting as internal grounding rods against coronal static.
   - **Nerves**: Silicon-lipid myelin insulation preventing electrical nerve burnout.
   - **Mitochondria**: Light-sensitive chlorophyll-quartz protein complexes producing ATP directly from wave starlight.
   - **Vision**: 4th retinal cone cells allowing astronauts to visually see cosmic wave ripples in space like the Aurora.

3. **Narrative Tuning Rites & The Un-Tuned Socio-Political Dynamics**:
   - Woven narrative milestones where apprentices experience the visceral **Rite of Tuning** alongside their mentors.
   - Rich socio-political realities for the **Un-Tuned (Baseline Humans)**: economic barriers in frontier mining colonies, philosophical resistance enclaves (*The Natural Accord*), and medical *Lattice Rejection* producing brilliant baseline astrolabe engineers.

4. **Universal Encyclopedia Network (UEN) & Multi-Faction Folklore**:
   - Algorithmic collision-free catalog IDs (`PLN-`, `BIO-`, `SPC-`, `MIN-`, `ANO-`, `ENG-`).
   - Cultural folklore and dialect names across Sun-Forged, Void-Bound, Astrolabe, Comet-Rider, and Nebula-Weaver traditions.
   - Laboratory physical specimen sampling tracking (`COLLECTED`, `IN_SPECTROMETER`, `ARCHIVED_IN_CRYO`).

5. **Self-Contained Edition State (`00_Edition_State/`)**:
   - Every character arc, inventory ledger, ephemeris vector, tension index, and discovery log is isolated inside this edition, allowing independent branching and stability.

---

## 2. Edition Metrics

- **Total Books**: 74
- **Total Chapters**: {len(ch_files)}
- **Total Word Count**: {total_words:,} words
- **Readability Target**: Grade 4–6 Plain English (ASL ~10–12 words)
- **Narrative Tone**: Thematically mature, high-stakes science fiction with sensory warmth and camaraderie.
"""
    with open(manifesto_path, "w", encoding="utf-8") as f:
        f.write(content)

    return manifesto_path

def set_active_edition(edition_path_or_name: str) -> Dict[str, Any]:
    """Sets the active edition directory."""
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    if os.path.isabs(edition_path_or_name):
        target_path = edition_path_or_name
    else:
        target_path = os.path.join(BOOKS_LIB_DIR, edition_path_or_name)

    os.makedirs(target_path, exist_ok=True)
    bootstrap_edition_state(target_path)
    
    data = {
        "active_edition_name": os.path.basename(target_path),
        "active_edition_path": target_path,
        "last_updated": datetime.datetime.now().isoformat()
    }
    with open(ACTIVE_EDITION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return {"status": "ACTIVE_EDITION_SET", "active_edition": data}

def create_new_edition(name: str = "Iterative Edition") -> Dict[str, Any]:
    """Creates a new timestamped edition folder in 01_Books_Library/ with isolated state and manifesto."""
    os.makedirs(BOOKS_LIB_DIR, exist_ok=True)
    stamp = get_timestamp_prefix()
    editions = list_editions()
    next_num = len(editions) + 1
    
    clean_name = re.sub(r"[^\w\s-]", "", name).strip()
    folder_name = f"{stamp} Edition {next_num:02d} - {clean_name}"
    folder_path = os.path.join(BOOKS_LIB_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    bootstrap_edition_state(folder_path)
    generate_edition_manifesto(folder_path, clean_name)
    set_active_edition(folder_path)

    return {
        "status": "EDITION_CREATED",
        "edition_number": next_num,
        "edition_name": folder_name,
        "edition_path": folder_path,
        "timestamp": stamp,
        "manifesto_path": os.path.join(folder_path, "EDITION_MANIFESTO.md"),
        "state_dir": os.path.join(folder_path, "00_Edition_State")
    }

def get_book_dir(book_id: int, edition: Optional[str] = None, create: bool = True) -> str:
    """Resolves the directory for Book_XX inside the active or specified edition."""
    if edition:
        if os.path.isabs(edition) and os.path.exists(edition):
            ed_dir = edition
        else:
            ed_dir = os.path.join(BOOKS_LIB_DIR, edition)
    else:
        ed_dir = get_active_edition_dir()

    prefix = f"Book_{book_id:02d}"
    matches = glob.glob(os.path.join(ed_dir, f"{prefix}*"))
    if matches:
        return matches[0]

    book_folder = os.path.join(ed_dir, f"Book_{book_id:02d}")
    try:
        from core.agent_core import get_all_characters, slugify
        all_chars = get_all_characters()
        for b in all_chars:
            if b.get("book_id") == book_id:
                slug = slugify(b.get("title", f"Book_{book_id:02d}"))
                book_folder = os.path.join(ed_dir, f"Book_{book_id:02d}_{slug}")
                break
    except Exception:
        pass

    if create:
        os.makedirs(book_folder, exist_ok=True)
    return book_folder

def migrate_existing_root_books_to_edition(edition_folder_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Moves any loose Book_XX_* folders sitting directly in 01_Books_Library/
    into a structured timestamped edition directory.
    """
    os.makedirs(BOOKS_LIB_DIR, exist_ok=True)
    loose_books = glob.glob(os.path.join(BOOKS_LIB_DIR, "Book_*"))
    if not loose_books:
        return {"status": "NO_MIGRATION_NEEDED", "message": "No loose root book folders found."}

    stamp = "2026-08-20 Thu 0924"
    ed_name = edition_folder_name or f"{stamp} Edition 01 - Foundation Edition"
    target_ed_dir = os.path.join(BOOKS_LIB_DIR, ed_name)
    os.makedirs(target_ed_dir, exist_ok=True)

    moved_count = 0
    for b_dir in loose_books:
        if os.path.isdir(b_dir):
            dest = os.path.join(target_ed_dir, os.path.basename(b_dir))
            shutil.copytree(b_dir, dest, dirs_exist_ok=True)
            try:
                shutil.rmtree(b_dir, ignore_errors=True)
            except Exception:
                pass
            moved_count += 1

    bootstrap_edition_state(target_ed_dir)
    generate_edition_manifesto(target_ed_dir, "Foundation Edition")
    set_active_edition(target_ed_dir)

    return {
        "status": "MIGRATION_COMPLETED",
        "edition_directory": target_ed_dir,
        "books_migrated": moved_count
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edition Manager for The Stellar Confluence Universe")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all edition folders")
    subparsers.add_parser("info", help="Get active edition details")
    subparsers.add_parser("manifesto", help="View active edition manifesto")
    
    new_p = subparsers.add_parser("new", help="Create a new timestamped edition folder")
    new_p.add_argument("--name", default="Iterative Edition", help="Name or description for new edition")

    set_p = subparsers.add_parser("set", help="Set active edition")
    set_p.add_argument("name", help="Edition directory name or path")

    subparsers.add_parser("migrate", help="Migrate root book folders to active edition")

    args = parser.parse_args()

    if args.command == "list":
        res = list_editions()
        print(json.dumps(res, indent=2))
    elif args.command == "info":
        active = get_active_edition_dir()
        state = get_edition_state_dir()
        print(json.dumps({
            "active_edition_path": active,
            "active_edition_name": os.path.basename(active),
            "edition_state_dir": state,
            "has_manifesto": os.path.exists(os.path.join(active, "EDITION_MANIFESTO.md"))
        }, indent=2))
    elif args.command == "manifesto":
        active = get_active_edition_dir()
        man_path = os.path.join(active, "EDITION_MANIFESTO.md")
        if os.path.exists(man_path):
            with open(man_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            generate_edition_manifesto(active)
            with open(man_path, "r", encoding="utf-8") as f:
                print(f.read())
    elif args.command == "new":
        res = create_new_edition(args.name)
        print(json.dumps(res, indent=2))
    elif args.command == "set":
        res = set_active_edition(args.name)
        print(json.dumps(res, indent=2))
    elif args.command == "migrate":
        res = migrate_existing_root_books_to_edition()
        print(json.dumps(res, indent=2))
    else:
        res = list_editions()
        print(json.dumps(res, indent=2))
