#!/usr/bin/env python3
"""
Confluence Wavefront Mathematical Wave Mechanics & Doppler Physics Engine
Computes 3D harmonic wave phase, localized wavefront energy intensity (I in [0.5, 1.5]),
and relativistic Doppler frequency shifts for celestial bodies and transit starships.
"""

import math
import sys
import json
import re
import argparse

# Fundamental Galactic Constants
WAVE_VECTOR = (0.0, 0.25, 0.0) # Propagates along Galactic +Y axis (radians / sector unit)
WAVE_ANGULAR_VELOCITY = 0.125   # Radians per GUT tick
WAVE_SPEED_C = 8.0              # Sectors per GUT tick (propagation velocity)
BASE_HARMONIC_FREQ = 144.0      # MegaHertz base cosmic resonance frequency

def parse_vec3(vec_str):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", str(vec_str))]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def calculate_wavefront_state(sector_coords, gut_time, velocity_vec=(0.0, 0.0, 0.0)):
    x, y, z = parse_vec3(sector_coords)
    vx, vy, vz = parse_vec3(velocity_vec)
    t = float(gut_time)

    # Wave equation: Phase = (k . r - w * t) mod 2pi
    k_dot_r = (WAVE_VECTOR[0] * x) + (WAVE_VECTOR[1] * y) + (WAVE_VECTOR[2] * z)
    raw_phase = k_dot_r - (WAVE_ANGULAR_VELOCITY * t)
    phase_rad = raw_phase % (2.0 * math.pi)
    phase_deg = math.degrees(phase_rad)

    # Localized Wavefront Energy Intensity (I in [0.5, 1.5])
    # Sinusoidal modulation of the incoming Confluence energy
    intensity_factor = round(1.0 + (0.5 * math.sin(phase_rad)), 3)

    if intensity_factor >= 1.3:
        zone = "CREST_SURGE (High Energy Pulse)"
        tactical_impact = "Energy output amplified by +50%; weapon and shield heat accumulation accelerated."
    elif intensity_factor <= 0.7:
        zone = "TROUGH_DAMPENING (Interference Shadow)"
        tactical_impact = "Wavefront density thinned by -30%; energy recharge sluggish; cloaks more stable."
    else:
        zone = "HARMONIC_EQUILIBRIUM"
        tactical_impact = "Nominal stable energy flux across all local systems."

    # Relativistic Doppler Shift for Starships in Transit
    # v_parallel is velocity projected along wave propagation direction (+Y)
    v_parallel = vy
    doppler_factor = round(1.0 + (v_parallel / WAVE_SPEED_C), 4)
    observed_freq_mhz = round(BASE_HARMONIC_FREQ * doppler_factor, 2)

    if doppler_factor > 1.05:
        doppler_effect = "BLUE-SHIFTED (Flying against wave vector: Higher perceived energy frequency & friction)"
    elif doppler_factor < 0.95:
        doppler_effect = "RED-SHIFTED (Surfing with wave vector: Lower perceived energy friction & smooth glide)"
    else:
        doppler_effect = "STATIONARY / ORTHOGONAL (Zero Doppler Distortion)"

    return {
        "sector_coordinates": [x, y, z],
        "galactic_time_gut": t,
        "wave_phase_degrees": round(phase_deg, 1),
        "wave_intensity_factor": intensity_factor,
        "wave_zone": zone,
        "tactical_impact": tactical_impact,
        "velocity_vector": [vx, vy, vz],
        "doppler_shift_factor": doppler_factor,
        "observed_frequency_mhz": observed_freq_mhz,
        "doppler_flight_profile": doppler_effect
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Confluence Wavefront Physics & Doppler Engine")
    parser.add_argument("--sector", default="[10, 5, 0]", help="3D Sector coordinates [X, Y, Z]")
    parser.add_argument("--gut", type=float, default=100.0, help="Galactic Universal Time (GUT)")
    parser.add_argument("--velocity", default="[0, 0, 0]", help="Velocity vector [Vx, Vy, Vz]")

    args = parser.parse_args()
    res = calculate_wavefront_state(args.sector, args.gut, args.velocity)
    print(json.dumps(res, indent=2))
