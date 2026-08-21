#!/usr/bin/env python3
"""
Interstellar Politics, Sociology & Civilizations Engine for The Stellar Confluence Universe
Simulates multi-tier galactic governance structures, societal stratification, civil mobility rites,
hospitality customs, sacred cosmic taboos, architectural philosophies, and bilateral treaties.
"""

import os
import sys
import json
import random
import argparse
from typing import Dict, Any, List, Optional

# Governance & Political Archetypes
GOVERNANCE_ARCHETYPES = [
    {
        "model_id": "SOLAR_HEGEMONIC_COUNCIL",
        "name": "Solar Hegemonic Artificer Council",
        "primary_factions": ["Sun-Forged Hegemony", "Plasma-Shepherds"],
        "leadership_structure": "Meritocratic Council of High Artificers and Chief Astronomers",
        "decision_making": "Photonic Consensus voting verified through solar observatory data arrays",
        "legal_charter": "The Radiant Accord: All beings have the right to clean stellar light, warmth, and safe orbital transit.",
        "diplomatic_stance": "Vigilant guardianship; welcomes peaceful travelers who respect solar corridors.",
        "economic_focus": "Solarite energy distribution, crystal refining, and deep-space beacon maintenance."
    },
    {
        "model_id": "SUBSPACE_MONASTIC_ENCLAVE",
        "name": "Subspace Monastic Assembly of Quiet Voices",
        "primary_factions": ["Void-Bound Monks", "Chrono-Navigators"],
        "leadership_structure": "Council of Twilight Elders and Silence-Keepers",
        "decision_making": "Contemplative Consensus reached during nadir eclipse vigils",
        "legal_charter": "The Law of Quiet Horizons: Power must be exercised with restraint, humility, and acoustic peace.",
        "diplomatic_stance": "Introspective neutrality; offers sanctuary and healing to any who approach without aggression.",
        "economic_focus": "Phase basalt quarrying, tachyon sands, and subterranean medicine."
    },
    {
        "model_id": "CLOCKWORK_GUILD_SYNDICATE",
        "name": "Grand Clockwork Artisan Syndicate",
        "primary_factions": ["Astrolabe Engineers"],
        "leadership_structure": "Elected Meridian Arbiters and Guild Masters of Precision",
        "decision_making": "Mathematical balance voting; proposals are weighed on mechanical voting balances",
        "legal_charter": "The Meridian Standardization Pact: Fair measure, true weight, and zero-defect craftsmanship for all worlds.",
        "diplomatic_stance": "Pragmatic commercial cooperation; enforces strict neutrality in orbital trade ports.",
        "economic_focus": "Precision brass gears, flywheels, chronometers, and automated orbital docks."
    },
    {
        "model_id": "NOMADIC_FLOTILLA_PARLIAMENT",
        "name": "United Flotilla Council of Wayfarers",
        "primary_factions": ["Comet-Riders", "Gravity-Surfers"],
        "leadership_structure": "Captain's Conclave with rotating Flotilla Admiral",
        "decision_making": "Radio-Beacon polling across all traveling convoys",
        "legal_charter": "The Free Drift Compact: The stars belong to those who wander; no barrier shall block open sky.",
        "diplomatic_stance": "Brisk, warm hospitality; highly protective of migration routes and comet nurseries.",
        "economic_focus": "Cryo-methane ice, comet vapor fuels, scout mapping, and search-and-rescue."
    },
    {
        "model_id": "DEEP_CORE_WORKER_COLLECTIVE",
        "name": "Tectonic Core Mining Collective",
        "primary_factions": ["Deep-Core Miners"],
        "leadership_structure": "Shaft Wardens and Geothermal Engineers Union",
        "decision_making": "Subterranean steam-chime consensus votes",
        "legal_charter": "The Bedrock Treaty: Equal share of ore, collective safety in the dark, and honoring the planetary spine.",
        "diplomatic_stance": "Sturdy, direct, and honest; values actions and shared labor over formal court speeches.",
        "economic_focus": "Dense structural metals, geothermal batteries, and earthquake dampeners."
    },
    {
        "model_id": "CRYSTAL_CHOIR_ACADEMY",
        "name": "Harmonic Suncatcher Choir Academy",
        "primary_factions": ["Crystal-Singers", "Nebula-Weavers"],
        "leadership_structure": "Harmonic Pitchmasters and Master Refractionists",
        "decision_making": "Acoustic resonance votes where proposals are played as multi-part chords",
        "legal_charter": "The Harmony Charter: Speech should build upon harmony, never dissonance; all worlds deserve pure song.",
        "diplomatic_stance": "Universal cultural ambassadors; hosts interstellar festivals and language exchanges.",
        "economic_focus": "Harmonic quartz, acoustic amplifiers, laser communication prisms, and musical instruments."
    },
    {
        "model_id": "BIO_SYMBIOTIC_COMMUNE",
        "name": "Living Canopy Ecological Stewardship",
        "primary_factions": ["Bio-Alchemists", "Tide-Wardens"],
        "leadership_structure": "Mycorrhizal Elders and Spore Keepers",
        "decision_making": "Ecological health councils assessing multi-generational planetary impact",
        "legal_charter": "The Living Biome Covenant: Never take from nature without planting two seeds in return.",
        "diplomatic_stance": "Gentle, protective guardians of indigenous fauna, flora, and alien biomes.",
        "economic_focus": "Medicinal star-bloom salves, living chitin hulls, bioluminescent algae, and water purification."
    }
]

# Sociological Systems & Cultural Traits
SOCIOLOGICAL_SYSTEMS = {
    "social_strata": [
        {"rank_title": "Apprentice Scout", "role": "Youth learning astronomy, tool maintenance, and environmental navigation.", "emblem": "Bronze Compass Pin"},
        {"rank_title": "Wayfarer Guide", "role": "Journeyman navigating planetary biomes, piloting skimmers, and escorting convoys.", "emblem": "Silver Star-Needle"},
        {"rank_title": "Master Artisan / Scholar", "role": "Experienced innovator crafting precision gear, leading research stations, and teaching.", "emblem": "Golden Astrolabe Ring"},
        {"rank_title": "High Artificer / Elder Keeper", "role": "Venerable mentor guiding galactic policy, tuning planetary beacons, and keeping ancient peace.", "emblem": "Prismatic Confluence Seal"}
    ],
    "rites_of_passage": [
        {
            "name": "The First Slingshot Flight",
            "description": "A young pilot navigates a solo skimmer or glider through a planetary thermal arch and lands smoothly without relying on auto-pilot.",
            "cultural_meaning": "Proves courage, steady hands, and deep respect for atmospheric physics."
        },
        {
            "name": "The Chasm Vigil of Silence",
            "description": "An initiate spends one entire planetary night in a deep basalt canyon without artificial light, listening to the acoustic echoes of the stone.",
            "cultural_meaning": "Teaches patience, calm focus, and understanding of the peaceful dark."
        },
        {
            "name": "The Meridian Gear Calibration",
            "description": "An engineering student must manually calibrate three intermeshing bronze gears to within two microns using only hand tools.",
            "cultural_meaning": "Instills pride in craftsmanship, precision, and the value of patience."
        },
        {
            "name": "The Grav-Whale Song Greeting",
            "description": "A deep-space wayfarer successfully matches the sub-acoustic frequency of a passing wild Grav-Whale using an acoustic chime pipe.",
            "cultural_meaning": "Signifies harmony with majestic alien life and gentle non-violent stewardship."
        }
    ],
    "hospitality_customs": [
        {
            "name": "The Offering of Warm Amber Tea and Polished Wishing Stone",
            "ritual_act": "Host presents a cup of spiced solar succulent tea and a smooth, pocket-sized mineral stone.",
            "dialogue_phrase": "May your thirst be quenched, and may this stone remember your peaceful footsteps in our hall."
        },
        {
            "name": "The Clean Tool and Fresh Oil Greeting",
            "ritual_act": "Host offers clean lint-free cloths and a drop of pure lavender machine oil to lubricate traveler's tools.",
            "dialogue_phrase": "Let no friction wear your bearings, friend; our workshop is your haven."
        },
        {
            "name": "The Twilight Lantern Lantern Blessing",
            "ritual_act": "Host lights a soft bioluminescent moss lantern and sets it in the window facing the guest's ship.",
            "dialogue_phrase": "A gentle light burns for you in the quiet, guiding your return whenever the path grows dim."
        },
        {
            "name": "The Shared Stardust Salt Pinch",
            "ritual_act": "Host and guest each take a pinch of sparkling mineral seasoning from a central crystal bowl.",
            "dialogue_phrase": "Born of the same ancient stars, we share the salt of friendship."
        }
    ],
    "sacred_cosmic_taboos": [
        {
            "taboo_id": "NO_BEACON_WEAPONIZATION",
            "rule": "Never direct harmful high-energy discharges at navigational beacons or observation telescopes.",
            "consequence": "Universal loss of docking privileges across all 74 star systems."
        },
        {
            "taboo_id": "PRESERVE_CREATURE_NURSERIES",
            "rule": "Never deploy high-thrust engines within 50 kilometers of a Grav-Whale or Light-Moth nesting ground.",
            "consequence": "Mandatory community service restoring environmental vegetation."
        },
        {
            "taboo_id": "SANCTITY_OF_DISTRESS_SIGNALS",
            "rule": "Every vessel, regardless of faction or rivalry, must acknowledge and relay an emergency distress beacon.",
            "consequence": "Stripping of pilot certification and public censure."
        },
        {
            "taboo_id": "RESPECT_HOSPITALITY_BREAD",
            "rule": "Never draw an energized tool or weapon within the boundary of a host's hospitality circle.",
            "consequence": "Immediate peaceful expulsion and mediation under the Meridian Arbiters."
        }
    ],
    "architectural_philosophies": [
        {
            "faction_group": "Solar & Radiant",
            "style_name": "Photonic Brass & Open Solarium Architecture",
            "materials": "Polished yellow bronze, solarite crystal glass, golden sandstone",
            "philosophy": "Buildings designed to catch every ray of daylight, channeling warm sunshine into subterranean gardens."
        },
        {
            "faction_group": "Void & Shadow",
            "style_name": "Basalt Acoustical Vaults & Twilight Terraces",
            "materials": "Smooth black volcanic basalt, bioluminescent moss mortar, sound-absorbing felt",
            "philosophy": "Structures designed for tranquil acoustics, where footsteps echo softly and starlight fills courtyard pools."
        },
        {
            "faction_group": "Astrolabe & Clockwork",
            "style_name": "Tiered Meridian Towers & Interlocking Aqueducts",
            "materials": "Riveted brass plates, precision bronze gears, carved granite counterweights",
            "philosophy": "Habitats integrated as living giant mechanisms, where water pumps and elevators run on perpetual gravity flywheels."
        },
        {
            "faction_group": "Bio & Organic",
            "style_name": "Living Canopy Arbors & Symbiotic Root Pavilions",
            "materials": "Grown ironwood trunks, glowing canopy leaves, molded bioluminescent chitin",
            "philosophy": "Architecture that grows naturally with the planetary forest without harming a single root."
        }
    ],
    "culinary_traditions": [
        {
            "name": "Amber Spice Succulent Tea & Honey-Grain Flatbread",
            "culture_group": "Sun-Forged & Solar Worlds",
            "description": "Warm, invigorating spiced infusion paired with sun-baked grain cakes that melt pleasantly on the tongue."
        },
        {
            "name": "Bioluminescent Canyon Moss Broth & Steamed Sea Tubers",
            "culture_group": "Void-Bound & Abyssal Worlds",
            "description": "Mild, soothing herbal broth glowing with gentle emerald bioluminescence, offering deep physical restoration."
        },
        {
            "name": "Precision Meridian Roasted Nut Paste & Crystallized Nectar Sticks",
            "culture_group": "Astrolabe & Clockwork Worlds",
            "description": "Nutrient-dense savory spread crafted with exact caloric ratios, favored by workshop artisans and gearwrights."
        },
        {
            "name": "Comet Methane-Frost Mint Sorbet & Sparkling Glider Punch",
            "culture_group": "Comet-Riders & Nomad Flotillas",
            "description": "Crisp, sweet cooling treat that crackles with refreshing effervescence like a burst of fresh mountain air."
        }
    ],
    "ethics_of_discovery": [
        "First Do No Harm: Every new world must be observed with gentleness and curiosity, leaving its living biomes pristine.",
        "The Open Light: Astronomical maps and navigation routes must be shared freely with all traveling wayfarers.",
        "Non-Intrusive Wonder: Alien creatures are allies and teachers; observe their migratory song without disturbing their young."
    ],
    "the_untuned_dynamics": {
        "definition": "Baseline un-augmented humans living without bio-piezoelectric quartz bone implants or retinal cone enhancements.",
        "frontier_economic_realities": "In heavy radiation belts or coronal frontiers, baseline workers rely on leaded bronze aprons, insulated suits, and mechanical chronometers rather than internal bio-resonance.",
        "philosophical_movement": "The Natural Accord: A vocal interstellar faction championing un-tuned human bodily integrity and pure mechanical craftsmanship.",
        "lattice_rejection_mastery": "Individuals whose biology rejects crystal grafting become the galaxy's most revered master clocksmiths, optical lens polishers, and acoustic wave navigators.",
        "societal_integration": "Respected as essential anchors of grounding, reminding the tuned artificers of baseline human perseverance and non-resonant wisdom."
    }
}

def get_untuned_sociological_profile(world_or_colony: str = "Aethel-Prime Frontier") -> Dict[str, Any]:
    """Returns the sociological profile and cultural status of the Un-Tuned on a target world."""
    return {
        "world_or_colony": world_or_colony,
        "population_classification": "Baseline Humanity (The Un-Tuned)",
        "dynamics": SOCIOLOGICAL_SYSTEMS["the_untuned_dynamics"],
        "primary_vocations": [
            "Master Escapement Gearwright",
            "Acoustic Subspace Signal Calibrator",
            "Heavy Radiation Shielding Fabricator",
            "Planetary Trade Route Arbiter"
        ],
        "cultural_respect_index": "94 / 100 (Revered for unaugmented precision & mechanical mastery)"
    }

def get_governance_model(faction_or_world: str) -> Dict[str, Any]:
    """Retrieves or generates the governance model and political structure for a faction or world."""
    for m in GOVERNANCE_ARCHETYPES:
        if any(faction_or_world.lower() in f.lower() for f in m["primary_factions"]):
            return m
    # Fallback to general syndicate
    return GOVERNANCE_ARCHETYPES[2]

def get_sociological_profile(faction_or_world: str = "Sun-Forged Hegemony") -> Dict[str, Any]:
    """Returns a full sociological profile including rites of passage, hospitality, taboos, culinary traditions, and architecture."""
    gov = get_governance_model(faction_or_world)
    
    # Pick matching architecture
    arch = SOCIOLOGICAL_SYSTEMS["architectural_philosophies"][0]
    for a in SOCIOLOGICAL_SYSTEMS["architectural_philosophies"]:
        if any(w.lower() in faction_or_world.lower() for w in a["faction_group"].split("&")):
            arch = a
            break

    # Pick culinary tradition
    cuisine = SOCIOLOGICAL_SYSTEMS["culinary_traditions"][0]
    for c in SOCIOLOGICAL_SYSTEMS["culinary_traditions"]:
        if any(w.lower() in faction_or_world.lower() for w in c["culture_group"].split("&")):
            cuisine = c
            break

    return {
        "status": "SOCIOLOGICAL_PROFILE_RESOLVED",
        "entity": faction_or_world,
        "governance_model": gov["name"],
        "leadership": gov["leadership_structure"],
        "core_charter": gov["legal_charter"],
        "diplomatic_stance": gov["diplomatic_stance"],
        "social_strata_hierarchy": SOCIOLOGICAL_SYSTEMS["social_strata"],
        "signature_rite_of_passage": random.choice(SOCIOLOGICAL_SYSTEMS["rites_of_passage"]),
        "hospitality_ritual": random.choice(SOCIOLOGICAL_SYSTEMS["hospitality_customs"]),
        "culinary_staple": cuisine,
        "sacred_taboos": SOCIOLOGICAL_SYSTEMS["sacred_cosmic_taboos"],
        "ethics_of_discovery": SOCIOLOGICAL_SYSTEMS["ethics_of_discovery"],
        "untuned_dynamics": SOCIOLOGICAL_SYSTEMS["the_untuned_dynamics"],
        "architectural_style": arch
    }

def get_diplomatic_treaties(faction_a: str, faction_b: str) -> Dict[str, Any]:
    """Generates the bilateral treaty framework and mutual commitments between two factions."""
    gov_a = get_governance_model(faction_a)
    gov_b = get_governance_model(faction_b)

    common_ground = f"Mutual adherence to the {gov_a['legal_charter'].split(':')[0]} and {gov_b['legal_charter'].split(':')[0]}."
    
    return {
        "faction_a": faction_a,
        "governance_a": gov_a["name"],
        "faction_b": faction_b,
        "governance_b": gov_b["name"],
        "active_treaties": [
            "The Open Stargate Corridor Convention",
            "The Neutral Trade Port Meridian Protocol",
            "The Joint Search and Rescue Emergency Pact"
        ],
        "core_shared_principle": common_ground,
        "dispute_resolution_mechanism": "Arbitration before a joint panel of High Artificers and Meridian Arbiters."
    }

def simulate_diplomatic_summit(
    faction_a: str = "Sun-Forged Hegemony",
    faction_b: str = "Void-Bound Monks",
    agenda_topic: str = "Shared Stargate Corridors & Navigational Beacons"
) -> Dict[str, Any]:
    """
    Simulates a high-stakes, peaceful interstellar diplomatic summit between two factions,
    featuring cultural hospitality rites, mutual gift exchanges, treaty ratifications, and shared stardust toasts.
    """
    prof_a = get_sociological_profile(faction_a)
    prof_b = get_sociological_profile(faction_b)
    treaties = get_diplomatic_treaties(faction_a, faction_b)

    gift_a = f"A polished golden solar lens reflecting the {prof_a['governance_model']}'s commitment to open light."
    gift_b = f"A carved basalt acoustic chime that sings soothing harmonic chords in the quiet."

    resolution = f"Both delegations unanimously ratify '{treaties['active_treaties'][0]}' and commit to joint patrol schedules."

    return {
        "status": "DIPLOMATIC_SUMMIT_CONCLUDED",
        "host_faction": faction_a,
        "guest_faction": faction_b,
        "summit_location": f"The Grand Meridian Neutral Assembly Hall (Sector [0, 0, 0])",
        "agenda_topic": agenda_topic,
        "opening_hospitality_rite": prof_a["hospitality_ritual"]["name"],
        "cultural_gift_exchange": {
            f"{faction_a}_offers": gift_a,
            f"{faction_b}_offers": gift_b
        },
        "summit_resolution": resolution,
        "shared_banquet_cuisine": f"{prof_a['culinary_staple']['name']} served alongside {prof_b['culinary_staple']['name']}",
        "diplomatic_outcome": "POSITIVE_PEACE_ACCORD (Friction reduced by 15 points, trade routes stabilized)"
    }

def generate_civic_interaction(faction_a: str, faction_b: str, interaction_type: str = "HOSPITALITY_MEETING") -> Dict[str, Any]:
    """Generates an engaging, warm, child-accessible diplomatic or cultural interaction between factions."""
    prof_a = get_sociological_profile(faction_a)
    prof_b = get_sociological_profile(faction_b)
    hosp = prof_a["hospitality_ritual"]

    return {
        "interaction_type": interaction_type,
        "host_faction": faction_a,
        "guest_faction": faction_b,
        "hospitality_performed": hosp["name"],
        "ritual_action": hosp["ritual_act"],
        "host_greeting": hosp["dialogue_phrase"],
        "cultural_significance": f"Demonstrates mutual respect under the {prof_a['governance_model']}.",
        "shared_taboo_observed": "Both parties ensure all tool safeties are engaged before entering the sanctuary."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interstellar Politics & Sociology Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all governance archetypes")

    gov_p = subparsers.add_parser("governance", help="Get governance model for faction")
    gov_p.add_argument("--faction", default="Sun-Forged Hegemony", help="Faction name")

    soc_p = subparsers.add_parser("profile", help="Get complete sociological profile")
    soc_p.add_argument("--world", default="Helios Prime", help="World or faction name")

    dip_p = subparsers.add_parser("treaties", help="Get treaties between factions")
    dip_p.add_argument("--a", default="Sun-Forged Hegemony", help="Faction A")
    dip_p.add_argument("--b", default="Astrolabe Engineers", help="Faction B")

    sum_p = subparsers.add_parser("summit", help="Simulate diplomatic peace summit")
    sum_p.add_argument("--faction1", default="Sun-Forged Hegemony", help="Host faction")
    sum_p.add_argument("--faction2", default="Void-Bound Monks", help="Guest faction")
    sum_p.add_argument("--topic", default="Shared Stargate Corridors & Navigational Beacons", help="Agenda topic")

    args = parser.parse_args()

    if args.command == "governance":
        res = get_governance_model(args.faction)
        print(json.dumps(res, indent=2))
    elif args.command == "profile":
        res = get_sociological_profile(args.world)
        print(json.dumps(res, indent=2))
    elif args.command == "treaties":
        res = get_diplomatic_treaties(args.a, args.b)
        print(json.dumps(res, indent=2))
    elif args.command == "summit":
        res = simulate_diplomatic_summit(args.faction1, args.faction2, args.topic)
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"total_archetypes": len(GOVERNANCE_ARCHETYPES), "archetypes": GOVERNANCE_ARCHETYPES}, indent=2))

