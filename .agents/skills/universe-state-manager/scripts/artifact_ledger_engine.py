#!/usr/bin/env python3
"""
Galactic Artifact Ledger & Relic Lineage Engine for The Stellar Confluence Universe
Tracks ancient cosmic relics, historical ownership chains of custody, active bearers,
and celestial harmonic frequencies across all 74 storylines.
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
ARTIFACT_LEDGER_JSON = os.path.join(SYSTEM_STATE_DIR, "artifact_ledger.json")

DEFAULT_MASTER_ARTIFACTS = {
    "Sol-Core Prism Lens": {
        "name": "Sol-Core Prism Lens",
        "origin_world": "Helios Prime (Sun-Forged Foundries)",
        "energy_type": "Focused Photonic Coherence",
        "harmonic_freq": "144.2 MHz",
        "current_bearer_book": 1,
        "current_bearer_hero": "Caelum Dawnrunner",
        "custody_chain": [
            {"gut": 0, "event": "Forged in the Great Solar Foundry of Helios Prime"},
            {"gut": 95, "event": "Bestowed to Apprentice Caelum Dawnrunner by Master Theron"}
        ],
        "tactical_power": "Focuses incoming Confluence Wavefront into high-intensity solar cutting beams."
    },
    "Umbral Keystone": {
        "name": "Umbral Keystone",
        "origin_world": "Umbra Chasm (Shadow Moon)",
        "energy_type": "Eclipse Phase Resonance",
        "harmonic_freq": "128.5 MHz",
        "current_bearer_book": 11,
        "current_bearer_hero": "Vespera Ray",
        "custody_chain": [
            {"gut": 0, "event": "Discovered in the basalt rift caves of Nadir Prime"},
            {"gut": 80, "event": "Entrusted to Vespera Ray by Elder Nyx for twilight reconnaissance"}
        ],
        "tactical_power": "Enables temporary matter phase-shifting through dense stone and hull armor."
    },
    "Master Chrono-Astrolabe": {
        "name": "Master Chrono-Astrolabe",
        "origin_world": "Aethelgard Gear-City",
        "energy_type": "Precision Mechanical Kinetics",
        "harmonic_freq": "160.0 MHz",
        "current_bearer_book": 21,
        "current_bearer_hero": "Tobias Cogsmith",
        "custody_chain": [
            {"gut": 10, "event": "Assembled by the Chief Gearwright Guild"},
            {"gut": 90, "event": "Awarded to Tobias Cogsmith at the Annual Chrono-Exposition"}
        ],
        "tactical_power": "Synchronizes orbital flywheels with zero friction during twilight transit."
    },
    "Cryo-Harpoon of Boreas": {
        "name": "Cryo-Harpoon of Boreas",
        "origin_world": "Comet Tail Perihelion",
        "energy_type": "Cryogenic Sublimation Thrust",
        "harmonic_freq": "152.4 MHz",
        "current_bearer_book": 31,
        "current_bearer_hero": "Orin Frostfang",
        "custody_chain": [
            {"gut": 25, "event": "Carved from high-density interstellar comet ice core"},
            {"gut": 92, "event": "Claimed by Orin Frostfang during the Great Regatta"}
        ],
        "tactical_power": "Anchors star-gliders to high-speed cometary dust plumes."
    }
}

def load_ledger():
    if os.path.exists(ARTIFACT_LEDGER_JSON):
        try:
            with open(ARTIFACT_LEDGER_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_MASTER_ARTIFACTS
    return DEFAULT_MASTER_ARTIFACTS

def save_ledger(ledger):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(ARTIFACT_LEDGER_JSON, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)

def list_artifacts():
    ledger = load_ledger()
    return {
        "total_master_artifacts": len(ledger),
        "artifacts": [
            {
                "name": art["name"],
                "bearer": f"{art['current_bearer_hero']} (Book {art['current_bearer_book']:02d})",
                "origin": art["origin_world"],
                "frequency": art["harmonic_freq"]
            }
            for art in ledger.values()
        ]
    }

def inspect_artifact(name):
    ledger = load_ledger()
    for k, v in ledger.items():
        if name.lower() in k.lower():
            return v
    return {"error": f"Artifact '{name}' not found in galactic ledger."}

def transfer_artifact(name, to_book_id, to_hero_name, gut_time, reason):
    ledger = load_ledger()
    matched_key = None
    for k in ledger.keys():
        if name.lower() in k.lower():
            matched_key = k
            break

    if not matched_key:
        return {"error": f"Artifact '{name}' not found."}

    art = ledger[matched_key]
    prev_bearer = art["current_bearer_hero"]
    prev_book = art["current_bearer_book"]

    art["current_bearer_book"] = int(to_book_id)
    art["current_bearer_hero"] = to_hero_name
    art["custody_chain"].append({
        "gut": int(gut_time),
        "event": f"Transferred from {prev_bearer} (Book {prev_book}) to {to_hero_name} (Book {to_book_id}): {reason}"
    })

    save_ledger(ledger)
    return {
        "status": "TRANSFERRED",
        "artifact": matched_key,
        "new_bearer": f"{to_hero_name} (Book {to_book_id})",
        "custody_chain_length": len(art["custody_chain"])
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Artifact Lineage Ledger")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all master artifacts")

    ins_p = subparsers.add_parser("inspect", help="Inspect artifact lineage")
    ins_p.add_argument("--name", required=True)

    tr_p = subparsers.add_parser("transfer", help="Transfer artifact custody")
    tr_p.add_argument("--name", required=True)
    tr_p.add_argument("--to-book", type=int, required=True)
    tr_p.add_argument("--to-hero", required=True)
    tr_p.add_argument("--gut", type=int, default=100)
    tr_p.add_argument("--reason", required=True)

    args = parser.parse_args()

    if args.command == "inspect":
        print(json.dumps(inspect_artifact(args.name), indent=2))
    elif args.command == "transfer":
        print(json.dumps(transfer_artifact(args.name, args.to_book, args.to_hero, args.gut, args.reason), indent=2))
    else:
        print(json.dumps(list_artifacts(), indent=2))
