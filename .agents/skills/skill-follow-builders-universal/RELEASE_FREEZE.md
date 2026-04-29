# Release Freeze Notes

Status: READY TO FREEZE
Date: 2026-04-21

## Final fixes applied before freeze

1. Ultra-brief deterministic heading normalized:
   - `templates/ultra-brief-template.md`
   - `## 必看 3 条` -> `## 必看3条`

2. Skill constraints tightened:
   - `SKILL.md`
   - Added explicit rule: ultra-brief section must contain exactly 3 bullet links.
   - Added explicit rule: mixed-language outputs must include `EN:` sentence per item.

## Stable assets

- `SKILL.md`
- `templates/bilingual-grouped-template.md`
- `templates/ultra-brief-template.md`

## Benchmark history

- iteration-2: delta +0.17
- iteration-3: delta +0.75 (optimistic baseline)
- iteration-4: delta +0.22 (stronger baseline, more realistic)

Recommended release baseline: iteration-4 methodology + current fixed templates.
