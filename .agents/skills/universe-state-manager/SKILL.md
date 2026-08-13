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
- Managing in-transit starships, waypoint ETAs, or cross-book environmental disruptions: `"sync transit"` or `"update ephemeris"`.

---

## 2. Core State Files Architecture

The universe state resides in `00_System_State/`:

1. **`00_System_State/character_registry.md`**:
   - Master index of all 74 books, titles, primary protagonists, factions (30 Core: Sun-Forged 1-10, Void-Bound 11-20, Astrolabe 21-30; 44 Expansion 31-74), home worlds/vessels, location types, and starting coordinates.
2. **`00_System_State/cosmic_clockwork.md`**:
   - Ephemeris ledger tracking current Galactic Universal Time (GUT), spatial sector coordinates `[X, Y, Z]`, facing angle $\theta$, active resonance state, and specific power capabilities/limitations.
3. **`00_System_State/rotation_tracker.md`**:
   - Round-robin queue controller: Active Book Index (1 - 74), Active Chapter Number (1 - N), Current GUT, and Next in Queue.
4. **`00_System_State/diary.md`**:
   - Append-only execution log of all completed chapters with timestamps and synopses.

---

## 3. Automation Scripts & Tools

### Bootstrap State
Initialize or regenerate the full 74-book state structure:
```bash
python .agents/skills/universe-state-manager/scripts/bootstrap_universe_state.py
```
*(Use `--force` to overwrite existing files, or `--dry-run` to preview).*

### Audit State Integrity
Run full diagnostics on state files and chapter library:
```bash
python .agents/skills/universe-state-manager/scripts/audit_universe_state.py
```

---

## 4. In-Transit Synchronization Rules

When a character departs a planet or station to travel across interstellar space:
1. Update their status in `cosmic_clockwork.md`:
   - Set `Loc_Type: DEEP_SPACE_TRANSIT`.
   - Compute `Eta_Destination_GUT` = Current GUT + Transit Duration.
2. Calculate their facing angle based on the starship's flight vector relative to the Confluence Wavefront beam.
3. Apply the **Deep-Space Exposure Rule**: Powers are 2x amplified in magnitude, but control is 2x more difficult; mistakes risk hull fractures.
4. **Cross-Book Environmental Ripple Effect**: If a character in another book fires a high-energy stellar beacon or destabilizes a gateway along that sector corridor, log the turbulence immediately into the traveling ship's next chapter.
