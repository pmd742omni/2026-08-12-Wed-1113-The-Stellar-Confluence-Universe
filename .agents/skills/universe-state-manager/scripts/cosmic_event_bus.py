#!/usr/bin/env python3
"""
Cosmic Event Bus & Cross-Book Ripple Hazard Tracker for The Stellar Confluence Universe
Records celestial beacon pulses, stargate disruptions, and stellar flares, computing spatial
proximity and environmental hazards for interacting storylines.
"""

import os
import sys
import json
import math
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
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
EVENTS_JSON = os.path.join(SYSTEM_STATE_DIR, "cosmic_events.json")

def parse_sector(sector_str):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", sector_str)]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def calculate_distance(s1, s2):
    x1, y1, z1 = parse_sector(s1) if isinstance(s1, str) else s1
    x2, y2, z2 = parse_sector(s2) if isinstance(s2, str) else s2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

def load_events():
    if not os.path.exists(EVENTS_JSON):
        return []
    try:
        with open(EVENTS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_events(events):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

def log_event(event_type, source_book, origin_sector, radius, start_gut, duration, description):
    events = load_events()
    new_event = {
        "id": f"EVT-{len(events)+1:04d}",
        "event_type": event_type.upper(),
        "source_book": source_book,
        "origin_sector": origin_sector,
        "blast_radius": float(radius),
        "start_gut": int(start_gut),
        "duration_gut": int(duration),
        "expiry_gut": int(start_gut) + int(duration),
        "description": description
    }
    events.append(new_event)
    save_events(events)
    return {"status": "logged", "event": new_event}

def check_hazards(target_sector, current_gut):
    events = load_events()
    active_hazards = []

    for ev in events:
        start = ev["start_gut"]
        expiry = ev["expiry_gut"]
        if start <= current_gut <= expiry:
            dist = calculate_distance(ev["origin_sector"], target_sector)
            if dist <= ev["blast_radius"]:
                intensity = round(1.0 - (dist / max(ev["blast_radius"], 0.001)), 2)
                active_hazards.append({
                    "event_id": ev["id"],
                    "event_type": ev["event_type"],
                    "source_book": ev["source_book"],
                    "distance_units": round(dist, 2),
                    "hazard_intensity": intensity,
                    "description": ev["description"],
                    "narrative_effect": f"ENVIRONMENTAL TURBULENCE: {ev['event_type']} from {ev['source_book']} is active (Dist: {dist:.1f} sectors, Intensity: {intensity*100:.0f}%). {ev['description']}"
                })

    return {
        "target_sector": target_sector,
        "current_gut": current_gut,
        "active_hazard_count": len(active_hazards),
        "hazards": active_hazards
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Event Bus & Ripple Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Log command
    log_p = subparsers.add_parser("log", help="Log a new cosmic ripple event")
    log_p.add_argument("--type", required=True, help="Event type (e.g. BEACON_PULSE, GATEWAY_DISRUPTION, SOLAR_FLARE)")
    log_p.add_argument("--source", required=True, help="Source book (e.g. Book 04)")
    log_p.add_argument("--sector", required=True, help="Origin sector coordinates '[X, Y, Z]'")
    log_p.add_argument("--radius", type=float, default=5.0, help="Influence radius in sector units")
    log_p.add_argument("--start-gut", type=int, required=True, help="GUT when event triggered")
    log_p.add_argument("--duration", type=int, default=10, help="Duration in GUT ticks")
    log_p.add_argument("--desc", required=True, help="Event description and environmental effect")

    # Check command
    check_p = subparsers.add_parser("check", help="Check active hazards for a sector")
    check_p.add_argument("--sector", required=True, help="Target sector coordinates '[X, Y, Z]'")
    check_p.add_argument("--gut", type=int, required=True, help="Current GUT tick")

    # List command
    list_p = subparsers.add_parser("list", help="List all recorded cosmic events")

    args = parser.parse_args()

    if args.command == "log":
        res = log_event(args.type, args.source, args.sector, args.radius, args.start_gut, args.duration, args.desc)
        print(json.dumps(res, indent=2))
    elif args.command == "check":
        res = check_hazards(args.sector, args.gut)
        print(json.dumps(res, indent=2))
    elif args.command == "list":
        print(json.dumps(load_events(), indent=2))
    else:
        parser.print_help()
