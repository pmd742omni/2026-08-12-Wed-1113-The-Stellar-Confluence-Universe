#!/usr/bin/env python3
"""
Galactic Subspace Broadcast Network & Newsfeed Wire for The Stellar Confluence Universe
Generates dynamic interstellar news briefs, emergency radio intercepts, and cosmic weather bulletins
derived from real-time system events, chapter actions, and faction diplomacy.
"""

import os
import sys
import json
import argparse
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")
EVENTS_JSON = os.path.join(SYSTEM_STATE_DIR, "cosmic_events.json")
ROT_TRACKER = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")

def get_broadcast_feed():
    # 1. Read recent diary entries
    recent_events = []
    if os.path.exists(DIARY_MD):
        with open(DIARY_MD, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip().startswith("|") and "GUT" in line and ":---" not in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 5:
                        recent_events.append({
                            "gut": parts[0],
                            "book": parts[1],
                            "hero": parts[3],
                            "action": parts[4]
                        })

    # 2. Read active cosmic hazards
    hazards = []
    if os.path.exists(EVENTS_JSON):
        try:
            with open(EVENTS_JSON, "r", encoding="utf-8") as f:
                hazards = json.load(f)
        except Exception:
            pass

    # 3. Generate Broadcast Stories
    feed_items = []

    # Weather bulletin
    for h in hazards:
        feed_items.append({
            "type": "COSMIC_WEATHER_ALERT",
            "priority": "HIGH",
            "headline": f"NAV-HAZARD: {h['event_type']} reported in Sector {h['origin_sector']}",
            "body": f"The Galactic Transit Bureau advises all deep-space vessels within {h['blast_radius']} sectors to secure heat exchangers and engage auxiliary inertial dampers. Source: {h['source_book']}.",
            "timestamp_gut": h.get("start_gut", 100)
        })

    # News Wire from Diary
    for ev in recent_events[-4:]:
        feed_items.append({
            "type": "GALACTIC_NEWS_WIRE",
            "priority": "NORMAL",
            "headline": f"UPDATE: {ev['hero']} ({ev['book']}) completes mission",
            "body": f"Reports from the local observatory confirm: {ev['action']}",
            "timestamp_gut": ev["gut"]
        })

    # Default ambient broadcasts if list is short
    if len(feed_items) < 3:
        feed_items.append({
            "type": "COMMERCE_DISPATCH",
            "priority": "LOW",
            "headline": "Meridian Trade Route: Brass and Crystal Cargo Clearing",
            "body": "Astrolabe gear transports report smooth synchronization across the equatorial orbital rings.",
            "timestamp_gut": "GUT 100"
        })
        feed_items.append({
            "type": "RADIO_INTERCEPT",
            "priority": "LOW",
            "headline": "Subspace Chime Detected on 144.2 MHz",
            "body": "'...steady signal locked on the southern dunes... all relays green... over.'",
            "timestamp_gut": "GUT 100"
        })

    return {
        "network": "Galactic News Network (GNN) & Subspace Relay Net",
        "total_bulletins": len(feed_items),
        "bulletins": feed_items
    }

def generate_radio_intercept(book_id):
    book_id = int(book_id)
    return {
        "channel": f"Subspace Relay 144.{book_id:02d} MHz",
        "signal_strength": "94% (High Clarity)",
        "transcript": [
            f"[Observatory Dispatch]: Calling all Sector stations, this is Relay {book_id:02d}.",
            f"[Flight Control]: We copy your beacon pulse loud and clear. Confluence Wavefront is steady.",
            f"[Observatory Dispatch]: Understood. Proceeding with standard round-robin rotation. Over."
        ]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Subspace Broadcast Network")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("feed", help="Get live galactic news wire and alerts")
    r_p = subparsers.add_parser("radio", help="Generate cockpit radio intercept transcript")
    r_p.add_argument("--book", type=int, default=1)

    args = parser.parse_args()

    if args.command == "radio":
        print(json.dumps(generate_radio_intercept(args.book), indent=2))
    else:
        print(json.dumps(get_broadcast_feed(), indent=2))
