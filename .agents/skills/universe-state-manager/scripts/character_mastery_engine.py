#!/usr/bin/env python3
"""
Character Growth, Progression & Skill Mastery Tree Engine for The Stellar Confluence Universe
Tracks protagonist ranks (Apprentice -> Adept -> Journey-Master -> High Artificer),
unlocked resonance abilities, stamina capacity, and character development milestones across all 74 storylines.
"""

import os
import sys
import json
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
MASTERY_STATE_JSON = os.path.join(SYSTEM_STATE_DIR, "character_mastery.json")

RANKS = ["Apprentice", "Adept", "Journey-Master", "High Artificer"]

DEFAULT_MASTERY_RECORD = {
    "1": {
        "book_id": 1,
        "hero_name": "Caelum Dawnrunner",
        "faction": "Sun-Forged Hegemony",
        "rank": "Apprentice",
        "level": 1,
        "mastery_points": 120,
        "stamina_pool": 100,
        "unlocked_techniques": ["Solar Beam Focusing", "Photonic Prism Refraction"],
        "milestones": [
            {"chapter": 1, "gut": 100, "event": "Calibrated the High Helios Solar Observatory Lens"}
        ]
    },
    "11": {
        "book_id": 11,
        "hero_name": "Vespera Ray",
        "faction": "Void-Bound Monks",
        "rank": "Apprentice",
        "level": 1,
        "mastery_points": 110,
        "stamina_pool": 100,
        "unlocked_techniques": ["Shadow Canopy Blending", "Basalt Phase-Stepping"],
        "milestones": [
            {"chapter": 1, "gut": 100, "event": "Navigated the Umbra Basalt Rift during Eclipse Nadir"}
        ]
    },
    "21": {
        "book_id": 21,
        "hero_name": "Tobias Cogsmith",
        "faction": "Astrolabe Engineers",
        "rank": "Apprentice",
        "level": 1,
        "mastery_points": 115,
        "stamina_pool": 100,
        "unlocked_techniques": ["Gear Train Synchronization", "Centrifugal Flywheel Balancing"],
        "milestones": [
            {"chapter": 1, "gut": 100, "event": "Balanced the Master Flywheel on Aethelgard Equatorial Ring"}
        ]
    }
}

def load_mastery_records():
    if os.path.exists(MASTERY_STATE_JSON):
        try:
            with open(MASTERY_STATE_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_MASTERY_RECORD
    return DEFAULT_MASTERY_RECORD

def save_mastery_records(records):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(MASTERY_STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def get_character_mastery(book_id):
    records = load_mastery_records()
    bid = str(int(book_id))
    if bid in records:
        return records[bid]
    
    # Resolve canonical character info from registry
    hero_name = f"Protagonist #{int(book_id):02d}"
    faction_name = "Sector Faction"
    char_reg = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
    if os.path.exists(char_reg):
        with open(char_reg, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if f"Book {int(book_id):02d}" in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 6:
                        hero_name = parts[2].replace("`", "")
                        faction_name = parts[3]
                    break

    # Generate baseline record for uninitialized book
    new_rec = {
        "book_id": int(book_id),
        "hero_name": hero_name,
        "faction": faction_name,
        "rank": "Apprentice",
        "level": 1,
        "mastery_points": 100,
        "stamina_pool": 100,
        "unlocked_techniques": [f"{faction_name.split()[0]} Resonance Technique"],
        "milestones": [{"chapter": 1, "gut": 100, "event": f"Initiated Journey across {faction_name}"}]
    }
    records[bid] = new_rec
    save_mastery_records(records)
    return new_rec

def award_experience(book_id, points, reason, chapter_num=1, gut_time=100):
    records = load_mastery_records()
    bid = str(int(book_id))
    rec = get_character_mastery(book_id)

    rec["mastery_points"] += int(points)
    
    # Calculate Level and Rank progression (Every 100 XP is 1 level; Every 3 levels is a Rank)
    new_level = 1 + (rec["mastery_points"] // 100)
    rec["level"] = new_level
    rank_idx = min(len(RANKS) - 1, (new_level - 1) // 3)
    rec["rank"] = RANKS[rank_idx]
    rec["stamina_pool"] = 100 + ((new_level - 1) * 15)

    rec["milestones"].append({
        "chapter": int(chapter_num),
        "gut": int(gut_time),
        "event": f"+{points} XP: {reason} (Rank: {rec['rank']})"
    })

    records[bid] = rec
    save_mastery_records(records)

    return {
        "status": "XP_AWARDED",
        "hero": rec["hero_name"],
        "total_xp": rec["mastery_points"],
        "level": rec["level"],
        "rank": rec["rank"],
        "stamina": rec["stamina_pool"]
    }

def unlock_technique(book_id, technique_name):
    records = load_mastery_records()
    bid = str(int(book_id))
    rec = get_character_mastery(book_id)

    if technique_name not in rec["unlocked_techniques"]:
        rec["unlocked_techniques"].append(technique_name)
        records[bid] = rec
        save_mastery_records(records)
        return {"status": "TECHNIQUE_UNLOCKED", "technique": technique_name, "hero": rec["hero_name"]}
    return {"status": "ALREADY_UNLOCKED", "technique": technique_name}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Character Growth & Mastery Tree Engine")
    subparsers = parser.add_subparsers(dest="command")

    get_p = subparsers.add_parser("get", help="Get mastery profile for a book")
    get_p.add_argument("--book", type=int, required=True)

    xp_p = subparsers.add_parser("award", help="Award XP and advance mastery")
    xp_p.add_argument("--book", type=int, required=True)
    xp_p.add_argument("--xp", type=int, required=True)
    xp_p.add_argument("--reason", required=True)
    xp_p.add_argument("--chap", type=int, default=1)
    xp_p.add_argument("--gut", type=int, default=100)

    tech_p = subparsers.add_parser("unlock", help="Unlock a new resonance technique")
    tech_p.add_argument("--book", type=int, required=True)
    tech_p.add_argument("--tech", required=True)

    args = parser.parse_args()

    if args.command == "award":
        print(json.dumps(award_experience(args.book, args.xp, args.reason, args.chap, args.gut), indent=2))
    elif args.command == "unlock":
        print(json.dumps(unlock_technique(args.book, args.tech), indent=2))
    elif args.command == "get":
        print(json.dumps(get_character_mastery(args.book), indent=2))
    else:
        print(json.dumps(get_character_mastery(1), indent=2))
