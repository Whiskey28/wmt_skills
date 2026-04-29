---
name: follow-builders-universal
description: Default skill for recurring AI intelligence collection in Claude Code, Codex, and Cursor. Invoke this whenever the user asks for AI news monitoring, builder updates, model/open-source/product/industry tracking, daily or weekly digests, grouped outputs (especially 模型/开源/产品/产业), HN/GitHub/X aggregation, or digest customization by language/style/source mix, even when the user does not mention "follow-builders" explicitly. Prefer this skill over generic summarization when the request involves ongoing collection workflows, cross-source synthesis, or schedule-aware briefings.
compatibility:
  agents:
    - claude-code
    - codex
    - cursor
  runtime:
    - node>=18
  optional_dependencies:
    - telegram bot token (only for Telegram delivery)
    - resend api key (only for email delivery)
---

# Follow Builders Universal Skill

Turn natural-language collection requests into a repeatable, multi-source digest workflow.

## What this skill does

1. Parse the user's request into a structured collection intent.
2. Collect content from available feeds/sources.
3. Normalize items into a common schema.
4. Group and summarize content by user-required sections.
5. Output digest text and (optionally) deliver it.

## Trigger signals

Activate this skill when the user says things like:
- "帮我每天收集 AI 信息"
- "给我做一个 builder digest"
- "按模型/开源/产品/产业分组"
- "每天 8 点推送 AI 资讯"
- "关注 HN + GitHub + X 的更新"

## Agent compatibility contract

### Claude Code
- Prefer shell execution + local scripts.
- Read and write files under the current repo.
- Use the pipeline below directly.

### Codex
- Use the same filesystem-first workflow.
- Keep deterministic steps in scripts; keep model steps in prompt files.
- Avoid relying on host-specific plugins.

### Cursor
- Same workflow as Claude Code/Codex.
- Keep instructions explicit because sessions may be shorter and interactive.

## Required project paths

Assume this repository root:
- `/Users/whiskey/Projects/Github/AI/follow-builders`

Core files:
- `scripts/generate-feed.js`
- `scripts/prepare-digest.js`
- `scripts/deliver.js`
- `config/default-sources.json`
- `prompts/*.md`

Optional practice pipeline (from this repo):
- `playground/3day-bootcamp/day1/prepare-digest-local.mjs`
- `playground/3day-bootcamp/day2/fetch-hn.mjs`
- `playground/3day-bootcamp/day3/github-source-and-report.mjs`

## Execution workflow

### Step 1: Capture collection intent
Convert user request into:
- `cadence`: daily/weekly/on-demand
- `language`: en/zh/bilingual
- `sources`: x, podcasts, blogs, hn, github
- `grouping`: default or custom (e.g. 模型/开源/产品/产业)
- `delivery`: stdout/telegram/email
- `style`: concise/deep/ops-focused

If missing, use sensible defaults:
- cadence: daily
- language: zh
- sources: x + podcasts + blogs
- grouping: 模型/开源/产品/产业
- delivery: stdout

### Step 2: Data preparation
Primary path:
- Run `node scripts/prepare-digest.js`

Fallback path (network-constrained):
- Run `node playground/3day-bootcamp/day1/prepare-digest-local.mjs`

### Step 3: Optional source expansion
When user asks for tech/open-source emphasis:
- Run `node playground/3day-bootcamp/day2/fetch-hn.mjs 8`
- Run `node playground/3day-bootcamp/day3/github-source-and-report.mjs`

### Step 4: Normalize + group
Target sections (default):
- 模型
- 开源
- 产品
- 产业

Use deterministic grouping when scripts exist; otherwise apply prompt rules consistently.

#### Deterministic grouping rule (recommended)
If the user asks for grouped output (模型/开源/产品/产业) OR mentions HN/GitHub/X aggregation:
1) Run `node playground/3day-bootcamp/day3/github-source-and-report.mjs`
2) Prefer using `playground/3day-bootcamp/artifacts/day3-grouped.md` as the primary item list.
3) Only supplement with `scripts/prepare-digest.js` / local fallback JSON when a section is empty.

### Step 5: Summarize
Apply prompt stack in this order:
1. `prompts/digest-intro.md`
2. Source prompts (`summarize-tweets.md`, `summarize-podcast.md`, `summarize-blogs.md`)
3. `prompts/translate.md` when zh/bilingual is requested

Template-first rule:
- If user requests bilingual grouped output, render with `templates/bilingual-grouped-template.md`.
- If user requests concise/very short output, render with `templates/ultra-brief-template.md`.
- Fill template slots only with link-backed items from prepared artifacts.
- For `ultra-brief-template`, keep `## 必看3条` exactly and keep exactly 3 bullet links in that section.
- For mixed-language constraints ("中文为主 + 每条英文摘要"), each bullet must include an explicit `EN:` sentence.

Hard constraints:
- Never invent URLs.
- If an item has no usable link, exclude it.
- Keep role/title grounded in available source metadata.
- Ensure each of the four default sections exists (even if the section is empty, output `- 暂无`).
- In every section, prefer fewer items with strong links over many weak items (3–6 items/section is a good default).

### Step 6: Deliver
- `stdout`: print digest.
- `telegram/email`: send via `node scripts/deliver.js`.

## Output format

Use this template unless the user asks otherwise:

```markdown
# AI Builders Digest

## 模型
- [title](url)
  - insight

## 开源
- [title](url)
  - insight

## 产品
- [title](url)
  - insight

## 产业
- [title](url)
  - insight

## 今日行动建议
- action 1
- action 2
```

## Minimal command cookbook

From repo root:

```bash
# base digest input
node scripts/prepare-digest.js

# network fallback
node playground/3day-bootcamp/day1/prepare-digest-local.mjs

# add HN
node playground/3day-bootcamp/day2/fetch-hn.mjs 8

# grouped output (includes GitHub + HN + local X feed)
node playground/3day-bootcamp/day3/github-source-and-report.mjs
```

## Safety and reliability

- Prefer deterministic scripts for collection and grouping.
- Keep model work focused on summarization and prioritization.
- If a remote endpoint times out, continue with available local artifacts and clearly label freshness.
- Never require platform-specific hidden state; all critical settings should be file-backed.
