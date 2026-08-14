#!/usr/bin/env python3
"""
74-World Planetary Ecology, Astrophysics & Resource Dependency Matrix
Catalogs gravity levels (g), atmospheric compositions, diurnal cycle lengths (GUT),
ecological biomes, key resource exports, and trade vulnerabilities across all 74 homeworlds.
"""

import os
import sys
import json
import argparse

PLANETARY_CATALOG = {
    "Helios Prime": {
        "world_name": "Helios Prime",
        "primary_faction": "Sun-Forged Hegemony",
        "astrophysics": {
            "stellar_type": "Binary F-Type Stars (Solaria & Vesperis)",
            "surface_gravity_g": 1.02,
            "atmospheric_pressure_atm": 1.10,
            "atmosphere_mix": "76% N2, 21% O2, 2.5% Ar, 0.5% Solar Ionized Trace",
            "diurnal_cycle_gut": 24,
            "axial_tilt_deg": 4.5
        },
        "biome": "Expansive Copper Sand Dunes, High Basalt Mesas, Glass-Fused Canyons",
        "key_exports": ["Sol-Core Focusing Crystals", "Photonic Prism Glass", "Refined Thermal Alloys"],
        "critical_vulnerabilities": ["Acute freshwater scarcity", "Solar storm thermal surges at Zenith facing"],
        "trade_synergies": ["Imports precision brass gears from Aethelgard", "Imports cryo-coolant from Gliesia"]
    },
    "Umbra Chasm": {
        "world_name": "Umbra Chasm (Nadir Prime)",
        "primary_faction": "Void-Bound Monks",
        "astrophysics": {
            "stellar_type": "Dim M-Class Dwarf (Tidally Locked Eclipse Moon)",
            "surface_gravity_g": 0.88,
            "atmospheric_pressure_atm": 0.95,
            "atmosphere_mix": "80% N2, 18% O2, 2% Umbral Trace Gases",
            "diurnal_cycle_gut": 36,
            "axial_tilt_deg": 0.0
        },
        "biome": "Deep Basalt Eclipse Chasms, Subterranean Bio-Luminescent Caverns",
        "key_exports": ["Phase-Resonant Basalt", "Nocturnal Glow Lichen", "Sound-Absorbing Cloak Fabrics"],
        "critical_vulnerabilities": ["Zero solar power generation in Nadir shadow", "Extreme hypothermic frost during eclipse lock"],
        "trade_synergies": ["Imports solar batteries from Helios Prime", "Exports raw phase-ore to Astrolabe Guilds"]
    },
    "Aethelgard": {
        "world_name": "Aethelgard Gear-City",
        "primary_faction": "Astrolabe Engineers",
        "astrophysics": {
            "stellar_type": "Equatorial Orbital Ring Artificial World",
            "surface_gravity_g": 1.00,
            "atmospheric_pressure_atm": 1.00,
            "atmosphere_mix": "78% N2, 21% O2, 1% Filtered Mist",
            "diurnal_cycle_gut": 6,
            "axial_tilt_deg": 0.0
        },
        "biome": "Tiered Brass Clockwork Habitations, Flywheel Towers, Steam-Vented Aqueducts",
        "key_exports": ["High-Torque Precision Brass", "Chrono-Astrolabes", "Orbital Stabilizer Gyros"],
        "critical_vulnerabilities": ["Mechanical bearing friction", "Heavy metal alloy exhaustion without mining supply"],
        "trade_synergies": ["Imports heavy ores from Deep-Core Miners", "Exports precision relays to all sectors"]
    },
    "Gliesia": {
        "world_name": "Gliesia Sublimation Tail",
        "primary_faction": "Comet-Riders",
        "astrophysics": {
            "stellar_type": "Hyperbolic Orbit Interstellar Comet Ring",
            "surface_gravity_g": 0.28,
            "atmospheric_pressure_atm": 0.20,
            "atmosphere_mix": "Sublimated H2O Vapor, Methane, Ionized Dust",
            "diurnal_cycle_gut": 12,
            "axial_tilt_deg": 28.0
        },
        "biome": "Glaciated Spires, Blue Vapor Slopes, Ionized Dust Cloud Plumes",
        "key_exports": ["Cryo-Ice Fuel Core", "Sublimation Thruster Gas", "Cosmic Dust Filters"],
        "critical_vulnerabilities": ["Atmospheric ablation near perihelion", "Weak surface gravity requires magnetic boots"],
        "trade_synergies": ["Exports coolant to Helios Prime Sun-Forges", "Imports structural alloy frames from Aethelgard"]
    }
}

def get_planetary_profile(world_or_book_id):
    query_str = str(world_or_book_id).strip()
    
    # Check by exact/partial world name
    for k, v in PLANETARY_CATALOG.items():
        if query_str.lower() in k.lower():
            return v

    # Procedural generation for remaining 70 worlds
    try:
        book_num = int(query_str)
    except ValueError:
        book_num = 42

    grav = round(0.6 + ((book_num % 10) * 0.08), 2)
    cycle = 10 + (book_num % 30)

    return {
        "world_name": f"Sector World #{book_num:02d}",
        "primary_faction": "Expansion Factions",
        "astrophysics": {
            "stellar_type": "G-Type Solar Primary",
            "surface_gravity_g": grav,
            "atmospheric_pressure_atm": 1.0,
            "atmosphere_mix": "Standard Breathable Mix",
            "diurnal_cycle_gut": cycle,
            "axial_tilt_deg": 12.5
        },
        "biome": "Crystalline Terraces and Flowing Mineral Rivers",
        "key_exports": [f"Sector Mineral Relic #{book_num:02d}", "Harmonic Conductor Dust"],
        "critical_vulnerabilities": ["Confluence Wavefront tidal oscillations"],
        "trade_synergies": ["Linked to regional Gateway Transit routes"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Planetary Ecology & Resource Matrix")
    parser.add_argument("--world", default="Helios Prime", help="World name or Book ID number")

    args = parser.parse_args()
    res = get_planetary_profile(args.world)
    print(json.dumps(res, indent=2))
