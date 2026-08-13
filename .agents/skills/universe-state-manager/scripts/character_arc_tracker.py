#!/usr/bin/env python3
"""
Character Arc, Inventory & Cross-Book Relationship Tracker for The Stellar Confluence Universe
Manages character inventories, artifact upgrades, physical conditions/wounds, and inter-faction
alliances across all 74 storylines.
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
ARCS_JSON = os.path.join(SYSTEM_STATE_DIR, "character_arcs.json")

def load_arcs():
    if not os.path.exists(ARCS_JSON):
        return {}
    try:
        with open(ARCS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_arcs(data):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(ARCS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_or_create_char_arc(book_id):
    arcs = load_arcs()
    b_key = f"Book_{int(book_id):02d}"
    if b_key not in arcs:
        arcs[b_key] = {
            "book_id": int(book_id),
            "inventory": [],
            "condition": "PEAK_HEALTH",
            "alliances": [],
            "major_milestones": []
        }
    return arcs, b_key

def add_inventory_item(book_id, item_name, item_desc=""):
    arcs, b_key = get_or_create_char_arc(book_id)
    item_entry = {"name": item_name, "description": item_desc}
    arcs[b_key]["inventory"].append(item_entry)
    save_arcs(arcs)
    return {"status": "item_added", "book": b_key, "item": item_entry}

def set_condition(book_id, condition_str):
    arcs, b_key = get_or_create_char_arc(book_id)
    arcs[b_key]["condition"] = condition_str
    save_arcs(arcs)
    return {"status": "condition_updated", "book": b_key, "condition": condition_str}

def add_alliance(book_id, ally_book_id, bond_description):
    arcs, b_key = get_or_create_char_arc(book_id)
    ally_key = f"Book_{int(ally_book_id):02d}"
    bond_entry = {"ally_book": ally_key, "bond": bond_description}
    arcs[b_key]["alliances"].append(bond_entry)
    save_arcs(arcs)
    return {"status": "alliance_recorded", "book": b_key, "alliance": bond_entry}

def inspect_arc(book_id):
    arcs = load_arcs()
    b_key = f"Book_{int(book_id):02d}"
    return arcs.get(b_key, {"message": f"No custom arc recorded for {b_key}; default fresh hero state."})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Character Arc & Inventory Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Inspect
    insp_p = subparsers.add_parser("inspect", help="Inspect character arc and inventory")
    insp_p.add_argument("--book", type=int, required=True, help="Book ID number (1-74)")

    # Add item
    item_p = subparsers.add_parser("add-item", help="Add artifact or equipment to character inventory")
    item_p.add_argument("--book", type=int, required=True)
    item_p.add_argument("--item", required=True)
    item_p.add_argument("--desc", default="")

    # Set condition
    cond_p = subparsers.add_parser("set-cond", help="Update character physical or mental condition")
    cond_p.add_argument("--book", type=int, required=True)
    cond_p.add_argument("--condition", required=True)

    # Add alliance
    ally_p = subparsers.add_parser("add-alliance", help="Record cross-book bond or alliance")
    ally_p.add_argument("--book", type=int, required=True)
    ally_p.add_argument("--ally-book", type=int, required=True)
    ally_p.add_argument("--bond", required=True)

    # List all
    subparsers.add_parser("list", help="List all tracked character arcs")

    args = parser.parse_args()

    if args.command == "inspect":
        print(json.dumps(inspect_arc(args.book), indent=2))
    elif args.command == "add-item":
        print(json.dumps(add_inventory_item(args.book, args.item, args.desc), indent=2))
    elif args.command == "set-cond":
        print(json.dumps(set_condition(args.book, args.condition), indent=2))
    elif args.command == "add-alliance":
        print(json.dumps(add_alliance(args.book, args.ally_book, args.bond), indent=2))
    elif args.command == "list":
        print(json.dumps(load_arcs(), indent=2))
    else:
        parser.print_help()
