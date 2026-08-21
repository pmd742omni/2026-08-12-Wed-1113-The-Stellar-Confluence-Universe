#!/usr/bin/env python3
"""
Cosmic Energy Matrix & Dynamic Energy Discovery Engine for The Stellar Confluence Universe.
Manages the 10 core cosmic energy forces, dynamic procedural energy discovery during
deep-space expeditions, mathematical wave/field propagation decay models, drive-core efficiencies,
thermal radiator heat-sink constraints, and multi-energy physical interaction simulation.
"""

import os
import sys
import json
import math
import hashlib
import datetime
import argparse
from typing import Dict, Any, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from core.edition_manager import get_edition_state_dir, get_state_file

CORE_ENERGY_FORCES: Dict[str, Dict[str, Any]] = {
    "CONFLUENCE_WAVEFRONT": {
        "name": "Confluence Wavefront Standing Wave",
        "category": "Spacetime Harmonic",
        "source": "Primordial Trinary Singularity Dynamo at Galactic Core",
        "frequency_band": "15 deg / 60 deg / Storm Crests (144.0 MHz Base)",
        "base_wavelength_ly": 5.0,
        "base_intensity_w_m2": 1500.0,
        "primary_application": "Propulsion, solar sail amplification, clockwork resonance",
        "physical_constraint": "Dependent on Facing Angle (theta); high heat at Zenith, blocked at Nadir",
        "drive_compatibility": ["SOLAR_SAIL_CUTTER", "CONFLUENCE_WAVE_RIDER", "ASTROLABE_GEAR_GONDOLA"]
    },
    "CORONAL_PLASMA_FLUX": {
        "name": "Coronal Prominence Plasma Flux",
        "category": "Stellar Thermal / Magnetic",
        "source": "Stellar magnetic burst loops and flare eruptions",
        "frequency_band": "High-energy magnetohydrodynamic thermal (450-800 THz)",
        "base_wavelength_ly": 0.001,
        "base_intensity_w_m2": 8500.0,
        "primary_application": "Kinetic plasma thrust, thermal smelting, laser charging, heat shields",
        "physical_constraint": "Rapid radiator overheating; requires magnetic containment",
        "drive_compatibility": ["ATMOSPHERIC_SKIMMER", "CORONAL_PLASMA_SCOOPER", "DYSON_ACCELERATOR_RUNNER"]
    },
    "DARK_MATTER_DRIFT": {
        "name": "Primordial Dark Matter Drift",
        "category": "Sub-Spatial Gravitational",
        "source": "Intergalactic dark matter currents between spiral arms",
        "frequency_band": "Non-baryonic low-frequency gravitational current (0.01-10 Hz)",
        "base_wavelength_ly": 25.0,
        "base_intensity_w_m2": 320.0,
        "primary_application": "Silent vacuum gliding, soundless stealth, cold shadow phasing",
        "physical_constraint": "Extreme cold exhaustion; physical weapon vulnerability",
        "drive_compatibility": ["VOID_PHASE_SHUTTLE", "DARK_MATTER_CARAVAN_BARGE"]
    },
    "TACHYON_CHRONO_FLUX": {
        "name": "Tachyon Chrono-Flux",
        "category": "Temporal Slipstream",
        "source": "Cosmic vacuum density pockets and frame-dragging ripples",
        "frequency_band": "Superluminal phase-velocity slipstream (1.2-5.8 GHz)",
        "base_wavelength_ly": 12.0,
        "base_intensity_w_m2": 2100.0,
        "primary_application": "Accelerated transit slipstreams, precision chronometer synchronization",
        "physical_constraint": "Temporal dilation strain; navigation sensor displacement",
        "drive_compatibility": ["TACHYON_SLIPSTREAM_FRIGATE", "COMET_SUBLIMATION_SKIFF"]
    },
    "BIOPHOTONIC_LIFE_FORCE": {
        "name": "Aetheric Biophotonic Life-Force",
        "category": "Organic Xenobiological",
        "source": "Living canopy forests, bioluminescent coral colossi, grav-whales",
        "frequency_band": "Bio-electric photonic chlorophyll resonance (520-565 nm)",
        "base_wavelength_ly": 0.05,
        "base_intensity_w_m2": 650.0,
        "primary_application": "Organic hull regeneration, neuro-spore mind-links, living ship growth",
        "physical_constraint": "Requires sunlight/nutrient feeding; vulnerable to radiation poisoning",
        "drive_compatibility": ["BENTHIC_ABYSSAL_CRAWLER", "BIO_ALCHEMIST_MANTA_CRAFT"]
    },
    "SINGULARITY_GRAV_TORSION": {
        "name": "Singularity Grav-Torsion",
        "category": "Micro-Singularity Rotational",
        "source": "Artificial micro-black hole containment vessels and core dynamos",
        "frequency_band": "High-torque gravitational frame-dragging (10-100 kHz)",
        "base_wavelength_ly": 0.2,
        "base_intensity_w_m2": 12000.0,
        "primary_application": "Planetary-scale tractor beams, artificial gravity plating, core drills",
        "physical_constraint": "Critical containment rupture risk; immense mass drag",
        "drive_compatibility": ["CYCLER_HABITAT_SHIP", "ION_FREIGHTER_CONVOY"]
    },
    "VACUUM_ZERO_POINT": {
        "name": "Vacuum Zero-Point Ground State",
        "category": "Subspace Neutral Baseline",
        "source": "Keystone Subspace Gateways and wormhole tunnels",
        "frequency_band": "Quantum vacuum ground state (Re = 0.5, Neutral)",
        "base_wavelength_ly": 0.0,
        "base_intensity_w_m2": 500.0,
        "primary_application": "Standard non-resonant kinetics, baseline mechanical calibration",
        "physical_constraint": "All Wavefront amplification completely decoupled",
        "drive_compatibility": ["KEYSTONE_SUB_SPACE_GATEWAY", "PLANETARY_MAGLEV_EXPRESS"]
    },
    "PIEZOGRAVITIC_HARMONIC": {
        "name": "Piezogravitic Mantle Lattice Harmonic",
        "category": "Geological Piezoelectric / Acoustic",
        "source": "Deep planetary quartz spires compressed by gravitational tides",
        "frequency_band": "Sub-acoustic seismic piezoelectric pulses (12-48 Hz)",
        "base_wavelength_ly": 0.02,
        "base_intensity_w_m2": 3800.0,
        "primary_application": "Clean planetary power grids, geothermal elevators, acoustic shielding",
        "physical_constraint": "Requires seismic stabilization jackets; risk of crystal shear under overtension",
        "drive_compatibility": ["ORBITAL_SKYHOOK_TETHER", "SAND_SAIL_SKIFF"]
    },
    "MAGNETAR_POLAR_JET": {
        "name": "Magnetar Relativistic Synchrotron Pulse",
        "category": "High-B Synchrotron Radiation",
        "source": "Ultra-dense neutron star magnetic poles (>10^11 Tesla)",
        "frequency_band": "Relativistic synchrotron X-ray/Gamma burst (10^18 Hz)",
        "base_wavelength_ly": 0.0001,
        "base_intensity_w_m2": 25000.0,
        "primary_application": "Deep-space slingshot acceleration, extreme alloy forging, magnetic catapults",
        "physical_constraint": "Lethal ionization without triple magnetic shielding; destroys unprotected electronics",
        "drive_compatibility": ["DYSON_ACCELERATOR_RUNNER", "CORONAL_PLASMA_SCOOPER"]
    },
    "CHRONO_SPATIAL_PHASE": {
        "name": "Chrono-Spatial Phase Harmonic",
        "category": "Sub-Quantum Acoustic Waveguide",
        "source": "Ancient Keystone Orrery alignments and resonance bells",
        "frequency_band": "Prismatic acoustic octave harmonics (432-864 Hz)",
        "base_wavelength_ly": 8.0,
        "base_intensity_w_m2": 1850.0,
        "primary_application": "Subspace beacon synchronization, long-range distress singing, peaceful navigation",
        "physical_constraint": "Requires precise pitch matching; dissonant chords cause signal dispersal",
        "drive_compatibility": ["CRYSTAL_RESONANCE_CRUISER", "CONFLUENCE_WAVE_RIDER"]
    }
}

def load_energy_matrix(edition: Optional[str] = None) -> Dict[str, Any]:
    """Loads the active edition's cosmic energy matrix state."""
    state_file = get_state_file("cosmic_energy_matrix.json", edition)
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if len(data.get("core_energies", {})) < len(CORE_ENERGY_FORCES):
                    data["core_energies"] = CORE_ENERGY_FORCES
                data["forces"] = CORE_ENERGY_FORCES
                return data
        except Exception:
            pass
    return {"version": "2.0", "core_energies": CORE_ENERGY_FORCES, "forces": CORE_ENERGY_FORCES, "discovered_energies": {}}

def save_energy_matrix(data: Dict[str, Any], edition: Optional[str] = None) -> None:
    """Saves the energy matrix to the active edition state."""
    state_file = get_state_file("cosmic_energy_matrix.json", edition)
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def calculate_field_propagation(
    energy_key: str,
    distance_units: float,
    facing_angle: float = 45.0,
    source_power_mw: float = 1000.0,
    gut_time: float = 100.0
) -> Dict[str, Any]:
    """
    Calculates spatial field intensity decay and standing wave modulation:
    I(r, theta) = I_0 * (1 / (1 + (r/r_0)^2)) * (1 + 0.5 * sin(2*pi*r/lambda - omega*t)) * cos^2(theta/2)
    """
    e_info = CORE_ENERGY_FORCES.get(energy_key.upper())
    if not e_info:
        e_info = CORE_ENERGY_FORCES["CONFLUENCE_WAVEFRONT"]

    r = max(0.01, float(distance_units))
    theta_rad = math.radians(float(facing_angle))
    r0 = max(0.5, e_info.get("base_wavelength_ly", 5.0))
    wavelength = max(0.1, e_info.get("base_wavelength_ly", 5.0))

    # Spatial geometric inverse-square attenuation with near-field saturation
    geom_decay = 1.0 / (1.0 + (r / r0) ** 2)

    # Harmonic phase modulation
    phase = (2.0 * math.pi * r / wavelength) - (0.125 * float(gut_time))
    wave_mod = 1.0 + (0.5 * math.sin(phase))

    # Angular facing factor (Zenith = 1.0, Twilight = 0.5, Nadir = 0.0 for radiant; inverse for dark)
    if "DARK" in energy_key.upper():
        angular_factor = math.sin(theta_rad / 2.0) ** 2
    else:
        angular_factor = math.cos(theta_rad / 2.0) ** 2

    # Received field intensity in MW/m^2
    received_intensity = round(source_power_mw * geom_decay * wave_mod * angular_factor, 2)
    flux_density_pct = round(min(150.0, (received_intensity / max(1.0, source_power_mw)) * 100.0), 1)
    facing_zone = "PEAK_ZENITH" if facing_angle <= 30.0 else ("SHADOW_NADIR" if facing_angle >= 150.0 else "TRANSIT_TWILIGHT")

    return {
        "status": "PROPAGATION_CALCULATED",
        "energy_key": energy_key.upper(),
        "energy_name": e_info["name"],
        "category": e_info["category"],
        "distance_units_ly": r,
        "facing_angle_deg": round(facing_angle, 1),
        "reception_facing_zone": facing_zone,
        "source_power_mw": source_power_mw,
        "geometric_decay_factor": round(geom_decay, 4),
        "harmonic_wave_modulation": round(wave_mod, 3),
        "angular_reception_factor": round(angular_factor, 3),
        "received_power_mw": received_intensity,
        "received_intensity_mw": received_intensity,
        "energy_absorption_pct": f"{flux_density_pct}%",
        "relative_flux_density": f"{flux_density_pct}%",
        "operational_status": "OPTIMAL_COUPLING" if flux_density_pct >= 40.0 else ("MARGINAL_SIGNAL" if flux_density_pct >= 10.0 else "DISSIPATED_BELOW_THRESHOLD")
    }

def calculate_drive_efficiency(
    energy_key: str,
    vehicle_id: str = "CONFLUENCE_WAVE_RIDER",
    thermal_sink_pct: float = 25.0,
    facing_angle: float = 30.0
) -> Dict[str, Any]:
    """
    Computes drive-core efficiency multiplier (eta in [0.1, 1.0]), thermal radiator load,
    and mandatory venting thresholds.
    """
    e_info = CORE_ENERGY_FORCES.get(energy_key.upper(), CORE_ENERGY_FORCES["CONFLUENCE_WAVEFRONT"])
    compatible = vehicle_id in e_info.get("drive_compatibility", []) or len(e_info.get("drive_compatibility", [])) == 0

    base_eta = 0.92 if compatible else 0.45
    
    # Thermal de-rating
    thermal_penalty = max(0.0, (thermal_sink_pct - 50.0) * 0.01) if thermal_sink_pct > 50.0 else 0.0
    
    # Facing alignment bonus/penalty
    theta_rad = math.radians(facing_angle)
    if "DARK" in energy_key.upper():
        facing_mult = math.sin(theta_rad / 2.0) ** 2
    else:
        facing_mult = math.cos(theta_rad / 2.0) ** 2

    effective_eta = max(0.1, min(0.99, round((base_eta - thermal_penalty) * (0.5 + 0.5 * facing_mult), 3)))
    thermal_buildup_rate = round(max(0.5, (1.0 - effective_eta) * 12.0), 2)

    needs_venting = thermal_sink_pct >= 75.0 or (facing_angle <= 20.0 and energy_key == "CORONAL_PLASMA_FLUX")

    return {
        "status": "DRIVE_EFFICIENCY_EVALUATED",
        "energy_key": energy_key.upper(),
        "vehicle_id": vehicle_id,
        "drive_core_compatibility": "NATIVE_HARMONIC" if compatible else "CROSS_FIELD_ADAPTER",
        "base_efficiency_eta": base_eta,
        "effective_thrust_efficiency": effective_eta,
        "efficiency_percentage": round(effective_eta * 100.0, 1),
        "thermal_sink_saturation_pct": thermal_sink_pct,
        "thermal_buildup_rate_kw_s": thermal_buildup_rate,
        "mandatory_venting_required": needs_venting,
        "radiator_venting_alert": "MANDATORY_VENTING" if needs_venting else "NOMINAL_COOLING",
        "tactical_guidance": "Thermal venting mandatory to prevent heat-sink rupture!" if needs_venting else "Radiators operating within safe convective margins."
    }

def discover_new_energy(
    name: str,
    coords: List[int],
    frequency_ghz: float,
    description: str,
    discoverer: str = "Caelum Dawnrunner",
    book_id: int = 1,
    edition: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a dynamically discovered exotic energy frequency."""
    raw_hash = hashlib.sha256(f"{name}_{coords}_{frequency_ghz}".encode('utf-8')).hexdigest()
    energy_id = f"ENG-{raw_hash[:4].upper()}-{raw_hash[4:8].upper()}"

    db = load_energy_matrix(edition)
    entry = {
        "energy_id": energy_id,
        "name": name,
        "frequency_ghz": frequency_ghz,
        "coordinates": coords,
        "description": description,
        "discovery": {
            "discoverer": discoverer,
            "book_id": book_id,
            "timestamp": datetime.datetime.now().isoformat()
        },
        "harnessing_discipline": "Resonant Spectrometry & Field Containment"
    }

    db["discovered_energies"][energy_id] = entry
    save_energy_matrix(db, edition)

    return entry

def simulate_energy_interaction(
    energy_1: str,
    energy_2: str,
    facing_angle: float = 45.0
) -> Dict[str, Any]:
    """Simulates physical synergy and interference between two energy fields."""
    e1_key = energy_1.upper()
    e2_key = energy_2.upper()

    synergy_score = 75.0
    interference_risk = "MODERATE"
    notes = "Harmonic resonance balance achieved."

    if (e1_key == "CONFLUENCE_WAVEFRONT" and e2_key == "CORONAL_PLASMA_FLUX") or (e2_key == "CONFLUENCE_WAVEFRONT" and e1_key == "CORONAL_PLASMA_FLUX"):
        if facing_angle <= 30.0:
            synergy_score = 95.0
            interference_risk = "CRITICAL_OVERHEAT"
            notes = "Extreme beam power surge with critical thermal venting requirements."
        else:
            synergy_score = 80.0
            interference_risk = "LOW"
            notes = "Stable plasma-sail propulsion."
    elif (e1_key == "DARK_MATTER_DRIFT" and e2_key == "CONFLUENCE_WAVEFRONT") or (e2_key == "DARK_MATTER_DRIFT" and e1_key == "CONFLUENCE_WAVEFRONT"):
        if facing_angle >= 150.0:
            synergy_score = 98.0
            interference_risk = "COLD_FATIGUE"
            notes = "Total rock-phasing and perfect radar stealth in planetary shadow."
        else:
            synergy_score = 30.0
            interference_risk = "DISSOLUTION"
            notes = "Wavefront starlight dissolves dark-matter cloak."
    elif (e1_key == "PIEZOGRAVITIC_HARMONIC" and e2_key == "CONFLUENCE_WAVEFRONT") or (e2_key == "PIEZOGRAVITIC_HARMONIC" and e1_key == "CONFLUENCE_WAVEFRONT"):
        synergy_score = 92.0
        interference_risk = "LOW"
        notes = "Clean piezoelectric induction with continuous gravitational power generation."
    elif (e1_key == "MAGNETAR_POLAR_JET" and e2_key == "TACHYON_CHRONO_FLUX") or (e2_key == "MAGNETAR_POLAR_JET" and e1_key == "TACHYON_CHRONO_FLUX"):
        synergy_score = 88.0
        interference_risk = "HIGH_SHEAR"
        notes = "Relativistic particle slingshot with significant temporal frame-dragging."

    return {
        "primary_energy": energy_1,
        "secondary_energy": energy_2,
        "facing_angle": facing_angle,
        "synergy_score": synergy_score,
        "interference_risk": interference_risk,
        "simulation_notes": notes
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmic Energy Matrix Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("catalog", help="List all 10 core cosmic energies")

    prop_p = subparsers.add_parser("propagate", help="Calculate spatial field propagation decay")
    prop_p.add_argument("--energy", default="CONFLUENCE_WAVEFRONT", help="Energy force key")
    prop_p.add_argument("--dist", type=float, default=5.0, help="Distance units in Light-Years")
    prop_p.add_argument("--facing", type=float, default=30.0, help="Facing angle degrees")
    prop_p.add_argument("--power", type=float, default=1000.0, help="Source power in MW")

    eff_p = subparsers.add_parser("efficiency", help="Calculate drive-core efficiency and thermal load")
    eff_p.add_argument("--energy", default="CONFLUENCE_WAVEFRONT", help="Energy force key")
    eff_p.add_argument("--vehicle", default="CONFLUENCE_WAVE_RIDER", help="Vehicle ID")
    eff_p.add_argument("--sink", type=float, default=30.0, help="Thermal sink saturation %")
    eff_p.add_argument("--facing", type=float, default=30.0, help="Facing angle degrees")

    sim_p = subparsers.add_parser("simulate", help="Simulate dual energy field interaction")
    sim_p.add_argument("--energy1", default="CONFLUENCE_WAVEFRONT")
    sim_p.add_argument("--energy2", default="CORONAL_PLASMA_FLUX")
    sim_p.add_argument("--facing", type=float, default=45.0)

    args = parser.parse_args()

    if args.command == "propagate":
        res = calculate_field_propagation(args.energy, args.dist, args.facing, args.power)
        print(json.dumps(res, indent=2))
    elif args.command == "efficiency":
        res = calculate_drive_efficiency(args.energy, args.vehicle, args.sink, args.facing)
        print(json.dumps(res, indent=2))
    elif args.command == "simulate":
        res = simulate_energy_interaction(args.energy1, args.energy2, args.facing)
        print(json.dumps(res, indent=2))
    else:
        matrix = load_energy_matrix()
        print(json.dumps({"total_core_energies": len(CORE_ENERGY_FORCES), "discovered_count": len(matrix.get("discovered_energies", {})), "catalog": CORE_ENERGY_FORCES}, indent=2))

