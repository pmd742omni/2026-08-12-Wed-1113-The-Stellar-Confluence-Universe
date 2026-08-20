---
name: universe-state-manager
description: Bootstraps, synchronizes, and audits the core universe state tracking files (character registry, cosmic clockwork ephemeris, rotation tracker, transit missions, trade economy, geopolitical tension, character mastery, relics ledger, route pathfinding, mesh network, transport engine, politics and sociology, and interactive visual dashboard) across all 74 books.
---

# Universe State Manager Skill

This skill provides the comprehensive backend state engine, celestial physics simulator, interplanetary transport mobility, multi-tier trade economy, politics, and sociology tracking systems for **The Stellar Confluence Universe** (`00_System_State/`).

---

## 1. Quick Master Hub Commands

Manage universe state directly via the unified master CLI hub (`.agents/hub.py`):

```bash
# 1. Inspect complete 360-degree storyline dossier card
python .agents/hub.py book 1

# 2. Global galactic search across all storylines, vehicles, relics, transits & inventory
python .agents/hub.py search "Skimmer"

# 3. Galactic Transport & Mobility
python .agents/hub.py transport catalog
python .agents/hub.py transport simulate --vehicle "SOLAR_SAIL_CUTTER" --dist 15.0

# 4. Interstellar Politics, Governance & Treaties
python .agents/hub.py politics governance --faction "Sun-Forged Hegemony"
python .agents/hub.py politics treaties --faction1 "Sun-Forged Hegemony" --faction2 "Astrolabe Engineers"

# 5. Interstellar Sociology, Traditions & Rites
python .agents/hub.py sociology profile --world "Helios Prime"
python .agents/hub.py sociology interaction --faction1 "Sun-Forged Hegemony" --faction2 "Void-Bound Monks"

# 6. Trade Economy & Multi-Currency System
python .agents/hub.py economy market
python .agents/hub.py economy convert --amount 100 --from-curr SOL_CREDIT --to-curr GUILD_SCRIP
python .agents/hub.py economy dispatch --origin "Helios Prime" --dest "Aethelgard Gear-City" --cargo "Photonic Prism Crystals" --tonnage 500

# 7. Full universe state, continuity, and physics audit
python .agents/hub.py state audit

# 8. Plan 3D interstellar routes & gateway conduits
python .agents/hub.py state route --origin "[10, 5, 0]" --destination "[-12, 4, 2]"

# 9. Query character relationships, mentors, rivals & comms mesh
python .agents/hub.py state mesh --book-id 1

# 10. Inspect or update character inventory, wounds & conditions
python .agents/hub.py state arcs --book-id 1
python .agents/hub.py state arcs --book-id 1 --add-item "Prism Key" --desc "Unlocks Sun Vault"

# 11. Extract cross-book lore callbacks & recurring motifs
python .agents/hub.py state lore --book-id 1

# 12. Check or adjust inter-faction diplomatic tension
python .agents/hub.py state tension --faction1 "Sun-Forged Hegemony" --faction2 "Void-Bound Monks"

# 13. Award character XP and inspect mastery progression
python .agents/hub.py state mastery --book-id 1 --award-xp 150 --achievement "Calibrated Oasis Lens"

# 14. Propagate in-transit starship missions & ephemeris
python .agents/hub.py state transit
python .agents/hub.py state ephemeris --current-gut 100 --target-gut 101 --save

# 15. Generate live SVG galactic radar & visual HTML studio dashboard
python .agents/hub.py state dashboard

# 16. Multi-book cross-state synchronization check
python .agents/hub.py state sync
```

---

## 2. Complete Universe State Toolchain Catalog

### A. Transport Mobility, Ephemeris & Spaceflight
1. **`galactic_transport_engine.py` / `hub.py transport`**:
   - 4-Tier Galactic Transport Taxonomy (Intra-Planetary, System-Level, Interstellar, Intergalactic, and Cultural Craft).
   - Computes propulsion type, velocity profiles, fuel/resonance demands, travel duration in GUT, and pilot sensory cockpit experiences.
2. **`cosmic_ephemeris_engine.py` / `hub.py state ephemeris`**:
   - Propagates astronomical time across all 74 storylines based on celestial geometry:
     - `SURFACE`: Planetary axial spin ($\omega_{rot} = 15^\circ / GUT$, 24 GUT full cycle).
     - `ORBITAL`: Orbital revolution ($\omega_{orb} = 60^\circ / GUT$, 6 GUT full orbit).
     - `DEEP_SPACE_TRANSIT`: Linear vector progression towards destination sector coordinates.
     - `GATEWAY_SUBSPACE`: Neutral baseline stasis ($Re = 0.5$, Wavefront disconnected).
3. **`galactic_navigator.py` / `hub.py state route`**:
   - 3D Euclidean and subspace pathfinding engine. Evaluates direct deep-space transit vs ancient gateway conduit shortcuts.
4. **`interstellar_transit_engine.py` / `hub.py state transit`**:
   - Starship mission tracker managing departures, vectors, velocities, remaining ticks, and automatic docking.
5. **`cosmic_event_bus.py` / `hub.py state hazards`**:
   - Dynamic environmental disruption ledger logging stellar flares, gateway collapses, and beacon pulses.

---

### B. Politics, Sociology, Trade & Character Progression
6. **`galactic_sociology_politics_engine.py` / `hub.py politics` & `hub.py sociology`**:
   - Governance models (Solar Hegemony, Monastic Enclaves, Clockwork Syndicates, Flotilla Parliaments, Deep-Core Collectives, Crystal Choirs, Bio-Communes).
   - Sociological stratification (Apprentice, Wayfarer, Master, High Artificer), rites of passage, hospitality customs, sacred cosmic taboos, and architectural philosophies.
7. **`galactic_trade_economy.py` / `hub.py economy`**:
   - 25+ commodities across 4 tiers, multi-currency valuation (Sol-Credits, Guild Scrip, Void-Tokens, Flotilla Vouchers), price elasticity, convoy scheduling, and planetary stockpiles.
8. **`galactic_tension_tracker.py` / `hub.py state tension`**:
   - Inter-faction tension indices (0–100), diplomatic states (`PEACEFUL_COOPERATION`, `TRADE_COMPACT`, `BORDER_MOBILIZATION`, `TOTAL_WAR`), and conflict logs.
9. **`character_mastery_engine.py` / `hub.py state mastery`**:
   - Experience tracking, skill ranks (`Novice`, `Apprentice`, `Adept`, `Journey-Master`, `Grand Luminary`), and milestone achievements.
10. **`artifact_ledger_engine.py` / `hub.py state relics`**:
    - Ancient relic ledger tracking provenance, custody transfers, and power couplings for legendary relics.
11. **`planetary_ecology_matrix.py` / `hub.py state ecology`**:
    - Ecological, gravitational, atmospheric, transport hub, and diurnal cycle database for all 74 primary worlds.

---

### C. Communications, Lore & State Synchronization
12. **`subspace_relay_router.py` / `hub.py state relay`**:
    - 3D multi-hop signal propagation simulator with packet latency and ion storm degradation modeling.
13. **`galactic_broadcast_feed.py` / `hub.py state broadcast`**:
    - Subspace news wire and cockpit radio feed synthesizer matching current ephemeris and geopolitics.
14. **`character_mesh_graph.py` / `hub.py state mesh`**:
    - Relational network graph mapping mentors, rivals, companions, and cross-faction alliances.
15. **`character_arc_tracker.py` / `hub.py state arcs`**:
    - Hero dynamic status ledger managing inventories, conditions/wounds, and quest items.
16. **`universe_lore_indexer.py` / `hub.py state lore`**:
    - Callback indexer identifying opportunities for shared lore, locations, and crossovers.
17. **`multi_book_sync_engine.py` / `hub.py state sync`**:
    - Cross-book state synchronization validator ensuring coherence across registry, clockwork, rotation, and arcs.
18. **`generate_universe_dashboard.py` / `hub.py state dashboard`**:
    - Visual studio dashboard generator rendering `00_System_State/universe_dashboard.html`.
19. **`bootstrap_universe_state.py` / `hub.py state bootstrap`**:
    - Zero-config state initialization engine for spinning up a fresh environment.
20. **`audit_universe_state.py` / `hub.py state audit`**:
    - Core state validation verifying file integrity, table formats, and field bounds.
