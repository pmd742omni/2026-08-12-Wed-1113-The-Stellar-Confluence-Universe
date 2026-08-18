---
name: prompt-response-flow
description: Maintains and updates the chronological pair-programming interaction journal in the Prompt-Response Flow directory with valid YAML frontmatter and formatted prompt-response blocks.
---

# Prompt-Response Flow Skill

This skill standardizes and automates the recording of developer prompts and agent responses inside the project's dedicated flow journal (e.g., `2026-08-12 Wed 1134 Prompt-Response Flow/`).

---

## 1. Trigger Conditions

Activate this workflow when:
- Logging a completed prompt-response pair: `"log flow entry"` or `"record interaction"`.
- Checking or fixing formatting in the Prompt-Response Flow journal.
- Creating a new session flow file.
- Inspecting session flow summary statistics.

---

## 2. File Schema & Formatting Standard

Each flow document MUST adhere to the following structure:

### YAML Frontmatter Block
```yaml
---
Name: "2026-08-12 Wed 1149 Prompt-Response Flow"
Version: "1.0"
Date: "2026-08-12 Wed 1149"
---
```

### Entry Format
```markdown
# YYYY-MM-DD Day

## HHMM

### Prompt

[Exact developer prompt text]

### Response

[Summary or full text of agent actions, tool runs, and explanations]
```

---

## 3. Automation Scripts & Master Hub Commands

### Append Entry via Master Hub
```bash
python .agents/hub.py flow log --prompt "<Prompt Text>" --response "<Response Text>"
```

### Inspect Active Flow Document
```bash
python .agents/hub.py flow active
```

### Summarize Current Flow Session Entries
```bash
python .agents/hub.py flow summary
```

### Create New Flow Session
```bash
python .agents/hub.py flow new
```
