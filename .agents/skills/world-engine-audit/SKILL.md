---
name: world-engine-audit
description: Audits celestial mechanics, wavefront alignment vectors, power constraint compliance, multi-book continuity, narrative paradox detection, runs the master 131+ sanity regression test suite, and executes the system doctor across all 74 storylines in The Stellar Confluence Universe.
---

# World Engine Audit Skill

This skill provides automated physics auditing, multi-book paradox detection, continuity verification, and the master **131-point in-process regression suite** for **The Stellar Confluence Universe**.

---

## 1. Quick Master Hub Commands

```bash
# 1. Instant in-process regression suite (131+ tests across all systems in ~1s)
python .agents/hub.py test

# 2. Comprehensive system doctor (State + Physics + Paradoxes + Tests)
python .agents/hub.py doctor

# 3. Chapter continuity and formatting validator
python .agents/hub.py audit continuity --file "01_Books_Library/Book_01_The_Solar_Crucible/Book_01_Chapter_01.md"

# 4. Multi-book consistency and paradox audit
python .agents/hub.py audit paradox

# 5. Celestial physics and ephemeris audit
python .agents/hub.py audit physics
```

---

## 2. Audit Tools Catalog

1. **`agent_self_test.py` / `hub.py test`**:
   - Master in-process test suite running **131 automated sanity checks** across all 5 skill modules (Document-Now, State Ephemeris, Wavefront Physics, 4-Tier Transport, Politics & Governance, Sociology, 25+ Commodities Economy, 25+ Quests, Story Generation, Multi-Book Consistency, CLI dispatchers) in ~1 second with 100% PASS verification.
2. **`agent_hub.py doctor` / `hub.py doctor`**:
   - 4-stage system health sweep evaluating state files, celestial physics ephemeris laws, paradox audits, and the regression test suite.
3. **`chapter_continuity_validator.py` / `hub.py audit continuity`**:
   - Audits chapter headers, GUT chronology, angular resonance alignment, and prose formatting.
4. **`multi_book_consistency_auditor.py` / `hub.py audit paradox`**:
   - Cross-book continuity auditor checking that no hero is in two places at once, relic custody is unique, and character arcs are consistent.
5. **`audit_lore_physics.py` / `hub.py audit physics`**:
   - Rigorous mathematical validator verifying angular orientation math, rotation frequencies, and orbital velocity conservation.
