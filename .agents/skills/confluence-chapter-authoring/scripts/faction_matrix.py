#!/usr/bin/env python3
"""
Comprehensive Faction Physics, Technology & Capability Matrix for The Stellar Confluence Universe
Defines deep physics mechanisms, signature equipment, tactical fighting styles, and distinct
Peak/Shadow/Transit/Deep-Space constraints for all 44+ core and expansion factions.
"""

import sys
import json
import argparse

FACTION_DATABASE = {
    # Core Factions (Books 01 - 30)
    "Sun-Forged Hegemony": {
        "domain": "Radiant Solar / Thermal Optics",
        "energy_medium": "Photonic Wavefront Absorption & Solar Core Crystal Lenses",
        "signature_gear": "Solar Beam Lenses, Photonic Aegis Armor, Thermal Glaives, Light-Prism Batteries",
        "tactical_style": "High-intensity linear beam strikes, luminous shield walls, focused thermal cutting",
        "peak_facing": {
            "buff": "SUPER-CHARGED: Luminous beam projection reaches maximum range; radiant shields withstand extreme kinetic impact.",
            "debuff": "OVERHEAT RISK: Heat sink exchangers rapidly reach critical melting point; requires heat purging vents."
        },
        "shadow_facing": {
            "buff": "NONE: Direct solar beam generation is fully disabled.",
            "debuff": "ECLIPSE LOCK: Powered armor systems shut down into mechanical lock; must rely on stored kinetic springs or auxiliary cells."
        },
        "transit_facing": {
            "buff": "HARMONIC BASELINE: Stable, predictable radiant beam output and moderate thermal shield capacity.",
            "debuff": "STANDARD LIMIT: Cannot sustain high-yield burst attacks without brief cooldown."
        },
        "subspace": "Photonic beams function at 50% baseline; solar recharge disabled."
    },
    "Void-Bound Monks": {
        "domain": "Umbral Shadow / Quantum Phase-Shifting",
        "energy_medium": "Photonic Absence / Nadir Gravitational Well Resonance",
        "signature_gear": "Obsidian Phase-Robes, Shadow-Weave Daggers, Null-Light Shrouds, Cold-Iron Hooks",
        "tactical_style": "Silent infiltration, molecular phase-shifting through physical barriers, light bending",
        "peak_facing": {
            "buff": "NONE: Shadow constructs dissolve under intense radiant pressure.",
            "debuff": "SEVERELY SUPPRESSED: Stealth shrouds fail, phase-stepping disabled; must rely on physical grit and melee blades."
        },
        "shadow_facing": {
            "buff": "APEX SHADOW SURGE: Full molecular phase-shifting through solid rock and bulkheads; complete visual invisibility.",
            "debuff": "COLD ACCELERATION: Deep shadow draws body warmth rapidly; prolonged use causes frost fatigue and shivering."
        },
        "transit_facing": {
            "buff": "HARMONIC BASELINE: Controlled short-range shadow tendrils, reliable stealth in dim shadows.",
            "debuff": "STANDARD LIMIT: Cannot phase through reinforced composite armor plating."
        },
        "subspace": "Stable stealth mechanics without celestial interference; neutral shadow baseline."
    },
    "Astrolabe Engineers": {
        "domain": "Clockwork Kinematics / Harmonic Resonance",
        "energy_medium": "Crystalline Micro-Gears, Inertial Flywheels, Harmonic Escapements",
        "signature_gear": "Brass Meridian Gauntlets, Gyroscopic Anchors, Chronometer Compasses, Torsion Crossbows",
        "tactical_style": "Kinetic momentum redirection, clockwork trap deployment, harmonic frequency disruption",
        "peak_facing": {
            "buff": "HYPER-EFFICIENT: Crystalline gear arrays spin with zero friction and instant kinetic torque.",
            "debuff": "CENTRIFUGAL STRESS: Extreme rotational velocities risk throwing gears off alignment if timing slips."
        },
        "shadow_facing": {
            "buff": "MOMENTUM BURST: Heavy flywheel kinetic energy can be discharged in powerful crushing blows.",
            "debuff": "MECHANICAL DRAG: High rotational resistance; gears feel heavy, requiring manual crank leverage."
        },
        "transit_facing": {
            "buff": "HARMONIC BASELINE: Smooth mechanical clockwork operation, precise chronometer synchronization.",
            "debuff": "STANDARD LIMIT: Energy output bounded by physical flywheel spring capacity."
        },
        "subspace": "Standard mechanical systems operate normally; chronometers require manual recalibration."
    },

    # Expansion Factions (Books 31 - 74)
    "Comet-Riders": {
        "domain": "Cryogenic Sublimation / Gravitational Singshotting",
        "energy_medium": "Volatile Ice Sublimation Jets & Ionized Dust Tails",
        "signature_gear": "Cryo-Skis, Sublimation Harpoons, Vapor Thruster Harnesses",
        "tactical_style": "High-velocity momentum strikes, flash-freeze vapor barriers, icy trajectory slingshots",
        "peak_facing": {
            "buff": "SUBLIMATION SURGE: Extreme ice vaporization creates massive kinetic thrust plumes.",
            "debuff": "RAPID MELTDOWN: Cryo-ice reserves vaporize prematurely; flight duration cut in half."
        },
        "shadow_facing": {
            "buff": "CRYOGENIC ARMOR: Ice constructs harden to diamond-like tensile strength.",
            "debuff": "THRUST INERTIA: Vapor jets produce minimal thrust without solar heating."
        },
        "transit_facing": {
            "buff": "HARMONIC GLIDE: Balanced ice-to-vapor conversion, ideal gliding maneuverability.",
            "debuff": "STANDARD LIMIT: Gliding speed bounded by local dust tail density."
        },
        "subspace": "Ice remains stable; kinetic glide relies purely on chemical thrusters."
    },
    "Nebula-Weavers": {
        "domain": "Ionized Gas Weaving / Electromagnetic Filamentation",
        "energy_medium": "Interstellar Gas Strands & Magnetic Loom Needles",
        "signature_gear": "Plasma Silk Spindles, Electromagnetic Looms, Ion Weave Nets",
        "tactical_style": "Electromagnetic web traps, sensory filament tripwires, luminous gas cloaking",
        "peak_facing": {
            "buff": "ION ENERGIZATION: Woven filaments glow with superheated plasma discharge.",
            "debuff": "STRAND BRITTLE: Intense radiation burns through fragile electromagnetic bonds."
        },
        "shadow_facing": {
            "buff": "GHOST WEAVE: Invisible magnetic nets undetectable by optical scanners.",
            "debuff": "LOW CHARGE: Web strands have minimal shock damage; purely physical trapping."
        },
        "transit_facing": {
            "buff": "HARMONIC WEAVE: Flexible, durable electromagnetic ropes and sensory arrays.",
            "debuff": "STANDARD LIMIT: Web radius limited to local ambient gas density."
        },
        "subspace": "Filament weaving requires localized gas canisters; cannot harvest ambient space."
    },
    "Deep-Core Miners": {
        "domain": "Tectonic Hydraulics / Magma Pressure Control",
        "energy_medium": "High-Density Geothermal Fluid & Core Piston Drives",
        "signature_gear": "Pneumatic Drill-Rigs, Basalt Exoskeletons, Seismic Resonators",
        "tactical_style": "Seismic shockwaves, localized ground tremors, hydraulic crushing force",
        "peak_facing": {
            "buff": "CORE EXPANSION: Hydraulic fluids superheat, doubling piston strike velocity.",
            "debuff": "OVERPRESSURE: Steam valves risk bursting if geothermal heat is not vented."
        },
        "shadow_facing": {
            "buff": "BASALT SOLIDITY: Heavy armored exoskeletons cool into unbreakable shields.",
            "debuff": "HYDRAULIC SLOWDOWN: Fluid viscosity thickens, reducing striking speed."
        },
        "transit_facing": {
            "buff": "HARMONIC DRILL: Steady seismic boring, stable hydraulic pressure.",
            "debuff": "STANDARD LIMIT: Drill depth constrained by physical bit durability."
        },
        "subspace": "Hydraulic pistons operate on mechanical spring backups."
    },
    "Gravity-Surfers": {
        "domain": "Singularity Vectoring / Metric Distortion",
        "energy_medium": "Micro-Graviton Wells & Inertial Dampening Sails",
        "signature_gear": "Graviton Surfboards, Metric Anchor Cleats, Singularity Slings",
        "tactical_style": "Gravitational free-fall acceleration, artificial gravity redirection, kinetic orbit diving",
        "peak_facing": {
            "buff": "GRAVITON WAVE: Ride radiant energy wavefronts at relativistic sub-light speeds.",
            "debuff": "TIDAL SHEAR: Gravitational tides cause intense physical strain on the pilot."
        },
        "shadow_facing": {
            "buff": "CLEAN ATTRACTION: Zero radiation interference allows micro-precise orbit calculations.",
            "debuff": "WEAK SURF: Must rely on existing planetary mass; cannot self-generate strong push vectors."
        },
        "transit_facing": {
            "buff": "HARMONIC ORBIT: Smooth gravitational glide around planetary bodies.",
            "debuff": "STANDARD LIMIT: Acceleration bounded by local gravitational gradient."
        },
        "subspace": "Graviton sails produce neutral baseline propulsion."
    },
    "Plasma-Shepherds": {
        "domain": "Magnetic Field Containment / Coronal Flares",
        "energy_medium": "Ionized Coronal Currents & Magnetic Lasso Coils",
        "signature_gear": "Magnetic Crooks, Plasma Bottle Traps, Flare Harnesses",
        "tactical_style": "Plasma whip strikes, directional coronal loop redirection, electromagnetic fencing",
        "peak_facing": {
            "buff": "SOLAR FLOCK SURGE: Plasma tendrils expand into roaring whips of solar fire.",
            "debuff": "COIL STRAIN: Magnetic coils heat rapidly, risking magnetic field collapse."
        },
        "shadow_facing": {
            "buff": "STABLE CONTAINMENT: Stored plasma bottles remain perfectly cool and stable.",
            "debuff": "NO HARVEST: Cannot draw ambient plasma from surroundings."
        },
        "transit_facing": {
            "buff": "HARMONIC HERD: Controlled plasma lasso manipulation, steady magnetic confinement.",
            "debuff": "STANDARD LIMIT: Plasma discharge capacity limited to carried tank reserves."
        },
        "subspace": "Bottled plasma functions normally; no external flare drawing."
    },
    "Chrono-Navigators": {
        "domain": "Subspace Temporal Metrics / Path Optimization",
        "energy_medium": "Tachyon Crystal Oscillators & Quantum Phase Dials",
        "signature_gear": "Chrono-Compasses, Temporal Sextants, Probability Chronometers",
        "tactical_style": "Micro-second precognition, optimal trajectory pathfinding, timeline divergence tracking",
        "peak_facing": {
            "buff": "PROBABILITY CLARITY: Wavefront alignment illuminates optimal navigational paths minutes ahead.",
            "debuff": "TEMPORAL DIZZINESS: Overwhelming sensory influx of multiple potential futures."
        },
        "shadow_facing": {
            "buff": "ANCHORED PRESENT: Complete immunity to subspace temporal drift.",
            "debuff": "BLIND DRIFT: Cannot project timeline paths beyond current local tick."
        },
        "transit_facing": {
            "buff": "HARMONIC CHRONO: Stable, reliable navigational path calculations.",
            "debuff": "STANDARD LIMIT: Calculations take standard computational processing time."
        },
        "subspace": "Operates at peak theoretical efficiency inside ancient wormholes."
    },
    "Bio-Alchemists": {
        "domain": "Symbiotic Flora / Photosynthetic Bioluminescence",
        "energy_medium": "Radiant Spores, Chlorophyll Chitin, Bioluminescent Vines",
        "signature_gear": "Spore Gauntlets, Photosynthetic Chitin Armor, Living Seed Pods",
        "tactical_style": "Rapid plant construct growth, bioluminescent flashes, symbiotic poison neutralizers",
        "peak_facing": {
            "buff": "RAPID BLOOM: Plant constructs grow in seconds into impenetrable thorn barricades.",
            "debuff": "DEHYDRATION: Photosynthesis rapidly consumes internal water reserves."
        },
        "shadow_facing": {
            "buff": "NOCTURNAL BIOLUMINESCENCE: Soft glowing spores release calming, healing vapors.",
            "debuff": "DORMANT GROWTH: Vines and seed constructs cannot expand without sunlight."
        },
        "transit_facing": {
            "buff": "HARMONIC METABOLISM: Balanced botanical growth and steady seed production.",
            "debuff": "STANDARD LIMIT: Seed growth speed bounded by normal bio-chemical rates."
        },
        "subspace": "Living seed pods enter suspended animation stasis."
    },
    "Crystal-Singers": {
        "domain": "Piezoelectric Sonance / Harmonic Crystal Resonance",
        "energy_medium": "Vibrating Quartz Prisms & Acoustic Tone Tuning",
        "signature_gear": "Resonant Tuning Forks, Crystal Chime Staffs, Sound-Refracting Shields",
        "tactical_style": "Acoustic pulse barriers, frequency dampening, crystal shattering waves",
        "peak_facing": {
            "buff": "SONIC CLARITY: Crystal lattices amplify acoustic soundwaves to crystalline brilliance.",
            "debuff": "HARMONIC OVERLOAD: Risk of micro-fracturing crystal tools under extreme vibration."
        },
        "shadow_facing": {
            "buff": "PURE ACOUSTICS: Subterranean silence enhances listening and micro-vibration detection.",
            "debuff": "COLD DAMPENING: Frozen crystal facets lose flexibility, dampening high-pitch tones."
        },
        "transit_facing": {
            "buff": "HARMONIC CHIME: Perfectly stable resonance tuning and crystal communication.",
            "debuff": "STANDARD LIMIT: Sound wave range bounded by atmospheric density."
        },
        "subspace": "Crystal vibrations maintain steady internal resonance."
    },
    "Tide-Wardens": {
        "domain": "Hydro-Kinetic Pressure / Oceanic Wave Dynamics",
        "energy_medium": "Pressurized Saline Fluid & Tidal Current Vectors",
        "signature_gear": "Hydro-Harpoons, Pressure-Sealed Shell Helms, Buoyant Jet Fins",
        "tactical_style": "Hydro-kinetic jet thrusts, tidal current redirection, deep-depth pressure shielding",
        "peak_facing": {
            "buff": "THERMAL CURRENT: Water jets superheat, creating high-pressure steam propulsion.",
            "debuff": "EVAPORATION: Rapid fluid loss requires constant water replenishment."
        },
        "shadow_facing": {
            "buff": "ABYSSAL STEALTH: Deep ocean currents provide complete thermal concealment.",
            "debuff": "DENSE VISCOSITY: Cold water reduces rapid steering reaction times."
        },
        "transit_facing": {
            "buff": "HARMONIC SWELL: Smooth hydrodynamic movement and reliable pressure seals.",
            "debuff": "STANDARD LIMIT: Propulsion bounded by onboard water reservoir."
        },
        "subspace": "Hydro systems operate normally on internal water tanks."
    },
    "Magnetar-Leapers": {
        "domain": "Electromagnetic Polarity / Flux Arc Propulsion",
        "energy_medium": "High-Flux Magnetic Coils & Polar Leap Cleats",
        "signature_gear": "Polarity Boots, Magnetic Arc Gloves, Flux Repulsion Gauntlets",
        "tactical_style": "Lightning-fast magnetic leaps, polar repulsion dodges, electromagnetic disarming arcs",
        "peak_facing": {
            "buff": "FLUX SURGE: Magnetic leap distance triples along solar wind flux lines.",
            "debuff": "POLARITY INVERSION RISK: Excessive charge can momentarily short-circuit boot circuits."
        },
        "shadow_facing": {
            "buff": "STEADY POLARITY: Absence of solar radiation enables micro-precise landing lock.",
            "debuff": "LOW VOLTAGE: Arc discharge loses offensive shock power."
        },
        "transit_facing": {
            "buff": "HARMONIC LEAP: Smooth, reliable magnetic navigation along planetary lines.",
            "debuff": "STANDARD LIMIT: Leap distance bounded by local magnetic field strength."
        },
        "subspace": "Requires artificial magnetic anchor points to leap."
    }
}

def get_faction_profile(faction_name):
    """Retrieves or synthesizes a rich faction profile."""
    clean = faction_name.strip()
    for key, data in FACTION_DATABASE.items():
        if key.lower() in clean.lower() or clean.lower() in key.lower():
            return {"matched_name": key, "profile": data}

    # Dynamic fallback for any newly invented expansion faction
    return {
        "matched_name": clean,
        "profile": {
            "domain": f"Cosmic Resonance: {clean}",
            "energy_medium": f"Ambient Confluence Wavefront Interaction ({clean})",
            "signature_gear": f"{clean} Harmonic Focusers & Resonant Tools",
            "tactical_style": f"Adaptive tactical maneuvers aligned with {clean} philosophy",
            "peak_facing": {
                "buff": f"WAVEFRONT AMPLIFICATION: {clean} techniques energized by direct radiant vector.",
                "debuff": "HEAT/ENERGY OVERLOAD: Requires active thermal/energy dissipation."
            },
            "shadow_facing": {
                "buff": f"INERTIAL FOCUS: Pure physical/gravitational stability without radiation interference.",
                "debuff": "ENERGY DEPLETION: Must rely on stored kinetic or auxiliary battery cells."
            },
            "transit_facing": {
                "buff": "HARMONIC BASELINE: Stable, predictable capability output.",
                "debuff": "STANDARD LIMIT: Bounded by standard stamina and equipment ratings."
            },
            "subspace": "Subspace isolation baseline (Re = 0.5)."
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Faction Physics & Technology Matrix")
    parser.add_argument("--faction", required=True, help="Faction name to inspect")
    
    args = parser.parse_args()
    res = get_faction_profile(args.faction)
    print(json.dumps(res, indent=2))
