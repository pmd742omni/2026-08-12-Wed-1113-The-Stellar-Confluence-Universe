---
name: confluence-chapter-authoring
description: Executes the strict 74-book round-robin chapter authoring protocol for The Stellar Confluence Universe, auditing spatial coordinates, calculating Confluence Wavefront angular resonance, enforcing power constraints, and drafting vivid chapters accessible to a 10-year-old.
---

# Confluence Chapter Authoring Skill

This skill orchestrates the authoring process for **The Stellar Confluence Universe** across its 74 interconnected books following the strict round-robin rotation protocol:
$$\text{[Book 01, Ch 1]} \to \text{[Book 02, Ch 1]} \to \dots \to \text{[Book 74, Ch 1]} \to \text{[Book 01, Ch 2]} \dots$$

---

## 1. Trigger Conditions

Activate this workflow whenever the developer specifies:
- `"write next chapter"` or `"author next chapter"`
- `"write chapter for Book [N]"`
- `"execute round-robin"` or `"advance story"`
- Prompts for character scenes, planetary events, or space transit adventures in the universe.

---

## 2. Standard Authoring Workflow

### Step 1: System State & Spatial Audit
1. Check the current active book index, chapter number, and GUT:
   ```bash
   python .agents/skills/confluence-chapter-authoring/scripts/advance_rotation.py --status
   ```
2. Read `00_System_State/character_registry.md` to identify:
   - Book Title & Series Number
   - Main Hero / Perspective Character
   - Faction Alignment (Sun-Forged, Void-Bound, Astrolabe, Expansion)
   - Current Location (`SURFACE`, `ORBITAL`, `DEEP_SPACE_TRANSIT`, `GATEWAY_SUBSPACE`) & Spatial Sector `[X, Y, Z]`.
3. Inspect `00_System_State/cosmic_clockwork.md` for active facing angles and recent environmental ripple events (e.g. stargate disruptions or beacon pulses triggered in preceding books).

---

### Step 2: Compute Resonance & Power Constraints
Execute the resonance calculator to determine the exact physics and power constraints:
```bash
python .agents/skills/confluence-chapter-authoring/scripts/calculate_resonance.py --facing <angle> --faction "<faction>" --loc <loc_type>
```

#### Angular Alignment Zones ($\theta$):
- **Peak Facing ($0^\circ \le \theta \le 30^\circ$)**: Supercharged solar power (overheat risk); Void suppressed; Astrolabe hyper-efficient.
- **Shadow Facing ($150^\circ \le \theta \le 180^\circ$)**: Solar eclipse lock (zero output); Void apex shadow surge (frost exhaustion); Astrolabe mechanical drag.
- **Transit Facing ($31^\circ \le \theta \le 149^\circ$)**: Harmonic baseline; stable, predictable powers.
- **Deep-Space Transit**: Unfiltered Volatility (powers 2x stronger, control 2x harder; accidental misuse risks hull breaches).
- **Gateway Subspace**: Neutral $Re = 0.5$ baseline.

---

### Step 3: Author the Chapter Payload
Draft the chapter adhering strictly to the **Narrative Standard**:
- **Tone & Accessibility**: Clean, vivid, sensory-rich prose easily understandable by a 10-year-old child, infused with cinematic wonder, high stakes, emotional warmth, and bravery (*Avatar: The Last Airbender*, *Studio Ghibli*, *Ender's Game*).
- **Physical Grounding**: Action scenes MUST actively reflect the computed power limitations (e.g., if a Sun-Forged knight is in shadow facing, their beam sword will not ignite; they must use physical grapple lines or kinetic spring blades).
- **Chapter File Path**: Save to `01_Books_Library/Book_XX_[Title_Slug]/Book_XX_Chapter_YY.md`.

---

### Step 4: Advance State & Log Diary Entry
1. Update `00_System_State/cosmic_clockwork.md` with the character's new post-chapter coordinates, facing angle, and status.
2. Append a 1-line execution summary to `00_System_State/diary.md`:
   ```markdown
   | GUT [N] | Book [XX] ([Title]) | Ch [YY] | [Character] | [1-sentence summary of major plot advancement] |
   ```
3. Advance the rotation queue to the next book:
   ```bash
   python .agents/skills/confluence-chapter-authoring/scripts/advance_rotation.py --advance
   ```

---

## 3. Chapter Markdown Template

```markdown
# Book [XX]: [Book Title]
## Chapter [YY]: [Chapter Subtitle]

**Galactic Universal Time (GUT)**: [GUT]
**Character**: [Hero Name] | **Faction**: [Faction]
**Location**: [Planet / Ship / Station Name] ([Loc_Type] | Sector `[X, Y, Z]`)
**Resonance State**: [Peak / Shadow / Transit / Deep-Space] ([Facing Angle]°)
**Active Constraint**: [E.g., Solar lenses locked in eclipse; relying on stored flywheel energy]

---

[Chapter prose body with vivid descriptions, dialogue, physical problem-solving, and emotional stakes...]
```
