#!/usr/bin/env python3
"""
Dynamic Galactic Tension & War/Peace State Engine for The Stellar Confluence Universe
Simulates evolving inter-faction diplomatic relations, escalating or de-escalating tension
indices (0-100) based on chapter events, cosmic ripple hazards, and border treaties.
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
TENSION_STATE_JSON = os.path.join(SYSTEM_STATE_DIR, "galactic_tension.json")

DEFAULT_TENSIONS = {
    "Sun-Forged Hegemony::Void-Bound Monks": {
        "faction_a": "Sun-Forged Hegemony",
        "faction_b": "Void-Bound Monks",
        "tension_index": 88,
        "diplomatic_state": "OPEN_RIVALRY",
        "history": [
            {"gut": 0, "delta": 0, "state": "OPEN_RIVALRY", "reason": "Historic Twilight Border Disputed Sector Treaty"}
        ]
    },
    "Sun-Forged Hegemony::Astrolabe Engineers": {
        "faction_a": "Sun-Forged Hegemony",
        "faction_b": "Astrolabe Engineers",
        "tension_index": 35,
        "diplomatic_state": "TRADE_PACT_STABLE",
        "history": [
            {"gut": 0, "delta": 0, "state": "TRADE_PACT_STABLE", "reason": "Solar Furnace Precision Brass Trade Agreement"}
        ]
    },
    "Void-Bound Monks::Astrolabe Engineers": {
        "faction_a": "Void-Bound Monks",
        "faction_b": "Astrolabe Engineers",
        "tension_index": 48,
        "diplomatic_state": "COLD_WAR_FRICTION",
        "history": [
            {"gut": 0, "delta": 0, "state": "COLD_WAR_FRICTION", "reason": "Phase-Resonant Basalt Export Disputes"}
        ]
    },
    "Astrolabe Engineers::Comet-Riders": {
        "faction_a": "Astrolabe Engineers",
        "faction_b": "Comet-Riders",
        "tension_index": 20,
        "diplomatic_state": "ALLIANCE_HARMONY",
        "history": [
            {"gut": 0, "delta": 0, "state": "ALLIANCE_HARMONY", "reason": "Cryo-Coolant Supply Pact for Orbital Flywheels"}
        ]
    }
}

def make_key(a, b):
    pair = sorted([a.strip(), b.strip()])
    return f"{pair[0]}::{pair[1]}"

def determine_state(tension):
    if tension < 25:
        return "ALLIANCE_HARMONY"
    elif tension < 50:
        return "TRADE_PACT_STABLE"
    elif tension < 75:
        return "COLD_WAR_FRICTION"
    elif tension < 90:
        return "OPEN_RIVALRY"
    else:
        return "BORDER_MOBILIZATION"

def load_tensions():
    if os.path.exists(TENSION_STATE_JSON):
        try:
            with open(TENSION_STATE_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_TENSIONS
    return DEFAULT_TENSIONS

def save_tensions(tensions):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(TENSION_STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(tensions, f, indent=2)

def get_tension(fac_a, fac_b):
    tensions = load_tensions()
    key = make_key(fac_a, fac_b)
    if key in tensions:
        return tensions[key]
    
    # Default baseline for unmapped expansion factions
    return {
        "faction_a": fac_a,
        "faction_b": fac_b,
        "tension_index": 50,
        "diplomatic_state": "COLD_WAR_FRICTION",
        "history": [{"gut": 0, "delta": 0, "state": "COLD_WAR_FRICTION", "reason": "Standard Interstellar Frontier Stance"}]
    }

def adjust_tension(fac_a, fac_b, delta, reason, gut_time=100):
    tensions = load_tensions()
    key = make_key(fac_a, fac_b)
    
    entry = get_tension(fac_a, fac_b)
    old_tension = entry["tension_index"]
    new_tension = max(0, min(100, old_tension + delta))
    new_state = determine_state(new_tension)

    entry["tension_index"] = new_tension
    entry["diplomatic_state"] = new_state
    entry["history"].append({
        "gut": int(gut_time),
        "delta": delta,
        "new_tension": new_tension,
        "state": new_state,
        "reason": reason
    })

    tensions[key] = entry
    save_tensions(tensions)

    return {
        "status": "TENSION_UPDATED",
        "pairing": key,
        "old_tension": old_tension,
        "new_tension": new_tension,
        "diplomatic_state": new_state,
        "delta": delta,
        "reason": reason
    }

def list_all_tensions():
    tensions = load_tensions()
    return {
        "total_tracked_pairings": len(tensions),
        "pairings": list(tensions.values())
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Galactic Tension Tracker")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all tracked faction tensions")

    get_p = subparsers.add_parser("get", help="Get tension between two factions")
    get_p.add_argument("--a", required=True)
    get_p.add_argument("--b", required=True)

    adj_p = subparsers.add_parser("adjust", help="Adjust tension between two factions")
    adj_p.add_argument("--a", required=True)
    adj_p.add_argument("--b", required=True)
    adj_p.add_argument("--delta", type=int, required=True)
    adj_p.add_argument("--reason", required=True)
    adj_p.add_argument("--gut", type=int, default=100)

    args = parser.parse_args()

    if args.command == "get":
        print(json.dumps(get_tension(args.a, args.b), indent=2))
    elif args.command == "adjust":
        print(json.dumps(adjust_tension(args.a, args.b, args.delta, args.reason, args.gut), indent=2))
    else:
        print(json.dumps(list_all_tensions(), indent=2))
