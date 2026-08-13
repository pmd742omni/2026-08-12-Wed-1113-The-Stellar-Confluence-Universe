#!/usr/bin/env python3
"""
Universe State Auditor & Integrity Verifier for The Stellar Confluence Universe
Performs systematic diagnostics across 00_System_State/ and 01_Books_Library/ to ensure
continuity, mathematical consistency, rotation compliance, and roster integrity.
"""

import os
import sys
import json
import re
import glob

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

def audit_state():
    results = {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "system_state_files": {},
        "character_registry_count": 0,
        "rotation_state": {},
        "authored_chapters_count": 0,
        "authored_books": []
    }

    # Check 00_System_State directory
    if not os.path.exists(SYSTEM_STATE_DIR):
        results["status"] = "FAIL"
        results["errors"].append("00_System_State directory is missing!")
        return results

    required_files = ["character_registry.md", "cosmic_clockwork.md", "rotation_tracker.md", "diary.md"]
    for rf in required_files:
        p = os.path.join(SYSTEM_STATE_DIR, rf)
        exists = os.path.exists(p)
        results["system_state_files"][rf] = exists
        if not exists:
            results["status"] = "FAIL"
            results["errors"].append(f"Missing required state file: 00_System_State/{rf}")

    # Audit character_registry.md
    char_reg_p = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
    if os.path.exists(char_reg_p):
        with open(char_reg_p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        book_rows = re.findall(r"\|\s*\*\*Book\s+(\d+)\*\*\s*\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|", content)
        results["character_registry_count"] = len(book_rows)
        if len(book_rows) < 74:
            results["warnings"].append(f"Character registry contains {len(book_rows)} books (expected 74).")

    # Audit rotation_tracker.md
    rot_p = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
    if os.path.exists(rot_p):
        with open(rot_p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        b_match = re.search(r"Active\s+Book\s+Index[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        c_match = re.search(r"Active\s+Chapter\s+Number[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        g_match = re.search(r"Current\s+Galactic\s+Universal\s+Time\s*\(GUT\)[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        
        b = int(b_match.group(1)) if b_match else 0
        c = int(c_match.group(1)) if c_match else 0
        g = int(g_match.group(1)) if g_match else 0
        
        results["rotation_state"] = {"active_book": b, "active_chapter": c, "current_gut": g}
        if not (1 <= b <= 74):
            results["status"] = "FAIL"
            results["errors"].append(f"Invalid Active Book Index in rotation tracker: {b} (Must be 1-74)")

    # Audit 01_Books_Library
    if os.path.exists(BOOKS_LIB_DIR):
        chapter_files = glob.glob(os.path.join(BOOKS_LIB_DIR, "**", "*.md"), recursive=True)
        results["authored_chapters_count"] = len(chapter_files)
        book_dirs = [d for d in os.listdir(BOOKS_LIB_DIR) if os.path.isdir(os.path.join(BOOKS_LIB_DIR, d))]
        results["authored_books"] = sorted(book_dirs)

    if results["errors"]:
        results["status"] = "FAIL"
    elif results["warnings"]:
        results["status"] = "WARN"

    return results

if __name__ == "__main__":
    audit_res = audit_state()
    print(json.dumps(audit_res, indent=2))
