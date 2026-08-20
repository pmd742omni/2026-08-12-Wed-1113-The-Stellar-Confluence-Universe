---
name: confluence-chapter-authoring
description: Executes the strict 74-book round-robin chapter authoring protocol for The Stellar Confluence Universe, auditing spatial coordinates, calculating Confluence Wavefront angular resonance, enforcing power constraints, generating 3-act narrative blueprints, dialect profiles, storyboards, audio scripts, vehicle transport kinematics, and drafting vivid chapters accessible to a 10-year-old child.
---

# Confluence Chapter Authoring Skill

This skill orchestrates the end-to-end authoring and creative production process for **The Stellar Confluence Universe** across all 74 interconnected books following the strict round-robin rotation protocol:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \dots$$

---

## 1. Unified Master Authoring Pipeline

Execute every authoring step directly via the master CLI hub (`.agents/hub.py`):

```bash
# ONE-SHOT MASTER CYCLE (Prepare -> Draft -> Evaluate -> Polish -> Complete):
python .agents/hub.py author cycle --book-id 1

# Or execute step-by-step:
# 1. Prepare next chapter stub, audit physical constraints & generate 3-act scene blueprint
python .agents/hub.py author prepare

# 2. Generate 25+ rich galactic adventure quests with 5-stage blueprints
python .agents/hub.py author quest --book-id 1

# 3. Generate co-pilot draft prose (Grade 4-6 readability, vehicle mobility, sensory richness)
python .agents/hub.py author draft --book-id 1 --chapter 1 --style EXPLORATION_DISCOVERY

# 4. Evaluate prose readability (Grade 4-6 target), rhythm cadence, technobabble & synonyms
python .agents/hub.py author evaluate --file "01_Books_Library/Book_01_The_Solar_Crucible/Book_01_Chapter_01.md"

# 5. Polish sensory details & simplify complex vocabulary
python .agents/hub.py author polish --text "Caelum adjusted the hot metal dial."
python .agents/hub.py author soundscape --text "The golden lens hummed with a dazzling beam."

# 6. Complete chapter, award mastery XP, log diary & advance queue
python .agents/hub.py author complete --synopsis "Caelum calibrates the solar lens under high thermal strain to save the oasis array." --gut-delta 1
```

---

## 2. Complete Creative & Technical Toolchain Catalog

### A. Core Engine, Physics & Rotation
1. **`chapter_engine.py` / `hub.py author cycle` / `hub.py author prepare` / `hub.py author complete`**:
   - Master orchestrator. Scaffolds chapter stubs, executes one-shot authoring cycles, evaluates prose, awards mastery XP, updates diary, propagates ephemeris, and advances rotation.
2. **`story_generator.py` / `hub.py author draft`**:
   - Composes complete Grade 4–6 chapter drafts synthesizing ephemeris, resonance limitations, vehicle transport kinematics, governance models, character voices, and 3-act beats.
3. **`confluence_wave_physics.py` / `hub.py author physics`**:
   - Computes 3D sinusoidal wave phase, localized wavefront energy intensity factor, and relativistic Doppler frequency shift.
4. **`calculate_resonance.py` / `hub.py author resonance`**:
   - Computes facing angle resonance state (`PEAK_FACING`, `TRANSIT_FACING`, `SHADOW_FACING`, `GATEWAY_SUBSPACE`) and power output constraints.
5. **`faction_matrix.py` / `hub.py author faction`**:
   - Technical encyclopedia and capability database for all 74 factions.
6. **`faction_diplomacy_engine.py` / `hub.py author diplomacy`**:
   - Bilateral diplomatic stances, friction indices (0–100), historical treaties, and conflict hooks.
7. **`resonance_artifact_engine.py` / `hub.py author relic`**:
   - Computes kinetic charge decay, power output (kW), and thermal overheat risk for signature relics.

---

### B. Narrative Quality, Quests & Character Voices
8. **`chapter_prose_evaluator.py` / `hub.py author evaluate`**:
   - Flesch-Kincaid Grade Level (4–6 target), read-aloud sentence rhythm variance (standard deviation), sensory density, and technobabble gatekeeper.
9. **`prose_polisher.py` / `hub.py author polish`**:
   - Sensory enrichment engine replacing generic verbs with tactile, acoustic, and luminous descriptions.
10. **`character_voice_profiler.py` / `hub.py author voice`**:
    - Faction dialect profiler checking cadence, idioms, and cultural authenticity.
11. **`cross_encounter_engine.py` / `hub.py author encounter`**:
    - Dual-protagonist crossover dialogue and action simulator.
12. **`galactic_adventure_engine.py` / `hub.py author quest`**:
    - Generates 25+ high-stakes, child-friendly cosmic exploration quests, vehicle piloting challenges, trade convoy escorts, and physical problem-solving challenges tailored to character location and facing angle.

---

### C. Multimedia & Production
13. **`audiobook_director.py` / `hub.py author audiobook`**:
    - Audio production scripts with emotion tags, pacing notes, and Web Audio synth frequencies.
14. **`scene_storyboard_generator.py` / `hub.py author storyboard`**:
    - 3-keyframe cinematic visual prompts (Opening Wide Shot, Conflict Mid-Shot, Climax Close-Up).
15. **`anthology_compiler.py` / `hub.py author compile`**:
    - Compiles all written chapters of a book into a full manuscript under `01_Books_Library/Manuscripts/`.
16. **`universe_simulation_loop.py` / `hub.py author simulate`**:
    - High-speed macro simulation stepping ephemeris, tension, trade, and milestones forward.

---

## 3. Narrative Quality Standards

1. **Grade 4-6 Accessibility**: Prose must pass `chapter_prose_evaluator.py` ($FKGL \in [3.5, 7.0]$). Avoid complex technobabble; use grounded, tactile physical terms.
2. **Dynamic Audio Cadence**: Alternate short, punchy action sentences (3–6 words) with descriptive phrases (10–14 words) for read-aloud cadence.
3. **Physical Drama & Vehicle Realism**: Power constraints dictate action. When resonance drops or thermal overheat occurs, characters must use clever tactics, vehicle aerodynamics, teamwork, and grit.
