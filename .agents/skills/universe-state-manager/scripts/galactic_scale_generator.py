#!/usr/bin/env python3
"""
Galactic Scale Engine & Procedural Universe Generator for The Stellar Confluence Universe
Generates infinite star systems, exotic planetary biomes, majestic alien creatures (xenobiology),
interstellar cultures & traditions, local transport hubs, governance models, and dynamic sub-factions
across trillions of coordinates [X, Y, Z].
"""

import os
import sys
import json
import math
import hashlib
import random
import argparse
from typing import Dict, Any, List, Optional

# Ensure core and parent script paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Stellar Classifications & Astronomical Phenomena
STELLAR_CLASSIFICATIONS = [
    {
        "type": "O-TYPE_HYPERGIANT",
        "description": "Blazing blue-white hypergiant radiating extreme ultraviolet luminosity and fierce stellar winds.",
        "color_vibe": "Cobalt Blue and Blinding White",
        "luminosity_solar": 50000.0,
        "radiation_hazard": "Extreme Ionizing Surge",
        "wavefront_interaction": "Supercharges radiant lenses with violent harmonic harmonics."
    },
    {
        "type": "B-TYPE_BLUE_STAR",
        "description": "Luminous blue star with intense high-energy photonic radiation and fast rotation.",
        "color_vibe": "Azure and Electric Cyan",
        "luminosity_solar": 800.0,
        "radiation_hazard": "High Photonic Pressure",
        "wavefront_interaction": "Smooth, high-yield beam focusing."
    },
    {
        "type": "A-TYPE_WHITE_STAR",
        "description": "Bright white main-sequence star with strong ionized hydrogen absorption lines.",
        "color_vibe": "Pure Diamond White",
        "luminosity_solar": 25.0,
        "radiation_hazard": "Moderate UV",
        "wavefront_interaction": "Optimal crystal clarity for optical arrays."
    },
    {
        "type": "F-TYPE_YELLOW_WHITE_BINARY",
        "description": "Graceful binary star pair revolving around a shared gravitational barycenter.",
        "color_vibe": "Warm Amber and Golden White",
        "luminosity_solar": 3.5,
        "radiation_hazard": "Low to Moderate",
        "wavefront_interaction": "Harmonic dual-wave interference patterns."
    },
    {
        "type": "G-TYPE_SOLAR_PRIMARY",
        "description": "Stable yellow dwarf providing benevolent warmth and balanced daylight spectrums.",
        "color_vibe": "Golden Honey and Emerald Flare",
        "luminosity_solar": 1.0,
        "radiation_hazard": "Baseline Low",
        "wavefront_interaction": "Perfect balance of solar charging and thermal safety."
    },
    {
        "type": "K-TYPE_ORANGE_DWARF",
        "description": "Long-lived orange dwarf star with steady, tranquil radiance and low flare volatility.",
        "color_vibe": "Deep Tangerine and Russet Bronze",
        "luminosity_solar": 0.35,
        "radiation_hazard": "Minimal",
        "wavefront_interaction": "Calm, continuous energy absorption."
    },
    {
        "type": "M-TYPE_RED_DWARF_SYSTEM",
        "description": "Dim, cool red dwarf harboring close-orbit tidally locked worlds and occasional superflares.",
        "color_vibe": "Crimson Ruby and Smoldering Ember",
        "luminosity_solar": 0.05,
        "radiation_hazard": "Variable Flare Bursts",
        "wavefront_interaction": "Apex conditions for shadow-weaving and stealth hulls."
    },
    {
        "type": "MAGNETAR_PULSAR_BEACON",
        "description": "Ultra-dense spinning neutron star projecting quadrillion-Gauss magnetic fields and periodic beam pulses.",
        "color_vibe": "Violet Lightning and Pulsing Emerald Arc",
        "luminosity_solar": 0.001,
        "radiation_hazard": "Cataclysmic Magnetic Flux",
        "wavefront_interaction": "Induces rhythmic sub-space resonance shocks across entire sector."
    },
    {
        "type": "MICRO_SINGULARITY_ACCRETION_DISK",
        "description": "Ancient stellar-mass black hole surrounded by a luminous, swirling relativistic accretion ring.",
        "color_vibe": "Obsidian Void haloed by Neon Gold Plasma",
        "luminosity_solar": 1500.0,
        "radiation_hazard": "Gravitational Tidal Shear",
        "wavefront_interaction": "Bends the Confluence Wavefront into extreme slingshot vectors."
    },
    {
        "type": "DIFFUSE_EMISSION_NEBULA_CLUSTER",
        "description": "Expansive interstellar nursery of glowing ionized gas, dust pillars, and proto-stellar cores.",
        "color_vibe": "Iridescent Magenta, Cyan, and Phosphor Lilac",
        "luminosity_solar": 12.0,
        "radiation_hazard": "Static Ion Drift",
        "wavefront_interaction": "Conducts wavefront vibrations like a giant cosmic musical harp."
    }
]

# 30+ Exotic Celestial Biomes
EXOTIC_BIOME_ARCHETYPES = [
    {
        "biome_id": "CRYSTAL_SPIRE_FOREST",
        "name": "Crystalline Spires & Harmonic Quartz Canopies",
        "terrain": "Towering natural prisms of vibrating silicate crystal growing over mineral pools.",
        "atmosphere": "77% N2, 21% O2, 2% Resonant Silicate Mist",
        "gravity_range": [0.8, 1.15],
        "key_resource": "Harmonic Quartz Prisms",
        "transport_hub": "Resonant Quartz Suncatcher Port & Glider Tramways",
        "environmental_wonder": "Singing crystal groves that chime when Confluence Wavefront crests."
    },
    {
        "biome_id": "BIOLUMINESCENT_ABYSSAL_FJORDS",
        "name": "Bioluminescent Fjord Coastlines & Sea-Spore Terraces",
        "terrain": "Deep marine rifts glowing with phosphorescent algae and stepped emerald shelf canyons.",
        "atmosphere": "75% N2, 23% O2, 2% Moisture / Bioluminescent Spores",
        "gravity_range": [0.9, 1.05],
        "key_resource": "Luminescent Sea Spores",
        "transport_hub": "Sub-Oceanic Benthic Crawler Gantry & Hydrofoil Docks",
        "environmental_wonder": "Night-glowing tidal swells that illuminate sea-caves in vibrant turquoise."
    },
    {
        "biome_id": "COPPER_SAND_DUNES",
        "name": "Shifting Copper Dunes & High Basalt Mesas",
        "terrain": "Expansive rolling dunes of pulverized metallic sand beneath towering tablelands.",
        "atmosphere": "76% N2, 21% O2, 2.5% Ar, 0.5% Solar Ionized Trace",
        "gravity_range": [0.95, 1.1],
        "key_resource": "Sol-Core Focusing Crystals",
        "transport_hub": "Copper Sand-Sail Skiff Anchorage & Thermal Launch Arches",
        "environmental_wonder": "Mirage arcs that focus sunlight into dazzling golden bridges."
    },
    {
        "biome_id": "GLACIATED_VAPOR_SLOPES",
        "name": "Sub-Zero Glaciated Slopes & Comet Vapor Plumes",
        "terrain": "Pristine blue methane-ice ridges vented by roaring cryo-steam geysers.",
        "atmosphere": "Sublimated H2O Vapor, Methane, Ionized Dust",
        "gravity_range": [0.25, 0.5],
        "key_resource": "High-Density Cryo-Ice",
        "transport_hub": "Cryo-Sublimation Skiff Slipways & Catapult Launch Troughs",
        "environmental_wonder": "Low-gravity ice plumes allowing starfarers to leap hundreds of meters."
    },
    {
        "biome_id": "FLOATING_CLOUD_ARCHIPELAGOS",
        "name": "Suspended Gas Islands & Magnetic Cloud Bridges",
        "terrain": "Lightweight porous islands drifting on dense tropospheric thermal currents.",
        "atmosphere": "72% N2, 20% O2, 6% Water Vapor, 2% Helium",
        "gravity_range": [0.55, 0.85],
        "key_resource": "Aerostat Buoyancy Crystals",
        "transport_hub": "Aerostat Float-Barge Moorings & Skyhook Tether Terminals",
        "environmental_wonder": "Vast cloud waterfalls falling endlessly into shimmering storm beds."
    },
    {
        "biome_id": "BASALT_MAGMA_VAULTS",
        "name": "Subterranean Magma Vaults & Tectonic Steam Wells",
        "terrain": "Gigantic obsidian caverns heated by subterranean magma rivers and hydraulic columns.",
        "atmosphere": "70% N2, 18% CO2, 10% O2, 2% Sulfur Trace",
        "gravity_range": [1.2, 1.5],
        "key_resource": "Dense Basalt Ore & Geothermal Cells",
        "transport_hub": "Geothermal Shaft Elevators & Heavy Tectonic Rail Borers",
        "environmental_wonder": "Tectonic resonance pulses that power massive natural steam organs."
    },
    {
        "biome_id": "PLASMA_CORONAL_REEFS",
        "name": "Orbital Solar Prominence Reefs & Magnetic Bridges",
        "terrain": "Stationary magnetic scaffolding capturing roaring ribbons of stellar plasma.",
        "atmosphere": "Shielded Habitat Nitrogen-Oxygen Matrix",
        "gravity_range": [0.65, 0.9],
        "key_resource": "Bottled Solar Plasma",
        "transport_hub": "Magnetic Coronal Scooper Berths & Solar-Sail Staging Rings",
        "environmental_wonder": "Dancing coronal arches looping millions of kilometers over star platforms."
    },
    {
        "biome_id": "TEMPORAL_TIDAL_SHALLOWS",
        "name": "Luminous Chrono-Lagoons & Tachyon Sands",
        "terrain": "Iridescent turquoise shallows where water droplets hover suspended during wave shifts.",
        "atmosphere": "78% N2, 21% O2, 1% Tachyon Trace",
        "gravity_range": [0.9, 1.02],
        "key_resource": "Tachyon Chrono-Crystals",
        "transport_hub": "Chrono-Skiff Tidal Slipways & Tachyon Slipstream Waypoints",
        "environmental_wonder": "Ripples in the sand that display gentle glimpses of upcoming wavefront crests."
    },
    {
        "biome_id": "GREAT_BIO_CANOPY",
        "name": "Bioluminescent Mega-Canopies & Symbiotic Root Cities",
        "terrain": "Enormous kilometer-tall trees with interconnected root walkways and spore gardens.",
        "atmosphere": "74% N2, 24% O2, 2% Living Spore Mist",
        "gravity_range": [0.85, 1.1],
        "key_resource": "Medicinal Spore Salves & Living Chitin",
        "transport_hub": "Living Manta-Craft Roosts & Canopy Cableway Gliders",
        "environmental_wonder": "Bioluminescent leaf-lanterns that open in rhythm with passing starships."
    },
    {
        "biome_id": "GRAVITON_WELL_CRATERS",
        "name": "Singularity Vector Arcs & Curved Graviton Slopes",
        "terrain": "Smooth obsidian basins engineered to slingshot kinetic gliders into orbital escape.",
        "atmosphere": "78% N2, 21% O2, 1% Filtered Mist",
        "gravity_range": [0.7, 1.25],
        "key_resource": "Graviton Well Anchors",
        "transport_hub": "Gravitational Slingshot Chutes & Sub-orbital Launch Bowls",
        "environmental_wonder": "Gravitational slides where children and scouts practice frictionless gliding."
    },
    {
        "biome_id": "SILICON_WEBBED_CANYONS",
        "name": "Ionized Filament Webs & Phosphor Mist Valleys",
        "terrain": "Deep chasms spanned by intricate electromagnetic silk nets woven across cliffs.",
        "atmosphere": "76% N2, 21% O2, 3% Ionized Gas Vapor",
        "gravity_range": [0.4, 0.75],
        "key_resource": "Plasma Silk Filaments",
        "transport_hub": "Filament Web Suspension Trams & Subspace Glider Hangars",
        "environmental_wonder": "Luminous webs that catch cosmic dust and glow like multicolored constellations."
    },
    {
        "biome_id": "CLOCKWORK_RING_MEGACITY",
        "name": "Tiered Brass Habitats & Flywheel Meridian Towers",
        "terrain": "Massive artificial orbital rings interlocked by giant bronze gear trains and aqueducts.",
        "atmosphere": "78% N2, 21% O2, 1% Filtered Mist",
        "gravity_range": [0.95, 1.05],
        "key_resource": "High-Torque Precision Brass & Chrono-Astrolabes",
        "transport_hub": "Interlocking Meridian Gear-Gondola Rails & Vacuum Mag-Lev Terminals",
        "environmental_wonder": "Synchronized meridian chimes that ring in harmony across entire planetary sectors."
    }
]

# Boundless Cosmic Wonders & Anomalies Catalog
COSMIC_ANOMALIES_CATALOG = [
    {
        "anomaly_id": "DYSON_SWARM_ORBITAL_FORGE",
        "name": "The Great Dyson Photonic Collector Swarm",
        "scale": "System Scale (100 Million km orbital ring)",
        "scientific_basis": "Trillions of synchronized solar-sail mirrors orbiting a star to harness pure radiant luminosity without blocking planetary life.",
        "intuitive_analogy": "Like billions of tiny golden umbrellas angled to catch sunbeams and beam warm, clean power across the entire star system.",
        "sensory_spectacle": "A glittering diamond belt circling the star, pulsing with emerald and golden energy beams like a living cosmic crown.",
        "navigational_significance": "Provides hyper-charged solar battery recharging and instantaneous photonic data relays."
    },
    {
        "anomaly_id": "SINGING_QUARTZ_NEBULA",
        "name": "The Harmonic Resonance Nebular Harp",
        "scale": "Sector Scale (3 Light-Years Across)",
        "scientific_basis": "Suspended ionized silicate micro-crystals vibrating in harmonic frequency with incoming Confluence Wavefronts.",
        "intuitive_analogy": "Like a giant cosmic musical harp strung across light-years that chimes in sweet, soothing chords as stellar waves pass through.",
        "sensory_spectacle": "Gleaming lavender and turquoise dust clouds that physically hum like cello strings when starships glide through.",
        "navigational_significance": "Acoustic beacon network that allows sub-light vessels to navigate without electronic radar."
    },
    {
        "anomaly_id": "GRAVITATIONAL_LENSING_MIRAGE",
        "name": "The Prismatic Einstein Ring Window",
        "scale": "Stellar Scale (0.5 Light-Years)",
        "scientific_basis": "A massive micro-singularity warping surrounding space, bending distant galaxy light into a perfect circular rainbow lens.",
        "intuitive_analogy": "Like looking through a giant crystal magnifying glass held up in space, showing events happening on the other side of the galaxy.",
        "sensory_spectacle": "A swirling kaleidoscope of ancient stars and multicolored nebulae warped into brilliant glowing concentric halos.",
        "navigational_significance": "Permits direct real-time visual observation of distant sectors without subspace lag."
    },
    {
        "anomaly_id": "TACHYON_SLIPSTREAM_GEYSER",
        "name": "The Primordial Chrono-Slipstream Well",
        "scale": "Planetary Scale (120,000 km jet)",
        "scientific_basis": "A concentrated relativistic particle plume vented from a deep subspace fissure, creating localized low-drag transit corridors.",
        "intuitive_analogy": "Like an underwater waterslide made of pure glowing starlight that whisks exploration ships across star systems in minutes.",
        "sensory_spectacle": "A sapphire jet of crackling starlight rushing into deep space, where suspended water droplets freeze in glowing time-loops.",
        "navigational_significance": "Enables Tier 3 interstellar craft to achieve 50c super-luminal speeds with zero fuel burn."
    },
    {
        "anomaly_id": "ANCIENT_KEYSTONE_STARFORGE",
        "name": "The Keystone Celestial Artificer Ring",
        "scale": "Mega-Structure (25,000 km diameter)",
        "scientific_basis": "Precursor magnetic containment ring anchored over a calm stellar pole, utilizing natural coronal flares to forge ultra-dense alloys.",
        "intuitive_analogy": "A giant floating blacksmith's anvil where starfarers use the gentle heat of the star to craft perfect brass gears and glass lenses.",
        "sensory_spectacle": "Golden arcs of plasma looping gracefully through circular brass gantries into crystal cooling pools.",
        "navigational_significance": "Universal repair and calibration sanctuary for all peaceful space travelers."
    }
]

# Xenobiology: Majestic Alien Creatures & Fauna
ALIEN_CREATURE_CATALOG = [
    {
        "species_name": "Grav-Whale (Leviathan Gravitas)",
        "temperament": "Gentle, majestic, highly intelligent nomadic traveler",
        "biome_niche": "Deep space void, asteroid belts, and gas giant upper stratospheres",
        "size_scale": "Colossal (40 to 120 meters long)",
        "sensory_capability": "Detects Confluence Wavefront ripples across several light-hours",
        "interaction_protocol": "Broadcasts harmonic sub-acoustic chimes; safe to fly alongside in sub-light formation.",
        "dietary_medium": "Grazes on ionized cosmic dust and charged solar wind plumes",
        "adventure_hook": "A lost juvenile Grav-Whale is separated from its pod near an active debris field and needs guidance."
    },
    {
        "species_name": "Photonic Light-Moth (Lepidoptera Solaris)",
        "temperament": "Curious, playful, attracted to focused radiant beams",
        "biome_niche": "Copper sand dunes, solar observatories, and glass canyons",
        "size_scale": "Small to Medium (0.5 to 1.5 meter wingspan)",
        "sensory_capability": "Prismatic crystal wings reflect sunlight into vibrant shielding halos",
        "interaction_protocol": "Easily befriended by holding up a polished solar lens with steady, gentle light.",
        "dietary_medium": "Nectar of solar-blooming desert succulents",
        "adventure_hook": "Flocks of Light-Moths have nested inside a telescope dome, refracting signals into dazzling star maps."
    },
    {
        "species_name": "Phase-Stalker (Umbra Felis)",
        "temperament": "Elusive, watchful, loyal guardian of quiet subterranean paths",
        "biome_niche": "Basalt eclipse chasms and subterranean bioluminescent caverns",
        "size_scale": "Medium (2 to 3 meters length, sleek quadruped)",
        "sensory_capability": "Can momentarily phase through solid rock to avoid falling debris",
        "interaction_protocol": "Approach with quiet footsteps and offer glowing moss; never make sudden loud noises.",
        "dietary_medium": "Consumes subterranean mineral salts and twilight lichen",
        "adventure_hook": "A Phase-Stalker guides an injured apprentice monk out of a collapsed basalt tunnel."
    },
    {
        "species_name": "Silicon-Weaver Spider (Arachna Filamenti)",
        "temperament": "Industrious, peaceful, master architect of electromagnetic webs",
        "biome_niche": "Nebula loom spires and magnetic cliff chasms",
        "size_scale": "Large (1 to 2 meters across)",
        "sensory_capability": "Spins plasma-conductive silk lines that detect micro-vibrations in starship hulls",
        "interaction_protocol": "Communicate using rhythmic pulse taps on support cables.",
        "dietary_medium": "Harvests electrostatic charge from passing gas clouds",
        "adventure_hook": "Spiders have woven a safety net across a damaged bridge, preventing cargo transport loss."
    },
    {
        "species_name": "Coronal Drake (Draco Solaris)",
        "temperament": "Spirited, brave, loves diving through stellar prominence loops",
        "biome_niche": "Solar forge platforms and coronal magnetic arcs",
        "size_scale": "Large (8 to 15 meters wingspan, metallic thermal scales)",
        "sensory_capability": "Immune to extreme radiant heat; channels excess thermal energy through crest fins",
        "interaction_protocol": "Align magnetic lasso gently with its flight path; responds to whistling thermal tones.",
        "dietary_medium": "Absorbs raw solar plasma flare bursts",
        "adventure_hook": "A Coronal Drake alerts plasma shepherds to an unexpected coronal mass ejection before sensors trip."
    },
    {
        "species_name": "Chrono-Tortoise (Aevum Testudo)",
        "temperament": "Wise, tranquil, ancient living chronometer",
        "biome_niche": "Tachyon shallows and tidal chrono-lagoons",
        "size_scale": "Huge (3 to 6 meters shell diameter)",
        "sensory_capability": "Carries crystalline shell facets that rotate like precision gears to mark tidal epochs",
        "interaction_protocol": "Speak in slow, clear sentences; safe to ride across deep tidal shallows.",
        "dietary_medium": "Slowly grazes on temporal kelp and mineral crystals",
        "adventure_hook": "An ancient Chrono-Tortoise carries the lost coordinates to a forgotten stellar stargate etched into its shell."
    },
    {
        "species_name": "Bioluminescent Coral Colossus (Polypus Giganteus)",
        "temperament": "Stationary, nurturing, living reef sanctuary",
        "biome_niche": "Bioluminescent abyssal fjords and ocean shallows",
        "size_scale": "Massive (Hundreds of meters wide)",
        "sensory_capability": "Creates an oxygen-rich, warm water oasis shielded from surface storms",
        "interaction_protocol": "Swim gently near exterior lanterns; emits soothing flute-like tones through siphon tubes.",
        "dietary_medium": "Photosynthetic and chemosynthetic ocean currents",
        "adventure_hook": "Provides emergency underwater refuge for starship crew whose shuttle ditched in a coastal lagoon."
    },
    {
        "species_name": "Magnetic Glide-Ray (Manta Magnetica)",
        "temperament": "Graceful, playful, loves surfing planetary magnetic lines",
        "biome_niche": "Upper atmospheres of ring worlds and gas giants",
        "size_scale": "Medium to Large (4 to 8 meters wingspan)",
        "sensory_capability": "Glides along magnetic field lines with zero propulsion fuel",
        "interaction_protocol": "Match glider pitch with the ray's wing tilt; enjoys flying in tandem formations.",
        "dietary_medium": "Filters airborne pollen and charged atmospheric aerosols",
        "adventure_hook": "A flight of Glide-Rays guides a solar glider through an atmospheric storm safely to landing."
    }
]

# Interstellar Cultures, Customs & Traditions
CULTURE_TRAITS = {
    "philosophies": [
        "The Harmonic Convergence: All stars and starfarers are threads in a single great tapestry.",
        "The Law of the Lens: Truth is discovered when minds align with calm focus and clear vision.",
        "The Quiet Watch: In silence and patience, the hidden paths of the universe reveal themselves.",
        "The Clockwork Balance: Every tooth in the gear, no matter how small, keeps the entire galaxy turning.",
        "The Wave-Rider's Creed: Never fight the current; find the curve of gravity and ride it with courage.",
        "The Seedling's Promise: Nurture your friends and worlds, and shelter will grow when storms arrive."
    ],
    "hospitality_rituals": [
        "Presenting a cool, freshly polished glass of sweet solar nectar upon greeting.",
        "Sharing a bowl of glowing bioluminescent tea brewed from subterranean canyon leaves.",
        "Gift of a hand-carved miniature brass compass calibrated to the visitor's homeworld.",
        "Offering a warm thermal blanket and a cup of pure melted comet-tail ice water.",
        "Waving a woven plasma-silk ribbon to signal peace, sanctuary, and open landing bays.",
        "Exchanging a small, smooth wishing stone harvested from the deepest bedrock stratum."
    ],
    "art_and_craftsmanship": [
        "Stained-glass solar sculptures that project moving star maps across city plazas.",
        "Obsidian acoustic chimes that sing soft lullabies when twilight winds sweep the canyons.",
        "Precision brass music boxes driven by miniature perpetual gravity flywheels.",
        "Tapestries woven from luminescent gas filaments that shift colors with seasonal tides.",
        "Intricate rock-crystal carvings depicting legendary space navigators and their bioships.",
        "Living bonsai spore trees cultivated to illuminate household reading alcoves."
    ],
    "sacred_festivals": [
        "The Festival of the Zenith Meridian (Celebration of light, lens polishing, and solar games)",
        "The Twilight Night of Echoes (Candlelit canyon walks and quiet storytelling under star clusters)",
        "The Great Orrery Springing (Day-long festival where the grand meridian gears are oiled and wound)",
        "The Cometary Regatta (Youth space-glider race through illuminated vapor rings)",
        "The Spore Bloom Carnival (Night-blooming flora light up the mega-canopy in dazzling rainbow colors)",
        "The Tide-Turning Feast (Sharing ocean-harvested delicacies and launching glowing paper sky-buoys)"
    ]
}

# Sub-Faction Enclave Archetypes
SUB_FACTION_ROLES = [
    "Planetary Cartographers Guild",
    "Solar Observatory Artificers",
    "Deep-Space Search & Rescue Fleet",
    "Astrolabe Chronometer Apprentices",
    "Xenobiological Wildlife Wardens",
    "Interstellar Merchant Caravan Enclave",
    "Subterranean Hydro-Engineers Guild",
    "Nebula Filament Artisans Collective",
    "Gravitational Slingshot Scouts",
    "Coronal Beacon Maintenance Crew",
    "Subspace Relay Signal Keepers",
    "Symbiotic Flora Gardeners Alliance"
]

def hash_coords(coords: str) -> int:
    """Computes a deterministic integer seed from 3D coordinates or a string name."""
    clean = coords.strip().lower()
    h = hashlib.sha256(clean.encode("utf-8")).hexdigest()
    return int(h[:8], 16)

def generate_star_system(coords: str = "[0, 0, 0]", system_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Procedurally generates a complete, astronomically grounded star system
    for ANY arbitrary coordinates [X, Y, Z] in the universe.
    """
    seed = hash_coords(f"{coords}_{system_name or ''}")
    rng = random.Random(seed)

    # 1. Stellar Primary
    stellar_class = rng.choice(STELLAR_CLASSIFICATIONS)
    system_name = system_name or f"Sector-{abs(seed % 10000):04d} ({stellar_class['type'].split('_')[0]})"

    # 2. Planetary Body Count
    planet_count = rng.randint(2, 8)
    planets = []

    for i in range(1, planet_count + 1):
        p_seed = seed + i * 997
        p_rng = random.Random(p_seed)
        
        biome = p_rng.choice(EXOTIC_BIOME_ARCHETYPES)
        creature = p_rng.choice(ALIEN_CREATURE_CATALOG)
        grav = round(p_rng.uniform(biome["gravity_range"][0], biome["gravity_range"][1]), 2)
        cycle = p_rng.randint(6, 48)
        axial = round(p_rng.uniform(0.0, 35.0), 1)

        p_name = f"{system_name} - World {chr(64 + i)} ({biome['name'].split('&')[0].strip()})"
        planets.append({
            "planet_index": i,
            "planet_name": p_name,
            "orbital_distance_au": round(0.4 * i + p_rng.uniform(0.1, 0.3), 2),
            "biome_id": biome["biome_id"],
            "biome_title": biome["name"],
            "terrain_summary": biome["terrain"],
            "atmospheric_mix": biome["atmosphere"],
            "surface_gravity_g": grav,
            "diurnal_cycle_gut": cycle,
            "axial_tilt_deg": axial,
            "key_exports": [biome["key_resource"], f"Pure Refined Core #{i}"],
            "transport_infrastructure": biome.get("transport_hub", "Standard Orbital Spaceport"),
            "environmental_wonder": biome["environmental_wonder"],
            "indigenous_creature": {
                "species": creature["species_name"],
                "temperament": creature["temperament"],
                "scale": creature["size_scale"],
                "wonder_interaction": creature["interaction_protocol"]
            }
        })

    # 3. Interstellar Culture & Traditions
    culture = {
        "dominant_philosophy": rng.choice(CULTURE_TRAITS["philosophies"]),
        "hospitality_custom": rng.choice(CULTURE_TRAITS["hospitality_rituals"]),
        "signature_art": rng.choice(CULTURE_TRAITS["art_and_craftsmanship"]),
        "annual_festival": rng.choice(CULTURE_TRAITS["sacred_festivals"])
    }

    # 4. Local Sub-Factions / Enclaves
    sub_factions = [
        f"{rng.choice(SUB_FACTION_ROLES)} of {system_name}",
        f"Order of the {stellar_class['color_vibe'].split()[0]} Horizon"
    ]

    return {
        "status": "SYSTEM_GENERATED",
        "coordinates": coords,
        "system_name": system_name,
        "stellar_classification": stellar_class["type"],
        "stellar_description": stellar_class["description"],
        "stellar_color_vibe": stellar_class["color_vibe"],
        "luminosity_solar": stellar_class["luminosity_solar"],
        "radiation_hazard": stellar_class["radiation_hazard"],
        "confluence_wave_interaction": stellar_class["wavefront_interaction"],
        "total_planetary_bodies": planet_count,
        "planets": planets,
        "indigenous_culture": culture,
        "active_sub_factions": sub_factions
    }

def generate_full_planetary_system(coords: str = "[0, 0, 0]", system_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a full, multi-body star system featuring goldilocks habitable zone calculations,
    rocky inner worlds, habitable ribbon moons, gas giants with shepherd rings, asteroid belts, and Oort cloud reservoirs.
    """
    base = generate_star_system(coords, system_name)
    seed = hash_coords(f"full_{coords}_{system_name or ''}")
    rng = random.Random(seed)

    lum = base.get("luminosity_solar", 1.0)
    # Goldilocks habitable zone: R_hab = sqrt(L_solar)
    hab_center_au = round(math.sqrt(max(0.01, lum)), 2)
    hab_inner_au = round(hab_center_au * 0.85, 2)
    hab_outer_au = round(hab_center_au * 1.35, 2)

    # Add astronomy details to planets
    enhanced_planets = []
    for p in base["planets"]:
        dist = p["orbital_distance_au"]
        is_habitable = (hab_inner_au <= dist <= hab_outer_au)
        zone_desc = "Goldilocks Habitable Zone" if is_habitable else ("Inner Thermal Scorched Zone" if dist < hab_inner_au else "Outer Cryo-Glaciated Zone")
        
        # Kepler's Third Law: Period (Years) = sqrt(a^3 / M)
        mass_star = next((s.get("mass_solar", 1.0) for s in STELLAR_CLASSIFICATIONS if s["type"] == base["stellar_classification"]), 1.0)
        orbital_period_years = round(math.sqrt((dist ** 3) / max(0.1, mass_star)), 2)
        
        # Moon system
        moon_count = rng.randint(0, 4) if dist < 2.0 else rng.randint(3, 14)
        moons = [f"{p['planet_name']} - Moon {j+1}" for j in range(moon_count)]

        enhanced_p = dict(p)
        enhanced_p["habitable_zone_status"] = zone_desc
        enhanced_p["is_habitable_zone"] = is_habitable
        enhanced_p["orbital_period_standard_years"] = orbital_period_years
        enhanced_p["moon_count"] = moon_count
        enhanced_p["major_moons"] = moons[:3]
        enhanced_planets.append(enhanced_p)

    # Asteroid Belts and Megastructures
    asteroid_belt = {
        "name": f"{base['system_name']} Primary Asteroid Ring",
        "orbital_radius_au": round(hab_outer_au * 1.6, 2),
        "composition": "Silicate, Refined Brass Nodules & High-Density Sol-Core Ore",
        "mining_stations": rng.randint(2, 6)
    }

    return {
        "status": "FULL_PLANETARY_SYSTEM_GENERATED",
        "coordinates": coords,
        "system_name": base["system_name"],
        "stellar_classification": base["stellar_classification"],
        "stellar_color_vibe": base["stellar_color_vibe"],
        "luminosity_solar": lum,
        "habitable_zone_range_au": f"{hab_inner_au} AU to {hab_outer_au} AU (Center: {hab_center_au} AU)",
        "total_planets": len(enhanced_planets),
        "planets": enhanced_planets,
        "asteroid_belt": asteroid_belt,
        "indigenous_culture": base["indigenous_culture"],
        "active_sub_factions": base["active_sub_factions"]
    }

def generate_cosmic_anomaly(coords: str = "[0, 0, 0]", anomaly_type: Optional[str] = None) -> Dict[str, Any]:
    """Generates an awe-inspiring cosmic anomaly or ancient megastructure for exploration adventures."""
    seed = hash_coords(f"anomaly_{coords}_{anomaly_type or ''}")
    rng = random.Random(seed)

    if anomaly_type:
        anomaly = next((a for a in COSMIC_ANOMALIES_CATALOG if a["anomaly_id"] == anomaly_type.upper()), rng.choice(COSMIC_ANOMALIES_CATALOG))
    else:
        anomaly = rng.choice(COSMIC_ANOMALIES_CATALOG)

    return {
        "status": "COSMIC_ANOMALY_GENERATED",
        "coordinates": coords,
        "anomaly_id": anomaly["anomaly_id"],
        "name": anomaly["name"],
        "scale": anomaly["scale"],
        "scientific_basis": anomaly["scientific_basis"],
        "intuitive_analogy": anomaly["intuitive_analogy"],
        "sensory_spectacle": anomaly["sensory_spectacle"],
        "navigational_significance": anomaly["navigational_significance"],
        "adventure_recommendation": "Explore anomaly using harmonic sensors and maintain safe standoff distance."
    }

def generate_xenobiology_ecosystem(biome_id: Optional[str] = None, seed_str: str = "ecosystem") -> Dict[str, Any]:
    """Generates a complete multi-tier living ecological network (producers, grazers, leviathans, stewards)."""
    seed = hash_coords(f"{biome_id or ''}_{seed_str}")
    rng = random.Random(seed)

    biome = next((b for b in EXOTIC_BIOME_ARCHETYPES if b["biome_id"] == biome_id), rng.choice(EXOTIC_BIOME_ARCHETYPES))
    primary_creature = rng.choice(ALIEN_CREATURE_CATALOG)
    secondary_creature = rng.choice([c for c in ALIEN_CREATURE_CATALOG if c != primary_creature])

    producers = [
        f"Luminescent {biome['name'].split()[0]} Algal Blooms (Converts Confluence wavefronts into pure sugars)",
        f"Thermophilic Quartz Lichen (Harvests geothermal warmth and mineral salts)"
    ]
    grazers = [
        f"Gliding {biome['name'].split()[0]} Spore-Motes (Filters airborne pollen and dust)",
        f"Miniature {primary_creature['species_name'].split()[0]} Companions"
    ]

    return {
        "status": "ECOSYSTEM_GENERATED",
        "biome_id": biome["biome_id"],
        "biome_title": biome["name"],
        "atmospheric_medium": biome["atmosphere"],
        "primary_producers": producers,
        "herbivorous_grazers": grazers,
        "apex_majestic_fauna": [primary_creature["species_name"], secondary_creature["species_name"]],
        "ecological_symbiosis": f"{primary_creature['species_name'].split()[0]} feeds on spore plumes and spreads crystal seeds across {biome['terrain'][:40]}...",
        "ethical_observation_code": "Preserve natural migratory channels; never use high-thrust engines within 50 km."
    }

def generate_subfaction_enclave(core_faction: str = "Sun-Forged Hegemony", seed_str: str = "enclave") -> Dict[str, Any]:
    """Procedurally generates a unique cultural sub-faction enclave across millions of world offshoots."""
    seed = hash_coords(f"{core_faction}_{seed_str}")
    rng = random.Random(seed)

    role = rng.choice(SUB_FACTION_ROLES)
    mottos = [
        "Steer true, fear no shadow.",
        "Every tooth in the gear counts.",
        "Patience opens the deepest doors.",
        "Share the stardust and keep the peace.",
        "Honor the wind and the craft."
    ]
    specialties = [
        "Hand-polished prismatic quartz telescope lenses",
        "Ultra-light ceramic sand-skis for high-speed desert sailing",
        "Acoustic sub-chime communicators for Grav-Whale signaling",
        "Self-lubricating perpetual brass gear bearings",
        "Warm amber tea blending and herbal star-bloom salves"
    ]

    return {
        "status": "SUB_FACTION_ENCLAVE_GENERATED",
        "enclave_name": f"{role} of {core_faction} (Sector-{abs(seed % 1000):03d})",
        "parent_faction": core_faction,
        "cultural_motto": rng.choice(mottos),
        "craftsmanship_specialty": rng.choice(specialties),
        "traditional_staple": f"Warm spiced tea and {rng.choice(['crispy honey-grain wafers', 'sweet roasted succotash', 'sun-dried berry rolls'])}",
        "civic_role": "Maintains navigational safety and welcomes friendly travelers in the sector."
    }

def generate_creature_encounter(biome_id: Optional[str] = None, seed_str: str = "encounter") -> Dict[str, Any]:
    """Generates an engaging, non-violent alien creature encounter for adventures or chapters."""
    seed = hash_coords(f"{biome_id or ''}_{seed_str}")
    rng = random.Random(seed)

    creature = rng.choice(ALIEN_CREATURE_CATALOG)
    biome = next((b for b in EXOTIC_BIOME_ARCHETYPES if b["biome_id"] == biome_id), rng.choice(EXOTIC_BIOME_ARCHETYPES))

    return {
        "status": "CREATURE_ENCOUNTER_GENERATED",
        "creature_name": creature["species_name"],
        "size_scale": creature["size_scale"],
        "temperament": creature["temperament"],
        "habitat": f"{biome['name']} ({creature['biome_niche']})",
        "sensory_specialty": creature["sensory_capability"],
        "dietary_source": creature["dietary_medium"],
        "friendly_handling_protocol": creature["interaction_protocol"],
        "adventure_scenario": creature["adventure_hook"]
    }

def generate_cultural_profile(faction_or_world: str = "Sun-Forged Hegemony") -> Dict[str, Any]:
    """Generates a deep cultural and traditional profile for any faction or world."""
    seed = hash_coords(faction_or_world)
    rng = random.Random(seed)

    return {
        "status": "CULTURAL_PROFILE_GENERATED",
        "entity_name": faction_or_world,
        "core_philosophy": rng.choice(CULTURE_TRAITS["philosophies"]),
        "hospitality_ritual": rng.choice(CULTURE_TRAITS["hospitality_rituals"]),
        "art_form": rng.choice(CULTURE_TRAITS["art_and_craftsmanship"]),
        "sacred_festival": rng.choice(CULTURE_TRAITS["sacred_festivals"]),
        "traditional_greeting": f"May your path be steady under the {rng.choice(['radiant dawn', 'calm twilight', 'turning stars', 'gentle tide', 'clear compass'])}."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Scale Engine & Procedural Universe Generator")
    parser.add_argument("action", choices=["system", "system-full", "explore", "creature", "culture", "anomaly", "ecosystem", "enclave"], default="explore", nargs="?")
    parser.add_argument("--coords", default="[125, -42, 88]", help="3D Sector coordinates")
    parser.add_argument("--name", help="System or entity name")
    parser.add_argument("--biome", help="Biome ID filter")
    parser.add_argument("--faction", default="Comet-Riders", help="Faction or entity name for culture")
    parser.add_argument("--anomaly", help="Anomaly ID filter")

    args = parser.parse_args()

    if args.action in ["system", "explore"]:
        res = generate_star_system(args.coords, args.name)
    elif args.action == "system-full":
        res = generate_full_planetary_system(args.coords, args.name)
    elif args.action == "creature":
        res = generate_creature_encounter(args.biome, args.name or "wild")
    elif args.action == "culture":
        res = generate_cultural_profile(args.faction or args.name or "Universal")
    elif args.action == "anomaly":
        res = generate_cosmic_anomaly(args.coords, args.anomaly)
    elif args.action == "ecosystem":
        res = generate_xenobiology_ecosystem(args.biome, args.name or "eco")
    elif args.action == "enclave":
        res = generate_subfaction_enclave(args.faction or "Sun-Forged Hegemony", args.name or "enclave")
    else:
        res = {"error": f"Unknown action {args.action}"}

    print(json.dumps(res, indent=2))

