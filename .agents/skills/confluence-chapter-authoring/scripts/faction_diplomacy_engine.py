#!/usr/bin/env python3
"""
Faction Diplomacy, Treaties & Galactic Tension Engine for The Stellar Confluence Universe
Computes diplomatic stances, inter-faction tension indices (0-100), historical treaties,
and automated plot conflict hooks between interacting factions.
"""

import sys
import json
import argparse

DIPLOMATIC_RELATIONS = {
    ("Sun-Forged Hegemony", "Void-Bound Monks"): {
        "stance": "OPEN_RIVALRY",
        "tension_index": 88,
        "historic_treaty": "None (The Zenith-Nadir Schism)",
        "ideological_conflict": "Solar expansionism & radiant cleansing vs Sacred shadow sanctity & phase preservation",
        "resource_dispute": "Control over tidal-locked twilight corridor planets where sunlight and shadow meet",
        "plot_conflict_hook": "A radiant expedition threatens to illuminate a sacred shadow cave, risking an armed border skirmish."
    },
    ("Sun-Forged Hegemony", "Astrolabe Engineers"): {
        "stance": "STRATEGIC_TRADE_PACT",
        "tension_index": 22,
        "historic_treaty": "The Meridian Accord of GUT 50",
        "ideological_conflict": "Solar authoritarian command vs Methodical clockwork autonomy",
        "resource_dispute": "Export tariffs on refined solar focusing crystals and high-torque flywheel brass",
        "plot_conflict_hook": "A delayed shipment of crystal lenses halts construction on a star-forge orbital station."
    },
    ("Void-Bound Monks", "Astrolabe Engineers"): {
        "stance": "CAUTIOUS_NEUTRALITY",
        "tension_index": 42,
        "historic_treaty": "The Silent Gear Compact",
        "ideological_conflict": "Quiet contemplation and organic shadows vs Rhythmic kinetic noise and gear construction",
        "resource_dispute": "Engineers surveying ancient basalt ruins for ore deposits without monk permission",
        "plot_conflict_hook": "Clockwork surveyors accidentally trigger a slumbering umbral resonance trap in deep caverns."
    },
    ("Astrolabe Engineers", "Deep-Core Miners"): {
        "stance": "RESOURCE_ALLIANCE",
        "tension_index": 12,
        "historic_treaty": "The Tectonic Foundry Guild Pact",
        "ideological_conflict": "Precision surface assembly vs Heavy subterranean excavation",
        "resource_dispute": "Fair distribution of subterranean basalt alloys and magma energy tapped from planetary cores",
        "plot_conflict_hook": "A sudden magma chamber rupture threatens a joint mining platform; teamwork is required to vent the pressure."
    },
    ("Comet-Riders", "Solar-Sailors"): {
        "stance": "FRIENDLY_RIVALRY",
        "tension_index": 28,
        "historic_treaty": "The Solar Wind Regatta Charter",
        "ideological_conflict": "Volatile ice sublimation speed vs Elegant light-pressure gliding",
        "resource_dispute": "Right of way along high-velocity solar flare slingshot corridors",
        "plot_conflict_hook": "A daring race across an asteroid belt turns into an emergency rescue when solar debris strikes a sail."
    },
    ("Void-Bound Monks", "Stargate Sentinels"): {
        "stance": "COLD_WAR_FRICTION",
        "tension_index": 68,
        "historic_treaty": "The Keystone Gate Ceasefire",
        "ideological_conflict": "Unrestricted subspace phase-stepping vs Strict gateway toll enforcement and containment",
        "resource_dispute": "Jurisdiction over undocumented subspace rift portals",
        "plot_conflict_hook": "A rogue phase-walker bypasses a sentinel checkpoint, triggering an automatic security lockdown."
    }
}

def normalize_pair(f1, f2):
    f1_clean = f1.strip()
    f2_clean = f2.strip()
    return tuple(sorted([f1_clean, f2_clean]))

def get_diplomatic_relation(faction_a, faction_b):
    if faction_a.strip().lower() == faction_b.strip().lower():
        return {
            "faction_a": faction_a,
            "faction_b": faction_b,
            "stance": "INTRA_FACTION_ALLIANCE",
            "tension_index": 5,
            "historic_treaty": "Internal Faction Accord",
            "plot_conflict_hook": "Internal generational debate between cautious elders and eager young apprentices."
        }

    # Search exact or partial match
    for (k1, k2), rel in DIPLOMATIC_RELATIONS.items():
        if (k1.lower() in faction_a.lower() and k2.lower() in faction_b.lower()) or \
           (k2.lower() in faction_a.lower() and k1.lower() in faction_b.lower()):
            return {
                "faction_a": faction_a,
                "faction_b": faction_b,
                "matched_factions": [k1, k2],
                "stance": rel["stance"],
                "tension_index": rel["tension_index"],
                "historic_treaty": rel["historic_treaty"],
                "ideological_conflict": rel.get("ideological_conflict", ""),
                "resource_dispute": rel.get("resource_dispute", ""),
                "plot_conflict_hook": rel["plot_conflict_hook"]
            }

    # Default procedural dynamic relation
    return {
        "faction_a": faction_a,
        "faction_b": faction_b,
        "matched_factions": [faction_a, faction_b],
        "stance": "NEUTRAL_COEXISTENCE",
        "tension_index": 35,
        "historic_treaty": "Galactic Confluence General Accord",
        "plot_conflict_hook": f"A shared logistical challenge across Sector borders requires {faction_a} and {faction_b} to coordinate skills."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Faction Diplomacy & Tension Matrix")
    parser.add_argument("--faction-a", required=True, help="First faction name")
    parser.add_argument("--faction-b", required=True, help="Second faction name")
    
    args = parser.parse_args()
    res = get_diplomatic_relation(args.faction_a, args.faction_b)
    print(json.dumps(res, indent=2))
