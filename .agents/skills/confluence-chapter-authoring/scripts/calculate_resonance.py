#!/usr/bin/env python3
"""
Resonance & Capability Constraints Calculator for The Stellar Confluence Universe
Integrates with the Faction Physics Matrix to compute angular alignment, location modifiers,
deep-space volatility, and distinct faction power limits.
"""

import sys
import json
import argparse
import os

# Ensure faction_matrix is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from faction_matrix import get_faction_profile

def calculate_resonance(facing_angle, faction, loc_type):
    # Normalize facing angle to 0 - 180
    angle = abs(float(facing_angle)) % 360
    if angle > 180:
        angle = 360 - angle

    loc_upper = loc_type.upper().strip()
    faction_clean = faction.strip()

    # Determine Base Resonance State
    if loc_upper == "GATEWAY_SUBSPACE":
        state = "GATEWAY_SUBSPACE"
        resonance_val = 0.5
        facing_desc = "Subspace Void (Disconnected from Wavefront)"
    elif 0 <= angle <= 30:
        state = "PEAK_FACING"
        resonance_val = 1.0 - (angle / 60.0)
        facing_desc = f"Direct Zenith Facing ({angle:.1f}° Alignment)"
    elif 150 <= angle <= 180:
        state = "SHADOW_FACING"
        resonance_val = (180 - angle) / 60.0
        facing_desc = f"Planetary Occlusion / Nadir Facing ({angle:.1f}° Alignment)"
    else:
        state = "TRANSIT_FACING"
        resonance_val = 0.5
        facing_desc = f"Horizon / Twilight Facing ({angle:.1f}° Alignment)"

    is_deep_space = (loc_upper == "DEEP_SPACE_TRANSIT")

    # Fetch rich faction physics profile
    f_info = get_faction_profile(faction_clean)
    matched_faction = f_info["matched_name"]
    profile = f_info["profile"]

    if state == "PEAK_FACING":
        buff = profile["peak_facing"]["buff"]
        debuff = profile["peak_facing"]["debuff"]
    elif state == "SHADOW_FACING":
        buff = profile["shadow_facing"]["buff"]
        debuff = profile["shadow_facing"]["debuff"]
    elif state == "TRANSIT_FACING":
        buff = profile["transit_facing"]["buff"]
        debuff = profile["transit_facing"]["debuff"]
    else: # GATEWAY_SUBSPACE
        buff = f"SUBSPACE BASELINE: {profile.get('subspace', 'Standard baseline operation')}"
        debuff = "SUBSPACE DISCONNECTION: Cosmic Wavefront buffs are completely neutralized (Re = 0.5)."

    # Apply deep space environmental volatility
    if is_deep_space:
        buff = f"[UNFILTERED DEEP-SPACE VOLATILITY 2x BUFF] {buff}"
        debuff = f"[UNFILTERED DEEP-SPACE VOLATILITY 2x DIFFICULTY] Control is 2x harder. {debuff} Accidental misuse risks hull breaches!"

    return {
        "faction_input": faction_clean,
        "matched_faction": matched_faction,
        "faction_domain": profile.get("domain", ""),
        "energy_medium": profile.get("energy_medium", ""),
        "signature_gear": profile.get("signature_gear", ""),
        "tactical_style": profile.get("tactical_style", ""),
        "location_type": loc_upper,
        "facing_angle_deg": angle,
        "facing_description": facing_desc,
        "resonance_state": state,
        "resonance_factor": round(resonance_val, 3),
        "is_deep_space_volatile": is_deep_space,
        "power_capability": buff,
        "active_limitation": debuff,
        "narrative_hook": f"Hero operates under {state} ({angle:.1f}°). Capabilities: {buff} Limitations: {debuff}"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Stellar Confluence Resonance & Power Constraints")
    parser.add_argument("--facing", type=float, default=0.0, help="Facing angle in degrees relative to Confluence Wavefront (0 - 180)")
    parser.add_argument("--faction", type=str, default="Sun-Forged Hegemony", help="Faction name")
    parser.add_argument("--loc", type=str, default="SURFACE", help="Location type (SURFACE, ORBITAL, DEEP_SPACE_TRANSIT, GATEWAY_SUBSPACE)")
    
    args = parser.parse_args()
    res = calculate_resonance(args.facing, args.faction, args.loc)
    print(json.dumps(res, indent=2))
