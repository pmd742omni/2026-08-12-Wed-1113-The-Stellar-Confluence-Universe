---
name: world-engine-audit
description: Audits celestial mechanics, wavefront alignment vectors, power constraint compliance, multi-book continuity, narrative paradox detection, runs the master 76+ sanity regression test suite, and executes the system doctor across all 74 storylines in The Stellar Confluence Universe.
---

# World Engine Audit Skill

This skill performs physical, astronomical, multi-book lore continuity, and comprehensive system regression sanity testing for **The Stellar Confluence Universe**.

---

## 1. Quick Master Hub Commands

```bash
# 1. Execute full 76+ in-process regression and sanity test suite (<1s)
python .agents/hub.py test

# 2. Execute comprehensive system doctor (State + Physics + Paradoxes + Tests)
python .agents/hub.py doctor
# or
python .agents/hub.py audit all

# 3. Audit chapter continuity & physical constraint adherence
python .agents/hub.py audit continuity --file "01_Books_Library/Book_01_The_Solar_Crucible/Book_01_Chapter_01.md"

# 4. Audit cross-story paradoxes and timeline integrity
python .agents/hub.py audit paradox

# 5. Audit celestial physics, ephemeris bounds, and resonance compliance
python .agents/hub.py audit physics
```

---

## 2. Complete Audit Toolchain Catalog

1. **`agent_self_test.py` / `hub.py test`**:
   - Master in-process regression suite executing **76+ automated sanity checks** across all skills in under 1 second.
   - Tests timestamps, Ndebele lexicon, ephemeris propagation, event bus hazards, 3D navigation, character arcs, dashboard generation, lore callbacks, character mesh, broadcast feeds, cockpit radio, interstellar transits, relic transfers, planetary ecologies, tension tracker, mastery progression, subspace routing, trade economy, wave physics, Doppler shift, faction matrix, diplomacy, 3-act narrative blueprints, dual-hero encounters, resonance calculations, autonomous drafting, prose polishing, audiobook director scripts, storyboards, dialect profiler, manuscript compilation, prose readability (FKGL & cadence), chapter continuity, simulation loop, multi-book paradoxes, master hub dispatcher, core path bindings, safe JSON IO, ANSI styling, terminal overview generator, doctor diagnostic sweep, full physics validation, 360-degree storyline dossier cards, global galactic search (storylines, relics, inventories), child-friendly synonym suggestions, auto-simplifying prose polisher, one-shot chapter cycle, and master CLI handlers.

2. **`chapter_continuity_validator.py` / `hub.py audit continuity`**:
   - Deep chapter continuity auditor. Verifies that written prose matches metadata headers, protagonist names, homeworld settings, current resonance states, inventory items, active hazards, and power limitations.

3. **`multi_book_consistency_auditor.py` / `hub.py audit paradox`**:
   - Macro cross-story paradox auditor. Cross-references all 74 book timelines, ensuring no character occupies two locations simultaneously, verifying artifact ownership chains, checking waypoint transit timelines, and detecting timeline paradoxes.

4. **`audit_lore_physics.py` / `hub.py audit physics`**:
   - Astronomical and physics law auditor. Validates that facing angles $\theta \in [0^\circ, 180^\circ]$, rotation speeds $\omega_{rot} = 15^\circ / GUT$, orbital speeds $\omega_{orb} = 60^\circ / GUT$, resonance definitions match angular zones, and deep-space power multipliers are strictly enforced.
