#!/usr/bin/env python3
"""
Universal Encyclopedia Network (UEN) Engine for The Stellar Confluence Universe.
Manages collision-free unique scientific cataloging across trillions of star systems,
multi-faction cultural common names and folklore, sensor telemetry scanning, and physical
laboratory specimen sampling custody ledgers.
"""

import os
import sys
import json
import hashlib
import re
import datetime
import argparse
from typing import Dict, Any, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
if AGENTS_DIR not in sys.path:
    sys.path.insert(0, AGENTS_DIR)

from core.edition_manager import get_edition_state_dir, get_state_file

ENTITY_PREFIXES = {
    "planet": "PLN",
    "biome": "BIO",
    "species": "SPC",
    "mineral": "MIN",
    "anomaly": "ANO",
    "energy": "ENG"
}

FACTION_FOLKLORE_THEMES = {
    "Sun-Forged Hegemony": "Dawn vigilance, radiant solar honor, noon-star purity",
    "Void-Bound Monks": "Quiet shadows, subterranean lanterns, umbral silence guidance",
    "Astrolabe Engineers": "Gear metrology, optical dial calibration, mechanical harmony",
    "Comet-Riders": "Frost-tail navigation, vapor-skimming folklore, drift winds",
    "Nebula-Weavers": "Silken gas currents, plasma tapestry weaving, chromatic threads",
    "Deep-Core Miners": "Bedrock resonance, seismic pulse tracking, molten foundry lore",
    "Bio-Alchemists": "Photosynthetic healing, living canopy mind-links, spore taxonomy",
    "Crystal-Singers": "Prismatic acoustic frequencies, singing quartz choir harmonics",
    "Tide-Wardens": "Abyssal depth pressure, tidal resonance, bioluminescent currents",
    "Magnetar-Leapers": "High-induction magnetic slingshots, coronal flare leaping",
    "Chrono-Navigators": "Temporal phase slipping, ancient starlight echoes, orrery alignments",
    "Plasma-Shepherds": "Coronal loop wrangling, solar flame herding, magnetic pinch crafts"
}

SAMPLE_STATUSES = [
    "COLLECTED",
    "IN_SPECTROMETER",
    "UNDER_CRYO_ANALYSIS",
    "ARCHIVED_IN_ROYAL_VAULT",
    "SAMPLE_DEPLETED",
    "MOUNTED_IN_ORRERY",
    "STORED_IN_STASIS_FIELD"
]

def generate_collision_free_id(entity_type: str, name: str, sector_coords: List[int]) -> str:
    """Generates an algorithmic collision-free catalog ID."""
    prefix = ENTITY_PREFIXES.get(entity_type.lower(), "ENT")
    coord_str = f"{sector_coords[0]}_{sector_coords[1]}_{sector_coords[2]}"
    raw_hash = hashlib.sha256(f"{name}_{coord_str}_{entity_type}".encode('utf-8')).hexdigest()
    sec_code = raw_hash[:4].upper()
    ent_code = raw_hash[4:8].upper()
    return f"{prefix}-{sec_code}-{ent_code}"

def load_encyclopedia(edition: Optional[str] = None) -> Dict[str, Any]:
    """Loads the active edition's encyclopedia network registry."""
    state_file = get_state_file("encyclopedia_network.json", edition)
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": "2.0", "entities": {}, "discoveries_count": 0}

def save_encyclopedia(data: Dict[str, Any], edition: Optional[str] = None) -> None:
    """Saves the encyclopedia registry to the active edition state."""
    state_file = get_state_file("encyclopedia_network.json", edition)
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def generate_multi_faction_names(entity_type: str, name: str) -> Dict[str, str]:
    """Generates culturally tailored multi-faction folklore names for any specimen."""
    return {
        "Sun-Forged Hegemony": f"Dawn-{name}",
        "Void-Bound Monks": f"Umbral {name} Ghost",
        "Astrolabe Engineers": f"Resonant {name} Mechanism",
        "Comet-Riders": f"Frost-{name} Skimmer",
        "Nebula-Weavers": f"Silken Chromatic {name}",
        "Deep-Core Miners": f"Bedrock {name} Core",
        "Bio-Alchemists": f"Symbiotic Living {name}",
        "Crystal-Singers": f"Singing Prismatic {name}",
        "Tide-Wardens": f"Abyssal Trench {name}",
        "Magnetar-Leapers": f"Electrified Flux-{name}",
        "Chrono-Navigators": f"Chrono-Aligned {name}",
        "Plasma-Shepherds": f"Coronal Flare {name}"
    }

def register_discovery(
    entity_type: str,
    name: str,
    hero: str = "Caelum Dawnrunner",
    book_id: int = 1,
    world: str = "Helios Prime",
    coords: Optional[List[int]] = None,
    gut: int = 100,
    telemetry: Optional[Dict[str, Any]] = None,
    faction_names: Optional[Dict[str, str]] = None,
    sample_status: Optional[str] = "COLLECTED",
    edition: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a new planet, biome, species, mineral, or anomaly in the UEN."""
    coords = coords or [15, -8, 42]
    cat_id = generate_collision_free_id(entity_type, name, coords)
    
    db = load_encyclopedia(edition)
    
    # Generate multi-faction cultural folklore names if not provided
    if not faction_names:
        faction_names = generate_multi_faction_names(entity_type, name)

    sample_id = f"SAMP-{cat_id.split('-')[-1]}-A"

    entry = {
        "catalog_id": cat_id,
        "entity_type": entity_type.lower(),
        "universal_standard_name": name,
        "faction_common_names": faction_names,
        "discovery": {
            "discoverer": hero,
            "book_id": book_id,
            "world": world,
            "coordinates": coords,
            "gut_timestamp": gut,
            "registration_date": datetime.datetime.now().isoformat()
        },
        "scientific_telemetry": telemetry or {
            "spectrum_absorption": "Wavefront Mid-Harmonic",
            "morphology": f"Naturally crystallized {entity_type} structure",
            "handling_protocol": "Non-violent acoustic and photonic stabilization",
            "density_g_cm3": 3.45,
            "thermal_tolerance_k": 1850.0
        },
        "specimen_custody": {
            "sample_id": sample_id,
            "status": sample_status if sample_status in SAMPLE_STATUSES else "COLLECTED",
            "lab_findings": "Specimen successfully logged in vessel research bay.",
            "custody_history": [
                {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": sample_status if sample_status in SAMPLE_STATUSES else "COLLECTED",
                    "logged_by": hero,
                    "location": f"{world} Research Bay"
                }
            ]
        }
    }

    db["entities"][cat_id] = entry
    db["discoveries_count"] = len(db["entities"])
    save_encyclopedia(db, edition)

    return entry

def list_discoveries(entity_type: Optional[str] = None, edition: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns all discoveries filtered optionally by entity type."""
    db = load_encyclopedia(edition)
    res = []
    for cid, ent in db.get("entities", {}).items():
        if entity_type is None or ent.get("entity_type") == entity_type.lower():
            res.append(ent)
    return res

def search_encyclopedia(query: str, edition: Optional[str] = None) -> List[Dict[str, Any]]:
    """Performs full-text search across standard names, faction names, and telemetry."""
    db = load_encyclopedia(edition)
    q = query.lower()
    matches = []
    for cid, ent in db.get("entities", {}).items():
        matched = False
        if q in cid.lower() or q in ent.get("universal_standard_name", "").lower():
            matched = True
        elif any(q in fn.lower() for fn in ent.get("faction_common_names", {}).values()):
            matched = True
        elif q in ent.get("discovery", {}).get("discoverer", "").lower():
            matched = True
        elif q in json.dumps(ent.get("scientific_telemetry", {})).lower():
            matched = True

        if matched:
            matches.append(ent)
    return matches

def update_sample_custody(
    catalog_id: str,
    status: str,
    findings: str,
    handler_hero: str = "Chief Artificer",
    edition: Optional[str] = None
) -> Dict[str, Any]:
    """Updates the physical laboratory specimen custody state and appends to custody history."""
    db = load_encyclopedia(edition)
    if catalog_id not in db.get("entities", {}):
        return {"error": f"Catalog ID {catalog_id} not found in encyclopedia."}
    
    if status not in SAMPLE_STATUSES:
        status = "IN_SPECTROMETER"

    ent = db["entities"][catalog_id]
    ent["specimen_custody"]["status"] = status
    ent["specimen_custody"]["lab_findings"] = findings
    ent["specimen_custody"]["last_tested_date"] = datetime.datetime.now().isoformat()
    
    if "custody_history" not in ent["specimen_custody"]:
        ent["specimen_custody"]["custody_history"] = []

    ent["specimen_custody"]["custody_history"].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "status": status,
        "logged_by": handler_hero,
        "findings_note": findings
    })

    save_encyclopedia(db, edition)
    return ent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Encyclopedia Network CLI")
    subparsers = parser.add_subparsers(dest="command")

    reg_p = subparsers.add_parser("register", help="Register new discovery")
    reg_p.add_argument("--type", default="mineral", choices=["planet", "biome", "species", "mineral", "anomaly", "energy"])
    reg_p.add_argument("--name", default="Piezogravitic Quartz")
    reg_p.add_argument("--hero", default="Dr. Elian Vance")
    reg_p.add_argument("--book-id", type=int, default=1)
    reg_p.add_argument("--world", default="Aethel-Prime")

    list_p = subparsers.add_parser("list", help="List all discoveries")
    list_p.add_argument("--type", help="Filter by entity type")

    search_p = subparsers.add_parser("search", help="Search encyclopedia")
    search_p.add_argument("--query", required=True)

    cust_p = subparsers.add_parser("sample", help="Update sample custody")
    cust_p.add_argument("--catalog-id", required=True)
    cust_p.add_argument("--status", default="IN_SPECTROMETER")
    cust_p.add_argument("--findings", default="Spectrometry scan nominal.")

    args = parser.parse_args()

    if args.command == "register":
        res = register_discovery(args.type, args.name, args.hero, args.book_id, args.world)
        print(json.dumps(res, indent=2))
    elif args.command == "list":
        res = list_discoveries(args.type)
        print(json.dumps(res, indent=2))
    elif args.command == "search":
        res = search_encyclopedia(args.query)
        print(json.dumps(res, indent=2))
    elif args.command == "sample":
        res = update_sample_custody(args.catalog_id, args.status, args.findings)
        print(json.dumps(res, indent=2))
    else:
        d = register_discovery(
            "mineral",
            "Piezogravitic Quartz",
            "Dr. Elian Vance",
            1,
            "Aethel-Prime",
            [0, 0, 0],
            1,
            {"piezoelectric_voltage": "10,000V induction", "crystal_age": "4.2 Billion Years"},
            {"Sun-Forged Hegemony": "Dawn-Resonator Pillar", "Void-Bound Monks": "Singing Basalt Spire", "Astrolabe Engineers": "Natural Escapement Core"}
        )
        print(json.dumps(d, indent=2))

