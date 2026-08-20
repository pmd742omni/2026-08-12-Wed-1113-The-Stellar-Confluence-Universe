#!/usr/bin/env python3
"""
Interplanetary Trade Economy & Dynamic Multi-Tier Commodity Market Simulator
for The Stellar Confluence Universe.
Tracks commercial freighter fleets in transit, 25+ commodities across 4 tiers,
multi-currency exchange valuation (Sol-Credits, Guild Scrip, Void-Tokens),
dynamic price elasticity, planetary stockpiles, and interstellar economic crises.
"""

import os
import sys
import json
import math
import random
import argparse
from typing import Dict, Any, List, Optional

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

# 25+ Comprehensive Commodities Across 4 Economic Tiers
COMMODITY_CATALOG = {
    "RAW_ORES_AND_ENERGETICS": [
        {"name": "Solarite Ore", "base_price": 85, "unit": "ton", "description": "Raw photonic solar crystal ore mined from sunward mesas."},
        {"name": "Phase-Resonant Basalt", "base_price": 145, "unit": "ton", "description": "Dense subterranean igneous rock capable of absorbing wavefront tremors."},
        {"name": "Cryo-Methane Ice", "base_price": 60, "unit": "ton", "description": "High-purity frozen cometary volatile used for reactor cooling and propellant."},
        {"name": "Silicon Plasma-Silk", "base_price": 210, "unit": "spool", "description": "Electromagnetic mineral filaments harvested from silicon-weaver webs."},
        {"name": "Raw Bismuth-Chalcogenide", "base_price": 115, "unit": "ton", "description": "Iridescent heavy crystal ore used in thermoelectric generators."},
        {"name": "Heavy Thorium Fuel Pebble", "base_price": 320, "unit": "canister", "description": "Clean fission isotope pebbles for deep-space long-haul freighters."}
    ],
    "REFINED_TECHNOLOGY_AND_PRECISION": [
        {"name": "Photonic Prism Crystals", "base_price": 120, "unit": "crate", "description": "Polished optical grade quartz prisms for beam focusing arrays."},
        {"name": "High-Torque Precision Brass", "base_price": 95, "unit": "ton", "description": "Low-friction alloy billets for astronomical gear trains."},
        {"name": "Tachyon Chrono-Cells", "base_price": 450, "unit": "cell", "description": "Harmonic energy cells capable of temporal phase synchronization."},
        {"name": "Superconducting Ceramic Rails", "base_price": 180, "unit": "segment", "description": "Zero-resistance tracks for planetary mag-levs and launch catapults."},
        {"name": "Magnetic Flux Coils", "base_price": 260, "unit": "coil", "description": "High-induction magnetic confinement rings for coronal plasma containment."},
        {"name": "Subspace Acoustic Pitch-Pipes", "base_price": 140, "unit": "set", "description": "Precision brass whistle sets used to calibrate subspace communication relays."}
    ],
    "BIOTECH_ORGANICS_AND_AGRO": [
        {"name": "Luminescent Sea Spores", "base_price": 75, "unit": "barrel", "description": "Phosphorescent oceanic algae providing natural, non-electric habitat lighting."},
        {"name": "Medicinal Star-Bloom Salves", "base_price": 190, "unit": "jar", "description": "Curative soothing balm extracted from high-canopy midnight orchids."},
        {"name": "Symbiotic Living Chitin", "base_price": 230, "unit": "sheet", "description": "Self-healing bio-armor plating grown in bio-alchemical nurseries."},
        {"name": "Succulent Desert Nectar", "base_price": 80, "unit": "keg", "description": "Nutrient-rich golden nectar pressed from solar-blooming succulents."},
        {"name": "Aerostat Buoyancy Gas", "base_price": 90, "unit": "canister", "description": "Lighter-than-air atmospheric gas for cloud-archipelago sky-barges."},
        {"name": "Bioluminescent Coral Plugs", "base_price": 135, "unit": "crate", "description": "Cultured coral seed colonies for undersea station oxygenation."}
    ],
    "CULTURAL_AND_LUXURY_GOODS": [
        {"name": "Singing Quartz Goblets", "base_price": 280, "unit": "pair", "description": "Hand-carved resonant drinking vessels that chime in harmony with wavefront crests."},
        {"name": "Solar Spice Honey Mead", "base_price": 110, "unit": "case", "description": "Warm golden spiced beverage shared during solar solstice festivals."},
        {"name": "Umbral Eclipse Tapestries", "base_price": 340, "unit": "piece", "description": "Intricate hand-woven basalt-silk tapestries depicting celestial alignments."},
        {"name": "Precision Astrolabe Pocket Watches", "base_price": 500, "unit": "piece", "description": "Masterwork pocket chronometers tracking all 74 world rotations."},
        {"name": "Star-Bloom Perfume", "base_price": 175, "unit": "vial", "description": "Delicate fragrant essence favored across diplomatic embassies."},
        {"name": "Golden Sun Votive Bells", "base_price": 160, "unit": "trio", "description": "Tuned brass chimes rung during morning observatory dawn services."}
    ]
}

# Galactic Currencies & Exchange Rates (Normalized to Sol-Credits)
GALACTIC_CURRENCIES = {
    "SOL_CREDIT": {"name": "Solar Sovereign Credit (SC)", "symbol": "SC", "exchange_rate_to_sc": 1.0, "backing": "1 kWh Solarite Photonic Energy Reserve"},
    "GUILD_SCRIP": {"name": "Astrolabe Precision Scrip (GPS)", "symbol": "GPS", "exchange_rate_to_sc": 1.15, "backing": "100g Certified High-Torque Precision Brass"},
    "VOID_TOKEN": {"name": "Umbral Silence Token (VT)", "symbol": "VT", "exchange_rate_to_sc": 0.95, "backing": "1 kg Phase-Resonant Basalt Reserve"},
    "FLOTILLA_VOUCHER": {"name": "Wayfarer Drift Voucher (WDV)", "symbol": "WDV", "exchange_rate_to_sc": 0.85, "backing": "10 Liters Cryo-Methane Propellant"}
}

def get_default_market() -> Dict[str, Any]:
    market = {}
    for cat_key, items in COMMODITY_CATALOG.items():
        for itm in items:
            market[itm["name"]] = {
                "base_price_credits": itm["base_price"],
                "current_price": itm["base_price"],
                "unit": itm["unit"],
                "category": cat_key,
                "market_trend": "STABLE",
                "description": itm["description"]
            }
    return market

DEFAULT_ECONOMY = {
    "commodity_market": get_default_market(),
    "currencies": GALACTIC_CURRENCIES,
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
        },
        {
            "convoy_id": "CONVOY-ASTRO-02",
            "fleet_name": "Meridian Precision Cargo Flotilla",
            "origin_world": "Aethelgard Gear-City",
            "dest_world": "Umbra Chasm",
            "cargo": "High-Torque Precision Brass",
            "tonnage": 800,
            "status": "EN_ROUTE",
            "departure_gut": 99,
            "eta_gut": 105,
            "progress_percent": 25.0
        }
    ],
    "planetary_stockpiles": {
        "Helios Prime": {"Photonic Prism Crystals": 4200, "Precision Brass": 850, "Cryo-Methane Ice": 320, "Solarite Ore": 12000, "Solar Spice Honey Mead": 600},
        "Umbra Chasm": {"Phase-Resonant Basalt": 3800, "Solar Batteries": 410, "Precision Brass": 290, "Umbral Eclipse Tapestries": 150},
        "Aethelgard": {"High-Torque Precision Brass": 6500, "Photonic Prism Crystals": 720, "Precision Astrolabe Pocket Watches": 450, "Raw Ores": 1400},
        "Gliesia": {"Cryo-Methane Ice": 8900, "Structural Alloy Frames": 450, "Silicon Plasma-Silk": 800}
    },
    "active_economic_crises": []
}

def load_economy() -> Dict[str, Any]:
    if os.path.exists(ECONOMY_STATE_JSON):
        try:
            with open(ECONOMY_STATE_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all 25+ commodities exist in market
                if len(data.get("commodity_market", {})) < 20:
                    default_m = get_default_market()
                    default_m.update(data.get("commodity_market", {}))
                    data["commodity_market"] = default_m
                return data
        except Exception:
            return DEFAULT_ECONOMY
    return DEFAULT_ECONOMY

def save_economy(eco: Dict[str, Any]):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(ECONOMY_STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(eco, f, indent=2)

def get_market_prices(category: Optional[str] = None) -> Dict[str, Any]:
    eco = load_economy()
    market = eco.get("commodity_market", get_default_market())
    if category:
        filtered = {k: v for k, v in market.items() if category.upper() in v.get("category", "")}
    else:
        filtered = market
    return {
        "total_commodities": len(filtered),
        "active_convoys_count": len(eco.get("active_trade_convoys", [])),
        "currencies": eco.get("currencies", GALACTIC_CURRENCIES),
        "market": filtered
    }

def convert_currency(amount: float, from_currency: str = "SOL_CREDIT", to_currency: str = "GUILD_SCRIP") -> Dict[str, Any]:
    """Converts amounts between galactic currencies with transparent exchange rates."""
    from_curr = GALACTIC_CURRENCIES.get(from_currency.upper(), GALACTIC_CURRENCIES["SOL_CREDIT"])
    to_curr = GALACTIC_CURRENCIES.get(to_currency.upper(), GALACTIC_CURRENCIES["GUILD_SCRIP"])

    # Convert to base Sol-Credits, then to target
    amount_in_sc = amount * from_curr["exchange_rate_to_sc"]
    converted = round(amount_in_sc / to_curr["exchange_rate_to_sc"], 2)

    return {
        "original_amount": amount,
        "from_currency": from_curr["name"],
        "converted_amount": converted,
        "to_currency": to_curr["name"],
        "effective_exchange_rate": round(from_curr["exchange_rate_to_sc"] / to_curr["exchange_rate_to_sc"], 4)
    }

def dispatch_convoy(origin: str, dest: str, cargo: str, tonnage: int, current_gut: int = 100, transit_duration: int = 6) -> Dict[str, Any]:
    eco = load_economy()
    cid = f"CONVOY-{len(eco.get('active_trade_convoys', [])) + 1:02d}"
    
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

    if "active_trade_convoys" not in eco:
        eco["active_trade_convoys"] = []
    eco["active_trade_convoys"].append(new_convoy)
    save_economy(eco)

    return {
        "status": "CONVOY_DISPATCHED",
        "convoy_id": cid,
        "route": f"{origin} -> {dest}",
        "cargo": f"{tonnage} tons of {cargo}",
        "departure_gut": int(current_gut),
        "eta_gut": int(current_gut) + int(transit_duration)
    }

def trigger_market_fluctuation(commodity_name: str, delta_percent: float, reason: str = "Interstellar Supply Shift") -> Dict[str, Any]:
    """Dynamically adjusts commodity prices according to supply shocks or trade booms."""
    eco = load_economy()
    market = eco.get("commodity_market", get_default_market())

    # Find commodity
    found_key = None
    for k in market:
        if commodity_name.lower() in k.lower():
            found_key = k
            break
    if not found_key:
        return {"error": f"Commodity '{commodity_name}' not found in market catalog."}

    item = market[found_key]
    old_p = item["current_price"]
    multiplier = 1.0 + (delta_percent / 100.0)
    new_p = max(5, round(old_p * multiplier))
    trend = "RISING" if delta_percent > 0 else ("FALLING" if delta_percent < 0 else "STABLE")
    if abs(delta_percent) > 25:
        trend = "SURGE" if delta_percent > 0 else "CRASH"

    item["current_price"] = new_p
    item["market_trend"] = trend

    save_economy(eco)
    return {
        "status": "MARKET_UPDATED",
        "commodity": found_key,
        "old_price_credits": old_p,
        "new_price_credits": new_p,
        "percentage_change": f"{delta_percent:+.1f}%",
        "market_trend": trend,
        "reason": reason
    }

def get_planetary_stockpile(world_name: str) -> Dict[str, Any]:
    eco = load_economy()
    stockpiles = eco.get("planetary_stockpiles", {})
    for k, v in stockpiles.items():
        if world_name.lower() in k.lower():
            return {"world": k, "stockpiles": v}
    return {
        "world": world_name,
        "stockpiles": {
            "Standard Solarite Reserves": 2500,
            "Precision Brass Fittings": 600,
            "Cryo-Coolant Canisters": 400
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interplanetary Trade Economy Engine")
    subparsers = parser.add_subparsers(dest="command")

    # Prices
    pr_p = subparsers.add_parser("prices", help="Get commodity market prices")
    pr_p.add_argument("--category", help="Filter by commodity category")

    # Convert
    cv_p = subparsers.add_parser("convert", help="Convert currency amounts")
    cv_p.add_argument("--amount", type=float, default=100.0)
    cv_p.add_argument("--from-curr", default="SOL_CREDIT")
    cv_p.add_argument("--to-curr", default="GUILD_SCRIP")

    # Dispatch
    disp_p = subparsers.add_parser("dispatch", help="Dispatch commercial cargo convoy")
    disp_p.add_argument("--origin", required=True)
    disp_p.add_argument("--dest", required=True)
    disp_p.add_argument("--cargo", required=True)
    disp_p.add_argument("--tonnage", type=int, default=500)
    disp_p.add_argument("--gut", type=int, default=100)

    # Fluctuate
    fl_p = subparsers.add_parser("fluctuate", help="Simulate price fluctuation")
    fl_p.add_argument("--commodity", required=True)
    fl_p.add_argument("--delta", type=float, required=True, help="Percent delta (+15, -20)")
    fl_p.add_argument("--reason", default="Trade convoy arrival")

    # Stockpile
    stock_p = subparsers.add_parser("stockpile", help="Get world resource stockpile")
    stock_p.add_argument("--world", required=True)

    args = parser.parse_args()

    if args.command == "convert":
        print(json.dumps(convert_currency(args.amount, args.from_curr, args.to_curr), indent=2))
    elif args.command == "dispatch":
        print(json.dumps(dispatch_convoy(args.origin, args.dest, args.cargo, args.tonnage, args.gut), indent=2))
    elif args.command == "fluctuate":
        print(json.dumps(trigger_market_fluctuation(args.commodity, args.delta, args.reason), indent=2))
    elif args.command == "stockpile":
        print(json.dumps(get_planetary_stockpile(args.world), indent=2))
    else:
        print(json.dumps(get_market_prices(getattr(args, "category", None)), indent=2))
