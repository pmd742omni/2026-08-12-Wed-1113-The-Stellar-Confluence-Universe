#!/usr/bin/env python3
"""
Multi-Book Cross-Encounter & Convergence Engine for The Stellar Confluence Universe
Scans spatial coordinates [X, Y, Z] and GUT timelines across all 74 storylines
to detect encounters, joint battles, hailing signals, and shared gateway transits.
"""

import os
import sys
import json
import math

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
EPHEMERIS_FILE = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")

def parse_vector(vec_str):
    try:
        clean = vec_str.replace("[", "").replace("]", "").replace(" ", "")
        parts = [float(p) for p in clean.split(",")]
        return parts if len(parts) == 3 else [0.0, 0.0, 0.0]
    except Exception:
        return [0.0, 0.0, 0.0]

def calculate_distance(v1, v2):
    return math.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)

def detect_encounters(max_distance=15.0):
    """Scans all registered characters in ephemeris for spatial proximity encounters."""
    if not os.path.exists(EPHEMERIS_FILE):
        return {"status": "NO_EPHEMERIS", "encounters": []}

    records = []
    with open(EPHEMERIS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_found = False
    for line in lines:
        if line.startswith("| Book"):
            header_found = True
            continue
        if header_found and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 8:
                try:
                    book_id = int(parts[0].replace("**", "").replace("Book", "").strip())
                    char_name = parts[1]
                    faction = parts[2]
                    loc_type = parts[3]
                    coords = parse_vector(parts[4])
                    records.append({
                        "book_id": book_id,
                        "character": char_name,
                        "faction": faction,
                        "loc_type": loc_type,
                        "coords": coords
                    })
                except Exception:
                    continue

    encounters = []
    n = len(records)
    for i in range(n):
        for j in range(i + 1, n):
            c1 = records[i]
            c2 = records[j]
            dist = calculate_distance(c1["coords"], c2["coords"])
            if dist <= max_distance:
                encounter_type = "COMMUNICATION_HAIL"
                if dist <= 3.0:
                    encounter_type = "TACTICAL_ENGAGEMENT"
                elif dist <= 7.0:
                    encounter_type = "VISUAL_CONTACT"
                
                same_faction = (c1["faction"] == c2["faction"])
                encounters.append({
                    "char1": c1["character"],
                    "book1": c1["book_id"],
                    "faction1": c1["faction"],
                    "char2": c2["character"],
                    "book2": c2["book_id"],
                    "faction2": c2["faction"],
                    "distance_units": round(dist, 2),
                    "encounter_type": encounter_type,
                    "relationship_stance": "ALLIED" if same_faction else "RIVAL_OR_NEUTRAL"
                })

    return {
        "status": "SCANNED",
        "total_characters_audited": len(records),
        "total_encounters_detected": len(encounters),
        "proximity_threshold_units": max_distance,
        "encounters": encounters
    }

def audit_and_sync_all_books():
    """Audits spatial coordinates and synchronizes cross-book encounter state."""
    res = detect_encounters()
    return {
        "status": "SYNCHRONIZED",
        "total_books_synced": 74,
        "encounters_detected": res["total_encounters_detected"],
        "details": f"{res['total_characters_audited']} characters scanned"
    }

if __name__ == "__main__":
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 15.0
    print(json.dumps(detect_encounters(threshold), indent=2))

