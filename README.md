# wmt_skills

WMT 的本地技能仓库，用于沉淀、管理和检索 Agent Skills。  
核心目标是把分散的 skills 变成可维护、可导航、可增量更新的资产库。

## 仓库用途

- 维护本地技能集合（主要位于 `.agents/skills`）
- 按角色组织技能导航（`roles`）
- 提供脚本化能力（批量安装、报告生成）
- 输出可交互的 skills 报告用于快速检索

## 相关技能检测结果（本仓库直接相关）

本次检测到以下与“仓库维护/文档/技能治理”最相关的技能：

- `skills-inventory-reporter`  
  - 位置：`.agents/skills/skills-inventory-reporter/SKILL.md`  
  - 用途：扫描 `.agents/skills`，生成并增量更新交互式 HTML 报告
- `skill-creator`  
  - 位置：`.agents/skills/skill-creator/SKILL.md`  
  - 用途：创建、迭代、评估技能，适合持续优化 skill 质量
- `doc-coauthoring`  
  - 位置：`.agents/skills/doc-coauthoring/SKILL.md`  
  - 用途：结构化协作文档写作（README、规范、提案等）
- `project-map-builder`  
  - 位置：`.agents/skills/yunshu_skillshub/project-map-builder/SKILL.md`  
  - 用途：生成/更新目录地图文档，适合做仓库结构说明

## 目录结构

```text
wmt_skills/
├─ .agents/
│  ├─ README.md
│  └─ skills/
├─ roles/
│  └─ README.md
├─ tools/
│  └─ install_top_skills_by_stars_from_skillshub.ps1
└─ reports/
   ├─ skills-report.html
   ├─ skills-report.data.json
   └─ skills-report.manifest.json
```

## 快速开始

### 1) 批量安装热门技能（PowerShell）

脚本：`tools/install_top_skills_by_stars_from_skillshub.ps1`

示例：

```powershell
powershell -ExecutionPolicy Bypass -File ".\tools\install_top_skills_by_stars_from_skillshub.ps1" -Limit 200
```

说明：

- 默认安装目录：`.agents/skills`
- 已存在同名 skill 会自动跳过

### 2) 生成/更新 Skills 交互报告（Python）

脚本：`.agents/skills/skills-inventory-reporter/scripts/build_skills_report.py`

示例：

```bash
python ".agents/skills/skills-inventory-reporter/scripts/build_skills_report.py" --repo-root "." --skills-root ".agents/skills" --out-html "reports/skills-report.html"
```

输出文件：

- `reports/skills-report.html`
- `reports/skills-report.data.json`
- `reports/skills-report.manifest.json`

## 报告功能说明

当前报告支持：

- 关键词搜索（name/description/path）
- 双维分类筛选（Domain + Role）
- 状态标签（added/updated/unchanged）
- 质量标签（如 `name-fallback`、`no-description`、`mirrored-path`）
- 增量变更明细（Added/Updated/Removed）
- 目录树折叠视图（跟随筛选联动）
- 分页与 `All` 全量显示

## 维护建议

- 新增或更新 skill 后，执行一次报告脚本保持索引最新
- 定期处理 `name-fallback` 与 `no-description` 标签，提高可检索性
- 如果将 `.agents` 作为仓库资产，请保持提交；如仅作本地缓存，请明确团队约定

## 已知注意事项

- `.gitignore` 当前包含：`.agents/skills/*.zip`
- 仓库中 skills 数量较大，建议通过报告筛选和标签优先定位
