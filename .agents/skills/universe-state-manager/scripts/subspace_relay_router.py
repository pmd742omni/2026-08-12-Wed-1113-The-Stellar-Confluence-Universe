#!/usr/bin/env python3
"""
3D Subspace Relay Network & Signal Routing Simulator for The Stellar Confluence Universe
Calculates multi-hop transmission routes across orbital relay buoys, packet latency in GUT ticks,
signal clarity degradation (0-100%), and atmospheric cosmic ion storm jamming.
"""

import os
import sys
import json
import math
import re
import argparse

RELAY_BUOYS = [
    {"id": "RELAY-SOL-ALPHA", "name": "Helios Prime High Solar Buoy", "coords": [10.0, 5.0, 0.0], "freq": "144.2 MHz"},
    {"id": "RELAY-GATE-ZERO", "name": "Central Ancient Gateway Repeater", "coords": [0.0, 0.0, 0.0], "freq": "144.0 MHz"},
    {"id": "RELAY-UMBRA-BETA", "name": "Nadir Umbral Eclipse Beacon", "coords": [-10.0, 5.0, 0.0], "freq": "128.5 MHz"},
    {"id": "RELAY-AETH-OMEGA", "name": "Aethelgard Gear-Ring Transceiver", "coords": [16.0, 5.0, 0.0], "freq": "160.0 MHz"},
    {"id": "RELAY-GLIES-CRY", "name": "Gliesia Perihelion Array", "coords": [-12.0, 4.0, 2.0], "freq": "152.4 MHz"}
]

def parse_coords(coord_input):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", str(coord_input))]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def euclidean_dist(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)

def route_transmission(origin_coords, dest_coords, carrier_freq_mhz=144.2, ion_storm=False):
    orig = parse_coords(origin_coords)
    dest = parse_coords(dest_coords)

    direct_dist = euclidean_dist(orig, dest)

    # Find nearest origin buoy and nearest dest buoy
    orig_buoy = min(RELAY_BUOYS, key=lambda b: euclidean_dist(orig, b["coords"]))
    dest_buoy = min(RELAY_BUOYS, key=lambda b: euclidean_dist(dest, b["coords"]))

    hops = []
    hops.append({"stage": "UPLINK", "station": f"Origin [{orig[0]:.1f}, {orig[1]:.1f}, {orig[2]:.1f}] -> {orig_buoy['name']}"})
    
    if orig_buoy["id"] != dest_buoy["id"]:
        # Subspace carrier transit between buoys
        hops.append({"stage": "GATEWAY_SUB_TRANSIT", "station": f"{orig_buoy['name']} -> Central Gateway Repeater -> {dest_buoy['name']}"})
    
    hops.append({"stage": "DOWNLINK", "station": f"{dest_buoy['name']} -> Destination [{dest[0]:.1f}, {dest[1]:.1f}, {dest[2]:.1f}]"})

    hop_count = len(hops)
    
    # Latency calculation: ~0.5 GUT per inter-sector hop
    latency_gut = max(1, math.ceil(direct_dist / 12.0) + (1 if ion_storm else 0))

    # Signal clarity: 100% minus 5% per hop, minus 25% if ion storm
    clarity_loss = (hop_count * 5.0) + (25.0 if ion_storm else 0.0)
    clarity_pct = round(max(10.0, 100.0 - clarity_loss), 1)

    status = "OPTIMAL" if clarity_pct >= 80 else ("DEGRADED" if clarity_pct >= 50 else "HEAVILY_JAMMED")

    return {
        "status": status,
        "direct_distance_units": round(direct_dist, 2),
        "packet_latency_gut": latency_gut,
        "signal_clarity_percent": clarity_pct,
        "carrier_frequency_mhz": carrier_freq_mhz,
        "ion_storm_interference": ion_storm,
        "total_hops": hop_count,
        "routing_hops": hops
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subspace Relay Network Router")
    parser.add_argument("--origin", default="[10, 5, 0]")
    parser.add_argument("--dest", default="[-12, 4, 2]")
    parser.add_argument("--freq", type=float, default=144.2)
    parser.add_argument("--ion-storm", action="store_true")

    args = parser.parse_args()
    res = route_transmission(args.origin, args.dest, args.freq, args.ion_storm)
    print(json.dumps(res, indent=2))
