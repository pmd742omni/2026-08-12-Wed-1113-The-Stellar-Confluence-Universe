---
name: confluence-chapter-authoring
description: Executes the strict 74-book round-robin chapter authoring protocol for The Stellar Confluence Universe, auditing spatial coordinates, calculating Confluence Wavefront angular resonance, enforcing power constraints, generating 3-act narrative blueprints, dialect profiles, storyboards, audio scripts, and drafting vivid chapters accessible to a 10-year-old child.
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

# 2. Generate co-pilot draft prose (Grade 4-6 readability, sensory richness)
python .agents/hub.py author draft --book-id 1 --chapter 1

# 3. Evaluate prose readability (Grade 4-6 target), rhythm cadence, technobabble & synonyms
python .agents/hub.py author evaluate --file "01_Books_Library/Book_01_The_Solar_Crucible/Book_01_Chapter_01.md"

# 4. Polish sensory details & simplify complex vocabulary
python .agents/hub.py author polish --text "Caelum adjusted the hot metal dial."
python .agents/hub.py author soundscape --text "The golden lens hummed with a dazzling beam."

# 5. Complete chapter, award mastery XP, log diary & advance queue
python .agents/hub.py author complete --synopsis "Caelum calibrates the solar lens under high thermal strain to save the oasis array." --gut-delta 1
```

---

## 2. Complete Creative & Technical Toolchain Catalog

### A. Core Engine, Physics & Rotation
1. **`chapter_engine.py` / `hub.py author cycle` / `hub.py author prepare` / `hub.py author complete`**:
   - Master orchestrator. Scaffolds chapter stubs, executes one-shot authoring cycles, evaluates prose, awards mastery XP, updates diary, propagates ephemeris, and advances rotation.
2. **`story_generator.py` / `hub.py author draft`**:
   - Composes complete Grade 4–6 chapter drafts synthesizing ephemeris, resonance limitations, character voices, and 3-act beats.
3. **`confluence_wave_physics.py` / `hub.py author physics`**:
   - Computes 3D sinusoidal wave phase, localized wavefront energy intensity factor, and relativistic Doppler frequency shift.
   ```bash
   python .agents/hub.py author physics --coords "[10, 5, 0]" --gut 100.0 --velocity 0.2
   ```
4. **`calculate_resonance.py` / `hub.py author resonance`**:
   - Computes facing angle resonance state (`PEAK_FACING`, `TRANSIT_FACING`, `SHADOW_FACING`, `GATEWAY_SUBSPACE`) and power output constraints.
   ```bash
   python .agents/hub.py author resonance --facing 15.0 --faction "Sun-Forged Hegemony" --loc SURFACE
   ```
5. **`faction_matrix.py` / `hub.py author faction`**:
   - Technical encyclopedia and capability database for all 74 factions.
   ```bash
   python .agents/hub.py author faction --faction "Nebula-Weavers"
   ```
6. **`faction_diplomacy_engine.py` / `hub.py author diplomacy`**:
   - Bilateral diplomatic stances, friction indices (0–100), historical treaties, and conflict hooks.
   ```bash
   python .agents/hub.py author diplomacy --faction1 "Sun-Forged Hegemony" --faction2 "Void-Bound Monks"
   ```
7. **`resonance_artifact_engine.py` / `hub.py author relic`**:
   - Computes kinetic charge decay, power output (kW), and thermal overheat risk for signature relics.
   ```bash
   python .agents/hub.py author relic --relic "SOLAR_LENS" --facing 15.0
   ```

---

### B. Narrative Quality & Character Voices
8. **`chapter_prose_evaluator.py` / `hub.py author evaluate`**:
   - Flesch-Kincaid Grade Level (4–6 target), read-aloud sentence rhythm variance (standard deviation), sensory density, and technobabble gatekeeper.
9. **`prose_polisher.py` / `hub.py author polish`**:
   - Sensory enrichment engine replacing generic verbs with tactile, acoustic, and luminous descriptions.
10. **`character_voice_profiler.py` / `hub.py author voice`**:
    - Faction dialect profiler checking cadence, idioms, and cultural authenticity.
    ```bash
    python .agents/hub.py author voice --book-id 1 --text '"Watch your heat gauge through the primary lens."'
    ```
11. **`cross_encounter_engine.py` / `hub.py author encounter`**:
    - Dual-protagonist crossover dialogue and action simulator.
    ```bash
    python .agents/hub.py author encounter --book1 1 --book2 11 --medium SUBSPACE_COMMS
    ```

---

### C. Multimedia & Production
12. **`audiobook_director.py` / `hub.py author audiobook`**:
    - Audio production scripts with emotion tags, pacing notes, and Web Audio synth frequencies.
13. **`scene_storyboard_generator.py` / `hub.py author storyboard`**:
    - 3-keyframe cinematic visual prompts (Opening Wide Shot, Conflict Mid-Shot, Climax Close-Up).
14. **`anthology_compiler.py` / `hub.py author compile`**:
    - Compiles all written chapters of a book into a full manuscript under `01_Books_Library/Manuscripts/`.
15. **`universe_simulation_loop.py` / `hub.py author simulate`**:
    - High-speed macro simulation stepping ephemeris, tension, trade, and milestones forward.
    ```bash
    python .agents/hub.py author simulate --steps 5 --dry-run
    ```

---

## 3. Narrative Quality Standards

1. **Grade 4-6 Accessibility**: Prose must pass `chapter_prose_evaluator.py` ($FKGL \in [3.5, 7.0]$). Avoid complex technobabble; use grounded, tactile physical terms.
2. **Dynamic Audio Cadence**: Alternate short, punchy action sentences (3–6 words) with descriptive phrases (10–14 words) for read-aloud cadence.
3. **Physical Drama**: Power constraints dictate action. When resonance drops or overheat occurs, characters must use clever tactics, teamwork, and grit.
