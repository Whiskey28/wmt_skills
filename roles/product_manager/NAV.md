# 产品经理（PM）- Skills 导航

## NAV_DATA（结构化）

```yaml
role: product_manager
role_display: 产品经理（PM）
skill_packages:
  - id: gstack
    type: local_family
    display: gstack/*
    why: 对齐/评审/交付/复盘的一揽子高杠杆技能
    pick_first:
      - gstack/plan-ceo-review
      - gstack/plan-design-review
      - gstack/office-hours
  - id: web-access
    type: local_skill
    display: web-access
    why: 联网搜索/抓取/网页交互（含登录态）
  - id: obsidian_and_mem
    type: local_family
    display: obsidian-skills/* + claude-mem/*
    why: 调研与决策沉淀、长期记忆、知识库管理
  - id: marketing_optional
    type: local_family
    display: marketingskills/*
    why: PM 兼增长/宣发时的 SEO/CRO/文案能力
    optional: true
skill_items_local:
  - id: gstack/plan-ceo-review
    package: gstack
  - id: gstack/plan-design-review
    package: gstack
  - id: gstack/office-hours
    package: gstack
  - id: claude-mem/*
    package: obsidian_and_mem
  - id: obsidian-skills/*
    package: obsidian_and_mem
  - id: baoyu-url-to-markdown
    package: web-access
  - id: baoyu-danger-x-to-markdown
    package: web-access
  - id: document-skills/pptx
  - id: document-skills/docx
skill_items_external:
  - name: acceptance-criteria-creator
    url: https://skillshub.wtf/jeremylongshore/claude-code-plugins-plus-skills/acceptance-criteria-creator?format=md
    purpose: 生成验收标准/验收条目
  - name: create-prd
    url: https://skillshub.wtf/phuryn/pm-skills/create-prd?format=md
    purpose: 生成 PRD
  - name: prd-increment-writer
    url: https://skillshub.wtf/Hmtheo/pm-skills-library/prd-increment-writer?format=md
    purpose: 增量式 PRD 编写
  - name: inc-prd-figma-make
    url: https://skillshub.wtf/Hmtheo/pm-skills-library/inc-prd-figma-make?format=md
    purpose: PRD → 原型/设计协作（偏 Figma 流程）
  - name: user-stories
    url: https://skillshub.wtf/phuryn/pm-skills/user-stories?format=md
    purpose: 用户故事生成
  - name: release-notes
    url: https://skillshub.wtf/phuryn/pm-skills/release-notes?format=md
    purpose: 发布说明/更新日志
```

## 你常见的交付物 / 任务

- PRD、用户故事、验收标准、版本范围说明
- 需求澄清与评审材料（对齐、取舍、风险）
- 原型与交互说明（含评审）
- 调研资料整理：竞品/用户/行业信息 → 结构化结论
- 版本发布对外说明（与运营/市场协作）

## 建议你优先收集/沉淀的 Skills 类型

- **需求澄清与结构化写作**：把自然语言需求变成 PRD/用户故事/验收条目
- **评审与决策辅助**：对方案做“挑战/补全/风险识别/边界澄清”
- **原型与表达**：把需求输出成可沟通的结构（原型、流程、信息架构、PPT）
- **信息搜集 → 知识化**：把网页/资料/讨论沉淀为可检索笔记
- **发布沟通素材**：公告、更新说明、FAQ、对外口径

## 推荐“大技能包”（先装一套，再挑工具）

- **`gstack/*`**：面向“从想法到交付”的一组高杠杆技能（对齐/评审/发布/验证/复盘等）
- **`web-access`**：统一的联网访问能力（搜索/抓取/页面交互/登录态）
- **`obsidian-skills/*` + `claude-mem/*`**：知识库与长期记忆（调研与决策沉淀）
- （可选）**`marketingskills/*`**：当 PM 兼增长/宣发时，用于 SEO/CRO/文案等

## Skillshub 推荐（外部可直接拉取）

- [acceptance-criteria-creator](https://skillshub.wtf/jeremylongshore/claude-code-plugins-plus-skills/acceptance-criteria-creator)：生成验收标准/验收条目
- [create-prd](https://skillshub.wtf/phuryn/pm-skills/create-prd)：生成 PRD
- [prd-increment-writer](https://skillshub.wtf/Hmtheo/pm-skills-library/prd-increment-writer)：增量式 PRD 编写
- [inc-prd-figma-make](https://skillshub.wtf/Hmtheo/pm-skills-library/inc-prd-figma-make)：PRD → 原型/设计协作（偏 Figma 流程）
- [user-stories](https://skillshub.wtf/phuryn/pm-skills/user-stories)：用户故事生成
- [release-notes](https://skillshub.wtf/phuryn/pm-skills/release-notes)：发布说明/更新日志

## 你电脑里现有技能库（家族示例）

- **从 `gstack/*` 优先用这些（PM 向）**：`gstack/plan-ceo-review`、`gstack/plan-design-review`、`gstack/office-hours`
- **知识沉淀/长期记忆**：`claude-mem/*`
- **笔记/知识库**：`obsidian-skills/*`
- **网页资料转 Markdown**：`baoyu-url-to-markdown`、`baoyu-danger-x-to-markdown`
- **文案/运营协作（若需要）**：`marketingskills/*`
- **PPT/文档类（若需要）**：`document-skills/pptx`、`document-skills/docx`

