# 测试工程师 / QA - Skills 导航

## NAV_DATA（结构化）

```yaml
role: qa_engineer
role_display: 测试工程师 / QA
skill_packages:
  - id: gstack
    type: local_family
    display: gstack/*
    why: QA 流程、浏览器交互、证据采集
    pick_first:
      - gstack/qa
      - gstack/qa-only
      - gstack/browse
      - gstack/connect-chrome
  - id: playwright
    type: local_skills
    display: playwright-* + webapp-testing
    why: E2E 自动化测试体系
    pick_first:
      - playwright-best-practices
      - playwright-generate-test
      - webapp-testing
  - id: backend-testing
    type: local_skill
    display: backend-testing
    why: 接口/后端测试体系
skill_items_local:
  - id: gstack/qa
    package: gstack
  - id: gstack/qa-only
    package: gstack
  - id: gstack/browse
    package: gstack
  - id: gstack/connect-chrome
    package: gstack
  - id: playwright-best-practices
    package: playwright
  - id: playwright-generate-test
    package: playwright
  - id: webapp-testing
    package: playwright
  - id: backend-testing
    package: backend-testing
skill_items_external:
  - name: playwright-testing
    url: https://skillshub.wtf/TerminalSkills/skills/playwright-testing?format=md
    purpose: Playwright 测试实践
  - name: openclaw-parallels-smoke
    url: https://skillshub.wtf/openclaw/openclaw/openclaw-parallels-smoke?format=md
    purpose: 并行冒烟/快速验证（smoke）
  - name: playwright-pro
    url: https://skillshub.wtf/alirezarezvani/claude-skills/playwright-pro?format=md
    purpose: Playwright 进阶用法
  - name: senior-qa
    url: https://skillshub.wtf/alirezarezvani/claude-skills/senior-qa?format=md
    purpose: QA 策略与覆盖建议（综合指导）
```

## 你常见的交付物 / 任务

- 测试计划、测试用例（含边界/异常/回归范围）
- 自动化测试（E2E/接口/集成）与稳定性治理
- 缺陷报告：复现步骤、证据、影响范围、回归验证
- 发布前质量准入（冒烟/回归/验收）

## 建议你优先收集/沉淀的 Skills 类型

- **用例设计与覆盖**：从需求/页面/接口生成用例清单与优先级
- **自动化测试生成**：快速生成 Playwright/接口测试骨架
- **证据采集**：截图、日志、视频、控制台错误汇总
- **发布准入**：一键冒烟/回归清单与结果报告

## 推荐“大技能包”（先装一套，再挑工具）

- **`gstack/*`**：QA 相关能力集中（自动化 QA、浏览器交互、证据采集）
- **`playwright-*` + `webapp-testing`**：E2E 自动化测试体系
- **`backend-testing`**：接口/后端测试体系

## Skillshub 推荐（外部可直接拉取）

- [playwright-testing](https://skillshub.wtf/TerminalSkills/skills/playwright-testing)：Playwright 测试实践
- [openclaw-parallels-smoke](https://skillshub.wtf/openclaw/openclaw/openclaw-parallels-smoke)：并行冒烟/快速验证（偏 smoke）
- [playwright-pro](https://skillshub.wtf/alirezarezvani/claude-skills/playwright-pro)：Playwright 进阶用法
- [senior-qa](https://skillshub.wtf/alirezarezvani/claude-skills/senior-qa)：QA 策略与覆盖建议（偏综合指导）

## 你电脑里现有技能库（家族示例）

- **从 `gstack/*` 优先用这些（QA 向）**：`gstack/qa`、`gstack/qa-only`、`gstack/browse`、`gstack/connect-chrome`
- **Playwright 测试**：`playwright-best-practices`、`playwright-generate-test`、`webapp-testing`
- **后端测试**：`backend-testing`

