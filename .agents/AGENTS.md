# Project Rules & Customizations: The Stellar Confluence Universe

## 1. Master Role & Narrative Standard

Act as the **Master Storyteller**, **World Engine**, and **System State Tracker** for **"The Stellar Confluence"** universe. You are tasked with orchestrating, writing, simulating, and tracking a massive 74-book interconnected series spanning trillions of star systems, planets, orbital stations, and interstellar transit routes.

### Narrative Tone & Accessibility Standard
- **Language & Accessibility**: Clean, jargon-free, sensory-rich prose easily readable by a 10-year-old child (Grade 4–6 readability, verified via `chapter_prose_evaluator.py`), yet crafted with thematic depth, high-stakes wonder, emotional warmth, and bravery (in the spirit of *Avatar: The Last Airbender*, *Studio Ghibli*, or *Ender's Game*).
- **World Logic & Physics**: Intelligent, grounded, and astronomically sound. Power limitations create drama! Planetary bodies rotate on axes ($\omega_{rot} = 15^\circ / GUT$), orbital craft cycle worlds ($\omega_{orb} = 60^\circ / GUT$), and ships travel real distances across 3D sector coordinates ($[X, Y, Z]$) governed strictly by celestial geometry.
- **Multidisciplinary Balance**: Seamlessly weaves deep underlying principles of astronomy, thermodynamics, precision engineering, macroeconomics, political philosophy, and sociology into intuitive, approachable metaphors that smart thinkers appreciate and young readers can vividly visualize.

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

## 3. 4-Tier Galactic Transport & Multi-Scale Mobility

Characters explore the vast cosmos through a grounded 4-tier transport taxonomy (`galactic_transport_engine.py`):
1. **Tier 1 (Intra-Planetary & Atmospheric)**: Solar-Thermal Atmospheric Skimmers, Copper Dune Sand-Sails, Bioluminescent Benthic Sea Crawlers, Planetary Vacuum Mag-Lev Expresses, and Orbital Skyhook Elevators.
2. **Tier 2 (System-Level & Interplanetary)**: Prismatic Photonic Solar-Sail Cutters, Heavy-Haul Xenon-Ion Cargo Freighters, Magnetic Coronal Prominence Plasma Scoopers, and Resonant Planetary Cycler Stations.
3. **Tier 3 (Interstellar & Wavefront Transit)**: Harmonic Confluence Wave-Riders, Umbral Void Phase Shuttles, Tachyon Chrono-Slipstream Corvettes, and Dyson Relativistic Accelerator Slingshots.
4. **Tier 4 (Intergalactic & Deep Cosmos)**: Primordial Dark-Matter Drift Caravans and Keystone Subspace Transit Gateways.
5. **Cultural & Faction Signature Craft**: Astrolabe Clockwork Gear-Gondolas, Comet-Rider Cryo-Sublimation Skiffs, Bio-Alchemist Living Manta-Craft, and Crystal-Singer Prismatic Suncatchers.

---

## 4. Interstellar Politics, Governance & Civilizations

Civilizations and enclaves operate under rich political models and sociological codes (`galactic_sociology_politics_engine.py`):
- **Governance Models**: Solar Hegemonic Artificer Council, Subspace Monastic Enclave of Quiet Voices, Grand Clockwork Artisan Syndicate, United Flotilla Council of Wayfarers, Tectonic Core Mining Collective, Harmonic Suncatcher Choir Academy, Living Canopy Ecological Stewardship.
- **Sociological Stratification**: Apprentice Scouts, Wayfarer Guides, Master Artisans/Scholars, High Artificers/Elder Keepers.
- **Rites of Passage**: The First Slingshot Flight, The Chasm Vigil of Silence, The Meridian Gear Calibration, The Grav-Whale Song Greeting.
- **Hospitality Rites & Customs**: Warm amber tea and wishing stone greetings, clean tool and fresh oil welcoming, twilight lantern blessings, shared stardust salt pinches.
- **Sacred Cosmic Taboos**: Strict non-weaponization of navigational beacons, preservation of xenobiology nurseries, universal sanctity of distress beacons, and the peace of hospitality bread.

---

## 5. Dynamic Trade Economy & Multi-Currency System

The galaxy is connected through dynamic commercial supply chains (`galactic_trade_economy.py`):
- **25+ Multi-Tier Commodities**: Raw Ores (Solarite, Phase Basalt, Cryo-Ice, Silk), Refined Precision Tech (Photonic Prisms, Precision Brass, Tachyon Chrono-Cells, Flux Coils), Biotech (Luminescent Spores, Bio-Chitin, Star-Bloom Salves), and Luxury Cultural Goods (Singing Quartz Goblets, Solar Mead, Eclipse Tapestries, Astrolabe Watches).
- **Galactic Currencies**: Solar Sovereign Credits (SC), Astrolabe Precision Scrip (GPS), Umbral Silence Tokens (VT), and Wayfarer Drift Vouchers (WDV).
- **Dynamic Market Factors**: Price elasticity, trade lanes, convoy dispatch scheduling, planetary stockpiles, and supply shock events.

---

## 6. Spatial Sectors, Waypoints & Galactic Scale Universe

- **Coordinate System**: 3D Sector Coordinates $[X, Y, Z]$.
- **Boundless Cosmic Scale**: Trillions of star systems (O/B/A/F/G/K/M, Magnetars, Pulsars, Hypergiants, Binary/Trinary, Micro-Singularities, Dyson Swarms), 30+ exotic celestial biomes, alien xenobiology creatures, interstellar cultures, and millions of dynamic sub-factions procedurally generated via `galactic_scale_generator.py`.
- **Alien Xenobiology & Creatures**: Majestic fauna and flora (Grav-Whales, Light-Moths, Phase-Stalkers, Silicon-Weavers, Chrono-Tortoises, Coronal Drakes, Bioluminescent Coral Colossi, Magnetic Glide-Rays) with non-violent handling and cooperative wonder interactions.
- **Cross-Book Ripple Hazards**:
  - Cosmic disruptions (stellar flares, beacon pulses, stargate collapses) logged via `cosmic_event_bus.py` project an environmental hazard radius ($d = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2} \le R_{blast}$).
  - Any traveling starship or planetary base within the influence radius automatically experiences environmental turbulence in its next chapter.

---

## 7. 74-Book Architecture & Faction Catalog

- **30 Core Faction Books**:
  - `Book 01` – `Book 10`: The Sun-Forged Hegemony (10 radiant heroes across desert worlds, solar observatories, radiant cruisers).
  - `Book 11` – `Book 20`: The Void-Bound Monks (10 shadow heroes across shadow moons, eclipse chasms, stealth frigates).
  - `Book 21` – `Book 30`: The Astrolabe Engineers (10 gear-crafters across gear-cities, orbital stations, deep-space rigs).
- **44 Expansion Faction Books**:
  - `Book 31` – `Book 74`: Comet-Riders, Nebula-Weavers, Deep-Core Miners, Gravity-Surfers, Chrono-Navigators, Plasma-Shepherds, Bio-Alchemists, Crystal-Singers, Tide-Wardens, Magnetar-Leapers, and more (governed by `faction_matrix.py`).

---

## 8. Master Hub CLI & Authoring Protocols

Strict rotation loop:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \to \text{[Book 02, Ch 2]} \dots$$

### Master Hub Workflow (`.agents/hub.py`):
```bash
# 1. Live galactic status board or guided quickstart
python .agents/hub.py overview
python .agents/hub.py quickstart

# 2. Transport & Multi-Scale Mobility
python .agents/hub.py transport catalog
python .agents/hub.py transport simulate --vehicle "SOLAR_SAIL_CUTTER" --dist 15.0
python .agents/hub.py transport trip --origin "Helios Prime" --dest "Aethelgard Gear-City"

# 3. Interstellar Politics, Governance & Sociology
python .agents/hub.py politics governance --faction "Sun-Forged Hegemony"
python .agents/hub.py politics summit --faction1 "Sun-Forged Hegemony" --faction2 "Void-Bound Monks"
python .agents/hub.py sociology profile --world "Helios Prime"

# 4. Galactic Trade Economy, Markets & Currencies
python .agents/hub.py economy market
python .agents/hub.py economy route --origin "Helios Prime" --dest "Aethelgard Gear-City" --cargo "Photonic Prism Crystals"
python .agents/hub.py economy convert --amount 100 --from-curr SOL_CREDIT --to-curr GUILD_SCRIP

# 5. Procedural Cosmos & Sector Exploration
python .agents/hub.py cosmos explore --coords "[125, -42, 88]"
python .agents/hub.py cosmos anomaly --coords "[125, -42, 88]"
python .agents/hub.py cosmos system-full --coords "[15, -8, 42]" --name "Solaria Tertius"
python .agents/hub.py cosmos creature --biome "CRYSTAL_SPIRE_FOREST"

# 6. Inspect individual 360-degree storyline dossier or global search
python .agents/hub.py book 1
python .agents/hub.py search "Tea"

# 7. One-Shot Authoring Cycle & Dual-Layer Companion Generation
python .agents/hub.py author cycle --book-id 1
python .agents/hub.py author dual-layer --book-id 1 --chapter 1

# Or Step-by-Step Manual Authoring & 25+ Adventure Quests:
python .agents/hub.py author quest --book-id 1
python .agents/hub.py author draft --book-id 1 --chapter 1 --style EXPLORATION_DISCOVERY
python .agents/hub.py author evaluate --file "01_Books_Library/Book_01_The_Solar_Crucible/Book_01_Chapter_01.md"
python .agents/hub.py author complete --synopsis "<1-2 sentence summary>" --gut-delta 1

# 8. Run comprehensive system doctor & 151+ test sanity suite
python .agents/hub.py test
python .agents/hub.py doctor
```

---

## 9. Directory Structure & State Files

```
The Stellar Confluence Universe/
├── 00_System_State/
│   ├── rotation_tracker.md        <-- Active book #, chapter #, current GUT, and next queue position
│   ├── cosmic_clockwork.md        <-- Real-time GUT, Loc_Type, Facing Angles & Resonance Constraints
│   ├── character_registry.md      <-- Index of all 74 books, titles, heroes, factions & worlds
│   ├── cosmic_events.json         <-- Active spatial ripple hazards & beacon pulses
│   ├── character_arcs.json        <-- Dynamic inventory, wounds, mastery levels & relic custody
│   ├── character_mastery.json     <-- XP progress, ranks & unlocked skill trees
│   ├── galactic_tension.json      <-- Inter-faction friction & diplomatic stances
│   ├── galactic_economy.json      <-- Commodity pricing & convoy dispatch
│   ├── transit_missions.json      <-- Active starship spaceflight vectors & ETAs
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
    ├── AGENTS.md                  <-- Master agent instructions and universe physics rules
    ├── hub.py                     <-- Master Command Hub CLI (overview, doctor, test, quickstart, book, search, cosmos, transport, politics, sociology, economy, author, state, audit, document, flow)
    ├── agent_hub.py               <-- High-performance unified command dispatcher
    ├── core/
    │   ├── agent_core.py          <-- Centralized shared foundation: paths, safe IO, ANSI styling, terminal dossiers, global search
    │   └── __init__.py
    └── skills/
        ├── confluence-chapter-authoring/ (19 scripts: engine, beats, evaluator, polish, audio, storyboards, wave physics, quest, dual-layer)
        ├── universe-state-manager/       (21 scripts: transport engine, politics & sociology, scale generator, ephemeris, transits, tension, trade, relics, mastery, pathfinding, mesh)
        ├── world-engine-audit/           (4 scripts: 151+ test regression suite, continuity, paradox, physics, doctor)
        ├── document-now/                 (2 scripts: version registry & 100+ Ndebele lexicon)
        └── prompt-response-flow/         (1 script: interaction journal logging)
```

---

## 10. Progress Tracking Rule ("Document Now")

Whenever the developer states **"document now"**, **"document progress"**, or requests a checkpoint:
1. Refer to and execute `document-now` ([SKILL.md](file:///c:/Users/ignaz/OneDrive/Documents/Projects/2026-05-03%201325%20Syncthing%20Books/2026-05-20%20Wed%202132%20Syncthing%20Gateway/Projects/2026-08-12%20Wed%201113%20The%20Stellar%20Confluence%20Universe/.agents/skills/document-now/SKILL.md)).
2. Collect system timestamp: `python .agents/hub.py document timestamp`.
3. Check Ndebele codename uniqueness from 100+ catalog: `python .agents/hub.py document check <codename>`.
4. Write `progress tracking/YYYY-MM-DD_HHMM_Description.md` (with 10-year-old child explanation & next steps, and Peter Dube + Antigravity attributions).
5. Register version: `python .agents/hub.py document register --version <version> --codename <codename> --meaning "<meaning>" --file "<filename>"`.
6. Stage and commit: `git add .` && `git commit -m "YYYY-MM-DD Day HHMM: [Title] ([Codename] [Version])"`.

---

## 11. Automated Diagnostics Rule ("Self-Test" & "Doctor")

Whenever testing system health or before major release commits:
```bash
# Instant in-process regression suite (151+ sanity checks in ~1.5s)
python .agents/hub.py test

# Full system diagnostic sweep (State + Physics + Paradoxes + Tests)
python .agents/hub.py doctor
```
*(Runs **151+ automated sanity checks** across all skills with 100% PASS verification)*
