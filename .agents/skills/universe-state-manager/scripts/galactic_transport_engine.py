#!/usr/bin/env python3
"""
Galactic Transport & Multi-Scale Mobility Engine for The Stellar Confluence Universe
Models the complete 4-tier galactic transport taxonomy:
- Tier 1: Intra-Planetary (Atmospheric Skimmers, Sand-Sails, Thermal Ridge Gliders, Benthic Crawlers, Mag-Levs, Sky-Hooks, Geothermal Elevators)
- Tier 2: System-Level / Interplanetary (Solar-Sail Cutters, Ion Freighters, Magnetic Catapult Slingers, Interplanetary Cycler Ships, Fusion Tugs, Coronal Scoopers)
- Tier 3: Interstellar (Confluence Wave-Riders, Subspace Jump-Gates, Tachyon Slipstream Corvettes, Void-Corridor Phase Shuttles, Dyson Accelerator Slingshots)
- Tier 4: Intergalactic / Deep Cosmos (Dark-Matter Drift Caravans, Super-Cluster Relays, Primordial Filament Choirs)
- Cultural & Faction Craft (Astrolabe Gear-Gondolas, Comet-Rider Sublimation Skiffs, Bio-Alchemist Living Manta-Craft, Crystal-Singer Resonant Prism Cruisers, Void Null-Mass Shuttles)

Provides propulsion physics, velocity profiles, fuel/resonance kinetics, cockpit handling protocols, and sensory pilot experiences.
"""

import os
import sys
import json
import math
import hashlib
import random
import argparse
from typing import Dict, Any, List, Optional

# Transport Taxonomy Catalogs
TRANSPORT_TIERS = {
    "TIER_1_INTRA_PLANETARY": {
        "tier_name": "Intra-Planetary & Atmospheric Transport",
        "scale_scope": "0 to 50,000 km (Surface to Low Planetary Orbit)",
        "typical_velocity_range": "100 km/h to 11.2 km/s (Sub-orbital to Escape Velocity)",
        "vehicles": [
            {
                "vehicle_id": "ATMOSPHERIC_SKIMMER",
                "name": "Solar-Thermal Atmospheric Skimmer",
                "propulsion_type": "Superheated Photonic Ramjet & Magnetic Foil Skids",
                "max_speed_kmh": 2400,
                "passenger_capacity": 6,
                "cargo_capacity_tons": 8,
                "energy_source": "Solarite Photonic Battery & Thermal Lift",
                "cockpit_vibe": "Panoramic tinted brass canopy, rhythmic hum of warm air intakes, smooth magnetic rudder sticks.",
                "handling_protocol": "Angle nose into thermal updrafts; feather port foil during sudden dust squalls.",
                "factions_favored": ["Sun-Forged Hegemony", "Plasma-Shepherds"]
            },
            {
                "vehicle_id": "SAND_SAIL_SKIFF",
                "name": "Copper Dune Sand-Sail Skiff",
                "propulsion_type": "Resonant Aerofoil Masts & Superconducting Ceramic Skis",
                "max_speed_kmh": 180,
                "passenger_capacity": 4,
                "cargo_capacity_tons": 3,
                "energy_source": "Planetary Trade Winds & Piezoelectric Sand Friction",
                "cockpit_vibe": "Open-deck helm, rushing desert breeze, clicking compass pulleys, and the singing sound of metallic dunes.",
                "handling_protocol": "Tack against the wind at 45 degrees; avoid sudden crest drops over razorback dunes.",
                "factions_favored": ["Sun-Forged Hegemony", "Deep-Core Miners"]
            },
            {
                "vehicle_id": "BENTHIC_ABYSSAL_CRAWLER",
                "name": "Bioluminescent Benthic Sea Crawler",
                "propulsion_type": "Multi-Leg Hydraulic Struts & Magneto-Hydrodynamic Thrusters",
                "max_speed_kmh": 60,
                "passenger_capacity": 12,
                "cargo_capacity_tons": 45,
                "energy_source": "Geothermal Heat Exchangers & Symbiotic Algal Cells",
                "cockpit_vibe": "Reinforced sapphire pressure dome, soft emerald bio-glow from exterior floodlights, deep oceanic purr.",
                "handling_protocol": "Maintain equalized ballast; follow bioluminescent spore trails across deep tectonic trenches.",
                "factions_favored": ["Tide-Wardens", "Bio-Alchemists"]
            },
            {
                "vehicle_id": "PLANETARY_MAGLEV_EXPRESS",
                "name": "Vacuum-Tube Meridian Mag-Lev Train",
                "propulsion_type": "Superconducting Magnetic Levitation & Linear Induction Coils",
                "max_speed_kmh": 6500,
                "passenger_capacity": 450,
                "cargo_capacity_tons": 600,
                "energy_source": "Central Planetary Grid & Flywheel Substations",
                "cockpit_vibe": "Silent, frictionless gliding, panoramic displays charting continent crossings, gentle chime of meridian stops.",
                "handling_protocol": "Automated switchback synchronization; monitor flux density during wavefront crossings.",
                "factions_favored": ["Astrolabe Engineers", "Nebula-Weavers"]
            },
            {
                "vehicle_id": "ORBITAL_SKYHOOK_TETHER",
                "name": "Equatorial Orbital Skyhook & Elevator Car",
                "propulsion_type": "Carbon-Nanotube Graphene Cable & Counterweight Traction Winch",
                "max_speed_kmh": 1200,
                "passenger_capacity": 80,
                "cargo_capacity_tons": 250,
                "energy_source": "Orbital Station Kinetic Momentum & Solar Arrays",
                "cockpit_vibe": "Gradual transition from atmospheric blue to star-studded obsidian black, floating sensation of weightlessness.",
                "handling_protocol": "Synchronize ascent speed with planetary rotational velocity; clamp safety brakes if solar wind exceeds 800 km/s.",
                "factions_favored": ["Astrolabe Engineers", "Sun-Forged Hegemony", "Comet-Riders"]
            }
        ]
    },
    "TIER_2_INTERPLANETARY_SYSTEM": {
        "tier_name": "System-Level & Interplanetary Transport",
        "scale_scope": "0.1 AU to 50 AU (Planetary Orbits to Oort Cloud)",
        "typical_velocity_range": "30 km/s to 0.05c (Sub-light Transit & Gravitational Slingshots)",
        "vehicles": [
            {
                "vehicle_id": "SOLAR_SAIL_CUTTER",
                "name": "Prismatic Photonic Solar-Sail Cutter",
                "propulsion_type": "Ultra-Thin Gossamer Reflective Mylar Sails & Ion Verniers",
                "max_speed_c_fraction": 0.02,
                "passenger_capacity": 8,
                "cargo_capacity_tons": 30,
                "energy_source": "Direct Photonic Radiation Pressure & Solar Wind",
                "cockpit_vibe": "Gleaming golden sail rigging, whisper-quiet hull, celestial star charts reflecting across polished glass.",
                "handling_protocol": "Angle sail quadrants to catch solar wind angle theta; trim tension when approaching orbital perihelion.",
                "factions_favored": ["Sun-Forged Hegemony", "Gravity-Surfers"]
            },
            {
                "vehicle_id": "ION_FREIGHTER_CONVOY",
                "name": "Heavy-Haul Xenon-Ion Cargo Cruiser",
                "propulsion_type": "Multi-Grid Hall-Effect Ion Thrusters & Fission Thermal Core",
                "max_speed_c_fraction": 0.01,
                "passenger_capacity": 16,
                "cargo_capacity_tons": 2500,
                "energy_source": "Refined Thorium Core & Large Solar Collector Wings",
                "cockpit_vibe": "Deep, reassuring cobalt engine glow, steady hum of cooling conduits, multi-screen telemetry banks.",
                "handling_protocol": "Plot continuous low-thrust burn vectors; initiate deceleration burn precisely at mid-transit waypoint.",
                "factions_favored": ["Astrolabe Engineers", "Deep-Core Miners", "Commercial Guilds"]
            },
            {
                "vehicle_id": "CORONAL_PLASMA_SCOOPER",
                "name": "Magnetic Prominence Plasma Harvester",
                "propulsion_type": "Magnetic Pinch Funnels & Relativistic Plasma Ejection",
                "max_speed_c_fraction": 0.035,
                "passenger_capacity": 6,
                "cargo_capacity_tons": 120,
                "energy_source": "Harvested Coronal Fusion Plasma",
                "cockpit_vibe": "Blinding exterior flares filtered to cool emerald on helm visors, intense magnetic resonance throbbing in deckplates.",
                "handling_protocol": "Maintain magnetic scoop stability at 1.2 Tesla; never dive deeper than chromosphere boundary zone.",
                "factions_favored": ["Plasma-Shepherds", "Sun-Forged Hegemony"]
            },
            {
                "vehicle_id": "CYCLER_HABITAT_SHIP",
                "name": "Interplanetary Resonant Cycler Station",
                "propulsion_type": "Gravitational Slingshots & Continuous Auxiliary Ion Propulsion",
                "max_speed_c_fraction": 0.015,
                "passenger_capacity": 1200,
                "cargo_capacity_tons": 15000,
                "energy_source": "Central Fusion Engine & Hydroponic Solar Rings",
                "cockpit_vibe": "Spacious rotating gravity ring, peaceful hydroponic parks under glass domes, bustling transit terminals.",
                "handling_protocol": "Perform precise micro-corrections during planetary flybys to preserve perpetual orbit resonance.",
                "factions_favored": ["Astrolabe Engineers", "Bio-Alchemists", "Interstellar Travelers"]
            }
        ]
    },
    "TIER_3_INTERSTELLAR": {
        "tier_name": "Interstellar & Wavefront Transit",
        "scale_scope": "0.1 to 1,000 Light-Years (Sector to Sector)",
        "typical_velocity_range": "0.5c to 50c (Super-luminal Wavefront Surfing & Subspace Fold)",
        "vehicles": [
            {
                "vehicle_id": "CONFLUENCE_WAVE_RIDER",
                "name": "Harmonic Confluence Wave-Rider Corvette",
                "propulsion_type": "Wavefront Compression Fins & Harmonic Resonance Keel",
                "max_speed_c_fraction": 8.5,
                "passenger_capacity": 10,
                "cargo_capacity_tons": 60,
                "energy_source": "Ambient Confluence Wavefront Harmonic Coupling",
                "cockpit_vibe": "Crystalline compass needles spinning in harmonic unison, iridescent glow along the hull seams, surging sensation of cosmic riding.",
                "handling_protocol": "Align ship pitch with wavefront crest angle; throttle power during peak facing to prevent lens burnout.",
                "factions_favored": ["Sun-Forged Hegemony", "Gravity-Surfers", "Crystal-Singers"]
            },
            {
                "vehicle_id": "VOID_PHASE_SHUTTLE",
                "name": "Umbral Void-Corridor Phase Shuttle",
                "propulsion_type": "Subspace Null-Mass Matrix & Basalt Dampening Sails",
                "max_speed_c_fraction": 6.2,
                "passenger_capacity": 8,
                "cargo_capacity_tons": 40,
                "energy_source": "Void-Essence Crystals & Cold Geothermal Cells",
                "cockpit_vibe": "Whisper-silent stealth hull, starlight fading to tranquil velvet indigo, gentle tactile feedback through basalt controls.",
                "handling_protocol": "Slip between gravity wells during nadir facing; keep energy emissions below 5 milliwatts.",
                "factions_favored": ["Void-Bound Monks", "Chrono-Navigators"]
            },
            {
                "vehicle_id": "TACHYON_SLIPSTREAM_FRIGATE",
                "name": "Tachyon Chrono-Slipstream Frigate",
                "propulsion_type": "Tachyon Condenser Coil & Temporal Waveguide Fins",
                "max_speed_c_fraction": 14.0,
                "passenger_capacity": 24,
                "cargo_capacity_tons": 350,
                "energy_source": "Singularity Chrono-Core & Tachyon Sands",
                "cockpit_vibe": "Chronometer dials turning in smooth reverse sync, star trails forming glowing cyan ribbons, crisp electric ozone scent.",
                "handling_protocol": "Maintain temporal phase lock; recalibrate chronometers upon emerging at destination sector.",
                "factions_favored": ["Chrono-Navigators", "Tide-Wardens"]
            },
            {
                "vehicle_id": "DYSON_ACCELERATOR_RUNNER",
                "name": "Dyson Swarm Relativistic Accelerator",
                "propulsion_type": "Focused 100-Gigawatt Laser Arrays & Magnetic Launch Troughs",
                "max_speed_c_fraction": 0.85,
                "passenger_capacity": 100,
                "cargo_capacity_tons": 5000,
                "energy_source": "Direct Dyson Swarm Megastructure Power",
                "cockpit_vibe": "Massive acceleration g-couch support, dazzling laser wake illuminating the cosmos, pinpoint navigation computers.",
                "handling_protocol": "Lock onto destination magnetic deceleration funnel; do not deviate from the photon beam center-line.",
                "factions_favored": ["Astrolabe Engineers", "Sun-Forged Hegemony"]
            }
        ]
    },
    "TIER_4_INTERGALACTIC_DEEP_COSMOS": {
        "tier_name": "Intergalactic & Primordial Scale Mobility",
        "scale_scope": "1,000 to 1,000,000 Light-Years (Across Galactic Arms & Voids)",
        "typical_velocity_range": "100c to Instantaneous Subspace Gateways",
        "vehicles": [
            {
                "vehicle_id": "DARK_MATTER_CARAVAN_BARGE",
                "name": "Primordial Dark-Matter Drift Caravan",
                "propulsion_type": "Dark-Matter Gravitational Anchors & Cosmic Filament Harpoons",
                "max_speed_c_fraction": 50.0,
                "passenger_capacity": 2000,
                "cargo_capacity_tons": 50000,
                "energy_source": "Primordial Filament Resonance & Singularity Anchors",
                "cockpit_vibe": "Deep cosmic tranquility, galaxies appearing as delicate glowing spirals on panoramic viewports, timeless grand scale.",
                "handling_protocol": "Follow cosmic dark matter filaments; coordinate chimes with the galactic choir array.",
                "factions_favored": ["Nebula-Weavers", "Chrono-Navigators", "Crystal-Singers"]
            },
            {
                "vehicle_id": "KEYSTONE_SUB_SPACE_GATEWAY",
                "name": "Keystone Subspace Transit Stargate",
                "propulsion_type": "Wormhole Einstein-Rosen Bridge & Harmonic Acoustic Stabilizers",
                "max_speed_c_fraction": 1000.0,
                "passenger_capacity": 5000,
                "cargo_capacity_tons": 100000,
                "energy_source": "Confluence Keystone & Stellar Core Tap",
                "cockpit_vibe": "Instantaneous transit flash, momentary zero-g harmonic chime, emerging smoothly into a new galactic sector.",
                "handling_protocol": "Transmit harmonic handshake key 30 seconds prior to gateway entry; match approach velocity to 500 m/s.",
                "factions_favored": ["All Factions", "Keystone Guardians"]
            }
        ]
    },
    "CULTURAL_FACTION_CRAFT": {
        "tier_name": "Cultural & Faction Signature Vehicles",
        "scale_scope": "Specialized Multiscale Missions",
        "typical_velocity_range": "Craft Specific",
        "vehicles": [
            {
                "vehicle_id": "ASTROLABE_GEAR_GONDOLA",
                "name": "Clockwork Meridian Gear-Gondola",
                "faction": "Astrolabe Engineers",
                "propulsion_type": "Interlocking Bronze Flywheels & High-Torque Steam Thrusters",
                "specialty": "Ultra-precise station docking, zero-backlash fine maneuvering, heavy structural assembly.",
                "cockpit_vibe": "Polished mahogany and brass dials, ticking escapements, fragrant steam, solid mechanical levers.",
                "handling_protocol": "Wind auxiliary spring before orbital docking; adjust gear ratios smoothly to match rotational speed."
            },
            {
                "vehicle_id": "COMET_SUBLIMATION_SKIFF",
                "name": "Comet-Rider Cryo-Sublimation Skiff",
                "faction": "Comet-Riders",
                "propulsion_type": "Flash-Sublimated Methane Vapor Jets & Thermal Outriggers",
                "specialty": "High-speed comet tail surfing, low-g ice field mining, rapid orbital scouting.",
                "cockpit_vibe": "Frost-rimed viewport glass, roaring hiss of sublimated vapor, agile fingertip steering yoke.",
                "handling_protocol": "Ride the comet vapor wake at a 15-degree trailing angle; vent thermal coils to prevent icing."
            },
            {
                "vehicle_id": "BIO_ALCHEMIST_MANTA_CRAFT",
                "name": "Symbiotic Bio-Chitin Manta-Craft",
                "faction": "Bio-Alchemists",
                "propulsion_type": "Living Chitin Wing Pulsing & Electrophoretic Spore Streams",
                "specialty": "Atmospheric-to-oceanic seamless amphibious transitions, organic self-healing hull, ecological research.",
                "cockpit_vibe": "Warm bioluminescent breathing interior, neural pulse interface that responds to gentle hand pressure, fresh herbal scent.",
                "handling_protocol": "Guide through calm thought and steady breathing; feed nutrient algae to wing nodes before long flights."
            },
            {
                "vehicle_id": "CRYSTAL_RESONANCE_CRUISER",
                "name": "Crystal-Singer Prismatic Suncatcher",
                "faction": "Crystal-Singers",
                "propulsion_type": "Acoustic Quartz Harmonic Bells & Photonic Refraction Sails",
                "specialty": "Deep-space communication relay, acoustic wave amplification, peaceful distress escort.",
                "cockpit_vibe": "Singing crystal chimes filling the cabin, shimmering rainbow refractions dancing across white stone bulkheads.",
                "handling_protocol": "Sing or hum into the acoustic pitch-pipe to steer; harmonize chords for extra propulsion bursts."
            }
        ]
    }
}

def get_all_vehicles() -> List[Dict[str, Any]]:
    """Returns a flat list of all vehicles across all tiers and factions."""
    all_v = []
    for tier_key, tier_data in TRANSPORT_TIERS.items():
        for v in tier_data.get("vehicles", []):
            item = dict(v)
            item["tier_category"] = tier_key
            item["tier_title"] = tier_data["tier_name"]
            all_v.append(item)
    return all_v

def get_vehicle_profile(vehicle_id_or_name: str) -> Optional[Dict[str, Any]]:
    """Looks up a vehicle by ID, name, or keyword."""
    query = vehicle_id_or_name.lower().replace("-", "_").strip()
    for v in get_all_vehicles():
        v_id = v.get("vehicle_id", "").lower().replace("-", "_")
        v_name = v.get("name", "").lower()
        if query in v_id or query in v_name:
            return v
    return None

def calculate_transit_kinetics(
    vehicle_id: str,
    distance_units: float,
    speed_multiplier: float = 1.0,
    cargo_tonnage: float = 0.0
) -> Dict[str, Any]:
    """
    Calculates travel time, energy expenditure, acceleration profile,
    and pilot experience for any transport journey across the universe.
    """
    v_prof = get_vehicle_profile(vehicle_id) or get_all_vehicles()[0]
    
    tier = v_prof.get("tier_category", "TIER_1_INTRA_PLANETARY")
    
    if "INTRA_PLANETARY" in tier:
        # Distance in km; standard 1 unit = 1,000 km
        dist_km = distance_units * 1000.0
        speed_kmh = max(10, v_prof.get("max_speed_kmh", 1000) * speed_multiplier)
        time_hours = dist_km / speed_kmh
        gut_time = max(0.1, round(time_hours / 24.0, 2))
    elif "INTERPLANETARY" in tier:
        # Distance in AU; standard 1 unit = 1 AU
        c_frac = max(0.005, v_prof.get("max_speed_c_fraction", 0.02) * speed_multiplier)
        gut_time = max(0.2, round((distance_units * 0.6) / (c_frac / 0.01), 2))
    elif "INTERSTELLAR" in tier:
        # Distance in Light-Years or Sector Units (1 Sector unit = 5 LY)
        c_frac = max(1.0, v_prof.get("max_speed_c_fraction", 8.0) * speed_multiplier)
        gut_time = max(0.5, round((distance_units * 5.0) / c_frac, 2))
    else: # INTERGALACTIC / CULTURAL
        c_frac = max(10.0, v_prof.get("max_speed_c_fraction", 50.0) * speed_multiplier)
        gut_time = max(0.1, round(distance_units / c_frac, 2))

    # Weight penalty
    max_cargo = max(1.0, v_prof.get("cargo_capacity_tons", 50.0))
    load_ratio = min(1.5, cargo_tonnage / max_cargo) if cargo_tonnage > 0 else 0.0
    effective_gut = round(gut_time * (1.0 + (load_ratio * 0.25)), 2)

    return {
        "vehicle_id": v_prof["vehicle_id"],
        "vehicle_name": v_prof["name"],
        "tier_category": v_prof["tier_category"],
        "distance_units": distance_units,
        "cargo_tonnage": cargo_tonnage,
        "load_factor": f"{round(load_ratio * 100, 1)}%",
        "estimated_duration_gut": effective_gut,
        "propulsion_type": v_prof["propulsion_type"],
        "energy_source": v_prof.get("energy_source", "Confluence Harmonic Array"),
        "cockpit_sensory_feel": v_prof.get("cockpit_vibe", "Steady flight instrumentation."),
        "pilot_handling_protocol": v_prof.get("handling_protocol", "Maintain safe vectors.")
    }

def get_cockpit_experience(vehicle_id: str, pilot_name: str = "The Pilot", environment: str = "Open Sky") -> Dict[str, Any]:
    """Generates an engaging, sensory-rich cockpit narrative description for story generation."""
    v = get_vehicle_profile(vehicle_id) or get_all_vehicles()[0]
    return {
        "pilot": pilot_name,
        "vehicle": v["name"],
        "environment": environment,
        "cockpit_description": f"{pilot_name} gripped the controls of the {v['name']}. {v['cockpit_vibe']}",
        "action_instruction": f"Applying the pilot guidelines: {v['handling_protocol']}",
        "propulsion_audio": f"The {v['propulsion_type'].lower()} hummed with steady, rhythmic power."
    }

def get_faction_vehicle_preference(faction_name: str) -> Dict[str, Any]:
    """Returns recommended transport craft suited to a given faction's culture and technology."""
    matches = []
    for v in get_all_vehicles():
        favs = v.get("factions_favored", [])
        if any(faction_name.lower() in f.lower() for f in favs) or (v.get("faction") and faction_name.lower() in v["faction"].lower()):
            matches.append(v)
    if not matches:
        matches = [get_all_vehicles()[0], get_all_vehicles()[5], get_all_vehicles()[8]]
    return {
        "faction": faction_name,
        "recommended_vehicles_count": len(matches),
        "vehicles": matches
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Transport & Mobility Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("catalog", help="List full galactic transport catalog")

    info_p = subparsers.add_parser("info", help="Get vehicle profile")
    info_p.add_argument("--vehicle", required=True, help="Vehicle ID or name")

    sim_p = subparsers.add_parser("simulate", help="Simulate transit journey kinetics")
    sim_p.add_argument("--vehicle", default="ATMOSPHERIC_SKIMMER", help="Vehicle ID")
    sim_p.add_argument("--dist", type=float, default=10.0, help="Distance units")
    sim_p.add_argument("--cargo", type=float, default=0.0, help="Cargo tonnage")
    sim_p.add_argument("--speed", type=float, default=1.0, help="Speed multiplier")

    pref_p = subparsers.add_parser("faction", help="Get faction transport preferences")
    pref_p.add_argument("--name", default="Sun-Forged Hegemony", help="Faction name")

    args = parser.parse_args()

    if args.command == "info":
        res = get_vehicle_profile(args.vehicle)
        print(json.dumps(res or {"error": f"Vehicle '{args.vehicle}' not found."}, indent=2))
    elif args.command == "simulate":
        res = calculate_transit_kinetics(args.vehicle, args.dist, args.speed, args.cargo)
        print(json.dumps(res, indent=2))
    elif args.command == "faction":
        res = get_faction_vehicle_preference(args.name)
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"total_vehicles": len(get_all_vehicles()), "catalog": TRANSPORT_TIERS}, indent=2))
