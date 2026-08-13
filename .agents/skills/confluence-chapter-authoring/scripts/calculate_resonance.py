#!/usr/bin/env python3
"""
Resonance & Capability Constraints Calculator for The Stellar Confluence Universe
Computes angular facing alignment (0° - 180°), location modifier, faction-specific power capabilities,
and active physical constraints for chapter authoring.
"""

import sys
import json
import argparse

def calculate_resonance(facing_angle, faction, loc_type):
    # Normalize facing angle to 0 - 180
    angle = abs(float(facing_angle)) % 360
    if angle > 180:
        angle = 360 - angle

    loc_upper = loc_type.upper().strip()
    faction_clean = faction.strip()
    faction_lower = faction_clean.lower()

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

    # Deep space volatility modifier
    is_deep_space = (loc_upper == "DEEP_SPACE_TRANSIT")
    is_orbital = (loc_upper == "ORBITAL")
    is_surface = (loc_upper == "SURFACE")

    # Faction capability and limitation logic
    if "sun" in faction_lower or "radiant" in faction_lower:
        faction_category = "Sun-Forged Hegemony"
        if state == "PEAK_FACING":
            buff = "SUPER-CHARGED: High-intensity solar beam output, blinding luminous radiance, long-range thermal projection."
            debuff = "OVERHEAT RISK: Lenses and power armor heat rapidly; equipment burns out or melts if unchanneled."
        elif state == "SHADOW_FACING":
            buff = "NONE: Solar lenses produce zero beam output. Powered armor shuts down into lock."
            debuff = "ECLIPSE LOCK: Must rely strictly on stored kinetic springs, auxiliary battery cells, or physical bravery."
        elif state == "TRANSIT_FACING":
            buff = "HARMONIC BASELINE: Stable, predictable radiant beams, moderate heat, steady thermal shields."
            debuff = "STANDARD LIMIT: Cannot sustain maximum burst output without overheating."
        else:
            buff = "SUBSPACE BASELINE: Standard kinetic & auxiliary capabilities; light-magic dampened."
            debuff = "DISCONNECTED: No natural solar recharge available."

    elif "void" in faction_lower or "shadow" in faction_lower or "monk" in faction_lower:
        faction_category = "Void-Bound Monks"
        if state == "PEAK_FACING":
            buff = "NONE: Shadow constructs dissolve under radiant pressure."
            debuff = "SEVERELY SUPPRESSED: Stealth cloaks fail, shadow-stepping disabled. Must rely purely on physical grit and melee weapons."
        elif state == "SHADOW_FACING":
            buff = "APEX SHADOW SURGE: Phase-shift through solid rock, weave dense shadow-cloaks, bend light completely around self."
            debuff = "COLD ACCELERATION: Deep shadow draws warmth from character's body; prolonged use induces frost exhaustion."
        elif state == "TRANSIT_FACING":
            buff = "HARMONIC BASELINE: Controlled short-range shadow tendrils, reliable stealth in dim cover."
            debuff = "STANDARD LIMIT: Cannot phase through thick composite materials."
        else:
            buff = "SUBSPACE BASELINE: Stable stealth mechanics without celestial interference."
            debuff = "NEUTRAL SHADOW: No apex surge potential."

    elif "astrolabe" in faction_lower or "engineer" in faction_lower or "gear" in faction_lower:
        faction_category = "Astrolabe Engineers"
        if state == "PEAK_FACING":
            buff = "HYPER-EFFICIENT: Crystalline gear arrays spin effortlessly with zero kinetic friction and instant torque."
            debuff = "CENTRIFUGAL STRESS: Extreme rotation speeds require precise timing to avoid throwing gears off axis."
        elif state == "SHADOW_FACING":
            buff = "HIGH-TORQUE POTENTIAL: Flywheel momentum can be discharged in heavy bursts."
            debuff = "MECHANICAL DRAG: High rotational resistance; gears feel heavy, must hand-crank flywheels or draw thermal battery."
        elif state == "TRANSIT_FACING":
            buff = "HARMONIC BASELINE: Predictable mechanical clockwork, smooth gear operation, steady chronometer synchronization."
            debuff = "STANDARD LIMIT: Power output bounded by physical flywheel storage capacity."
        else:
            buff = "SUBSPACE BASELINE: Standard mechanical gear systems function normally."
            debuff = "CHRONO-DRIFT: Subspace currents require frequent astrolabe recalibration."

    else:
        faction_category = f"Expansion Faction: {faction_clean}"
        if state == "PEAK_FACING":
            buff = "WAVEFRONT SURGE: Elemental/gravitational powers amplified by cosmic radiant vector."
            debuff = "STRESS SURGE: Power systems operate near critical threshold; tight control required."
        elif state == "SHADOW_FACING":
            buff = "NIGHT SURGE / INERTIAL FOCUS: Gravitational/inertial manipulation operates without radiant interference."
            debuff = "ENERGY STARVATION: Radiant-derived systems are powerless; rely on stored kinetic/chemical reserves."
        elif state == "TRANSIT_FACING":
            buff = "HARMONIC BASELINE: Balanced elemental control, predictable energy consumption."
            debuff = "STANDARD LIMIT: Standard physical stamina constraints."
        else:
            buff = "SUBSPACE BASELINE: Standard baseline operation."
            debuff = "SUBSPACE DAMPING: Advanced cosmic resonance techniques are muted."

    # Apply deep space environmental volatility
    if is_deep_space:
        buff = f"[UNFILTERED DEEP-SPACE VOLATILITY 2x BUFF] {buff}"
        debuff = f"[UNFILTERED DEEP-SPACE VOLATILITY 2x DIFFICULTY] Control is 2x harder. {debuff} Accidental misuse risks hull breaches!"

    return {
        "faction_input": faction_clean,
        "faction_category": faction_category,
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
    parser.add_argument("--faction", type=str, default="Sun-Forged", help="Faction name (e.g. Sun-Forged, Void-Bound, Astrolabe, Comet-Rider)")
    parser.add_argument("--loc", type=str, default="SURFACE", help="Location type (SURFACE, ORBITAL, DEEP_SPACE_TRANSIT, GATEWAY_SUBSPACE)")
    
    args = parser.parse_args()
    res = calculate_resonance(args.facing, args.faction, args.loc)
    print(json.dumps(res, indent=2))
