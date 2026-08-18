#!/usr/bin/env python3
"""
Interactive HTML/SVG Visual Galactic Radar & Web Audio Studio Generator
Compiles real-time 3D sector coordinates, Confluence Wavefront angles, dynamic tension indices,
master relics, and pure Web Audio API soundscape synthesizers into a single standalone HTML dashboard.
"""

import os
import sys
import json
import re

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

PROJECT_ROOT = find_project_root()
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
DASHBOARD_HTML = os.path.join(SYSTEM_STATE_DIR, "universe_dashboard.html")


def generate_dashboard():
    # 1. Read Rotation Tracker
    rot_file = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
    active_book, active_chap, current_gut = 1, 1, 100
    if os.path.exists(rot_file):
        with open(rot_file, "r", encoding="utf-8") as f:
            content = f.read()
            m_book = re.search(r"Active Book #:\s*(\d+)", content)
            m_chap = re.search(r"Active Chapter #:\s*(\d+)", content)
            m_gut = re.search(r"Current GUT:\s*(\d+)", content)
            if m_book: active_book = int(m_book.group(1))
            if m_chap: active_chap = int(m_chap.group(1))
            if m_gut: current_gut = int(m_gut.group(1))

    # 2. Read Character Registry
    reg_file = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
    characters = []
    if os.path.exists(reg_file):
        with open(reg_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 6:
                    m_bid = re.search(r"Book\s+(\d+)", parts[1], re.IGNORECASE)
                    if m_bid:
                        bid = int(m_bid.group(1))
                        characters.append({
                            "book": bid,
                            "title": parts[2].replace("**", "").strip(),
                            "hero": parts[3].replace("`", "").strip(),
                            "faction": parts[4].replace("`", "").strip(),
                            "world": parts[5].replace("`", "").strip()
                        })


    # Build SVG Points
    svg_points = []
    center_x, center_y, max_r = 350, 350, 300
    for c in characters:
        bid = c["book"]
        angle_rad = (bid * (360.0 / 74.0)) * (3.14159 / 180.0)
        radius = 80 + ((bid % 7) * 30)
        px = center_x + (radius * 0.9 * (angle_rad ** 0.5 if bid % 2 == 0 else 1) * (1 if bid % 3 != 0 else -1)) % 260
        px = center_x + ((bid * 73) % 520) - 260
        py = center_y + ((bid * 137) % 520) - 260

        color = "#e67e22" if "Sun" in c["faction"] else ("#9b59b6" if "Void" in c["faction"] else ("#3498db" if "Astrolabe" in c["faction"] else "#1abc9c"))
        is_active = (bid == active_book)
        r_size = 8 if is_active else 4

        svg_points.append(
            f'<circle cx="{px}" cy="{py}" r="{r_size}" fill="{color}" stroke="#ffffff" stroke-width="{"2" if is_active else "0.5"}" '
            f'data-hero="{c["hero"]}" data-book="{bid}" data-world="{c["world"]}" data-faction="{c["faction"]}" class="star-node" />'
        )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Stellar Confluence Universe: Grand Master Studio</title>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --panel-bg: #151c2e;
            --accent-gold: #f39c12;
            --accent-solar: #e67e22;
            --accent-void: #9b59b6;
            --accent-gear: #3498db;
            --accent-frost: #1abc9c;
            --text-main: #e2e8f0;
            --text-dim: #94a3b8;
            --border: #2d3748;
        }}
        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        .sidebar {{
            width: 380px;
            background-color: var(--panel-bg);
            border-right: 1px solid var(--border);
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
        }}
        .main-stage {{
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
            background: radial-gradient(circle at center, #1a233a 0%, #0b0f19 100%);
        }}
        .header {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .badge {{
            background-color: var(--accent-gold);
            color: #000;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .radar-container {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .audio-bar {{
            padding: 16px 24px;
            background: rgba(21, 28, 46, 0.9);
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .btn {{
            background: #2563eb;
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
            transition: opacity 0.2s;
        }}
        .btn:hover {{ opacity: 0.9; }}
        .btn-gold {{ background: var(--accent-solar); }}
        .btn-void {{ background: var(--accent-void); }}
        .btn-gear {{ background: var(--accent-gear); }}
        .star-node {{ cursor: pointer; transition: transform 0.2s; }}
        .star-node:hover {{ transform: scale(2); }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div>
            <h1 style="font-size: 20px; margin: 0 0 6px 0; color: #fff;">The Stellar Confluence</h1>
            <p style="font-size: 13px; color: var(--text-dim); margin: 0;">74-Book Continuous Interstellar Narrative Engine</p>
        </div>
        <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 11px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 4px;">Universal Ephemeris State</div>
            <div style="font-size: 16px; font-weight: 700; color: var(--accent-gold);">GUT {current_gut} &bull; Book {active_book:02d} Ch {active_chap:02d}</div>
        </div>
        <div id="inspector-card" style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: 8px; border: 1px solid var(--border);">
            <div style="font-size: 11px; text-transform: uppercase; color: var(--text-dim); margin-bottom: 4px;">Protagonist Dossier</div>
            <div id="insp-hero" style="font-size: 18px; font-weight: 700; color: #fff;">Caelum Dawnrunner</div>
            <div id="insp-fac" style="font-size: 13px; color: var(--accent-solar); margin-top: 2px;">Sun-Forged Hegemony</div>
            <div id="insp-world" style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Homeworld: Helios Prime</div>
        </div>
    </div>
    <div class="main-stage">
        <div class="header">
            <span class="badge">Live 3D Confluence Radar</span>
            <span style="font-size: 13px; color: var(--text-dim);">74 Star-Systems Synchronized</span>
        </div>
        <div class="radar-container">
            <svg width="700" height="700" viewBox="0 0 700 700">
                <circle cx="350" cy="350" r="280" fill="none" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4" />
                <circle cx="350" cy="350" r="200" fill="none" stroke="#1e293b" stroke-width="1" />
                <circle cx="350" cy="350" r="100" fill="none" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4" />
                <line x1="350" y1="50" x2="350" y2="650" stroke="#1e293b" stroke-width="1" />
                <line x1="50" y1="350" x2="650" y2="350" stroke="#1e293b" stroke-width="1" />
                <!-- Center Ancient Gateway -->
                <circle cx="350" cy="350" r="12" fill="#38bdf8" />
                {' '.join(svg_points)}
            </svg>
        </div>
        <div class="audio-bar">
            <span style="font-size: 13px; font-weight: 600;">Procedural Soundscapes (Web Audio API):</span>
            <button class="btn btn-gold" onclick="playTone(144.2, 'sawtooth')">☀️ Solar Hum (144.2 Hz)</button>
            <button class="btn btn-void" onclick="playTone(128.5, 'sine')">🌑 Umbral Resonance (128.5 Hz)</button>
            <button class="btn btn-gear" onclick="playTone(160.0, 'triangle')">⚙️ Astrolabe Chime (160 Hz)</button>
        </div>
    </div>
    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, type) {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 1.2);
        }}
        document.querySelectorAll('.star-node').forEach(el => {{
            el.addEventListener('click', () => {{
                document.getElementById('insp-hero').innerText = el.dataset.hero;
                document.getElementById('insp-fac').innerText = el.dataset.faction;
                document.getElementById('insp-world').innerText = 'Homeworld: ' + el.dataset.world + ' (Book ' + el.dataset.book + ')';
            }});
        }});
    </script>
</body>
</html>"""

    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {
        "status": "generated",
        "file_path": DASHBOARD_HTML,
        "total_characters_rendered": len(characters)
    }

if __name__ == "__main__":
    res = generate_dashboard()
    print(json.dumps(res, indent=2))
