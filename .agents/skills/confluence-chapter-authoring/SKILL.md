---
name: confluence-chapter-authoring
description: Executes the strict 74-book round-robin chapter authoring protocol for The Stellar Confluence Universe, auditing spatial coordinates, calculating Confluence Wavefront angular resonance, enforcing power constraints, and drafting vivid chapters accessible to a 10-year-old.
---

# Confluence Chapter Authoring Skill

This skill orchestrates the end-to-end authoring process for **The Stellar Confluence Universe** across its 74 interconnected books following the strict round-robin rotation protocol:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \dots$$

---

## 1. Fast One-Command Workflow (Unified Chapter Engine)

### Step 1: Prepare Chapter Stub & Audit Physical Constraints
```bash
python .agents/skills/confluence-chapter-authoring/scripts/chapter_engine.py prepare
```
This automatically:
1. Audits current active book index, chapter number, and GUT in `00_System_State/rotation_tracker.md`.
2. Resolves protagonist, faction, world/ship, and sector coordinates from `00_System_State/character_registry.md`.
3. Checks `00_System_State/cosmic_events.json` for active environmental hazards affecting that sector.
4. Computes active Wavefront angular facing $\theta$ and capability constraints.
5. Scaffolds the chapter file under `01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md` with structured metadata headers.

---

### Step 2: Author Chapter Payload
Draft the chapter adhering strictly to the **Narrative Standard**:
- **Tone & Accessibility**: Clean, vivid, sensory-rich prose easily understandable by a 10-year-old child, infused with cinematic wonder, high stakes, emotional warmth, and bravery (*Avatar: The Last Airbender*, *Studio Ghibli*, *Ender's Game*).
- **Physical Grounding**: Action scenes MUST actively reflect the computed power limitations (e.g., if a Sun-Forged knight is in shadow facing, their beam sword will not ignite; they must use physical grapple lines or kinetic spring blades).
- **Target File**: `01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md`.

---

### Step 3: Complete Chapter & Propagate Clockwork
```bash
python .agents/skills/confluence-chapter-authoring/scripts/chapter_engine.py complete --synopsis "<1-2 sentence summary of chapter action>" --gut-delta 1
```
This automatically:
1. Appends the synopsis entry to `00_System_State/diary.md`.
2. Propagates celestial ephemeris (planetary axial rotation, orbital cycles, starship vectors) across all 74 storylines in `00_System_State/cosmic_clockwork.md`.
3. Advances `00_System_State/rotation_tracker.md` to the next book in the round-robin queue.

---

## 2. Low-Level Diagnostic Tools

- **Calculate Resonance Manually**:
  ```bash
  python .agents/skills/confluence-chapter-authoring/scripts/calculate_resonance.py --facing <angle> --faction "<faction>" --loc <loc_type>
  ```
- **Inspect / Advance Rotation Tracker**:
  ```bash
  python .agents/skills/confluence-chapter-authoring/scripts/advance_rotation.py --status
  python .agents/skills/confluence-chapter-authoring/scripts/advance_rotation.py --advance
  ```
