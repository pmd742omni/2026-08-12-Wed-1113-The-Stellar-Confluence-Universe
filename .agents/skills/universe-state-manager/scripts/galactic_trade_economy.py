#!/usr/bin/env python3
"""
Interplanetary Trade Economy & Commercial Cargo Convoy Simulator for The Stellar Confluence Universe
Tracks commercial freighter fleets in transit, commodity market prices (Credits/ton),
planetary resource stockpiles, and supply shortages across all 74 star systems.
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
ECONOMY_STATE_JSON = os.path.join(SYSTEM_STATE_DIR, "galactic_economy.json")

DEFAULT_ECONOMY = {
    "commodity_market": {
        "Photonic Prism Crystals": {"base_price_credits": 120, "current_price": 125, "market_trend": "HIGH_DEMAND"},
        "Phase-Resonant Basalt": {"base_price_credits": 145, "current_price": 140, "market_trend": "STABLE"},
        "High-Torque Precision Brass": {"base_price_credits": 95, "current_price": 98, "market_trend": "STABLE"},
        "Cryo-Methane Ice": {"base_price_credits": 60, "current_price": 72, "market_trend": "RISING"}
    },
    "active_trade_convoys": [
        {
            "convoy_id": "CONVOY-SOL-01",
            "fleet_name": "Helios Solar Freight Guild",
            "origin_world": "Helios Prime",
            "dest_world": "Aethelgard Gear-City",
            "cargo": "Photonic Prism Crystals",
            "tonnage": 500,
            "status": "EN_ROUTE",
            "departure_gut": 98,
            "eta_gut": 104,
            "progress_percent": 33.3
        }
    ],
    "planetary_stockpiles": {
        "Helios Prime": {"Photonic Prism Crystals": 4200, "Precision Brass": 850, "Cryo-Methane Ice": 320},
        "Umbra Chasm": {"Phase-Resonant Basalt": 3800, "Solar Batteries": 410, "Precision Brass": 290},
        "Aethelgard": {"Precision Brass": 6500, "Photonic Prism Crystals": 720, "Raw Ores": 1400},
        "Gliesia": {"Cryo-Methane Ice": 8900, "Structural Alloy Frames": 450}
    }
}

def load_economy():
    if os.path.exists(ECONOMY_STATE_JSON):
        try:
            with open(ECONOMY_STATE_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_ECONOMY
    return DEFAULT_ECONOMY

def save_economy(eco):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(ECONOMY_STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(eco, f, indent=2)

def get_market_prices():
    eco = load_economy()
    return {
        "total_commodities": len(eco["commodity_market"]),
        "active_convoys_count": len(eco["active_trade_convoys"]),
        "market": eco["commodity_market"]
    }

def dispatch_convoy(origin, dest, cargo, tonnage, current_gut=100, transit_duration=6):
    eco = load_economy()
    cid = f"CONVOY-{len(eco['active_trade_convoys']) + 1:02d}"
    
    new_convoy = {
        "convoy_id": cid,
        "fleet_name": f"{origin} Commercial Convoy",
        "origin_world": origin,
        "dest_world": dest,
        "cargo": cargo,
        "tonnage": int(tonnage),
        "status": "EN_ROUTE",
        "departure_gut": int(current_gut),
        "eta_gut": int(current_gut) + int(transit_duration),
        "progress_percent": 0.0
    }

    eco["active_trade_convoys"].append(new_convoy)
    save_economy(eco)

    return {
        "status": "CONVOY_DISPATCHED",
        "convoy_id": cid,
        "route": f"{origin} -> {dest}",
        "cargo": f"{tonnage} tons of {cargo}",
        "eta_gut": int(current_gut) + int(transit_duration)
    }

def get_planetary_stockpile(world_name):
    eco = load_economy()
    for k, v in eco["planetary_stockpiles"].items():
        if world_name.lower() in k.lower():
            return {"world": k, "stockpiles": v}
    return {"world": world_name, "stockpiles": {"Standard Reserves": 1000}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interplanetary Trade Economy Engine")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("prices", help="Get commodity market prices")

    disp_p = subparsers.add_parser("dispatch", help="Dispatch commercial cargo convoy")
    disp_p.add_argument("--origin", required=True)
    disp_p.add_argument("--dest", required=True)
    disp_p.add_argument("--cargo", required=True)
    disp_p.add_argument("--tonnage", type=int, default=500)
    disp_p.add_argument("--gut", type=int, default=100)

    stock_p = subparsers.add_parser("stockpile", help="Get world resource stockpile")
    stock_p.add_argument("--world", required=True)

    args = parser.parse_args()

    if args.command == "dispatch":
        print(json.dumps(dispatch_convoy(args.origin, args.dest, args.cargo, args.tonnage, args.gut), indent=2))
    elif args.command == "stockpile":
        print(json.dumps(get_planetary_stockpile(args.world), indent=2))
    else:
        print(json.dumps(get_market_prices(), indent=2))
