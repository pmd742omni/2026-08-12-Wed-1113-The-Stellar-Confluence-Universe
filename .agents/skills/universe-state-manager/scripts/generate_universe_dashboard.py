#!/usr/bin/env python3
"""
Interactive Galactic Dashboard & Visual Universe Radar Generator for The Stellar Confluence Universe
Generates a standalone, zero-dependency visual HTML/SVG galactic radar map, faction hierarchy,
active cosmic ripple hazard overlays, and real-time round-robin queue visualizer.
"""

import os
import sys
import json
import re
import math
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
DASHBOARD_HTML = os.path.join(SYSTEM_STATE_DIR, "universe_dashboard.html")

def parse_sector(sector_str):
    nums = [float(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", str(sector_str))]
    while len(nums) < 3:
        nums.append(0.0)
    return nums[0], nums[1], nums[2]

def generate_dashboard():
    # 1. Read Rotation Tracker
    rot_p = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
    active_book = 1
    active_chap = 1
    curr_gut = 100
    if os.path.exists(rot_p):
        with open(rot_p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        b_m = re.search(r"Active\s+Book\s+Index[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        c_m = re.search(r"Active\s+Chapter\s+Number[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        g_m = re.search(r"Current\s+Galactic\s+Universal\s+Time\s*\(GUT\)[\*\s]*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
        if b_m: active_book = int(b_m.group(1))
        if c_m: active_chap = int(c_m.group(1))
        if g_m: curr_gut = int(g_m.group(1))

    # 2. Read Cosmic Clockwork
    clock_p = os.path.join(SYSTEM_STATE_DIR, "cosmic_clockwork.md")
    characters = []
    if os.path.exists(clock_p):
        with open(clock_p, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for line in lines:
            if not line.strip().startswith("|") or "GUT" in line or ":---" in line:
                continue
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 8:
                gut, b_id, char, loc, sector, facing, res, cap = parts[:8]
                x, y, z = parse_sector(sector)
                characters.append({
                    "book": b_id,
                    "character": char,
                    "loc_type": loc.replace("`", ""),
                    "sector": sector.replace("`", ""),
                    "x": x,
                    "y": y,
                    "z": z,
                    "facing": facing,
                    "resonance": res.replace("`", ""),
                    "capability": cap
                })

    # 3. Read Events
    events_p = os.path.join(SYSTEM_STATE_DIR, "cosmic_events.json")
    events = []
    if os.path.exists(events_p):
        try:
            with open(events_p, "r", encoding="utf-8") as f:
                events = json.load(f)
        except Exception:
            pass

    # 4. Generate SVG Radar Elements
    # Coordinate mapping: sector coords range roughly -35 to +35 -> map to SVG 800x800 viewBox (-40 to +40)
    def map_x(x): return 400 + (x * 9.0)
    def map_y(y): return 400 - (y * 9.0)

    svg_points = ""
    for c in characters:
        cx = map_x(c["x"])
        cy = map_y(c["y"])
        
        # Color coding by faction
        b_num_match = re.search(r"(\d+)", c["book"])
        b_num = int(b_num_match.group(1)) if b_num_match else 1
        
        if 1 <= b_num <= 10:
            fill_color = "#f59e0b" # Radiant Amber/Gold
            glow_class = "sun-forged"
        elif 11 <= b_num <= 20:
            fill_color = "#8b5cf6" # Void Violet
            glow_class = "void-bound"
        elif 21 <= b_num <= 30:
            fill_color = "#10b981" # Astrolabe Emerald
            glow_class = "astrolabe"
        else:
            fill_color = "#06b6d4" # Expansion Cyan
            glow_class = "expansion"

        is_active = (b_num == active_book)
        radius = 7 if is_active else 4
        stroke = "#ffffff" if is_active else "none"
        stroke_w = "2" if is_active else "0"

        svg_points += f"""<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill_color}" stroke="{stroke}" stroke-width="{stroke_w}" class="radar-dot {glow_class}">
            <title>{c['book']}: {c['character']} | Sector {c['sector']} | {c['resonance']} ({c['facing']})</title>
        </circle>
        <text x="{cx+6}" y="{cy+3}" font-size="8" fill="#94a3b8" font-family="monospace">{c['book']}</text>
        """

    # Event hazard rings
    svg_hazards = ""
    for ev in events:
        if ev.get("start_gut", 0) <= curr_gut <= ev.get("expiry_gut", 0):
            ex, ey, ez = parse_sector(ev["origin_sector"])
            ecx = map_x(ex)
            ecy = map_y(ey)
            er = ev["blast_radius"] * 9.0
            svg_hazards += f"""<circle cx="{ecx}" cy="{ecy}" r="{er}" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,4" class="hazard-pulse">
                <title>HAZARD {ev['id']}: {ev['event_type']} ({ev['source_book']})</title>
            </circle>"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Stellar Confluence Universe Dashboard</title>
<style>
  :root {{
    --bg: #0b0f19;
    --card: #131b2e;
    --border: #1e293b;
    --text: #e2e8f0;
    --muted: #64748b;
    --sun: #f59e0b;
    --void: #8b5cf6;
    --astro: #10b981;
    --exp: #06b6d4;
  }}
  body {{
    margin: 0;
    padding: 24px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 24px;
  }}
  h1 {{ margin: 0; font-size: 24px; font-weight: 700; }}
  .metrics {{
    display: flex;
    gap: 16px;
  }}
  .metric-badge {{
    background: var(--card);
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
  }}
  .metric-val {{ font-size: 18px; font-weight: bold; color: var(--sun); display: block; }}
  .main-layout {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
  }}
  .card h2 {{ margin-top: 0; font-size: 16px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
  svg.radar {{
    width: 100%;
    height: auto;
    background: #070a13;
    border-radius: 8px;
    border: 1px solid var(--border);
  }}
  .radar-dot {{ transition: all 0.2s; cursor: pointer; }}
  .radar-dot:hover {{ r: 9; filter: brightness(1.5); }}
  .legend {{
    display: flex;
    gap: 16px;
    margin-top: 12px;
    font-size: 12px;
  }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }}
  th, td {{
    text-align: left;
    padding: 8px;
    border-bottom: 1px solid var(--border);
  }}
  th {{ color: var(--muted); }}
  .active-row {{ background: rgba(245, 158, 11, 0.1); font-weight: bold; }}
  @keyframes pulse {{
    0% {{ transform: scale(0.98); opacity: 0.4; }}
    50% {{ transform: scale(1.02); opacity: 0.8; }}
    100% {{ transform: scale(0.98); opacity: 0.4; }}
  }}
  .hazard-pulse {{ animation: pulse 3s infinite ease-in-out; transform-origin: center; }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>The Stellar Confluence Universe</h1>
    <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">74-Book Interconnected Series State Engine</div>
  </div>
  <div class="metrics">
    <div class="metric-badge">
      <span class="metric-val">Book {active_book:02d}</span>
      <span>Active Queue</span>
    </div>
    <div class="metric-badge">
      <span class="metric-val">Chapter {active_chap:02d}</span>
      <span>Current Cycle</span>
    </div>
    <div class="metric-badge">
      <span class="metric-val">GUT {curr_gut}</span>
      <span>Galactic Universal Time</span>
    </div>
  </div>
</div>

<div class="main-layout">
  <!-- Left: Galactic Radar Map -->
  <div class="card">
    <h2>Galactic Spatial Radar (Sector X / Y Projection)</h2>
    <svg class="radar" viewBox="0 0 800 800">
      <!-- Grid & Rings -->
      <circle cx="400" cy="400" r="360" fill="none" stroke="#1e293b" stroke-width="1" />
      <circle cx="400" cy="400" r="270" fill="none" stroke="#1e293b" stroke-width="1" />
      <circle cx="400" cy="400" r="180" fill="none" stroke="#1e293b" stroke-width="1" />
      <circle cx="400" cy="400" r="90" fill="none" stroke="#1e293b" stroke-width="1" />
      <line x1="0" y1="400" x2="800" y2="400" stroke="#1e293b" stroke-width="1" />
      <line x1="400" y1="0" x2="400" y2="800" stroke="#1e293b" stroke-width="1" />
      
      <!-- Wavefront Direction Indicator -->
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" fill="#f59e0b" />
        </marker>
      </defs>
      <line x1="400" y1="760" x2="400" y2="700" stroke="#f59e0b" stroke-width="2" marker-end="url(#arrow)" />
      <text x="415" y="740" font-size="11" fill="#f59e0b" font-family="monospace">Confluence Wavefront Vector (+Y)</text>

      <!-- Active Hazards -->
      {svg_hazards}

      <!-- Character Coordinates -->
      {svg_points}
    </svg>

    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background: var(--sun)"></div> Sun-Forged (1-10)</div>
      <div class="legend-item"><div class="legend-dot" style="background: var(--void)"></div> Void-Bound (11-20)</div>
      <div class="legend-item"><div class="legend-dot" style="background: var(--astro)"></div> Astrolabe (21-30)</div>
      <div class="legend-item"><div class="legend-dot" style="background: var(--exp)"></div> Expansion (31-74)</div>
    </div>
  </div>

  <!-- Right: Active Ephemeris Table -->
  <div class="card" style="max-height: 840px; overflow-y: auto;">
    <h2>Active Cosmic Ephemeris ({len(characters)} Storylines)</h2>
    <table>
      <thead>
        <tr>
          <th>Book</th>
          <th>Hero</th>
          <th>Location</th>
          <th>Facing</th>
          <th>Resonance</th>
        </tr>
      </thead>
      <tbody>
"""

    for c in characters:
        b_num_match = re.search(r"(\d+)", c["book"])
        b_num = int(b_num_match.group(1)) if b_num_match else 1
        row_cls = "active-row" if b_num == active_book else ""
        html_content += f"""        <tr class="{row_cls}">
          <td>{c['book']}</td>
          <td>{c['character']}</td>
          <td><code>{c['loc_type']}</code> {c['sector']}</td>
          <td>{c['facing']}</td>
          <td><code>{c['resonance']}</code></td>
        </tr>
"""

    html_content += """      </tbody>
    </table>
  </div>
</div>

</body>
</html>"""

    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {
        "status": "generated",
        "file_path": DASHBOARD_HTML,
        "total_characters_rendered": len(characters),
        "active_hazards_rendered": len(events)
    }

if __name__ == "__main__":
    res = generate_dashboard()
    print(json.dumps(res, indent=2))
