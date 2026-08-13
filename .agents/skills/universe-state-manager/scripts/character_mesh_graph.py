#!/usr/bin/env python3
"""
Galactic Character Mesh Graph & Multi-Book Lineage Engine for The Stellar Confluence Universe
Maps cross-book hero relationships, mentor lineages, shared artifact bonds, and interstellar comms.
"""

import os
import sys
import json
import argparse

RELATIONSHIP_MESH = {
    1: { # Book 01: Caelum Dawnrunner (Sun-Forged)
        "mentor": "Master Theron (High Solar Artificer)",
        "allies": [
            {"book_id": 11, "hero": "Vespera Ray", "relation": "Secret Twilight Penpal / Shared Star-Shard Compass"},
            {"book_id": 21, "hero": "Tobias Cogsmith", "relation": "Childhood Friend & Gear Supplier"}
        ],
        "rivals": [
            {"book_id": 12, "hero": "Kaelen Umbra", "relation": "Border Patrol Rival across Meridian Corridor"}
        ],
        "shared_artifacts": ["Sol-Core Focusing Prism #01", "Dual Brass Polarizer Rings"],
        "comms_frequency": "144.20 MHz (Helios Observatory Beam)"
    },
    11: { # Book 11: Vespera Ray (Void-Bound)
        "mentor": "Elder Nyx (Shadow Keeper)",
        "allies": [
            {"book_id": 1, "hero": "Caelum Dawnrunner", "relation": "Secret Twilight Penpal / Shared Star-Shard Compass"},
            {"book_id": 31, "hero": "Orin Frostfang", "relation": "Cryo-Glider Route Guide"}
        ],
        "rivals": [
            {"book_id": 2, "hero": "Aurelia Solis", "relation": "Radiant Border Inquisitor"}
        ],
        "shared_artifacts": ["Star-Shard Umbral Compass", "Basalt Phase-Ring"],
        "comms_frequency": "128.50 MHz (Umbra Silent Sub-Band)"
    },
    21: { # Book 21: Tobias Cogsmith (Astrolabe)
        "mentor": "Chief Gearwright Gideon",
        "allies": [
            {"book_id": 1, "hero": "Caelum Dawnrunner", "relation": "Childhood Friend & Gear Supplier"},
            {"book_id": 41, "hero": "Darius Stonebreaker", "relation": "Heavy Foundry Partner"}
        ],
        "rivals": [
            {"book_id": 22, "hero": "Valeria Clockwork", "relation": "Annual Chrono-Exposition Competition Rival"}
        ],
        "shared_artifacts": ["Master Brass Caliper", "Harmonic Tuning Fork"],
        "comms_frequency": "160.00 MHz (Aethelgard Central Gear-Clock Dispatch)"
    }
}

def get_character_mesh(book_id):
    book_id = int(book_id)
    if book_id in RELATIONSHIP_MESH:
        return {
            "book_id": book_id,
            "mesh": RELATIONSHIP_MESH[book_id]
        }
    else:
        # Procedural fallback for expansion heroes
        return {
            "book_id": book_id,
            "mesh": {
                "mentor": f"Faction Elder of Book {book_id:02d}",
                "allies": [
                    {"book_id": (book_id % 74) + 1, "relation": "Neighboring Sector Scout"}
                ],
                "rivals": [],
                "shared_artifacts": [f"Sector Standard Relic #{book_id:02d}"],
                "comms_frequency": f"{140.0 + (book_id * 0.5):.2f} MHz"
            }
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Character Mesh Graph")
    parser.add_argument("--book", type=int, default=1, help="Book ID number (1-74)")

    args = parser.parse_args()
    res = get_character_mesh(args.book)
    print(json.dumps(res, indent=2))
