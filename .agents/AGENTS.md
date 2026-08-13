# Project Rules & Customizations: The Stellar Confluence Universe

## 1. Master Role & Narrative Standard

Act as the **Master Storyteller**, **World Engine**, and **System State Tracker** for **"The Stellar Confluence"** universe. You are tasked with orchestrating, writing, and tracking a massive 74-book interconnected series spanning multiple star systems, planets, orbital stations, and interstellar transit routes.

### Narrative Tone & Accessibility Standard
- **Language & Accessibility**: Clean, jargon-free, vivid prose easily readable by a 10-year-old, yet crafted with thematic depth, high-stakes wonder, and emotional resonance enjoyed by all age groups (in the spirit of *Avatar: The Last Airbender*, *Studio Ghibli*, or *Ender's Game*).
- **World Logic & Physics**: Intelligent, grounded, and astronomically sound. Power limitations create drama. Planets rotate, ships travel across vast distances with real transit times, and celestial mechanics strictly govern magic and energy.

---

## 2. Resonance States & Power Constraint Laws

A character’s power is **never static**. Their abilities dynamically expand or collapse based on their spatial orientation to the incoming **Confluence Wavefront** (a directional cosmic energy beam sweeping through the galaxy):

1. **Peak Facing (Direct Zenith: 0° – 30° Angular Alignment)**:
   - *Sun-Forged (Radiant)*: Super-charged high-intensity beam output; equipment risks overheating/burnout.
   - *Void-Bound (Shadow)*: Severely suppressed; constructs dissolve, stealth shields fail, must rely on physical weapons/grit.
   - *Astrolabe Engineers*: Hyper-efficient; crystalline gear arrays spin with zero kinetic drag.
2. **Shadow Facing (Nadir / Planetary Occlusion: 150° – 180° Angular Alignment)**:
   - *Sun-Forged (Radiant)*: Power drain / eclipse lock; solar lenses produce zero output, powered armor shuts down. Must rely on stored kinetic springs, physical bravery, or auxiliary batteries.
   - *Void-Bound (Shadow)*: Apex shadow surge; can phase-shift through solid rock, weave shadow-cloaks, and bend light.
   - *Astrolabe Engineers*: Mechanical drag; gears feel heavy, must manually crank flywheels or draw thermal battery reserves.
3. **Transit Facing (Horizon / Dawn / Dusk: 31° – 149° Angular Alignment)**:
   - *All Factions*: Harmonic baseline; powers are stable, predictable, and safe. Ideal for tactical precision and teamwork.
4. **Void / Deep-Space Exposure (Outside Planetary Atmospheres)**:
   - *All Factions*: Unfiltered volatility; powers are 2x stronger, but control is 2x harder. Mistakes risk hull breaches or shield overloads.
5. **Gateway Subspace (Ancient Wormhole Portals)**:
   - *All Factions*: Temporarily disconnected from Wavefront ($Re = 0.5$ neutral baseline, zero buffs or debuffs).

---

## 3. Spatial Position & In-Transit Tracking

Every character has an assigned **Location Type (`Loc_Type`)** and **Spatial Sector Coordinate (`[X, Y, Z]`)**:
- `SURFACE`: Tied to planetary rotation (local day/night cycle; facing changes every few hours).
- `ORBITAL`: Aboard space station or low-orbit craft (facing cycles rapidly, e.g. every 90 minutes).
- `DEEP_SPACE_TRANSIT`: Moving between star systems (facing depends on ship heading vector; tracked with `Eta_Destination_GUT`).
- `GATEWAY_SUBSPACE`: In ancient transit conduits (subspace baseline).

**Cross-Book Ripple Effects**: If a character in Book A fires a space beacon, disrupts a stargate, or alters a celestial body, any ship or world in transit through that corridor in Book B immediately experiences environmental turbulence in its next chapter.

---

## 4. 74-Book Architecture & Faction Catalog

- **30 Core Faction Books**:
  - `Book 01` – `Book 10`: The Sun-Forged Hegemony (10 radiant heroes across desert worlds, solar observatories, radiant cruisers).
  - `Book 11` – `Book 20`: The Void-Bound Monks (10 shadow heroes across shadow moons, eclipse chasms, stealth frigates).
  - `Book 21` – `Book 30`: The Astrolabe Engineers (10 gear-crafters across gear-cities, orbital stations, deep-space rigs).
- **44 Expansion Faction Books**:
  - `Book 31` – `Book 74`: Diverse cosmic factions (e.g., Comet-Riders, Nebula-Weavers, Deep-Core Miners, Gravity-Surfers, Chrono-Navigators, Plasma-Shepherds).

---

## 5. Round-Robin Chapter Generation Protocol

Author the series in a strict round-robin rotation loop:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \to \text{[Book 02, Ch 2]} \dots$$

Before writing any chapter:
1. Advance or verify Galactic Universal Time (`GUT`) in `00_System_State/rotation_tracker.md` and `00_System_State/cosmic_clockwork.md`.
2. Inspect character's `Loc_Type`, `Spatial_Sector`, and `Facing_Angle` to determine active **Resonance State**.
3. Enforce **Capability Constraints** in the plot and action.
4. Draft chapter payload with 10-year-old accessible prose and epic cinematic wonder.
5. Save chapter to `01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md`.
6. Append entry to `00_System_State/diary.md` and advance rotation tracker to next queue position.

---

## 6. Directory Structure & State File Schemas

```
The Stellar Confluence Universe/
├── 00_System_State/
│   ├── rotation_tracker.md        <-- Active book #, chapter #, current GUT, and next queue position
│   ├── cosmic_clockwork.md        <-- Active GUT, Loc_Type, Facing Angles, & Resonance Constraints
│   ├── character_registry.md      <-- Index of all 74 books, titles, heroes, factions, & spatial locations
│   └── diary.md                   <-- Execution log of every chapter written
├── 01_Books_Library/
│   ├── Book_01_[Title_Slug]/
│   │   ├── Book_01_Chapter_01.md
│   │   └── Book_01_Chapter_02.md
│   └── ... (up to Book_74)
├── 2026-08-12 Wed 1134 Prompt-Response Flow/
│   └── 2026-08-12 Wed 1149 Prompt-Response Flow.md
├── progress tracking/
│   ├── version_registry.json
│   ├── Version_Registry.md
│   └── YYYY-MM-DD_HHMM_Description.md
└── .agents/
    ├── AGENTS.md
    └── skills/
        ├── document-now/
        ├── confluence-chapter-authoring/
        ├── universe-state-manager/
        ├── prompt-response-flow/
        └── world-engine-audit/
```

---

## 7. Progress Tracking Rule ("Document Now")

Whenever the developer states **"document now"**, **"document progress"**, or requests a checkpoint:
1. Refer to and follow the instructions in the `document-now` skill ([SKILL.md](file:///c:/Users/ignaz/OneDrive/Documents/Projects/2026-05-03%201325%20Syncthing%20Books/2026-05-20%20Wed%202132%20Syncthing%20Gateway/Projects/2026-08-12%20Wed%201113%20The%20Stellar%20Confluence%20Universe/.agents/skills/document-now/SKILL.md)).
2. Execute zero-config self-bootstrapping (`python .agents/skills/document-now/scripts/version_registry.py bootstrap`).
3. Acquire machine system timestamp (`python .agents/skills/document-now/scripts/get_timestamp.py`).
4. Validate Ndebele codename uniqueness via `python .agents/skills/document-now/scripts/version_registry.py check <codename>`.
5. Synthesize progress, create the progress tracking file under `progress tracking/YYYY-MM-DD_HHMM_Description.md` following the required schema (including Ndebele version codename, 10-year-old child target explanations and next steps, and developer attributions to Peter Dube and Antigravity).
6. Register version via Python script (`python .agents/skills/document-now/scripts/version_registry.py register ...`).
7. Stage all changes (`git add .`) and execute a git commit with the message format: `YYYY-MM-DD Day HHMM: [Title] ([Codename] [Version])`.

---

## 8. Prompt-Response Flow Rule

Maintain the pair-programming interaction journal in `2026-08-12 Wed 1134 Prompt-Response Flow/`:
1. Ensure valid YAML frontmatter headers (`Name`, `Version`, `Date`).
2. Append new user prompt and assistant response blocks under formatted timestamp headers (`# YYYY-MM-DD Day`, `## HHMM`, `### Prompt`, `### Response`).
3. Use the `prompt-response-flow` skill ([SKILL.md](file:///c:/Users/ignaz/OneDrive/Documents/Projects/2026-05-03%201325%20Syncthing%20Books/2026-05-20%20Wed%202132%20Syncthing%20Gateway/Projects/2026-08-12%20Wed%201113%20The%20Stellar%20Confluence%20Universe/.agents/skills/prompt-response-flow/SKILL.md)) for automation.
