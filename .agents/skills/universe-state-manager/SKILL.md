---
name: universe-state-manager
description: Bootstraps, manages, and audits the core universe state tracking files (character registry, cosmic clockwork ephemeris, rotation tracker, and chapter diary) across all 74 books.
---

# Universe State Manager Skill

This skill provides comprehensive management, synchronization, and verification procedures for the **00_System_State/** directory in **The Stellar Confluence Universe**.

---

## 1. Trigger Conditions

Activate this skill when:
- Initializing a new workspace or restoring state files: `"bootstrap universe state"` or `"initialize state"`.
- Auditing universe integrity: `"audit state"`, `"check universe health"`, or `"verify rotation consistency"`.
- Managing in-transit starships, waypoint ETAs, or logging cross-book environmental disruptions: `"sync transit"`, `"log cosmic event"`, or `"check hazards"`.

---

## 2. Dynamic Ephemeris & Cosmic Event Bus

### Dynamic Ephemeris Engine (`cosmic_ephemeris_engine.py`)
Computes astronomical time propagation across all 74 storylines:
- **`SURFACE`**: Planetary axial spin ($\omega_{rot} = 15^\circ / GUT$, 24 GUT full rotation).
- **`ORBITAL`**: Rapid orbital transit ($\omega_{orb} = 60^\circ / GUT$, 6 GUT full orbit).
- **`DEEP_SPACE_TRANSIT`**: Vector heading towards destination sector; automatic orbital transition upon arrival.
- **`GATEWAY_SUBSPACE`**: Wavefront-disconnected neutral stasis ($Re = 0.5$).

```bash
# Propagate ephemeris by N ticks and save
python .agents/skills/universe-state-manager/scripts/cosmic_ephemeris_engine.py --current-gut <GUT> --advance-by <N> --save
```

### Cosmic Event Bus (`cosmic_event_bus.py`)
Records stellar flares, gateway collapses, or beacon pulses, calculating spatial ripple effects on nearby ships and worlds:

```bash
# Log a new cosmic event
python .agents/skills/universe-state-manager/scripts/cosmic_event_bus.py log \
  --type BEACON_PULSE \
  --source "Book 04" \
  --sector "[15, 6, 0]" \
  --radius 5.0 \
  --start-gut 100 \
  --duration 10 \
  --desc "High-intensity solar flare pulse radiating through Sector [15, 6, 0]"

# Check active hazards for any character's sector
python .agents/skills/universe-state-manager/scripts/cosmic_event_bus.py check --sector "[12, 5, 1]" --gut 105
```

---

## 3. Bootstrapping & Diagnostics

### Bootstrap 74-Book Universe Roster
```bash
python .agents/skills/universe-state-manager/scripts/bootstrap_universe_state.py
```

### Audit System State Integrity
```bash
python .agents/skills/universe-state-manager/scripts/audit_universe_state.py
```
