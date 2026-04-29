---

name: github-repo-evaluator
description: |
  用于当用户要对任意 GitHub 仓库（开源/私有）做系统化尽调/评估时触发。
  必须输出：S/A/B/C 评级与加权总分、证据驱动的优势/风险、以及可执行行动清单（P0/P1/P2）（并在需要时给出是否建议采用）。
  特别适用于：用户明确要求“生成并落盘/固化研究文档到 `github_research/repos/<owner__repo>/`”。
  固化要求：写入 `00_meta.md`、`report.md`、`10_evidence/gh_outputs.md`、`20_action_plan.md`、`99_notes.md`，并更新 `github_research/INDEX.md`。
  典型触发语（任一即可）：评估/尽调/系统化打分、给出 S/A/B/C、并固化到 github_research。
  
  也适用于：技术选型对比、引入依赖前的风险评估、检查文档/License 合规性、安全与活跃度信号评估。
compatibility:
  required:
    - GitHub CLI (gh) 已登录（可访问目标仓库）
    - 本地可运行 git（可选：克隆仓库做静态检查）
  optional:
    - ripgrep/rg（用于本地代码库快速检索）

- node/npm 或 python（仅当需要跑仓库自带 lint/test）

---

## 目标

对一个 GitHub 仓库做“可复用、可对比”的系统化评估，覆盖：

- 活跃度（Activity）
- 代码质量与安全性（Quality & Security）
- 社区贡献与流行度（Community & Popularity）
- 文档与合规性（Documentation & Compliance）

并给出**加权总分**与**S/A/B/C 级别**，附上可执行的改进建议与“是否建议采用/二开/进入白名单”的结论。

## 输入要求（你需要从用户处拿到）

至少一个即可：

- **仓库 URL**：如 `https://github.com/owner/repo`
- **owner/repo**：如 `owner/repo`

可选但强烈建议补充（若用户没说也别卡住，直接按默认做）：

- **评估用途**：依赖引入 / 二次开发 / 商业采购 / 学习参考 / 安全审计
- **风险偏好**：保守 / 中性 / 激进（影响阈值与建议语气）
- **最低门槛**：例如“必须 MIT/Apache-2.0”“必须有 CI”“必须近 90 天有提交”

## 输出格式（必须使用这个模板）

ALWAYS 输出一个 Markdown 报告，结构固定如下：

### 仓库评估报告：<owner/repo>

#### 1) 结论（30 秒读完）

- **综合评级**：S / A / B / C
- **加权总分**：<0-100>
- **是否建议采用**：建议 / 谨慎采用 / 不建议
- **采用前置条件**（如有）：<最多 3 条硬条件>

#### 2) 评分总览（按权重）

- **活跃度（40%）**：<分数>/100（子项见下）
- **代码质量与安全性（30%）**：<分数>/100
- **社区影响力（20%）**：<分数>/100
- **文档与合规（10%）**：<分数>/100

#### 3) 关键发现（证据驱动）

- **优势**：<3-6 条，必须带证据点（时间/数量/文件/配置/链接）>
- **风险**：<3-6 条，必须带证据点>

#### 4) 分项细评（可复查）

按本技能的“评分细则”逐项给出：分数、理由、证据、改进建议（若适用）。

#### 5) 玩转指南（Cursor / Codex）
把它当作“快速跑通仓库 + 判断是否值得采用”的通用工程路线图（尽量不依赖该仓库特有的命令名）。

执行规则（通用且可复查）：
1. 从根目录优先读取 `README`、`docs/`、以及任何“开发/运行/测试”入口文件（如 `CONTRIBUTING.md`、`DEVELOPMENT.md`、`Makefile`、`package.json`、`pyproject.toml`、`Cargo.toml` 等），提取该仓库真实存在的：安装/构建/启动/测试/示例运行 关键步骤与命令。
2. 根据仓库类型做轻量适配（启发式即可）：
   - 若检测到“技能/提示词/Agent 集合”特征（例如存在 `.claude-plugin/plugin.json` 或 `skills/**/SKILL.md`），则以该仓库提供的接入/初始化说明为准；
   - 否则按主语言给出通用运行方式（以 README/配置文件里出现的命令为准），如 Node（`npm/yarn/pnpm`）、Python（`python -m ...`）、Go（`go test ./...`）、Rust（`cargo test`）。
3. 输出一个最小验证闭环：先跑“最轻量的可执行步骤”（样例/最小测试/lint），再给出你建议进一步查看的 2-3 个风险点（license 合规、安全边界/披露、是否有 CI/安全扫描信号）。

硬性要求：不要臆造仓库不存在的命令；若根目录无法提取到可执行步骤，则改为列出“你需要从仓库作者确认/补充的最少信息清单”，并在证据里写明缺失原因来自哪些文件位置。

#### 6) 适用性判断（结合用户用途）

如果用户提供了用途/约束，在这里明确：

- **适合做什么**
- **不适合做什么**
- **替代方案建议**（可选，1-3 个方向即可）

#### 7) 下一步行动清单（可执行）

按优先级输出：

- **P0（必须）**：<最多 5 条>
- **P1（建议）**：<最多 5 条>
- **P2（可选）**：<最多 5 条>

---

## 文件固化（默认：当存在 `github_research/` 或用户明确要求“落盘/固化/生成研究文档”时必须执行）
如果环境允许写文件，则完成以下动作：
1. 解析 `owner/repo`，生成目录名：`github_research/repos/<owner__repo>/`
2. 确保存在 `10_evidence/` 子目录。
3. 生成/更新固定文件：
   - `00_meta.md`
   - `report.md`
   - `10_evidence/gh_outputs.md`
   - `20_action_plan.md`
   - `99_notes.md`
4. 将本次评估输出中以下内容分别写入对应文件：
   - 报告主体（含结论/评分/发现/分项细评/玩转指南/适用性判断/行动清单）→ `report.md`
   - `gh` / GitHub API 关键字段与计算口径 → `10_evidence/gh_outputs.md`
   - P0/P1/P2 → `20_action_plan.md`
5. 更新 `github_research/INDEX.md`：为 `<owner__repo>` 增加/更新一行（综合评级、加权总分、是否建议采用、最近研究时间）。

> 若环境不支持写文件，仍然必须先输出完整 Markdown 报告；并明确告知“落盘能力不可用”。

---

## 评估方法（执行步骤）

遵循“先远程数据 → 再本地验证（可选）→ 最后出分”的顺序，避免一上来就克隆浪费时间。

### A. 远程（GitHub API / 仓库元信息）

优先使用 `gh` 获取客观数据（不要手填/臆测）。

#### 1) 基础信息

- 仓库是否归档（archived）、是否有默认分支保护（如可见）
- Stars / Forks / Watchers / Open issues
- 主要语言占比

推荐命令（按需使用）：

```bash
gh repo view owner/repo --json name,description,visibility,isArchived,isFork,defaultBranchRef,primaryLanguage,languages,licenseInfo,createdAt,updatedAt,homepageUrl,stargazerCount,forkCount,watchers,issues,pullRequests
```

```bash
gh api repos/owner/repo/releases --paginate
```

```bash
gh api repos/owner/repo/issues?state=open --paginate
gh api repos/owner/repo/issues?state=closed --paginate
gh api repos/owner/repo/pulls?state=open --paginate
gh api repos/owner/repo/pulls?state=closed --paginate
```

```bash
gh api repos/owner/repo/commits?per_page=1
```

```bash
gh api repos/owner/repo/contributors --paginate
```

#### 2) DTA 风格活跃度判断（偏重“近况 + 趋势”）

至少取三个时间窗：

- **近 30 天**
- **近 90 天**
- **近 365 天**

重点观察：

- 提交是否持续（不是一次性冲刺后长期静默）
- release 是否稳定
- issue/PR 的响应是否有节奏（不是“堆积成山”）

#### 3) 安全信号（若权限可见）

尽可能检查：

- Security Policy（`SECURITY.md`）
- Dependabot（依赖更新 PR / alerts）
- Code scanning / secret scanning（如果是 GHAS 才可能看到）

> 注意：私有仓库或权限不足时要明确写出“不可见/无法确认”，不要猜。

### B. 本地（可选但推荐：静态规范与质量信号）

当仓库看起来值得进一步评估时，再克隆做快速静态检查。

```bash
git clone --depth 1 https://github.com/owner/repo.git
cd repo
```

检查点（只做“信号检查”，避免陷入完整阅读代码）：

- **项目规范**：`.editorconfig`、`.gitattributes`、`.gitignore`、`CODEOWNERS`、`CODE_OF_CONDUCT.md`
- **CI**：`.github/workflows/`* 或其他 CI 配置
- **测试**：`test/`、`tests/`、`__tests__/`、`pytest.ini`、`vitest/jest` 配置等
- **Lint/格式化**：`eslint`/`prettier`/`ruff`/`black`/`golangci-lint` 等
- **依赖与构建**：`package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` 等
- **文档**：`README.md`、`docs/`、示例、FAQ

若用户目标是“是否能落地使用/引入”，优先跑最小验证（仅在成本可控时）：

- `npm test` / `pnpm test` / `pytest -q` / `go test ./...` 等（选择项目主流命令）

---

## 评分模型（强制）

采用 0-100 的分数体系，每个维度先算子项得分再加权。

### 权重（默认）

- **活跃度**：40%
- **代码质量与安全性**：30%
- **社区影响力**：20%
- **文档与合规**：10%

> 若用户声明了用途（例如“企业生产依赖”或“安全极度保守”），可以在报告里说明“基于用途做了轻微权重调整”，但必须保留“默认权重下的分数”用于横向对比。

### 项目类型识别（影响评分子项）
先判断仓库类型，然后用对应的“质量子项映射”打分：
- **Skill-Collection（技能集合仓库）**：包含 `.claude-plugin/plugin.json`，且存在 `skills/**/SKILL.md` 或类似“技能/脚本/工作流文档”结构。
- **普通代码库（Code Repo）**：存在 `src/`、`package.json/go.mod/pyproject.toml/Cargo.toml` 等典型运行时代码资产。

Skill-Collection 的关键变化：
- “测试/CI”不作为硬惩罚项（它可能根本不存在）；改用“技能结构完整性与确定性/安全边界”来衡量质量。
- “Release 节奏”如果没有 GitHub Releases，则改用 Tag/最近提交/里程碑文档的更新来衡量维护节奏。

### 维度一：活跃度（40%）

子项（每项 0-5 分，映射到 0-100）：

- **提交频率/连续性**：近 90 天是否持续有提交；是否多人提交
- **最后提交时间**：>365 天无提交通常直接强风险
- **版本节奏（Release/Tag/里程碑）**：普通代码库看 release；Skill-Collection 若无 releases，则看 tags/关键文档/skill 结构更新的持续性
- **Issue/PR 处理速度**：打开/关闭比例、平均关闭时长（用样本估算也可以）
- **维护者响应**：PR review/讨论是否存在

建议粗略阈值（可按项目类型调整）：

- 5：近 30 天有多次提交 + 近 90 天持续 + 近 12 个月有 release 或明确的里程碑
- 3：近 90 天偶发提交或只有依赖更新；release 不稳定但有维护迹象
- 1：近 12 个月基本无动静
- 0：归档/长期停滞且无替代维护渠道

### 维度二：代码质量与安全性（30%）

子项（0-5）：

- **规范化配置**：`.editorconfig`/lint/format/类型检查配置是否齐全
- **质量保障信号**：
  - 普通代码库：测试/CI/覆盖率信号优先
  - Skill-Collection：技能结构完整性（每个 SKILL.md 有 `name/description/触发场景/输出模板`）、一致性（与 `plugin.json` 的 skill 路径/数量一致）、以及安全边界文档（如 out-of-scope/question-limits、危险操作拒绝/guardrails）
- **安全治理**：`SECURITY.md`、依赖更新机制、已知漏洞处理痕迹
- **工程可维护性信号**：模块结构清晰、构建脚本合理、依赖不过度陈旧（只做信号，不做主观贬低）
- **机密泄漏风险（信号）**：是否把密钥写进仓库（只报告发现的证据，避免扩散敏感内容）

### 维度三：社区贡献与流行度（20%）

子项（0-5）：

- **Stars/Forks/Watchers**：结合项目年龄；避免“唯 star 论”
- **贡献者数量与集中度**：是否单点风险（绝大多数提交来自 1 人）
- **互动活跃**：Discussions、PR 评论、issue 讨论质量
- **生态位置**：是否被其他知名项目依赖/引用（可选，若能快速确认）

### 维度四：文档与合规（10%）

子项（0-5）：

- **README 清晰度**：安装/使用/示例/FAQ/限制说明
- **LICENSE**：是否存在且明确（缺失通常直接判合规风险）
- **CONTRIBUTING**：是否有贡献指南、开发环境说明
- **变更记录**：`CHANGELOG.md` 或 release notes 质量

---

## 评级映射（强制）

以加权总分（0-100）映射：

- **S**：≥ 85（高活跃 + 高质量 + 文档规范 + 有 CI/CD 或等价保障：例如 skill 结构完整性与安全边界良好）
- **A**：70–84（整体可靠，存在少量短板但可接受）
- **B**：50–69（可用但风险较多；适合学习/非关键路径/需要自建保障）
- **C**：< 50（维护停滞或合规/安全/质量缺陷明显，不建议依赖）

并加一个“红线规则”（任意命中则建议至少降 1 级或直接“不建议采用”）：

- **无 LICENSE 且用户用途涉及分发/商用/企业合规**
- **近 365 天无提交且无明确维护声明**
- **明显泄露密钥/凭证（或历史泄露未处理）**

---

## 写作要求（避免误导）

- **证据优先**：每个关键结论至少有一个可复查证据点（日期、数量、文件名、配置路径或 `gh` 输出字段）。
- **不胡猜**：权限不可见就写“不可见/无法确认”，并说明缺失会带来的风险。
- **不扩散敏感信息**：如果发现疑似密钥，只描述“类型与位置的抽象信息”，不要粘贴完整值。
- **语气对齐用途**：用户是“评估是否引入生产依赖”时，建议更保守；是“学习参考”时，建议可更开放。

## 3 个测试用例（供未来自测）

1. “帮我按 S/A/B/C 评估这个仓库：`vercel/next.js`，并给出是否适合企业生产依赖的结论。”
2. “我想二开这个 repo：`owner/repo`（私有仓库），重点看活跃度、测试、CI、安全风险，输出行动清单。”
3. “我在做技术选型，对比 `foo/bar` 和 `baz/qux` 哪个更值得采用，按你这个模型各打一次分并对比。”

