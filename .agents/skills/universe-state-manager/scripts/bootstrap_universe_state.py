#!/usr/bin/env python3
"""
Universe State Bootstrapper & Catalog Generator for The Stellar Confluence Universe
Generates, updates, or restores the authoritative 74-Book Character Registry, Cosmic Clockwork,
Rotation Tracker, and Diary files in 00_System_State/.
"""

import os
import sys
import json
import argparse

def find_project_root():
    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, "00_System_State")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return cwd

PROJECT_ROOT = find_project_root()
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
ROTATION_TRACKER_MD = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
COSMIC_CLOCKWORK_MD = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")
CHARACTER_REGISTRY_MD = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")

# Authoritative 74-Book Universe Roster
ROSTER_DATA = [
    # Books 01 - 10: Sun-Forged Hegemony (Radiant / Solar)
    {"id": 1, "title": "The Solar Crucible", "hero": "Caelum Dawnrunner", "faction": "Sun-Forged Hegemony", "world": "Helios Prime", "loc": "SURFACE", "sector": "[10, 5, 0]", "facing": 15},
    {"id": 2, "title": "Crown of Sol", "hero": "Captain Vespera Ray", "faction": "Sun-Forged Hegemony", "world": "Solar Bastion Station", "loc": "ORBITAL", "sector": "[12, 5, 1]", "facing": 25},
    {"id": 3, "title": "Mirage of the Amber Sands", "hero": "Tariq Sunstrider", "faction": "Sun-Forged Hegemony", "world": "Kaelen-7 (Desert World)", "loc": "SURFACE", "sector": "[14, 4, -2]", "facing": 10},
    {"id": 4, "title": "Ignition Vector", "hero": "Navigator Lyra Solis", "faction": "Sun-Forged Hegemony", "world": "Cruiser *Corona Victor*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[15, 6, 0]", "facing": 30},
    {"id": 5, "title": "Lenses of the Zenith", "hero": "High Optician Orin", "faction": "Sun-Forged Hegemony", "world": "The Zenith Observatory", "loc": "SURFACE", "sector": "[11, 8, 2]", "facing": 5},
    {"id": 6, "title": "The Gilded Flare", "hero": "Seraphina Goldvein", "faction": "Sun-Forged Hegemony", "world": "Aurelia Mining Spire", "loc": "SURFACE", "sector": "[13, 7, -1]", "facing": 20},
    {"id": 7, "title": "Shield of the Noon Star", "hero": "Commander Brant", "faction": "Sun-Forged Hegemony", "world": "Star-Forge Orbital Aegis", "loc": "ORBITAL", "sector": "[16, 5, 3]", "facing": 18},
    {"id": 8, "title": "Prism of the Dawn", "hero": "Kaelen Lightweaver", "faction": "Sun-Forged Hegemony", "world": "Prism Oasis", "loc": "SURFACE", "sector": "[10, 3, -3]", "facing": 28},
    {"id": 9, "title": "Radiant Crucible", "hero": "Forge-Master Theron", "faction": "Sun-Forged Hegemony", "world": "The Pyre Foundry", "loc": "SURFACE", "sector": "[12, 2, 1]", "facing": 12},
    {"id": 10, "title": "Wings of the Sun-Bird", "hero": "Aria Skydancer", "faction": "Sun-Forged Hegemony", "world": "Thermal Glider Station", "loc": "ORBITAL", "sector": "[14, 6, 4]", "facing": 22},

    # Books 11 - 20: Void-Bound Monks (Shadow / Phase-Shifting)
    {"id": 11, "title": "Shadow Over Umbra", "hero": "Kage Silentstep", "faction": "Void-Bound Monks", "world": "Umbra Minor (Shadow Moon)", "loc": "SURFACE", "sector": "[-10, 5, 0]", "facing": 165},
    {"id": 12, "title": "The Eclipse Chasm", "hero": "Nyx Riftseeker", "faction": "Void-Bound Monks", "world": "Abyssal Rift Valley", "loc": "SURFACE", "sector": "[-12, 4, 2]", "facing": 175},
    {"id": 13, "title": "Silent Frigate", "hero": "Captain Vane", "faction": "Void-Bound Monks", "world": "Stealth Vessel *Ghost-Prow*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[-15, 6, 0]", "facing": 160},
    {"id": 14, "title": "Monastery of the Black Gate", "hero": "Elder Morren", "faction": "Void-Bound Monks", "world": "The Obsidian Citadel", "loc": "SURFACE", "sector": "[-11, 8, -2]", "facing": 178},
    {"id": 15, "title": "Whispers in the Dark", "hero": "Liora Shadeborn", "faction": "Void-Bound Monks", "world": "Sub-surface Crypts", "loc": "SURFACE", "sector": "[-13, 7, 1]", "facing": 170},
    {"id": 16, "title": "Tears of the Penumbra", "hero": "Brother Ronin", "faction": "Void-Bound Monks", "world": "Penumbra Orbital Spire", "loc": "ORBITAL", "sector": "[-16, 5, -1]", "facing": 155},
    {"id": 17, "title": "Phase-Walkers of the Maw", "hero": "Zephyr the Unseen", "faction": "Void-Bound Monks", "world": "The Void Maw", "loc": "GATEWAY_SUBSPACE", "sector": "[-18, 0, 0]", "facing": 90},
    {"id": 18, "title": "Shroud of the Night-Mother", "hero": "Matron Karen", "faction": "Void-Bound Monks", "world": "Nightfall Moon", "loc": "SURFACE", "sector": "[-14, 3, 3]", "facing": 172},
    {"id": 19, "title": "The Obsidian Seal", "hero": "Acolyte Fen", "faction": "Void-Bound Monks", "world": "Basalt Sanctum", "loc": "SURFACE", "sector": "[-10, 2, -2]", "facing": 168},
    {"id": 20, "title": "Veil of the Eclipse", "hero": "Master Kuro", "faction": "Void-Bound Monks", "world": "Umbral Station Alpha", "loc": "ORBITAL", "sector": "[-12, 6, 2]", "facing": 162},

    # Books 21 - 30: Astrolabe Engineers (Clockwork / Kinetic / Harmonic)
    {"id": 21, "title": "Gears of the Great Orrery", "hero": "Tobias Cogsmith", "faction": "Astrolabe Engineers", "world": "The Clockwork Moon", "loc": "SURFACE", "sector": "[0, 10, 5]", "facing": 45},
    {"id": 22, "title": "The Chronometer Nexus", "hero": "Master Horologist Vera", "faction": "Astrolabe Engineers", "world": "Orrery Prime Spire", "loc": "ORBITAL", "sector": "[2, 12, 4]", "facing": 60},
    {"id": 23, "title": "Flywheel of Iron Ridge", "hero": "Garrick Gearhead", "faction": "Astrolabe Engineers", "world": "Ferrum Industrial Basin", "loc": "SURFACE", "sector": "[-2, 11, 3]", "facing": 50},
    {"id": 24, "title": "Crystalline Pendulum", "hero": "Elia Springtide", "faction": "Astrolabe Engineers", "world": "Rig *The Gyro-Anchor*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[0, 15, 6]", "facing": 70},
    {"id": 25, "title": "The Brass Astrolabe", "hero": "Caelen Dialmaker", "faction": "Astrolabe Engineers", "world": "Brass Meridian City", "loc": "SURFACE", "sector": "[3, 9, 2]", "faction": "Astrolabe Engineers", "facing": 40},
    {"id": 26, "title": "The Escapement Labyrinth", "hero": "Thurston Ratchet", "faction": "Astrolabe Engineers", "world": "Deep Vault Orrery", "loc": "SURFACE", "sector": "[1, 8, -3]", "facing": 80},
    {"id": 27, "title": "Springs of the Zenith Ring", "hero": "Lina Torsion", "faction": "Astrolabe Engineers", "world": "Ring Station Archimedes", "loc": "ORBITAL", "sector": "[-1, 14, 5]", "facing": 55},
    {"id": 28, "title": "The Harmonic Governor", "hero": "Orson Balancemaster", "faction": "Astrolabe Engineers", "world": "Harmonic Dam Facility", "loc": "SURFACE", "sector": "[4, 10, -1]", "facing": 65},
    {"id": 29, "title": "Torque and Velocity", "hero": "Kendra Vector", "faction": "Astrolabe Engineers", "world": "Cruiser *Kinetic Drive*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[2, 16, 7]", "facing": 75},
    {"id": 30, "title": "The Master Chronometer", "hero": "Grand Clocksmith Aldous", "faction": "Astrolabe Engineers", "world": "The Great Chronograph", "loc": "SURFACE", "sector": "[0, 8, 4]", "facing": 48},

    # Books 31 - 74: Expansion Factions (44 Books Total)
    {"id": 31, "title": "Riders of the Ice Comet", "hero": "Talon Frostskimmer", "faction": "Comet-Riders", "world": "Comet Halley-V", "loc": "DEEP_SPACE_TRANSIT", "sector": "[20, 0, 10]", "facing": 85},
    {"id": 32, "title": "The Nebula Silk Loom", "hero": "Aria Gossamer", "faction": "Nebula-Weavers", "world": "Opal Cloud Cluster", "loc": "ORBITAL", "sector": "[0, 20, -5]", "facing": 90},
    {"id": 33, "title": "Drill-Rig at the World Core", "hero": "Magda Magmabore", "faction": "Deep-Core Miners", "world": "Pyros Core Station", "loc": "SURFACE", "sector": "[-5, -15, 0]", "facing": 140},
    {"id": 34, "title": "Gravity-Surfers of the Rim", "hero": "Corin Wellspring", "faction": "Gravity-Surfers", "world": "Singularity Verge Rig", "loc": "ORBITAL", "sector": "[30, 10, -10]", "facing": 60},
    {"id": 35, "title": "Shepherds of the Ion Sea", "hero": "Joren Plasmahook", "faction": "Plasma-Shepherds", "world": "Ion Flare Belt", "loc": "DEEP_SPACE_TRANSIT", "sector": "[18, -12, 4]", "facing": 35},
    {"id": 36, "title": "The Chrono-Compass", "hero": "Mira Timefinder", "faction": "Chrono-Navigators", "world": "Subspace Conduit Seven", "loc": "GATEWAY_SUBSPACE", "sector": "[0, 0, 0]", "facing": 90},
    {"id": 37, "title": "Spore-Gardens of Aethel", "hero": "Sylva Greenbloom", "faction": "Bio-Alchemists", "world": "Aethel-IV Garden World", "loc": "SURFACE", "sector": "[8, -8, 8]", "facing": 50},
    {"id": 38, "title": "Echoes of the Crystal Spine", "hero": "Karris Resonator", "faction": "Crystal-Singers", "world": "Spires of Lithos", "loc": "SURFACE", "sector": "[-8, 12, -6]", "facing": 110},
    {"id": 39, "title": "The Tide-Locked Sentinel", "hero": "Gideon Stillwater", "faction": "Tide-Wardens", "world": "Oceanus Twilight Strip", "loc": "SURFACE", "sector": "[15, -15, 2]", "facing": 90},
    {"id": 40, "title": "Wings Over the Gas Colossus", "hero": "Nesta Skywing", "faction": "Storm-Gliders", "world": "Jupiter-Class Haven Spire", "loc": "ORBITAL", "sector": "[22, 14, -8]", "facing": 40},
    {"id": 41, "title": "The Asteroid Caravanserai", "hero": "Zayd Driftwalker", "faction": "Drift-Merchants", "world": "Asteroid Emporium 9", "loc": "DEEP_SPACE_TRANSIT", "sector": "[5, -10, 15]", "facing": 70},
    {"id": 42, "title": "Runners of the Magnetic Web", "hero": "Tesla Sparkchaser", "faction": "Magnetar-Leapers", "world": "Pulsar Ridge Node", "loc": "ORBITAL", "sector": "[-20, 15, 10]", "facing": 25},
    {"id": 43, "title": "The Molten Foundry of Hephaestus", "hero": "Volcan Smeltmaster", "faction": "Magma-Founders", "world": "Hephaestus Basin", "loc": "SURFACE", "sector": "[10, -20, -5]", "facing": 20},
    {"id": 44, "title": "Guardians of the Ancient Gate", "hero": "Aegis Gatewarden", "faction": "Stargate Sentinels", "world": "The Keystone Gate", "loc": "GATEWAY_SUBSPACE", "sector": "[0, 0, 100]", "facing": 90},
    {"id": 45, "title": "The Bioluminescent Trench", "hero": "Marina Deepglow", "faction": "Abyssal Divers", "world": "Hydra Deep Trench", "loc": "SURFACE", "sector": "[-14, -14, 0]", "facing": 175},
    {"id": 46, "title": "Harvesters of the Solar Sail", "hero": "Kite Windrunner", "faction": "Solar-Sailors", "world": "Light-Sail Barge *Zephyr*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[25, 0, 0]", "facing": 10},
    {"id": 47, "title": "The Silicon Forest", "hero": "Chip Arborist", "faction": "Silica-Botanists", "world": "Glass World Silex", "loc": "SURFACE", "sector": "[6, 18, -12]", "facing": 55},
    {"id": 48, "title": "Dune-Crawlers of the Red wastes", "hero": "Rust Sandtracker", "faction": "Rust-Nomads", "world": "Crimson Barrens", "loc": "SURFACE", "sector": "[17, -8, -10]", "facing": 30},
    {"id": 49, "title": "The Ring-City of Saturnia", "hero": "Vera Ringwarden", "faction": "Orbital Architects", "world": "Saturnia Habitat Ring", "loc": "ORBITAL", "sector": "[8, 25, 4]", "facing": 65},
    {"id": 50, "title": "Hunters of the Dark Matter Wake", "hero": "Darius Shadowtracker", "faction": "Dark-Matter Scavengers", "world": "Frigate *Null-Point*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[-25, -5, 12]", "facing": 165},
    {"id": 51, "title": "The Atmospheric Skiff", "hero": "Aero Cloudstrider", "faction": "Cloud-Keepers", "world": "Zephyr Cloud Port", "loc": "ORBITAL", "sector": "[12, 10, -15]", "facing": 45},
    {"id": 52, "title": "The Antimatter Reservoir", "hero": "Valen Containment", "faction": "Annihilation Engineers", "world": "Positron Spire", "loc": "ORBITAL", "sector": "[-5, 20, 20]", "facing": 85},
    {"id": 53, "title": "The Cinder Plains of Phaeton", "hero": "Pyra Flamecaller", "faction": "Ember-Dancers", "world": "Phaeton Caldera", "loc": "SURFACE", "sector": "[14, -18, 6]", "facing": 15},
    {"id": 54, "title": "The Ghost-Fleet of the Outer Belt", "hero": "Wraith Helmsman", "faction": "Derelict-Salvagers", "world": "Graveyard Cluster 13", "loc": "DEEP_SPACE_TRANSIT", "sector": "[-30, 0, -15]", "facing": 150},
    {"id": 55, "title": "Symphony of the Pulsar Beacon", "hero": "Lyrica Beaconkeeper", "faction": "Signal-Keepers", "world": "Pulsar Relay Epsilon", "loc": "ORBITAL", "sector": "[0, -25, 18]", "facing": 70},
    {"id": 56, "title": "The Diamond Rain Caverns", "hero": "Gem Crystalline", "faction": "Carbon-Crafters", "world": "Neptunian Core Platform", "loc": "SURFACE", "sector": "[-18, 18, -4]", "facing": 120},
    {"id": 57, "title": "Pilgrims of the Event Horizon", "hero": "Zenith Gravitybound", "faction": "Horizon-Seekers", "world": "Kerr-Hole Observation Spire", "loc": "ORBITAL", "sector": "[35, 5, -20]", "facing": 40},
    {"id": 58, "title": "The Aurora Weavers", "hero": "Lumi Ribbondancer", "faction": "Aurora-Weavers", "world": "Borealis Pole City", "loc": "SURFACE", "sector": "[5, 5, 25]", "facing": 35},
    {"id": 59, "title": "The Quantum Lock", "hero": "Tess Qubit", "faction": "Quantum-Cryptographers", "world": "Zero-Kelvin Array", "loc": "SURFACE", "sector": "[-10, -10, -20]", "facing": 100},
    {"id": 60, "title": "Drifters of the Solar Corona", "hero": "Flare Heatshield", "faction": "Sun-Divers", "world": "Diver Vessel *Icarus-XI*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[5, 0, 0]", "facing": 0},
    {"id": 61, "title": "The Void-Whale Shepherds", "hero": "Levi Singer", "faction": "Void-Fauna Handlers", "world": "Creature Pod Alpha", "loc": "DEEP_SPACE_TRANSIT", "sector": "[-22, -18, 8]", "facing": 135},
    {"id": 62, "title": "The Sub-Glacial Trench", "hero": "Frost Aquanaut", "faction": "Cryo-Explorers", "world": "Europa-Class Ocean", "loc": "SURFACE", "sector": "[-12, 10, 15]", "facing": 160},
    {"id": 63, "title": "The Kinetic Trebuchet", "hero": "Braced Slingmaster", "faction": "Mass-Driver Guild", "world": "Lunar Launch Rail", "loc": "SURFACE", "sector": "[8, -5, -8]", "facing": 50},
    {"id": 64, "title": "The Living Starship", "hero": "Symbio Biomancer", "faction": "Organic-Shipwrights", "world": "Bio-Vessel *Gaea*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[15, 15, 15]", "facing": 65},
    {"id": 65, "title": "The Mirror Array of Solitude", "hero": "Reflect Mirrorwright", "faction": "Heliostat-Masters", "world": "Mirror Field Desolation", "loc": "SURFACE", "sector": "[20, -10, 5]", "facing": 12},
    {"id": 66, "title": "The Gravity Sling of Jupiter", "hero": "Vector Slingshot", "faction": "Orbital Dynamics Guild", "world": "Transfer Craft *Velocity*", "loc": "DEEP_SPACE_TRANSIT", "sector": "[18, 12, -6]", "facing": 45},
    {"id": 67, "title": "The Iron Asteroid Stronghold", "hero": "Ferrus Castellan", "faction": "Asteroid Fortress Clan", "world": "Fortress Asteroid 101", "loc": "ORBITAL", "sector": "[-15, -8, 10]", "facing": 110},
    {"id": 68, "title": "The Tachyon Sensor Net", "hero": "Pulse Scout", "faction": "Early-Warning Rangers", "world": "Deep Sensor Prowler", "loc": "DEEP_SPACE_TRANSIT", "sector": "[0, 30, -10]", "facing": 90},
    {"id": 69, "title": "The Hydrothermal Spire", "hero": "Vapour Ventmaster", "faction": "Thermal Vent Guild", "world": "Boiling Shelf Base", "loc": "SURFACE", "sector": "[-8, -22, -10]", "facing": 150},
    {"id": 70, "title": "The Stellar Cartographer", "hero": "Atlas Skymapper", "faction": "Cosmic Mapmakers", "world": "Cartography Dome", "loc": "SURFACE", "sector": "[10, 20, 10]", "facing": 60},
    {"id": 71, "title": "The Magnetic Shieldwall", "hero": "Flux Barricader", "faction": "Magnetosphere Wardens", "world": "Shield Generator Spire", "loc": "ORBITAL", "sector": "[12, -14, 18]", "facing": 30},
    {"id": 72, "title": "The Deep Space Tether", "hero": "Cable Climber", "faction": "Space-Elevator Crew", "world": "Equatorial Spindle 1", "loc": "ORBITAL", "sector": "[6, -6, 0]", "facing": 55},
    {"id": 73, "title": "The Subspace Beacon of Hope", "hero": "Beacon Relaymaster", "faction": "Interstellar Courier Union", "world": "Relay Hub Prime", "loc": "GATEWAY_SUBSPACE", "sector": "[0, 0, 50]", "facing": 90},
    {"id": 74, "title": "The Grand Confluence Convergence", "hero": "Harmonia Nexus", "faction": "Confluence Council", "world": "The Grand Galactic Confluence Hub", "loc": "ORBITAL", "sector": "[0, 0, 0]", "facing": 0}
]

def generate_character_registry():
    """Generates the full 74-Book Character Registry Markdown document."""
    md = "# The Stellar Confluence Universe: 74-Book Master Character Registry\n\n"
    md += "Complete catalog of all 74 books, primary viewpoint heroes, factions, home worlds/ships, initial location types, and starting spatial sector coordinates.\n\n"
    md += "| Book ID | Book Title | Primary Protagonist | Faction | Starting World / Vessel | Location Type | Sector [X, Y, Z] |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for item in ROSTER_DATA:
        md += f"| **Book {item['id']:02d}** | {item['title']} | `{item['hero']}` | {item['faction']} | {item['world']} | `{item['loc']}` | `{item['sector']}` |\n"

    return md

def generate_cosmic_clockwork():
    """Generates the initial cosmic clockwork state table."""
    md = "# The Stellar Confluence Universe: Cosmic Clockwork & Ephemeris Tracker\n\n"
    md += "Tracks real-time Galactic Universal Time (GUT), spatial coordinates, facing angle relative to Confluence Wavefront vector, and active power limitations.\n\n"
    md += "| GUT | Book ID | Character | Loc_Type | Sector [X,Y,Z] | Facing_Angle | Resonance State | Active Power Capability / Limitation |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for item in ROSTER_DATA:
        # Determine initial state
        facing = item["facing"]
        if item["loc"] == "GATEWAY_SUBSPACE":
            res_state = "GATEWAY_SUBSPACE"
            cap = "Neutral Subspace Baseline (No buffs/debuffs)"
        elif 0 <= facing <= 30:
            res_state = "PEAK_FACING"
            cap = "Super-charged Wavefront alignment; equipment heat dissipation required"
        elif 150 <= facing <= 180:
            res_state = "SHADOW_FACING"
            cap = "Planetary occlusion / Eclipse lock; physical or auxiliary power only"
        else:
            res_state = "TRANSIT_FACING"
            cap = "Harmonic baseline; stable energy usage"

        if item["loc"] == "DEEP_SPACE_TRANSIT":
            cap = f"[Deep-Space 2x Volatility] {cap}"

        md += f"| 100 | Book {item['id']:02d} | {item['hero']} | `{item['loc']}` | `{item['sector']}` | {facing}° | `{res_state}` | {cap} |\n"

    return md

def bootstrap_state(force=False):
    """Bootstraps 00_System_State files."""
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    created = []

    # 1. Character Registry
    if force or not os.path.exists(CHARACTER_REGISTRY_MD):
        with open(CHARACTER_REGISTRY_MD, "w", encoding="utf-8") as f:
            f.write(generate_character_registry())
        created.append(CHARACTER_REGISTRY_MD)

    # 2. Cosmic Clockwork
    if force or not os.path.exists(COSMIC_CLOCKWORK_MD):
        with open(COSMIC_CLOCKWORK_MD, "w", encoding="utf-8") as f:
            f.write(generate_cosmic_clockwork())
        created.append(COSMIC_CLOCKWORK_MD)

    # 3. Rotation Tracker
    if force or not os.path.exists(ROTATION_TRACKER_MD):
        from advance_rotation import write_rotation_tracker
        write_rotation_tracker(1, 1, 100)
        created.append(ROTATION_TRACKER_MD)

    # 4. Diary
    if force or not os.path.exists(DIARY_MD):
        with open(DIARY_MD, "w", encoding="utf-8") as f:
            f.write("# The Stellar Confluence Universe: Diary of Completed Chapters\n\n")
            f.write("| GUT | Book | Chapter | Character | Synopsis / Action Summary |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        created.append(DIARY_MD)

    return {
        "status": "bootstrapped",
        "created_or_updated_files": created,
        "total_books_registered": len(ROSTER_DATA)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap Universe State for The Stellar Confluence Universe")
    parser.add_argument("--force", action="store_true", help="Overwrite existing state files")
    parser.add_argument("--dry-run", action="store_true", help="Preview roster count without writing")
    
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"total_books": len(ROSTER_DATA), "sample": ROSTER_DATA[:3]}, indent=2))
    else:
        # Ensure advance_rotation is importable from sibling skill scripts if needed
        sys.path.insert(0, os.path.join(PROJECT_ROOT, ".agents", "skills", "confluence-chapter-authoring", "scripts"))
        res = bootstrap_state(force=args.force)
        print(json.dumps(res, indent=2))
