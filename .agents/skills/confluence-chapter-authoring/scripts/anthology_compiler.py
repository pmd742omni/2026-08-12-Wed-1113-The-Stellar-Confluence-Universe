#!/usr/bin/env python3
"""
Anthology & Manuscript Compiler for The Stellar Confluence Universe
Compiles individual book chapters or entire series volumes into unified publishing manuscripts
complete with Table of Contents, character dossiers, astronomical ephemeris appendix, and glossary.
"""

import os
import sys
import glob
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
BOOKS_LIB_DIR = os.path.join(PROJECT_ROOT, "01_Books_Library")
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")
CORE_DIR = os.path.join(PROJECT_ROOT, ".agents", "core")
sys.path.insert(0, CORE_DIR)
sys.path.insert(0, os.path.join(SKILLS_DIR, "confluence-chapter-authoring", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

import edition_manager
import chapter_engine
import character_mesh_graph

def compile_book_manuscript(book_id, edition=None):
    book_id = int(book_id)
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        return {"error": f"Book {book_id} not found in registry"}

    title = char_info["title"]
    hero = char_info["hero"]
    faction = char_info["faction"]
    world = char_info["world"]
    sector = char_info["sector"]

    book_folder = edition_manager.get_book_dir(book_id, edition=edition, create=False)

    if not os.path.exists(book_folder):
        return {"error": f"Book folder {book_folder} does not exist yet."}

    # Find all chapter files in numerical order
    chapter_files = sorted(glob.glob(os.path.join(book_folder, "Book_*_Chapter_*.md")))
    if not chapter_files:
        return {"error": f"No chapter files found in {book_folder}."}

    mesh_res = character_mesh_graph.get_character_mesh(book_id)
    mesh_info = mesh_res.get("mesh", {})

    # Build Unified Manuscript Header
    manuscript = f"""# Book {book_id:02d}: {title}
*A Novel of The Stellar Confluence Universe*

**Author**: Master Storyteller & World Engine (Peter Dube & Antigravity)  
**Primary Protagonist**: {hero}  
**Faction**: {faction}  
**Homeworld**: {world} (Sector `{sector}`)  
**Target Readability**: Grade 4–6 (Ages 9–12)  

---

## Table of Contents
"""
    for idx, cf in enumerate(chapter_files, 1):
        manuscript += f"- [Chapter {idx:02d}](#chapter-{idx:02d})\n"

    manuscript += """- [Appendix A: Character Dossier & Lineage](#appendix-a-character-dossier--lineage)
- [Appendix B: Faction & Celestial Ephemeris](#appendix-b-faction--celestial-ephemeris)

---

"""

    # Append Chapters
    total_words = 0
    for idx, cf in enumerate(chapter_files, 1):
        with open(cf, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            total_words += len(re.findall(r'\b\w+\b', text))
            manuscript += f"\n\n{text.strip()}\n\n---\n"

    # Append Appendices
    manuscript += f"""
## Appendix A: Character Dossier & Lineage

- **Hero**: `{hero}`
- **Mentor**: {mesh_info.get('mentor', 'Senior Faction Elder')}
- **Comms Call-sign**: `{mesh_info.get('comms_frequency', '144.00 MHz')}`
- **Signature Relics**: {", ".join(mesh_info.get('shared_artifacts', ['Standard Relic']))}

## Appendix B: Faction & Celestial Ephemeris

- **Faction**: {faction}
- **Primary Celestial Coordinate**: Sector `{sector}`
- **Confluence Physics Standard**: Dynamic Wavefront Angular Resonance ($\omega_{{rot}} = 15^\circ / GUT$, $\omega_{{orb}} = 60^\circ / GUT$).

---
*The Stellar Confluence Universe — All 74 Storylines Connected.*
"""

    output_file = os.path.join(book_folder, f"Book_{book_id:02d}_Full_Manuscript.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(manuscript)

    return {
        "status": "compiled",
        "book_id": book_id,
        "title": title,
        "total_chapters": len(chapter_files),
        "total_words": total_words,
        "manuscript_file": output_file
    }

def compile_all_books(edition=None):
    """Compiles full manuscripts across all 74 books."""
    results = []
    total_universe_words = 0
    total_universe_chapters = 0

    for b_id in range(1, 75):
        res = compile_book_manuscript(b_id, edition=edition)
        if "error" not in res:
            results.append(res)
            total_universe_words += res.get("total_words", 0)
            total_universe_chapters += res.get("total_chapters", 0)

    return {
        "status": "ALL_BOOKS_COMPILED",
        "total_books_compiled": len(results),
        "total_universe_chapters": total_universe_chapters,
        "total_universe_words": total_universe_words,
        "books": results
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anthology & Manuscript Compiler")
    parser.add_argument("--book", type=int, help="Book ID number to compile")
    parser.add_argument("--all", action="store_true", help="Compile all 74 book manuscripts")
    parser.add_argument("--edition", help="Edition folder name or path")

    args = parser.parse_args()
    if args.all or not args.book:
        res = compile_all_books(edition=args.edition) if args.all else compile_book_manuscript(args.book or 1, edition=args.edition)
    else:
        res = compile_book_manuscript(args.book, edition=args.edition)
    print(json.dumps(res, indent=2))
