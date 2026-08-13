#!/usr/bin/env python3
"""
Dynamic Celestial Ephemeris & Spatial Propagation Engine for The Stellar Confluence Universe
Computes planetary axial rotation, orbital revolution cycles, and interstellar starship transit
vectors across Galactic Universal Time (GUT).
"""

import os
import sys
import json
import re
import math
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
COSMIC_CLOCKWORK_MD = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")

# Celestial Mechanics Angular Velocity Defaults (degrees per 1 GUT tick)
ROTATION_RATES = {
    "SURFACE": 15.0,        # Planetary axial spin (e.g. 24 GUT = 360° day/night cycle)
    "ORBITAL": 60.0,        # Low-orbit velocity (e.g. 6 GUT = 360° orbit)
    "DEEP_SPACE_TRANSIT": 0.0,  # Fixed heading vector relative to Wavefront
    "GATEWAY_SUBSPACE": 0.0     # Subspace isolation
}

def parse_sector(sector_str):
    """Parses '[X, Y, Z]' string into a float tuple."""
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", sector_str)]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def format_sector(x, y, z):
    return f"[{round(x, 1):g}, {round(y, 1):g}, {round(z, 1):g}]"

def normalize_angle_to_wavefront(raw_angle):
    """Normalizes raw 0-360 orbital/axial angle to 0-180 Wavefront alignment angle."""
    deg = abs(raw_angle) % 360.0
    if deg > 180.0:
        deg = 360.0 - deg
    return round(deg, 1)

def compute_resonance_state(angle_deg, loc_type):
    loc_clean = loc_type.upper().strip()
    if loc_clean == "GATEWAY_SUBSPACE":
        return "GATEWAY_SUBSPACE", "Neutral Subspace Baseline (No buffs/debuffs)"
    
    if 0 <= angle_deg <= 30:
        state = "PEAK_FACING"
        desc = "Super-charged Wavefront alignment; equipment heat dissipation required"
    elif 150 <= angle_deg <= 180:
        state = "SHADOW_FACING"
        desc = "Planetary occlusion / Eclipse lock; physical or auxiliary power only"
    else:
        state = "TRANSIT_FACING"
        desc = "Harmonic baseline; stable energy usage"

    if loc_clean == "DEEP_SPACE_TRANSIT":
        desc = f"[Deep-Space 2x Volatility] {desc}"

    return state, desc

def propagate_ephemeris(current_gut, target_gut, save=False):
    """Propagates all character positions and angles from current_gut to target_gut."""
    delta_gut = target_gut - current_gut
    if not os.path.exists(COSMIC_CLOCKWORK_MD):
        return {"error": "cosmic_clockwork.md does not exist"}

    with open(COSMIC_CLOCKWORK_MD, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    header_lines = []
    data_rows = []
    updated_records = []

    for line in lines:
        if not line.strip().startswith("|") or "GUT" in line or ":---" in line:
            header_lines.append(line)
            continue

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 8:
            continue

        gut_str, book_id, char, loc_type, sector_str, facing_str, res_state, cap = parts[:8]
        loc_clean = loc_type.replace("`", "").strip().upper()
        
        # Parse current facing angle
        angle_match = re.search(r"([\d\.]+)", facing_str)
        curr_angle = float(angle_match.group(1)) if angle_match else 0.0

        # Compute new facing angle based on velocity
        rate = ROTATION_RATES.get(loc_clean, 0.0)
        raw_new_angle = curr_angle + (rate * delta_gut)
        new_angle = normalize_angle_to_wavefront(raw_new_angle)

        new_res_state, new_cap = compute_resonance_state(new_angle, loc_clean)

        updated_row = f"| {target_gut} | {book_id} | {char} | `{loc_clean}` | {sector_str} | {new_angle}° | `{new_res_state}` | {new_cap} |\n"
        data_rows.append(updated_row)
        
        updated_records.append({
            "book_id": book_id,
            "character": char,
            "loc_type": loc_clean,
            "sector": sector_str,
            "previous_angle": curr_angle,
            "new_angle": new_angle,
            "resonance_state": new_res_state
        })

    if save:
        with open(COSMIC_CLOCKWORK_MD, "w", encoding="utf-8") as f:
            f.writelines(header_lines)
            f.writelines(data_rows)

    return {
        "previous_gut": current_gut,
        "new_gut": target_gut,
        "delta_gut": delta_gut,
        "total_characters_propagated": len(updated_records),
        "records": updated_records,
        "saved": save
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Propagate Celestial Ephemeris across GUT")
    parser.add_argument("--current-gut", type=int, default=100, help="Current GUT tick")
    parser.add_argument("--advance-by", type=int, default=1, help="Advance GUT by N ticks")
    parser.add_argument("--save", action="store_true", help="Save updated state to cosmic_clockwork.md")
    
    args = parser.parse_args()
    target = args.current_gut + args.advance_by
    res = propagate_ephemeris(args.current_gut, target, save=args.save)
    print(json.dumps(res, indent=2))
