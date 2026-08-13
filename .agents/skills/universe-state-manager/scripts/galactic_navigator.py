#!/usr/bin/env python3
"""
Galactic Route Planner & 3D Spatial Navigator for The Stellar Confluence Universe
Computes interstellar distances, Ancient Gateway shortcuts, transit durations, waypoint
trajectories, and wavefront exposure risk along interstellar corridors.
"""

import os
import sys
import json
import math
import re
import argparse

# Major Ancient Gateway Nexus Conduits in the Galaxy
GATEWAY_NETWORKS = [
    {"name": "Sol-Umbra Keystone Gateway", "entry": [10, 5, 0], "exit": [-10, 5, 0], "subspace_length_gut": 2},
    {"name": "Orrery-Singularity Trans-Spur", "entry": [0, 10, 5], "exit": [30, 10, -10], "subspace_length_gut": 3},
    {"name": "Core-Periphery Deep Conduit", "entry": [0, 0, 0], "exit": [0, 0, 100], "subspace_length_gut": 4}
]

def parse_sector(s):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", str(s))]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def plan_interstellar_route(origin_str, dest_str, ship_speed_units_per_gut=2.0):
    p_orig = parse_sector(origin_str)
    p_dest = parse_sector(dest_str)

    direct_dist = distance(p_orig, p_dest)
    direct_gut = max(1, math.ceil(direct_dist / ship_speed_units_per_gut))

    # Evaluate Gateway Conduit Routes
    best_route_type = "DIRECT_DEEP_SPACE"
    best_duration_gut = direct_gut
    gateway_used = None
    waypoints = [
        {"name": "Departure Point", "sector": p_orig, "type": "ORIGIN"}
    ]

    for gw in GATEWAY_NETWORKS:
        d_to_gw = distance(p_orig, gw["entry"])
        d_from_gw = distance(gw["exit"], p_dest)
        total_gw_dist = d_to_gw + d_from_gw
        gw_duration = math.ceil(d_to_gw / ship_speed_units_per_gut) + gw["subspace_length_gut"] + math.ceil(d_from_gw / ship_speed_units_per_gut)

        if gw_duration < best_duration_gut:
            best_route_type = "GATEWAY_CONDUIT_TRANSIT"
            best_duration_gut = gw_duration
            gateway_used = gw["name"]
            waypoints = [
                {"name": "Departure Point", "sector": p_orig, "type": "ORIGIN"},
                {"name": f"Gateway Ingress ({gw['name']})", "sector": gw["entry"], "type": "GATEWAY_ENTRY"},
                {"name": f"Gateway Subspace Traverse", "sector": [0, 0, 0], "type": "GATEWAY_SUBSPACE"},
                {"name": f"Gateway Egress ({gw['name']})", "sector": gw["exit"], "type": "GATEWAY_EXIT"},
                {"name": "Destination Arrival", "sector": p_dest, "type": "DESTINATION"}
            ]

    if best_route_type == "DIRECT_DEEP_SPACE":
        waypoints.append({"name": "Destination Arrival", "sector": p_dest, "type": "DESTINATION"})

    return {
        "origin_sector": p_orig,
        "destination_sector": p_dest,
        "direct_distance_units": round(direct_dist, 2),
        "chosen_route_type": best_route_type,
        "gateway_conduit": gateway_used,
        "estimated_transit_duration_gut": best_duration_gut,
        "wavefront_exposure_profile": "UNFILTERED_VOLATILITY (2x Buff / 2x Hazard)" if best_route_type == "DIRECT_DEEP_SPACE" else "HYBRID (Subspace Safe Corridor)",
        "waypoints": waypoints,
        "narrative_flight_plan": f"Flight from {p_orig} to {p_dest}: Duration {best_duration_gut} GUT ticks via {best_route_type}."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plan Interstellar Galactic Routes")
    parser.add_argument("--origin", required=True, help="Origin sector '[X, Y, Z]'")
    parser.add_argument("--dest", required=True, help="Destination sector '[X, Y, Z]'")
    parser.add_argument("--speed", type=float, default=2.0, help="Ship speed in sector units per GUT")
    
    args = parser.parse_args()
    res = plan_interstellar_route(args.origin, args.dest, args.speed)
    print(json.dumps(res, indent=2))
