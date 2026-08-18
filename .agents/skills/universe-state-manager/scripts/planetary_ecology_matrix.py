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
    },
    "Vapor-Spire Station": {
        "world_name": "Vapor-Spire Station (Nebula Loom)",
        "primary_faction": "Nebula-Weavers",
        "astrophysics": {
            "stellar_type": "Diffuse Ionized Emission Nebula Belt",
            "surface_gravity_g": 0.35,
            "atmospheric_pressure_atm": 0.45,
            "atmosphere_mix": "Ionized Hydrogen, Helium, Luminescent Plasma Vapors",
            "diurnal_cycle_gut": 18,
            "axial_tilt_deg": 14.0
        },
        "biome": "Suspended Magnetic Loom Rigging, Phosphor Cloud Silks, Floating Gas Anchor Spires",
        "key_exports": ["Plasma Silk Filaments", "Electromagnetic Web Nets", "Ionized Gas Filters"],
        "critical_vulnerabilities": ["Vulnerable to coronal mass ejection burns", "Gas dispersal during solar winds"],
        "trade_synergies": ["Imports magnetic alloys from Deep-Core Miners", "Exports sensory filaments to Chrono-Navigators"]
    },
    "Cimmerian Core": {
        "world_name": "Cimmerian Deep Core",
        "primary_faction": "Deep-Core Miners",
        "astrophysics": {
            "stellar_type": "Dense Iron-Core Planet (High Basalt Mantle)",
            "surface_gravity_g": 1.45,
            "atmospheric_pressure_atm": 2.20,
            "atmosphere_mix": "70% N2, 18% CO2, 10% O2, 2% Sulfur Trace",
            "diurnal_cycle_gut": 48,
            "axial_tilt_deg": 2.0
        },
        "biome": "Subterranean Magma Piston Vaults, Basalt Stratum Shafts, Geothermal Steam Wells",
        "key_exports": ["Dense Basalt Ore", "Tectonic Hydraulic Fluid", "Geothermal Core Cells"],
        "critical_vulnerabilities": ["Thermal overpressure ruptures", "High gravity fatigue for foreign starfarers"],
        "trade_synergies": ["Exports raw metals to Aethelgard Gear-City", "Imports atmospheric filters from Helios Prime"]
    },
    "Acro-Singularity Ring": {
        "world_name": "Acro-Singularity Gravity Ring",
        "primary_faction": "Gravity-Surfers",
        "astrophysics": {
            "stellar_type": "Micro-Black Hole Orbital Accretion Disk",
            "surface_gravity_g": 0.90,
            "atmospheric_pressure_atm": 0.85,
            "atmosphere_mix": "Standard Pressurized Habitat Rings",
            "diurnal_cycle_gut": 8,
            "axial_tilt_deg": 45.0
        },
        "biome": "Curved Graviton Slopes, Singularity Launch Piers, Inertial Wave Arcs",
        "key_exports": ["Graviton Well Anchors", "Inertial Dampener Fluid", "Metric Dial Compasses"],
        "critical_vulnerabilities": ["Tidal shear stress", "Accretion flare disruptions"],
        "trade_synergies": ["Exports rapid transit slingshots", "Imports high-density alloys from Deep-Core Miners"]
    },
    "Coronaria Prominence": {
        "world_name": "Coronaria Solar Forge Platform",
        "primary_faction": "Plasma-Shepherds",
        "astrophysics": {
            "stellar_type": "Stellar Coronal Orbit Station",
            "surface_gravity_g": 0.75,
            "atmospheric_pressure_atm": 0.50,
            "atmosphere_mix": "Shielded Habitat Nitrogen-Oxygen Matrix",
            "diurnal_cycle_gut": 4,
            "axial_tilt_deg": 0.0
        },
        "biome": "Magnetic Lasso Tether Platforms, Roaring Plasma Flocks, Thermal Radiator Fins",
        "key_exports": ["Bottled Solar Plasma", "Coronal Magnetic Coils", "High-Energy Thermal Cells"],
        "critical_vulnerabilities": ["Magnetic field destabilization", "Extreme radiant heat exposure"],
        "trade_synergies": ["Exports bottled energy cells to Void-Bound Monks", "Imports cryo-insulators from Gliesia"]
    },
    "Chrono-Lagoon": {
        "world_name": "Chrono-Lagoon Tide World",
        "primary_faction": "Chrono-Navigators",
        "astrophysics": {
            "stellar_type": "Subspace Conduit Anchored Star System",
            "surface_gravity_g": 0.95,
            "atmospheric_pressure_atm": 1.05,
            "atmosphere_mix": "78% N2, 21% O2, 1% Tachyon Trace",
            "diurnal_cycle_gut": 20,
            "axial_tilt_deg": 8.0
        },
        "biome": "Luminous Tidal Shallows, Crystalline Chrono-Dials, Temporal Sextant Towers",
        "key_exports": ["Tachyon Chrono-Crystals", "Optimal Transit Route Charts", "Probability Lenses"],
        "critical_vulnerabilities": ["Subspace temporal drift", "Wavefront interference waves"],
        "trade_synergies": ["Exports stellar navigation telemetry to all 74 sectors", "Imports precision brass chronometers from Aethelgard"]
    },
    "Verdant Canopy": {
        "world_name": "Verdant Canopy World",
        "primary_faction": "Bio-Alchemists",
        "astrophysics": {
            "stellar_type": "Warm G-Class Star with High UV Spectrum",
            "surface_gravity_g": 0.98,
            "atmospheric_pressure_atm": 1.15,
            "atmosphere_mix": "74% N2, 24% O2, 2% Bioluminescent Spore Vapor",
            "diurnal_cycle_gut": 28,
            "axial_tilt_deg": 10.0
        },
        "biome": "Bioluminescent Great Canopies, Spore Gardens, Symbiotic Root Aqueducts",
        "key_exports": ["Medicinal Spore Salves", "Photosynthetic Chitin Armor", "Living Seed Pods"],
        "critical_vulnerabilities": ["Dehydration during high Zenith heatwaves", "Parasitic blight outbreaks"],
        "trade_synergies": ["Exports healing balms and oxygen canisters", "Imports focusing prism lenses from Helios Prime"]
    }
}

PROCEDURAL_BIOME_ARCHETYPES = [
    {"biome": "Crystalline Terraces and Flowing Mineral Rivers", "export": "Harmonic Quartz Prisms"},
    {"biome": "Bioluminescent Deep-Fjord Coastlines", "export": "Luminescent Sea Spores"},
    {"biome": "Basalt Volcanic Plateaus & Steam Geysers", "export": "Refined Geothermal Ingots"},
    {"biome": "Sub-Zero Glaciated Mountain Rifts", "export": "High-Density Cryo-Ice"},
    {"biome": "Magnetic Desert Spires & Copper Arches", "export": "Polarized Sand Crystals"},
    {"biome": "Suspended Orbital Ring Habitats & Cloud Bridges", "export": "Precision Atmospheric Regulators"}
]

def get_planetary_profile(world_or_book_id):
    query_str = str(world_or_book_id).strip()
    
    # Check by exact/partial world name
    for k, v in PLANETARY_CATALOG.items():
        if query_str.lower() in k.lower() or k.lower() in query_str.lower():
            return v

    # Procedural generation for remaining worlds
    try:
        book_num = int(query_str)
    except ValueError:
        book_num = 42

    grav = round(0.6 + ((book_num % 10) * 0.08), 2)
    cycle = 10 + (book_num % 30)
    archetype = PROCEDURAL_BIOME_ARCHETYPES[book_num % len(PROCEDURAL_BIOME_ARCHETYPES)]

    return {
        "world_name": f"Sector World #{book_num:02d}",
        "primary_faction": "Sector Exploration Faction",
        "astrophysics": {
            "stellar_type": "G-Type Solar Primary",
            "surface_gravity_g": grav,
            "atmospheric_pressure_atm": 1.0,
            "atmosphere_mix": "Standard Breathable Mix",
            "diurnal_cycle_gut": cycle,
            "axial_tilt_deg": round(5.0 + (book_num % 20), 1)
        },
        "biome": archetype["biome"],
        "key_exports": [archetype["export"], f"Sector Mineral Relic #{book_num:02d}"],
        "critical_vulnerabilities": ["Confluence Wavefront tidal oscillations"],
        "trade_synergies": ["Linked to regional Gateway Transit routes"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Planetary Ecology & Resource Matrix")
    parser.add_argument("--world", default="Helios Prime", help="World name or Book ID number")

    args = parser.parse_args()
    res = get_planetary_profile(args.world)
    print(json.dumps(res, indent=2))
