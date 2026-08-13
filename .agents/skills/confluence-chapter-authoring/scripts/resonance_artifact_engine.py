#!/usr/bin/env python3
"""
Resonance Artifact Crafting & Power Consumption Engine
Calculates kinetic decay, charge depletion, overheat risk, and state durability
for heroic artifacts (Astrolabe Flywheels, Void Phase-Cloaks, Solar Lenses, Gravity Boards)
under Confluence Wavefront angular facing states.
"""

import sys
import json
import math

ARTIFACT_TEMPLATES = {
    "SOLAR_LENS": {
        "faction": "Sun-Forged Hegemony",
        "base_efficiency": 0.85,
        "max_charge": 100.0,
        "peak_facing_charge_rate": 5.0,
        "shadow_facing_charge_rate": -2.0,
        "overheat_threshold_temp_c": 120.0
    },
    "VOID_CLOAK": {
        "faction": "Void-Bound Monks",
        "base_efficiency": 0.90,
        "max_charge": 100.0,
        "peak_facing_charge_rate": -4.0,
        "shadow_facing_charge_rate": 6.0,
        "overheat_threshold_temp_c": 85.0
    },
    "ASTROLABE_FLYWHEEL": {
        "faction": "Astrolabe Engineers",
        "base_efficiency": 0.95,
        "max_charge": 100.0,
        "peak_facing_charge_rate": 3.0,
        "shadow_facing_charge_rate": 0.5,
        "overheat_threshold_temp_c": 150.0
    },
    "GRAVITY_BOARD": {
        "faction": "Gravity-Surfers",
        "base_efficiency": 0.88,
        "max_charge": 100.0,
        "peak_facing_charge_rate": 4.0,
        "shadow_facing_charge_rate": 1.0,
        "overheat_threshold_temp_c": 110.0
    }
}

def calculate_artifact_performance(artifact_type, facing_angle_deg, current_charge=80.0, ambient_temp_c=25.0):
    """Calculates active power output, overheat risk, and charge delta based on facing angle."""
    template = ARTIFACT_TEMPLATES.get(artifact_type.upper(), ARTIFACT_TEMPLATES["SOLAR_LENS"])
    
    # Angle physics (0 = Zenith Peak, 90 = Baseline, 180 = Nadir Shadow)
    rad = math.radians(facing_angle_deg)
    zenith_factor = math.cos(rad) # 1.0 at peak, 0 at 90, -1 at 180
    
    if zenith_factor > 0.5:
        resonance_zone = "PEAK_FACING"
        charge_delta = template["peak_facing_charge_rate"]
        temp_delta = 15.0 * zenith_factor
    elif zenith_factor < -0.5:
        resonance_zone = "SHADOW_FACING"
        charge_delta = template["shadow_facing_charge_rate"]
        temp_delta = -5.0 * abs(zenith_factor)
    else:
        resonance_zone = "TRANSIT_FACING"
        charge_delta = (template["peak_facing_charge_rate"] + template["shadow_facing_charge_rate"]) / 2.0
        temp_delta = 2.0

    new_charge = max(0.0, min(template["max_charge"], current_charge + charge_delta))
    new_temp = ambient_temp_c + temp_delta
    
    overheat_risk_pct = round(max(0.0, min(100.0, ((new_temp / template["overheat_threshold_temp_c"]) ** 2) * 60.0)), 1)
    power_output_kw = round(50.0 * template["base_efficiency"] * (1.0 + zenith_factor * 0.5), 2)
    
    return {
        "artifact_type": artifact_type.upper(),
        "facing_angle_deg": facing_angle_deg,
        "resonance_zone": resonance_zone,
        "power_output_kw": power_output_kw,
        "previous_charge": current_charge,
        "new_charge": round(new_charge, 1),
        "charge_delta_per_gut": charge_delta,
        "operating_temp_c": round(new_temp, 1),
        "overheat_threshold_c": template["overheat_threshold_temp_c"],
        "overheat_risk_pct": overheat_risk_pct,
        "status": "OVERHEAT_WARNING" if overheat_risk_pct > 80.0 else "NOMINAL"
    }

if __name__ == "__main__":
    art = sys.argv[1] if len(sys.argv) > 1 else "SOLAR_LENS"
    angle = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0
    print(json.dumps(calculate_artifact_performance(art, angle), indent=2))
