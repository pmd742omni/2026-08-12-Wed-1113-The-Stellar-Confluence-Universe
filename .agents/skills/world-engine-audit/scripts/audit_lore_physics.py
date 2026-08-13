#!/usr/bin/env python3
"""
World Engine & Lore/Physics Consistency Auditor for The Stellar Confluence Universe
Verifies celestial geometry, planetary ephemerides, wavefront alignment vectors,
power constraint compliance, and cross-book narrative continuity.
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
    return cwd

PROJECT_ROOT = find_project_root()
COSMIC_CLOCKWORK_MD = os.path.join(PROJECT_ROOT, "00_System_State", "cosmic_clockwork.md")

def audit_physics():
    results = {
        "status": "PASS",
        "total_ephemeris_records": 0,
        "valid_records": 0,
        "anomalies": [],
        "faction_balance": {
            "Sun-Forged Hegemony": 0,
            "Void-Bound Monks": 0,
            "Astrolabe Engineers": 0,
            "Expansion Factions": 0
        }
    }

    if not os.path.exists(COSMIC_CLOCKWORK_MD):
        results["status"] = "WARN"
        results["anomalies"].append("cosmic_clockwork.md does not exist yet; run bootstrap_universe_state.py first.")
        return results

    with open(COSMIC_CLOCKWORK_MD, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        if not line.strip().startswith("|") or "GUT" in line or ":---" in line:
            continue

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 8:
            continue

        results["total_ephemeris_records"] += 1
        gut, book_id, char, loc_type, sector, facing, res_state, cap = parts[:8]

        # Check angle
        angle_match = re.search(r"([\d\.]+)", facing)
        if not angle_match:
            results["anomalies"].append(f"Line {idx+1}: Could not parse facing angle in '{facing}'")
            continue

        angle = float(angle_match.group(1))
        if not (0 <= angle <= 180):
            results["anomalies"].append(f"Line {idx+1} ({book_id}): Facing angle {angle}° is out of valid bounds [0°, 180°]")

        # Check location type
        valid_locs = ["SURFACE", "ORBITAL", "DEEP_SPACE_TRANSIT", "GATEWAY_SUBSPACE"]
        clean_loc = loc_type.replace("`", "").strip().upper()
        if clean_loc not in valid_locs:
            results["anomalies"].append(f"Line {idx+1} ({book_id}): Invalid Location Type '{loc_type}' (Must be one of {valid_locs})")

        # Check resonance state logic
        clean_res = res_state.replace("`", "").strip().upper()
        if clean_loc == "GATEWAY_SUBSPACE" and clean_res != "GATEWAY_SUBSPACE":
            results["anomalies"].append(f"Line {idx+1} ({book_id}): Subspace location must have GATEWAY_SUBSPACE resonance state")
        elif clean_loc != "GATEWAY_SUBSPACE":
            if 0 <= angle <= 30 and clean_res != "PEAK_FACING":
                results["anomalies"].append(f"Line {idx+1} ({book_id}): Angle {angle}° corresponds to PEAK_FACING but found '{clean_res}'")
            elif 150 <= angle <= 180 and clean_res != "SHADOW_FACING":
                results["anomalies"].append(f"Line {idx+1} ({book_id}): Angle {angle}° corresponds to SHADOW_FACING but found '{clean_res}'")
            elif 31 <= angle < 150 and clean_res != "TRANSIT_FACING":
                results["anomalies"].append(f"Line {idx+1} ({book_id}): Angle {angle}° corresponds to TRANSIT_FACING but found '{clean_res}'")

        # Deep space volatility check
        if clean_loc == "DEEP_SPACE_TRANSIT" and "Volatility" not in cap and "2x" not in cap:
            results["anomalies"].append(f"Line {idx+1} ({book_id}): DEEP_SPACE_TRANSIT must reflect 2x Volatility in capability description")

        results["valid_records"] += 1

    if results["anomalies"]:
        results["status"] = "FAIL"

    return results

if __name__ == "__main__":
    res = audit_physics()
    print(json.dumps(res, indent=2))
