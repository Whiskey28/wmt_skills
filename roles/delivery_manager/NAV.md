# 项目经理 / 交付经理（TPM/PMO）- Skills 导航

## NAV_DATA（结构化）

```yaml
role: delivery_manager
role_display: 项目经理 / 交付经理（TPM/PMO）
skill_packages:
  - id: gstack
    type: local_family
    display: gstack/*
    why: 发布/QA/回滚/复盘/基线/浏览器验证的端到端交付工具箱
    pick_first:
      - gstack/ship
      - gstack/land-and-deploy
      - gstack/setup-deploy
      - gstack/canary
      - gstack/benchmark
      - gstack/qa
      - gstack/qa-only
      - gstack/retro
      - gstack/learn
  - id: release-skills
    type: local_skill
    display: release-skills
    why: 通用发布/版本工作流
  - id: web-access
    type: local_skill
    display: web-access
    why: 联网检索与一手信息核实
  - id: claude-mem
    type: local_family
    display: claude-mem/*
    why: 项目过程/决策/复盘沉淀为可检索资产
    optional: true
skill_items_local:
  - id: gstack/ship
    package: gstack
  - id: gstack/land-and-deploy
    package: gstack
  - id: gstack/setup-deploy
    package: gstack
  - id: gstack/canary
    package: gstack
  - id: gstack/benchmark
    package: gstack
  - id: gstack/qa
    package: gstack
  - id: gstack/qa-only
    package: gstack
  - id: gstack/retro
    package: gstack
  - id: gstack/learn
    package: gstack
  - id: release-skills
    package: release-skills
  - id: claude-mem/*
    package: claude-mem
skill_items_external:
  - name: release-manager
    url: https://skillshub.wtf/alirezarezvani/claude-skills/release-manager?format=md
    purpose: 发布流程/版本管理辅助
  - name: status-report-generator
    url: https://skillshub.wtf/jeremylongshore/claude-code-plugins-plus-skills/status-report-generator?format=md
    purpose: 项目状态周报/状态报告
  - name: manager-make-new-plan
    url: https://skillshub.wtf/vosslab/vosslab-skills/manager-make-new-plan?format=md
    purpose: 新计划制定（里程碑/节奏）
  - name: manager-review-existing-plan
    url: https://skillshub.wtf/vosslab/vosslab-skills/manager-review-existing-plan?format=md
    purpose: 计划复核与风险点补全
  - name: deployment-patterns
    url: https://skillshub.wtf/affaan-m/everything-claude-code/deployment-patterns?format=md
    purpose: 部署模式/上线流程参考
  - name: release
    url: https://skillshub.wtf/paperclipai/paperclip/release?format=md
    purpose: 发布/交付动作模板化
```

## 你常见的交付物 / 任务

- 计划与里程碑、排期、依赖与资源协调
- 发布计划、上线 checklist、回滚预案、变更管理
- 项目周报/月报、风险清单、问题跟踪
- 质量门禁与验收流程（含回归策略）
- 事故复盘与过程改进

## 建议你优先收集/沉淀的 Skills 类型

- **发布与交付编排**：一键/半自动完成“准备→发布→验证→回滚”
- **质量准入与验证**：冒烟/回归/验收清单自动化
- **风险与变更治理**：变更评审、影响评估、发布窗口与回滚策略
- **过程资产沉淀**：周报/复盘模板化，输出稳定一致

## 推荐“大技能包”（先装一套，再挑工具）

- **`gstack/*`**：交付经理的“端到端交付工具箱”（发布、QA、回滚、复盘、基线、浏览器验证等）
- **`release-skills`**：通用发布/版本相关工作流
- **`web-access`**：联网检索与一手信息核实（必要时可用浏览器模式做验证）
- （可选）**`claude-mem/*`**：项目过程/决策/复盘沉淀为可检索资产

## Skillshub 推荐（外部可直接拉取）

- [release-manager](https://skillshub.wtf/alirezarezvani/claude-skills/release-manager)：发布流程/版本管理辅助
- [status-report-generator](https://skillshub.wtf/jeremylongshore/claude-code-plugins-plus-skills/status-report-generator)：项目状态周报/状态报告
- [manager-make-new-plan](https://skillshub.wtf/vosslab/vosslab-skills/manager-make-new-plan)：新计划制定（里程碑/节奏）
- [manager-review-existing-plan](https://skillshub.wtf/vosslab/vosslab-skills/manager-review-existing-plan)：计划复核与风险点补全
- [deployment-patterns](https://skillshub.wtf/affaan-m/everything-claude-code/deployment-patterns)：部署模式/上线流程参考
- [release](https://skillshub.wtf/paperclipai/paperclip/release)：发布/交付动作模板化

## 你电脑里现有技能库（家族示例）

- **从 `gstack/*` 优先用这些（交付/项目向）**：
  - 发布/交付：`gstack/ship`、`gstack/land-and-deploy`、`gstack/setup-deploy`
  - 上线后验证/基线：`gstack/canary`、`gstack/benchmark`
  - 质量检查：`gstack/qa`、`gstack/qa-only`
  - 复盘与沉淀：`gstack/retro`、`gstack/learn`
- **发布补充**：`release-skills`
- **长期记忆（可选）**：`claude-mem/*`

