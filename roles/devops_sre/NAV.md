# 运维 / DevOps / SRE - Skills 导航

## NAV_DATA（结构化）

```yaml
role: devops_sre
role_display: 运维 / DevOps / SRE
skill_packages:
  - id: gstack
    type: local_family
    display: gstack/*
    why: 发布/部署/验证/基线/护栏合集
    pick_first:
      - gstack/setup-deploy
      - gstack/land-and-deploy
      - gstack/ship
      - gstack/canary
      - gstack/benchmark
      - gstack/careful
      - gstack/guard
      - gstack/freeze
      - gstack/unfreeze
  - id: docker
    type: local_skills
    display: docker-expert + multi-stage-dockerfile
    why: 容器化与环境一致性
  - id: release-skills
    type: local_skill
    display: release-skills
    why: 发布版本与变更说明
skill_items_local:
  - id: gstack/setup-deploy
    package: gstack
  - id: gstack/land-and-deploy
    package: gstack
  - id: gstack/ship
    package: gstack
  - id: gstack/canary
    package: gstack
  - id: gstack/benchmark
    package: gstack
  - id: gstack/careful
    package: gstack
  - id: gstack/guard
    package: gstack
  - id: gstack/freeze
    package: gstack
  - id: gstack/unfreeze
    package: gstack
  - id: docker-expert
    package: docker
  - id: multi-stage-dockerfile
    package: docker
  - id: release-skills
    package: release-skills
skill_items_external:
  - name: devops-deploy
    url: https://skillshub.wtf/sickn33/antigravity-awesome-skills/devops-deploy?format=md
    purpose: 部署/交付操作建议
  - name: devops-troubleshooter
    url: https://skillshub.wtf/rmyndharis/antigravity-skills/devops-troubleshooter?format=md
    purpose: DevOps 排障/故障定位
  - name: incident-response-incident-response
    url: https://skillshub.wtf/sickn33/antigravity-awesome-skills/incident-response-incident-response?format=md
    purpose: 事故响应流程（模板化）
  - name: incident-responder
    url: https://skillshub.wtf/rmyndharis/antigravity-skills/incident-responder?format=md
    purpose: 事故处置协作与步骤
  - name: azure-sre-agent
    url: https://skillshub.wtf/MicrosoftDocs/Agent-Skills/azure-sre-agent?format=md
    purpose: Azure SRE（官方文档型技能）
```

## 你常见的交付物 / 任务

- CI/CD、部署、灰度、回滚、发布窗口管理
- 监控与告警、健康检查、性能基线与容量规划
- 故障处理：定位、缓解、复盘、预防性改进
- 环境与配置标准化（容器化、配置管理）

## 建议你优先收集/沉淀的 Skills 类型

- **发布编排**：自动化发布、回滚、上线后验证
- **可观测性与基准**：性能/错误监控、基线对比、回归报警
- **安全护栏**：危险命令拦截、权限最小化、变更审计
- **容器化与环境一致性**：镜像优化、多阶段构建、运行时安全

## 推荐“大技能包”（先装一套，再挑工具）

- **`gstack/*`**：发布/部署/验证/基线/护栏的合集（DevOps/SRE 高频）
- **`docker-expert` + `multi-stage-dockerfile`**：容器化体系
- **`release-skills`**：发布版本与变更说明（与工程侧对齐）

## Skillshub 推荐（外部可直接拉取）

- [devops-deploy](https://skillshub.wtf/sickn33/antigravity-awesome-skills/devops-deploy)：部署/交付操作建议
- [devops-troubleshooter](https://skillshub.wtf/rmyndharis/antigravity-skills/devops-troubleshooter)：DevOps 排障/故障定位
- [incident-response-incident-response](https://skillshub.wtf/sickn33/antigravity-awesome-skills/incident-response-incident-response)：事故响应流程（模板化）
- [incident-responder](https://skillshub.wtf/rmyndharis/antigravity-skills/incident-responder)：事故处置协作与步骤
- [azure-sre-agent](https://skillshub.wtf/MicrosoftDocs/Agent-Skills/azure-sre-agent)：Azure SRE（官方文档型技能）

## 你电脑里现有技能库（家族示例）

- **从 `gstack/*` 优先用这些（DevOps/SRE 向）**：
  - 部署/发布：`gstack/setup-deploy`、`gstack/land-and-deploy`、`gstack/ship`
  - 上线验证/基线：`gstack/canary`、`gstack/benchmark`
  - 安全护栏：`gstack/careful`、`gstack/guard`、`gstack/freeze`、`gstack/unfreeze`
- **容器化**：`docker-expert`、`multi-stage-dockerfile`

