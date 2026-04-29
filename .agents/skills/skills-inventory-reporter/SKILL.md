---
name: skills-inventory-reporter
description: Generate and incrementally update an interactive HTML inventory report for all skills under the current repository `.agents/skills` directory. Use this whenever the user asks to scan skills, organize messy skill folders, build a searchable/categorized skills catalog, compare newly added skills against an existing report, or quickly locate which skill to use.
---

# Skills Inventory Reporter

Builds a professional, interactive HTML report from repository skills, with incremental update support.

## When to use

Use this skill when the user wants to:

- Search all skills in the current repo quickly
- Turn a messy skills directory into a structured report
- Categorize skills (by description and by role)
- Track incremental skills changes and update only deltas

## Input assumptions

- The repository contains skills under `.agents/skills`
- Each skill is represented by `SKILL.md`
- Previous report may already exist at `reports/skills-report.html`

## Output

Always produce/update:

- `reports/skills-report.html` (interactive report)
- `reports/skills-report.data.json` (cached normalized data for incremental merge)
- `reports/skills-report.manifest.json` (file fingerprint index for delta detection)

## Required workflow

1. Scan `.agents/skills/**/SKILL.md`
2. Parse each skill:
   - `name` from frontmatter if present
   - `description` from frontmatter if present
   - relative path and role hints from path segments
3. Auto-classify in two dimensions:
   - **domain category**: inferred from description keywords
   - **role category**: inferred from path and naming patterns
4. Load previous `manifest` + `data` if both exist
5. Compute delta:
   - added
   - updated
   - removed
   - unchanged
6. Apply incremental merge to cached data
7. Regenerate HTML from merged data and include:
   - search
   - domain filters
   - role filters
   - sortable table
   - delta summary
8. Save updated `data` and `manifest`

## Non-negotiable behavior

- Do not guess missing values silently; keep empty string and mark as unknown where needed.
- Preserve duplicate skill entries if they exist in different paths.
- Keep report deterministic (stable sorting by path).
- Keep all generated files in ASCII.

## Recommended command

Run:

`python ".agents/skills/skills-inventory-reporter/scripts/build_skills_report.py" --repo-root "." --skills-root ".agents/skills" --out-html "reports/skills-report.html"`

## Success criteria

- Report opens as a single standalone HTML file
- Search/filter interactions work without external dependencies
- Delta summary is visible and reflects current scan vs previous cache
- Subsequent runs are incremental (merge based on fingerprints)
