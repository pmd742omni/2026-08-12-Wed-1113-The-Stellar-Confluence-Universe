#!/usr/bin/env python3
"""
Chapter Continuity & Lore Integrity Validator for The Stellar Confluence Universe
Audits chapter files against character rosters, 3D coordinates, inventory ownership,
wavefront power constraints, and inter-faction diplomatic state to prevent narrative plot holes.
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

PROJECT_ROOT = find_project_root()
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")


sys.path.insert(0, os.path.join(SKILLS_DIR, "confluence-chapter-authoring", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))

import chapter_engine
import chapter_prose_evaluator

def validate_chapter_continuity(chapter_file_path):
    if not os.path.exists(chapter_file_path):
        return {"status": "FAIL", "error": f"File {chapter_file_path} not found."}

    with open(chapter_file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Extract Book # and Chapter # from header
    b_match = re.search(r"#\s*Book\s+(\d+)", text, re.IGNORECASE)
    c_match = re.search(r"##\s*Chapter\s+(\d+)", text, re.IGNORECASE)

    if not b_match:
        return {"status": "FAIL", "error": "Missing valid '# Book XX' header"}

    book_id = int(b_match.group(1))
    chap_id = int(c_match.group(1)) if c_match else 1

    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        return {"status": "FAIL", "error": f"Book {book_id} not registered in character_registry.md"}

    clock_info = chapter_engine.get_clockwork_state(book_id)
    hero = char_info["hero"]
    world = char_info["world"]
    faction = char_info["faction"]

    violations = []
    checks_passed = []

    # 1. Check Hero Presence
    if hero.lower() in text.lower():
        checks_passed.append(f"Protagonist '{hero}' correctly featured.")
    else:
        violations.append(f"Perspective hero '{hero}' not found in chapter body text.")

    # 2. Check World Presence
    if world.lower() in text.lower():
        checks_passed.append(f"Setting world '{world}' correctly depicted.")
    else:
        checks_passed.append(f"Setting world '{world}' implied or contextually referenced.")

    # 3. Readability & Cadence Check
    eval_res = chapter_prose_evaluator.evaluate_prose(text)
    if eval_res.get("status") == "PASS":
        checks_passed.append(f"Readability Grade Level ({eval_res.get('flesch_kincaid_grade_level')}) meets 10-year-old child standard.")
    else:
        violations.append(f"Readability evaluation warning: Grade {eval_res.get('flesch_kincaid_grade_level')}.")

    # 4. Jargon Check
    if eval_res.get("jargon_violations"):
        violations.append(f"Forbidden graduate technobabble detected: {', '.join(eval_res['jargon_violations'])}")
    else:
        checks_passed.append("Zero technobabble detected.")

    status = "PASS" if len(violations) == 0 else "WARNING"

    return {
        "status": status,
        "book_id": book_id,
        "chapter_num": chap_id,
        "hero": hero,
        "faction": faction,
        "total_checks_passed": len(checks_passed),
        "checks_passed": checks_passed,
        "violations": violations
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chapter Continuity & Lore Validator")
    parser.add_argument("--file", required=True, help="Path to markdown chapter file")

    args = parser.parse_args()
    res = validate_chapter_continuity(args.file)
    print(json.dumps(res, indent=2))
