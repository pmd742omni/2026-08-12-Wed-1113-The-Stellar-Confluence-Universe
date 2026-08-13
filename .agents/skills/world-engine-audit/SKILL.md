---
name: world-engine-audit
description: Audits celestial mechanics, wavefront alignment vectors, power constraint compliance, and faction balance across all 74 storylines in The Stellar Confluence Universe.
---

# World Engine Audit Skill

This skill performs physical, astronomical, and lore consistency checks across **The Stellar Confluence Universe** to ensure that all 74 storylines adhere strictly to celestial mechanics and power limitation laws.

---

## 1. Trigger Conditions

Activate this skill when:
- `"audit lore"` or `"audit physics"`
- `"validate celestial mechanics"`
- `"check faction balance"` or `"verify wavefront vectors"`
- Reviewing cross-book storyline consistency before major releases.

---

## 2. Core Physics & Lore Constraints

1. **Angular Alignment Bounds**:
   - Facing angle $\theta$ relative to the incoming Confluence Wavefront vector MUST fall strictly within $0^\circ \le \theta \le 180^\circ$.
2. **Resonance State Consistency**:
   - $0^\circ \le \theta \le 30^\circ \implies$ `PEAK_FACING`
   - $31^\circ \le \theta \le 149^\circ \implies$ `TRANSIT_FACING`
   - $150^\circ \le \theta \le 180^\circ \implies$ `SHADOW_FACING`
   - `GATEWAY_SUBSPACE` $\implies$ Disconnected neutral baseline ($Re = 0.5$)
3. **Environmental Volatility**:
   - Characters in `DEEP_SPACE_TRANSIT` (outside planetary atmospheres) MUST experience **2x Amplified Power** and **2x Difficulty in Control**.
4. **Faction Distribution**:
   - Core 30 Books: Exactly 10 Sun-Forged Hegemony, 10 Void-Bound Monks, 10 Astrolabe Engineers.
   - Expansion 44 Books: Comet-Riders, Nebula-Weavers, Deep-Core Miners, Gravity-Surfers, etc.

---

## 3. Automation Scripts & Tools

### Run Physics Diagnostics
```bash
python .agents/skills/world-engine-audit/scripts/audit_lore_physics.py
```
Outputs validation status, record counts, and any detected anomalies in angle bounds, location types, or resonance definitions.
