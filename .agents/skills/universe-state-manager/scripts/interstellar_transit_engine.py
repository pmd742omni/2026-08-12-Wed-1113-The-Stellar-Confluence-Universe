#!/usr/bin/env python3
"""
3D Interstellar Transit Vector Engine & Orbital Docking Propagator
Simulates real-time 3D vector physics for starships in DEEP_SPACE_TRANSIT, advancing coordinates
each GUT tick (r_new = r_old + v * dt), computing transit progress (0% -> 100%), and executing
automatic orbital insertions upon arrival.
"""

import os
import sys
import json
import math
import re
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
TRANSIT_STATE_JSON = os.path.join(SYSTEM_STATE_DIR, "transit_missions.json")

def parse_sector(sector_str):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", str(sector_str))]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def load_transit_missions():
    if os.path.exists(TRANSIT_STATE_JSON):
        try:
            with open(TRANSIT_STATE_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_transit_missions(missions):
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(TRANSIT_STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(missions, f, indent=2)

def start_transit_mission(book_id, origin_sector, dest_sector, dest_world_name, speed=2.0, start_gut=100):
    book_id = int(book_id)
    ox, oy, oz = parse_sector(origin_sector)
    dx, dy, dz = parse_sector(dest_sector)
    
    dist = math.sqrt((dx - ox)**2 + (dy - oy)**2 + (dz - oz)**2)
    if dist < 0.001:
        return {"error": "Origin and destination sectors are identical."}

    duration_gut = max(1, math.ceil(dist / speed))
    vx = ((dx - ox) / dist) * speed
    vy = ((dy - oy) / dist) * speed
    vz = ((dz - oz) / dist) * speed

    mission = {
        "book_id": book_id,
        "status": "IN_TRANSIT",
        "origin_world": f"Sector [{ox:.1f}, {oy:.1f}, {oz:.1f}]",
        "origin_coords": [ox, oy, oz],
        "current_coords": [ox, oy, oz],
        "dest_world": dest_world_name,
        "dest_coords": [dx, dy, dz],
        "speed_units_per_gut": speed,
        "velocity_vector": [round(vx, 3), round(vy, 3), round(vz, 3)],
        "total_distance_units": round(dist, 2),
        "distance_traveled": 0.0,
        "start_gut": start_gut,
        "estimated_arrival_gut": start_gut + duration_gut,
        "progress_percent": 0.0
    }

    missions = load_transit_missions()
    missions[str(book_id)] = mission
    save_transit_missions(missions)

    return {
        "status": "MISSION_INITIATED",
        "book_id": book_id,
        "destination": dest_world_name,
        "duration_gut": duration_gut,
        "estimated_arrival_gut": start_gut + duration_gut,
        "velocity_vector": [round(vx, 3), round(vy, 3), round(vz, 3)]
    }

def propagate_transits(gut_delta=1):
    missions = load_transit_missions()
    updated = []

    for bid, m in missions.items():
        if m["status"] == "IN_TRANSIT":
            cx, cy, cz = m["current_coords"]
            dx, dy, dz = m["dest_coords"]
            vx, vy, vz = m["velocity_vector"]

            # Advance coordinates: r(t + dt) = r(t) + v * dt
            new_x = cx + (vx * gut_delta)
            new_y = cy + (vy * gut_delta)
            new_z = cz + (vz * gut_delta)

            # Check distance to destination
            rem_dist = math.sqrt((dx - new_x)**2 + (dy - new_y)**2 + (dz - new_z)**2)
            step_dist = m["speed_units_per_gut"] * gut_delta

            if rem_dist <= step_dist * 0.75:
                # Arrived at destination -> execute orbital docking insertion
                m["status"] = "ARRIVED_ORBITAL_DOCK"
                m["current_coords"] = [dx, dy, dz]
                m["progress_percent"] = 100.0
                m["distance_traveled"] = m["total_distance_units"]
            else:
                m["current_coords"] = [round(new_x, 2), round(new_y, 2), round(new_z, 2)]
                dist_done = m["total_distance_units"] - rem_dist
                m["distance_traveled"] = round(dist_done, 2)
                m["progress_percent"] = round(min(99.0, (dist_done / m["total_distance_units"]) * 100), 1)

            updated.append(m)

    save_transit_missions(missions)
    return {
        "propagated_missions_count": len(updated),
        "missions": updated
    }

def get_transit_status(book_id):
    missions = load_transit_missions()
    bid_str = str(int(book_id))
    if bid_str in missions:
        return missions[bid_str]
    return {
        "book_id": int(book_id),
        "status": "STATIONARY_ORBITAL_OR_SURFACE",
        "message": "No active deep-space transit flight plan."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3D Interstellar Transit Vector Engine")
    subparsers = parser.add_subparsers(dest="command")

    # Start
    st_p = subparsers.add_parser("start", help="Start deep space transit")
    st_p.add_argument("--book", type=int, required=True)
    st_p.add_argument("--origin", default="[10, 5, 0]")
    st_p.add_argument("--dest", required=True)
    st_p.add_argument("--dest-name", default="Target World")
    st_p.add_argument("--speed", type=float, default=2.0)
    st_p.add_argument("--gut", type=int, default=100)

    # Propagate
    pr_p = subparsers.add_parser("propagate", help="Advance active transits")
    pr_p.add_argument("--gut-delta", type=int, default=1)

    # Status
    sp_p = subparsers.add_parser("status", help="Get transit status")
    sp_p.add_argument("--book", type=int, required=True)

    args = parser.parse_args()

    if args.command == "start":
        print(json.dumps(start_transit_mission(args.book, args.origin, args.dest, args.dest_name, args.speed, args.gut), indent=2))
    elif args.command == "propagate":
        print(json.dumps(propagate_transits(args.gut_delta), indent=2))
    elif args.command == "status":
        print(json.dumps(get_transit_status(args.book), indent=2))
    else:
        print(json.dumps(propagate_transits(1), indent=2))
