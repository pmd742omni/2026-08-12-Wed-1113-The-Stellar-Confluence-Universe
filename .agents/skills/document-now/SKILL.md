---
name: document-now
description: Automatically executes the standardized "Document Now" progress tracking workflow whenever the developer states "document now", "document progress", or requests a checkpoint update.
---

# Document Now Workflow Skill

This skill provides comprehensive instructions for executing the standardized **Document Now** progress tracking workflow in **The Stellar Confluence Universe** project.

---

## 1. Trigger Conditions

Execute this workflow immediately whenever the developer states:
- `"document now"`
- `"document progress"`
- `"checkpoint"` or `"create checkpoint"`
- Requests a formal progress snapshot or release log for the workspace.

---

## 2. Standard Operating Procedure

### Step 0: Zero-Config Self-Bootstrapping
Ensure the workspace progress tracking system is initialized:
```bash
python .agents/skills/document-now/scripts/version_registry.py bootstrap
```
This command automatically:
1. Locates the project root.
2. Initializes `progress tracking/` directory if missing.
3. Initializes `progress tracking/version_registry.json` and `progress tracking/Version_Registry.md`.
4. Validates Git repository status.
5. Returns `next_version` (e.g., `1.0.0`) and `suggested_codename` (e.g., `Isisekelo`).

---

### Step 1: Collect Authoritative Timestamps
Extract accurate system date and time strings dynamically:
```bash
python .agents/skills/document-now/scripts/get_timestamp.py
```
Outputs:
- `file_prefix`: `YYYY-MM-DD_HHMM` (for progress tracking filename)
- `git_prefix`: `YYYY-MM-DD Day HHMM` (for Git commit message header)
- `human_date_time`: Formatted date string for Markdown body

---

### Step 2: Progress Synthesis & Codename Uniqueness Check
1. **Analyze Accomplishments**: Review recent prompts, files changed, lore/state advancements, or tool modifications.
2. **Compute Next Version**:
   ```bash
   python .agents/skills/document-now/scripts/version_registry.py next-version
   ```
3. **Select & Verify Unique Ndebele Codename**:
   Get vocabulary suggestions or propose a word, then check uniqueness:
   ```bash
   python .agents/skills/document-now/scripts/version_registry.py suggest 5
   python .agents/skills/document-now/scripts/version_registry.py check <proposed_codename>
   ```
   *Requirement*: The check MUST return `"unique": true`.
4. **Draft Explanations for a 10-Year-Old Child**:
   - Codename translation and plain-English child-friendly explanation.
   - Child-friendly next steps.
5. **Set Development Attribution**:
   - Attribute co-development to `Peter Dube` and `Antigravity (AI Coding Assistant)`.

---

### Step 3: Create Progress Tracking File
Write `progress tracking/YYYY-MM-DD_HHMM_Description.md` adhering strictly to this schema:

```markdown
# [Title]

## Description
[High-level summary of changes and accomplishments]

## Progress
* [Key accomplishment bullet 1]
* [Key accomplishment bullet 2]
* [Key accomplishment bullet 3]

## Date & Time
[Formatted Human Date Time, e.g., Thursday, 13 August 2026, 09:51 PM (local time)]

## Version [Version Number] ([Ndebele Codename])
* **Codename**: [Ndebele Codename] ([English Meaning])
* **Explanation**: [Clear explanation targeted at a 10-year-old child]

## Next Steps
* [Child-friendly next action 1]
* [Child-friendly next action 2]

## Details of nature of development
Co-developed by Peter Dube and Antigravity (AI Coding Assistant).
* [Role and contributions]
```

---

### Step 4: Register Version in Registry Database
Register the new version into the database and Markdown table:
```bash
python .agents/skills/document-now/scripts/version_registry.py register <version> <codename> "<meaning>" "<human_date_time>" <filename>
```

---

### Step 5: Git Commit
Stage all modifications and create a standardized commit:
```bash
git add .
git commit -m "<YYYY-MM-DD Day HHMM>: [Title] ([Ndebele Codename] [Version])"
```
*(Example: `2026-08-13 Thu 2155: Initial Optimization of Agent Skills and Universe Registry (Isisekelo Version 1.0.0)`)*
