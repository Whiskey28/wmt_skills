# 研究 / 数据 / 科研 - Skills 导航

## NAV_DATA（结构化）

```yaml
role: research_data
role_display: 研究 / 数据 / 科研
skill_packages:
  - id: claude_scientific_skills
    type: local_family
    display: claude-scientific-skills/*
    why: 科研/数据全家桶（数据库、统计、绘图、领域库）
  - id: literature_and_citation
    type: local_skills
    display: literature-review + citation-bibliography-generator
    why: 综述与引用治理
  - id: web-access
    type: local_skill
    display: web-access
    why: 抓取/核实一手来源（可选）
    optional: true
skill_items_local:
  - id: claude-scientific-skills/*
    package: claude_scientific_skills
  - id: literature-review
    package: literature_and_citation
  - id: citation-bibliography-generator
    package: literature_and_citation
  - id: paper-polish
  - id: paper-writing-section
skill_items_external:
  - name: literature-review
    url: https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/literature-review?format=md
    purpose: 系统性综述工作流
  - name: citation-management
    url: https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/citation-management?format=md
    purpose: 引用信息核对与 BibTeX 治理
  - name: perplexity-search
    url: https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/perplexity-search?format=md
    purpose: 研究检索（联网检索与引用）
  - name: scientific-writing
    url: https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/scientific-writing?format=md
    purpose: 科研写作（IMRAD 等结构）
  - name: chart-generation
    url: https://skillshub.wtf/michaelboeding/skills/chart-generation?format=md
    purpose: 图表生成（可视化产出）
```

## 你常见的交付物 / 任务

- 文献检索、资料收集、引用与参考文献整理
- 数据分析、统计建模、可视化出图
- 研究报告/技术报告/实验记录（可复现）

## 建议你优先收集/沉淀的 Skills 类型

- **研究检索与证据链**：数据库检索、引用格式化、综述生成
- **分析与建模工具链**：统计、时序、ML、领域库（按需）
- **科研图表与报告**：可视化、论文写作/润色、结构化输出

## 推荐“大技能包”（先装一套，再挑工具）

- **`claude-scientific-skills/*`**：科研/数据全家桶（数据库、统计、绘图、领域库）
- **`literature-review` + `citation-bibliography-generator`**：综述与引用治理
- （可选）**`web-access`**：需要核实一手来源、抓取网页/文档时使用

## Skillshub 推荐（外部可直接拉取）

- [literature-review](https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/literature-review)：系统性综述工作流
- [citation-management](https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/citation-management)：引用信息核对与 BibTeX 等治理
- [perplexity-search](https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/perplexity-search)：研究检索（联网检索与引用）
- [scientific-writing](https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/scientific-writing)：科研写作（IMRAD 等结构）
- [chart-generation](https://skillshub.wtf/michaelboeding/skills/chart-generation)：图表生成（可视化产出）

## 你电脑里现有技能库（家族示例）

- **科学与数据工具库（大合集）**：`claude-scientific-skills/*`
- **综述与引用**：`literature-review`、`citation-bibliography-generator`
- **论文润色/章节写作**：`paper-polish`、`paper-writing-section`

