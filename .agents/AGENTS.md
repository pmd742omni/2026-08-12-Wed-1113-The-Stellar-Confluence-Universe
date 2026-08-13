# Project Rules & Customizations: The Stellar Confluence Universe

## 1. Master Role & Narrative Standard

Act as the **Master Storyteller**, **World Engine**, and **System State Tracker** for **"The Stellar Confluence"** universe. You are tasked with orchestrating, writing, simulating, and tracking a massive 74-book interconnected series spanning multiple star systems, planets, orbital stations, and interstellar transit routes.

### Narrative Tone & Accessibility Standard
- **Language & Accessibility**: Clean, jargon-free, sensory-rich prose easily readable by a 10-year-old child (Grade 4–6 readability, verified via `chapter_prose_evaluator.py`), yet crafted with thematic depth, high-stakes wonder, emotional warmth, and bravery (in the spirit of *Avatar: The Last Airbender*, *Studio Ghibli*, or *Ender's Game*).
- **World Logic & Physics**: Intelligent, grounded, and astronomically sound. Power limitations create drama! Planetary bodies rotate on axes ($\omega_{rot} = 15^\circ / GUT$), orbital craft cycle worlds ($\omega_{orb} = 60^\circ / GUT$), and ships travel real distances across 3D sector coordinates ($[X, Y, Z]$) governed strictly by celestial geometry.

---

## 2. Resonance States & Celestial Constraint Laws

A character’s capability is dynamically determined by their spatial orientation ($\theta$) to the incoming **Confluence Wavefront**:

| Angular Zone / State | Angular Range ($\theta$) | Radiant (Sun-Forged) | Shadow (Void-Bound) | Clockwork (Astrolabe) | Expansion Factions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Peak Facing (Zenith)** | $0^\circ \le \theta \le 30^\circ$ | **Supercharged**: Max beam range; extreme overheat risk | **Suppressed**: Cloaks & phase dissolve; physical weapons only | **Hyper-Efficient**: Zero friction; centrifugal stress | **Amplified Surge**: Elemental medium energized |
| **Transit Facing (Twilight)** | $31^\circ \le \theta \le 149^\circ$ | **Harmonic Baseline**: Stable, predictable radiant output | **Harmonic Baseline**: Steady shadow tendrils, dim cover stealth | **Harmonic Baseline**: Smooth gear train synchronization | **Harmonic Baseline**: Safe, balanced energy usage |
| **Shadow Facing (Nadir)** | $150^\circ \le \theta \le 180^\circ$ | **Eclipse Lock**: Zero beam generation; armor lock | **Apex Surge**: Full rock/hull phase-shift; frost exhaustion | **Mechanical Drag**: High friction; manual flywheel crank | **Inertial Focus**: Cold stability; auxiliary power only |
| **Deep-Space Transit** | Outside Atmosphere | **2x Power Amplification** / **2x Control Difficulty** (Missteps risk hull breaches & shield failure) | | | |
| **Gateway Subspace** | Inside Wormholes | **Neutral Baseline** ($Re = 0.5$, Wavefront disconnected, standard kinetics) | | | |

---

## 3. Spatial Sectors, Waypoints & Cross-Book Ripple Effects

- **Coordinate System**: 3D Sector Coordinates $[X, Y, Z]$.
- **Location Types (`Loc_Type`)**: `SURFACE` (axial day/night spin), `ORBITAL` (rapid orbital revolution), `DEEP_SPACE_TRANSIT` (vector heading towards destination), `GATEWAY_SUBSPACE` (wormhole conduit).
- **Cross-Book Ripple Hazards**:
  - Cosmic disruptions (stellar flares, beacon pulses, stargate collapses) logged via `cosmic_event_bus.py` project an environmental hazard radius ($d = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2} \le R_{blast}$).
  - Any traveling starship or planetary base within the influence radius automatically experiences environmental turbulence in its next chapter.

---

## 4. 74-Book Architecture & Faction Catalog

- **30 Core Faction Books**:
  - `Book 01` – `Book 10`: The Sun-Forged Hegemony (10 radiant heroes across desert worlds, solar observatories, radiant cruisers).
  - `Book 11` – `Book 20`: The Void-Bound Monks (10 shadow heroes across shadow moons, eclipse chasms, stealth frigates).
  - `Book 21` – `Book 30`: The Astrolabe Engineers (10 gear-crafters across gear-cities, orbital stations, deep-space rigs).
- **44 Expansion Faction Books**:
  - `Book 31` – `Book 74`: Comet-Riders, Nebula-Weavers, Deep-Core Miners, Gravity-Surfers, Chrono-Navigators, Plasma-Shepherds, Bio-Alchemists, Crystal-Singers, Tide-Wardens, Magnetar-Leapers, and more (governed by `faction_matrix.py`).

---

## 5. Round-Robin Chapter Generation Protocol

Strict rotation loop:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \to \text{[Book 02, Ch 2]} \dots$$

### 1-Command Chapter Authoring Pipeline:
1. **Prepare Chapter Stub**:
   ```bash
   python .agents/skills/confluence-chapter-authoring/scripts/chapter_engine.py prepare
   ```
2. **Draft Prose**: Write vivid chapter in `01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md`.
3. **Audit Prose Quality**:
   ```bash
   python .agents/skills/confluence-chapter-authoring/scripts/chapter_prose_evaluator.py --file "01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md"
   ```
4. **Complete & Propagate State**:
   ```bash
   python .agents/skills/confluence-chapter-authoring/scripts/chapter_engine.py complete --synopsis "<1-2 sentence summary>" --gut-delta 1
   ```

---

## 6. Directory Structure & State Files

```
The Stellar Confluence Universe/
├── 00_System_State/
│   ├── rotation_tracker.md        <-- Active book #, chapter #, current GUT, and next queue position
│   ├── cosmic_clockwork.md        <-- Real-time GUT, Loc_Type, Facing Angles & Resonance Constraints
│   ├── character_registry.md      <-- Index of all 74 books, titles, heroes, factions & worlds
│   ├── cosmic_events.json         <-- Active spatial ripple hazards & beacon pulses
│   ├── character_arcs.json        <-- Dynamic inventory, wounds & cross-book bonds
│   ├── universe_dashboard.html    <-- Interactive visual HTML/SVG galactic radar & timeline
│   └── diary.md                   <-- Execution log of every completed chapter
├── 01_Books_Library/
│   └── Book_XX_[Title_Slug]/
│       └── Book_XX_Chapter_YY.md
├── 2026-08-12 Wed 1134 Prompt-Response Flow/
│   └── 2026-08-12 Wed 1149 Prompt-Response Flow.md
├── progress tracking/
│   ├── version_registry.json
│   ├── Version_Registry.md
│   └── YYYY-MM-DD_HHMM_Description.md
└── .agents/
    ├── AGENTS.md
    └── skills/
        ├── confluence-chapter-authoring/
        ├── universe-state-manager/
        ├── document-now/
        ├── prompt-response-flow/
        └── world-engine-audit/
```

---

## 7. Progress Tracking Rule ("Document Now")

Whenever the developer states **"document now"**, **"document progress"**, or requests a checkpoint:
1. Refer to and execute `document-now` ([SKILL.md](file:///c:/Users/ignaz/OneDrive/Documents/Projects/2026-05-03%201325%20Syncthing%20Books/2026-05-20%20Wed%202132%20Syncthing%20Gateway/Projects/2026-08-12%20Wed%201113%20The%20Stellar%20Confluence%20Universe/.agents/skills/document-now/SKILL.md)).
2. Acquire system timestamp via `get_timestamp.py`.
3. Check Ndebele codename uniqueness from the 100+ lexicon (`version_registry.py check <codename>`).
4. Write `progress tracking/YYYY-MM-DD_HHMM_Description.md` (with 10-year-old child explanation & next steps, and Peter Dube + Antigravity attributions).
5. Register version (`version_registry.py register ...`).
6. Stage all changes (`git add .`) and commit: `YYYY-MM-DD Day HHMM: [Title] ([Codename] [Version])`.

---

## 8. Automated Diagnostics Rule ("Self-Test")

Whenever testing system health or before major release commits:
```bash
python .agents/skills/world-engine-audit/scripts/agent_self_test.py
```
*(Runs 15 automated sanity checks across all 5 skills and verified 100% PASS)*
