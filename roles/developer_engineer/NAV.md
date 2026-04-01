# 开发工程师（前端/后端/全栈）- Skills 导航

## NAV_DATA（结构化）

```yaml
role: developer_engineer
role_display: 开发工程师（前端/后端/全栈）
skill_packages:
  - id: gstack
    type: local_family
    display: gstack/*
    why: 排障、浏览器验证、QA、发布与部署等（开发常用“高杠杆外设”）
    pick_first:
      - gstack/investigate
  - id: playwright
    type: local_skills
    display: playwright-*
    why: E2E/前端自动化测试体系
    pick_first:
      - playwright-best-practices
      - playwright-generate-test
      - webapp-testing
  - id: backend-testing
    type: local_skill
    display: backend-testing
    why: 后端测试体系
  - id: refactor
    type: local_skills
    display: refactor + code-refactoring
    why: 重构与可维护性治理
  - id: docker
    type: local_skills
    display: docker-expert + multi-stage-dockerfile
    why: 容器化与环境一致性
skill_items_local:
  - id: refactor
    package: refactor
  - id: code-refactoring
    package: refactor
  - id: backend-testing
    package: backend-testing
  - id: playwright-best-practices
    package: playwright
  - id: playwright-generate-test
    package: playwright
  - id: webapp-testing
    package: playwright
  - id: gstack/investigate
    package: gstack
  - id: superpowers/skills/systematic-debugging
  - id: docker-expert
    package: docker
  - id: multi-stage-dockerfile
    package: docker
skill_items_external:
  - name: senior-fullstack
    url: https://skillshub.wtf/alirezarezvani/claude-skills/senior-fullstack?format=md
    purpose: 全栈实现/架构与落地建议（综合指导）
  - name: debug
    url: https://skillshub.wtf/pproenca/dot-skills/debug?format=md
    purpose: 调试与定位辅助
  - name: code-refactor
    url: https://skillshub.wtf/mhattingpete/claude-skills-marketplace/code-refactor?format=md
    purpose: 代码重构建议
  - name: code-refactoring-refactor-clean
    url: https://skillshub.wtf/sickn33/antigravity-awesome-skills/code-refactoring-refactor-clean?format=md
    purpose: 清理式重构
  - name: fp-refactor
    url: https://skillshub.wtf/sickn33/antigravity-awesome-skills/fp-refactor?format=md
    purpose: 函数式重构思路（风格化）
```

## 你常见的交付物 / 任务

- 需求落地：代码实现、接口/数据模型、页面/组件
- Debug：定位问题、复现、修复、回归验证
- 测试：单测/集成/E2E、测试数据准备
- 重构：结构调整、性能优化、依赖升级、技术债治理
- 交付：构建、部署、发布说明、环境脚本

## 建议你优先收集/沉淀的 Skills 类型

- **编码加速与脚手架**：生成模板、通用模块、统一工程约定
- **测试生成与最佳实践**：覆盖策略、用例生成、稳定性治理
- **调试排障**：日志→结论→修复补丁→验证
- **重构与可维护性**：小步重构、重复消除、命名统一、风险控制
- **交付脚本化**：构建/部署/回滚脚本、环境一致性

## 推荐“大技能包”（先装一套，再挑工具）

- `**gstack/*`**：包含排障、浏览器验证、QA、发布与部署等（开发常用的“高杠杆外设”）
- `**playwright-*` + `webapp-testing**`：前端/E2E 自动化测试体系
- `**backend-testing**`：后端测试体系
- `**refactor` / `code-refactoring**`：工程重构能力
- `**docker-expert` / `multi-stage-dockerfile**`：容器化与环境一致性

## Skillshub 推荐（外部可直接拉取）

- [senior-fullstack](https://skillshub.wtf/alirezarezvani/claude-skills/senior-fullstack)：全栈实现/架构与落地建议（偏综合指导）
- [debug](https://skillshub.wtf/pproenca/dot-skills/debug)：调试与定位辅助
- [code-refactor](https://skillshub.wtf/mhattingpete/claude-skills-marketplace/code-refactor)：代码重构建议
- [code-refactoring-refactor-clean](https://skillshub.wtf/sickn33/antigravity-awesome-skills/code-refactoring-refactor-clean)：清理式重构
- [fp-refactor](https://skillshub.wtf/sickn33/antigravity-awesome-skills/fp-refactor)：函数式重构思路（偏风格化）

## 你电脑里现有技能库（家族示例）

- **重构**：`refactor`、`code-refactoring`
- **测试（后端）**：`backend-testing`
- **E2E/前端测试**：`playwright-best-practices`、`playwright-generate-test`、`webapp-testing`
- **系统化排障**：`gstack/investigate`、`superpowers/skills/systematic-debugging`
- **容器化/镜像**：`docker-expert`、`multi-stage-dockerfile`

