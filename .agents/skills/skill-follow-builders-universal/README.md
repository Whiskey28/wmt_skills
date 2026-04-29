# follow-builders-universal

A cross-agent skill package for Claude Code, Codex, and Cursor.

## Install options

Use this repo as canonical source:
- `/Users/whiskey/Projects/Github/AI/follow-builders`

Recommended links:

```bash
# Claude Code
mkdir -p ~/.claude/skills
ln -sfn "/Users/whiskey/Projects/Github/AI/follow-builders/skill-follow-builders-universal" ~/.claude/skills/follow-builders-universal

# Cursor (workspace-level conventions may vary; keep path fixed and reference SKILL.md directly)
# Codex (same idea: point skill loader to this directory)
```

## Invocation examples

- "帮我按模型/开源/产品/产业生成今天的 AI 简报"
- "Collect AI builder updates daily from X + podcasts + blogs"
- "Use local fallback and still produce digest"

## Validation

Test prompts are in:
- `evals/evals.json`
