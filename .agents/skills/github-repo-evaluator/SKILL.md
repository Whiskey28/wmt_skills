---

name: github-repo-evaluator
description: |
  对任意 GitHub 仓库（开源/私有）做系统化尽调：输出 S/A/B/C、加权总分、证据型优势/风险、仓库定位与意义、玩转指南、适用性与 P0/P1/P2 行动项。
  只要用户提到「评估仓库 / 尽调 / 打分 / SABC / 技术选型 / 依赖风险 / License / 安全审计 / 固化 github_research」就应使用本技能（宁可多用）。
  落盘：`github_research/repos/<owner__repo>/` 下 `00_meta`、`report`、`10_evidence`、`20_action_plan`、`99_notes`、更新 `INDEX.md`；条件生成 `30_cli_commands.md`（规则见正文，勿臆造命令）。
  本地克隆根目录由环境变量 `GITHUB_REPO_EVALUATE_CLONE_ROOT` 决定；未设置时用 `$HOME/Projects/Github/Analyse`；分析结束后**禁止删除**克隆目录。
  评分细则、CLI 判定、API 不可用时的回退、完整文件清单见 SKILL.md 正文（description 仅为触发摘要）。
compatibility:
  required:
    - GitHub CLI (gh) 已登录（可访问目标仓库；若不可用则改用 GitHub REST API 并写明限制）
    - 本地可运行 git（推荐：用于克隆到默认分析目录并做静态检查）
  optional:
    - ripgrep/rg（用于本地代码库快速检索）
    - node/npm/pnpm/yarn 或 python/uv/pip（用于提取或运行仓库脚本、测试与 --help 自检）

---

## 目标

对一个 GitHub 仓库做“可复用、可对比”的系统化评估，覆盖：

- 活跃度（Activity）
- 代码质量与安全性（Quality & Security）
- 社区贡献与流行度（Community & Popularity）
- 文档与合规性（Documentation & Compliance）

并给出**加权总分**与**S/A/B/C 级别**，附上可执行的改进建议与“是否建议采用/二开/进入白名单”的结论。

## 执行顺序（推荐，避免漏步骤）

1. **解析** `owner/repo`（从 URL 或短名）。
2. **远程元数据**：尽量用 `gh` 或 GitHub REST API 拉取 stars、issue、语言、license 等（若失败见「远程不可用时的回退」）。
3. **本地克隆（按需）**：若需要文件证据、命令溯源或 `git log` 活跃度，将仓库置于 **`<CLONE_ROOT>/<owner>__<repo>`**（`<CLONE_ROOT>` 见「本地克隆路径」）；禁止事后删除。
4. **类型与 CLI 判定**：项目类型（Code vs Skill-Collection）+「是否需要终端命令」+ 冲突裁决。
5. **打分**：按评分模型填四维与加权总分。
6. **输出**：先给用户完整 Markdown 报告；若允许写盘，再执行「文件固化」。

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

#### 4) 仓库定位与意义（必须）
回答以下问题并给出证据：
- **这个仓库本身是做什么的**（一句话定位 + 1 段展开）
- **它的核心价值/意义是什么**（对用户、团队或生态）
- **它在同类项目中的角色**（基础设施/工具库/工作流资产/应用产品）
- **你为什么会（或不会）选择它**（结合用户用途，不要空泛）

#### 5) 分项细评（可复查）

按本技能的“评分细则”逐项给出：分数、理由、证据、改进建议（若适用）。

#### 6) 玩转指南（Cursor / Codex）
把它当作“快速跑通仓库 + 判断是否值得采用”的通用工程路线图（尽量不依赖该仓库特有的命令名）。

执行规则（通用且可复查）：
1. 从根目录优先读取 `README`、`docs/`、以及任何“开发/运行/测试”入口文件（如 `CONTRIBUTING.md`、`DEVELOPMENT.md`、`Makefile`、`package.json`、`pyproject.toml`、`Cargo.toml` 等），提取该仓库真实存在的：安装/构建/启动/测试/示例运行 关键步骤与命令。
2. 根据仓库类型做轻量适配（启发式即可）：
   - 若检测到“技能/提示词/Agent 集合”特征（例如存在 `.claude-plugin/plugin.json` 或 `skills/**/SKILL.md`），则以该仓库提供的接入/初始化说明为准；
   - 否则按主语言给出通用运行方式（以 README/配置文件里出现的命令为准），如 Node（`npm/yarn/pnpm`）、Python（`python -m ...`）、Go（`go test ./...`）、Rust（`cargo test`）。
3. 输出一个最小验证闭环：先跑“最轻量的可执行步骤”（样例/最小测试/lint），再给出你建议进一步查看的 2-3 个风险点（license 合规、安全边界/披露、是否有 CI/安全扫描信号）。
4. **命令清单（落盘时）**：若正在写入 `github_research/repos/<owner__repo>/`，先按「是否需要终端命令」做判定（见下文章节）。**仅当判定为「需要」且能从仓库文件/CI/文档追溯到真实命令时**，生成或更新 `30_cli_commands.md`，本节末尾用一行链向 `./30_cli_commands.md`。**若判定为「不需要」**，不生成该文件，并在 `99_notes.md` 写一行：`CLI 清单：已跳过 — <理由>`。**若判定为「需要」但证据不足以列出命令**，不生成空壳，并在 `99_notes.md` / `10_evidence/gh_outputs.md` 说明缺失项。

硬性要求：不要臆造仓库不存在的命令；若根目录无法提取到可执行步骤，则改为列出“你需要从仓库作者确认/补充的最少信息清单”，并在证据里写明缺失原因来自哪些文件位置。

#### 7) 适用性判断（结合用户用途）

如果用户提供了用途/约束，在这里明确：

- **适合做什么**
- **不适合做什么**
- **替代方案建议**（可选，1-3 个方向即可）

#### 8) 下一步行动清单（可执行）

按优先级输出：

- **P0（必须）**：<最多 5 条>
- **P1（建议）**：<最多 5 条>
- **P2（可选）**：<最多 5 条>

### 落盘时 `00_meta.md` 建议字段（与报告一致、避免漏项）

在与「文件固化」一并写入时，`00_meta.md` 至少包含：

| 字段 | 说明 |
|------|------|
| 仓库名 / URL | `owner/repo` 与可访问的 `https://github.com/...` |
| 研究时间 | ISO 日期或会话日期 |
| 研究用途 / 风险偏好 | 若用户未说明可写「默认：学习/选型」 |
| **本地克隆绝对路径** | 实际使用的 `<CLONE_ROOT>/<owner>__<repo>`，或「未克隆」+ 原因 |
| **CLI 清单** | 已生成 `30_cli_commands.md` / 已跳过 + 一句理由 |
| 可选 | 综合评级、加权分一句、索引用关键词 |

（详细写入分工仍以「文件固化」一节为准。）

---

## 本地克隆路径（可配置；禁止删除）

当用户提供了仓库 URL（或 `owner/repo`）且需要**本地文件证据**（静态检查、命令溯源、`git log` 统计等）时：

1. **克隆根目录 `<CLONE_ROOT>`**（跨机器通用）  
   - 优先读取环境变量 **`GITHUB_REPO_EVALUATE_CLONE_ROOT`**。  
   - 若未设置：使用 **`$HOME/Projects/Github/Analyse`**（Windows 用等价用户主目录，如 `%USERPROFILE%\Projects\Github\Analyse`）。  
   - 个人若曾使用其他固定目录，可在 shell 中 `export GITHUB_REPO_EVALUATE_CLONE_ROOT=/你的/路径` 保持习惯，无需改 skill。
2. **完整目标路径**：`<CLONE_ROOT>/<owner>__<repo>`（与 `github_research/repos/<owner__repo>/` 命名一致，便于对照）。
3. **若该目录已存在**：进入后 `git remote -v` 校验是否为同一仓库；是则 `git fetch` + `git pull --ff-only`，**禁止**为「重新克隆」而删除整个目录。
4. **若目录不存在**：`git clone <url> "<CLONE_ROOT>/<owner>__<repo>"`（可加 `--depth 1`；需要更准确提交统计时再 `git fetch --deepen`）。
5. **分析结束后**：**不得**对该路径执行 `rm`、`git clean -fd`、清空目录等破坏性操作。
6. **落盘引用**：在 `10_evidence/gh_outputs.md`（及 `30_cli_commands.md` 头信息，若生成）写明 **实际解析后的绝对路径**（含 `<CLONE_ROOT>` 展开结果）。

> 用户在消息里**另行指定**克隆目录时，以用户路径为准，仍遵守「分析后不删除」。

**Shell 一次性写法示例**（Unix）：

```bash
export CLONE_ROOT="${GITHUB_REPO_EVALUATE_CLONE_ROOT:-$HOME/Projects/Github/Analyse}"
# 目标目录："$CLONE_ROOT/owner__repo"
```

---

## 是否需要终端命令（启发式判定）

在决定是否生成 `30_cli_commands.md` 之前，必须先给出 **YES / NO** 判定（可在内心推理，但落盘时必须在 `99_notes.md` 用一句话说明）。

### 判定为 **需要终端命令**（倾向生成 `30_cli_commands.md`，前提是命令可溯源）

满足 **任一** 即可：

- 存在典型**应用/库/SDK** 信号：`package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`pom.xml`、`build.gradle`、`Makefile`、`Dockerfile`、`docker-compose*.yml` 等。
- `README` / `docs` / CI 中出现 **install、build、run、test、lint、docker compose** 等可执行指令。
- 仓库为 **CLI 工具**、**服务端**（需 `npm run dev`、`uvicorn`、`go run` 等启动）、或 **爬虫/自动化/脚本型** 项目。
- 用户**明确要求**终端命令清单（始终视为「需要」，但若仓库确实无可溯源命令则仍不生成文件，只说明原因）。

### 判定为 **不需要终端命令**（不生成 `30_cli_commands.md`，必须写理由）

满足 **任一** 即可（除非用户强制要求清单且仓库有可溯源命令）：

- **纯文档/电子书/笔记合集**：几乎全是 `.md`，无构建入口；阅读即可，无统一 shell 工作流。
- **数据集或静态资源仓**：以下载链接或 Git LFS 为主，无「在本仓执行构建」的必要步骤。
- **Skill-Collection（技能集合）**且消费路径明确为「导入 IDE / 插件市场 / 复制 SKILL.md」，文档**未**给出统一的 `npm`/`pip`/脚本安装闭环 → 玩转指南用叙事即可，**不设** `30_cli_commands.md`（或在 `99_notes` 说明「无统一 CLI，按插件文档操作」）。
- **单文件脚本说明**且 README 仅写「复制到项目」而无包管理与命令 —— 可只在 `report.md` 玩转指南描述，**不必**单独清单文件。

### 边界情况

- 判定为「需要」但**找不到任何可溯源命令**：**不生成空文件**；`99_notes.md` 写明「判定需要 CLI，但文档/CI 未提供可摘录命令」。
- 判定为「不需要」但用户**强行索要**清单：在 `99_notes.md` 解释为何不生成；若仓库确实存在少量脚本命令且可溯源，可**例外**生成简短清单（标题注明「可选/非常规用途」）。

### 冲突裁决（YES 与 NO 同时出现信号时）

按下列顺序**择优一侧**，并在 `99_notes.md` 用一句话说明裁决依据：

1. **README 主路径优先**：若 README 的首要「快速开始」明确以终端安装/运行为主（出现可复制命令块），倾向 **需要 CLI**。若明确写「仅插件市场 / 仅复制 SKILL / 无命令行」为主路径，倾向 **不需要 CLI**。
2. **文档站辅助文件**：存在 `package.json` 但仅用于 **文档站/VitePress/docusaurus**，且主 README 不要求读者本地 build → 倾向 **不需要**（除非 CONTRIBUTING 要求维护者必须跑构建）。
3. **构建信号兜底**：若仍模糊，且存在 **Makefile / Dockerfile / CI 中的真实 build、test job** → 倾向 **需要 CLI**（维护者与高级用户通常需要终端）。
4. **仍无法判断**：默认 **不需要** 单独 `30_cli_commands.md`，但在 `玩转指南` 写清楚「若参与开发可再看 CONTRIBUTING/CI」；若用户强制要清单，再按「边界情况」例外处理。

---

## CLI 命令清单模块（通用，可落盘）

与 `report.md` 中叙事型「玩转指南」分工：**玩转指南**讲路线、前置条件与风险；**`30_cli_commands.md`** 只收录可在终端照抄的命令块（及占位符/环境变量名）。本模块描述**适用于任意语言与仓库类型**的工作方式；禁止在本 SKILL 正文中硬编码某个开源项目的专有命令。

### 何时生成 `github_research/repos/<owner__repo>/30_cli_commands.md`

必须**同时**满足：

1. 「是否需要终端命令」判定为 **需要**（见上一节）；**或**用户明确要求清单且仓库存在可溯源命令；
2. 能从本地克隆（默认路径见「本地克隆路径」）或 README/CI/Makefile 等 **追溯到真实命令**。

### 何时不生成（必须留痕）

与「是否需要终端命令」「冲突裁决」一致；不重复罗列。核心：**不需要** 或 **无可溯源命令** → 不建空文件，并在 `99_notes.md` 留痕。

### 证据发现顺序（按优先级，跨栈通用）

1. **人类可读入口**：`README*`，`CONTRIBUTING.md`，`DEVELOPMENT.md`，`INSTALL*`，`docs/` 下安装/运行页。
2. **任务与编排**：`Makefile`，`justfile`，`Taskfile.yml`，`Dockerfile`，`docker-compose*.yml` / `compose.yaml`。
3. **包管理器声明**：`package.json` → `scripts`；`pyproject.toml` / `Pipfile` / `requirements*.txt`；`Cargo.toml`；`go.mod` 与旁路文档；`pom.xml` / `build.gradle*` 等（只摘录文档或脚本中**已出现**的命令）。
4. **CI 工作流**：`.github/workflows/*`、`gitlab-ci.yml` 等 → 提取维护者**实际运行**的命令，并注明证据（文件名 + job/step 意图即可）。
5. **CLI 自描述**：仅当入口明确（文档、`[project.scripts]`、已知 `main`/`cli` 模块）时，可列出「建议在本机执行 `<entry> --help` 展开选项」；**不得编造未在 `--help` 或文档中出现的子命令**。

### `30_cli_commands.md` 推荐结构（通用骨架）

1. **头信息**：本地克隆绝对路径（用户提供的）或占位 `<YOUR_CLONE_PATH>`；**证据来源**列表（如 `README.md` 章节、`package.json#scripts`、某 workflow 路径）。
2. **前置检查**：仅列文档声明的版本（语言、包管理器、Docker）。
3. **安装 / 同步依赖**：与仓库一致的一条或多条命令（`uv sync`、`npm ci`、`pnpm install`、`cargo build` 等）。
4. **运行主路径**：最小闭环（如 dev server、CLI 样例子命令）。
5. **测试与静态检查**：仅当存在配置或脚本时收录（`pytest`、`pnpm test`、`go test ./...`、`make test`）。
6. **可选：容器 / 数据库 / 部署**：仅当仓库内存在对应 compose 或文档章节。
7. **合规提示**：一两句指向 `LICENSE` / 免责声明；**不做法律结论**。
8. **维护记录**：评估日期与本次增补说明。

### 写作纪律

- **零臆造**：每条命令须在头信息「证据来源」中可指向具体文件或 CI 片段；不确定则写「需向维护者确认」而非填空命令。
- **零敏感信息**：禁止粘贴真实 Cookie、token、私钥、密码；用环境变量名或 `<SET_ME>`。
- **与 `report.md` 互链**：若已生成 `30_cli_commands.md`，玩转指南末尾保留一行指向 [`30_cli_commands.md`](./30_cli_commands.md)。若**未生成**（判定不需要终端命令或无可溯源命令），玩转指南末尾写一句：**「未单独落盘 CLI 清单：`<理由摘要>`，详见 `99_notes.md`。」**

---

## 文件固化（默认：当存在 `github_research/` 或用户明确要求“落盘/固化/生成研究文档”时必须执行）
如果环境允许写文件，则完成以下动作：
1. 解析 `owner/repo`，生成目录名：`github_research/repos/<owner__repo>/`
2. 确保存在 `10_evidence/` 子目录。
3. **始终**生成/更新的核心文件：
   - `00_meta.md`
   - `report.md`
   - `10_evidence/gh_outputs.md`（须包含本地克隆绝对路径：`<CLONE_ROOT>/<owner>__<repo>` 是否已使用、解析后的值；若用户另有指定则写实际路径）
   - `20_action_plan.md`
   - `99_notes.md`（须包含：**是否需要终端命令**的判定一句话；以及 **`30_cli_commands.md` 已生成 / 已跳过** 及理由）
4. **条件生成**：`30_cli_commands.md` — 仅当「是否需要终端命令」为 **需要** 且命令可溯源时写入；否则**不创建该文件**。
5. 将本次评估输出中以下内容分别写入对应文件：
   - 报告主体（含结论/评分/关键发现/仓库定位与意义/分项细评/玩转指南/适用性判断/行动清单）→ `report.md`
   - `gh` / GitHub API 关键字段与计算口径 + **本地克隆绝对路径** → `10_evidence/gh_outputs.md`
   - P0/P1/P2 → `20_action_plan.md`
   - 仓库定位一句话与价值摘要（可选复写）→ `00_meta.md` 与 `99_notes.md`
   - 可拷贝终端命令清单 → `30_cli_commands.md`（**仅当**本节第 4 步条件满足）
6. 更新 `github_research/INDEX.md`：为 `<owner__repo>` 增加/更新一行（综合评级、加权总分、是否建议采用、最近研究时间）。

> 若环境不支持写文件，仍然必须先输出完整 Markdown 报告；并明确告知“落盘能力不可用”。

---

## 评估方法（执行步骤）

默认顺序：**先尽力远程元数据** → **再按需克隆到 `<CLONE_ROOT>/<owner>__<repo>`**（见「本地克隆路径」）→ **综合打分与落盘**。若远程接口不可用，允许**先克隆再本地统计**（见下节回退），并在证据中写明顺序变更原因。

### A. 远程（GitHub API / 仓库元信息）

优先使用 `gh` 获取客观数据（不要手填/臆测）。

#### 远程不可用或限流时的回退（P1）

以下**任一**成立时，不要阻塞尽调：

- `gh` 未登录、`gh` 失败，或 **HTTP 403/429**（API 限流）；
- 私有仓 token 不足导致 API 空结果。

**回退策略（按优先级）**：

1. **未认证 GitHub REST API**（公开仓库）：`GET https://api.github.com/repos/owner/repo` 等；在 `10_evidence/gh_outputs.md` 注明「未认证请求及速率限制风险」。
2. **优先克隆**到 `<CLONE_ROOT>/<owner>__<repo>`，用本地 `git log --since=...` 统计近 30/90/365 天提交、读取 `README`/CI/目录结构补全证据；在证据中写「活跃度以本地 git 为准」。
3. **仍不可得**：明确写「不可确认」项（如 open issues 数），并说明对评分的影响（通常保守降分）。

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

### B. 本地（推荐：静态规范与质量信号）

当用户提供了可克隆的仓库引用且需要做本地证据时，**使用默认目录**（勿删除，见上文「本地克隆路径」）：

```bash
CLONE_ROOT="${GITHUB_REPO_EVALUATE_CLONE_ROOT:-$HOME/Projects/Github/Analyse}"
TARGET="$CLONE_ROOT/owner__repo"
# 若目录不存在：
git clone --depth 1 https://github.com/owner/repo.git "$TARGET"

# 若目录已存在且 remote 一致：
cd "$TARGET" && git pull --ff-only
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

## 测试用例（供未来自测）

1. “帮我按 S/A/B/C 评估这个仓库：`vercel/next.js`，并给出是否适合企业生产依赖的结论。”
2. “我想二开这个 repo：`owner/repo`（私有仓库），重点看活跃度、测试、CI、安全风险，输出行动清单。”
3. “我在做技术选型，对比 `foo/bar` 和 `baz/qux` 哪个更值得采用，按你这个模型各打一次分并对比。”
4. “评估 `owner/repo` 并固化到 `github_research`；克隆到 `$CLONE_ROOT/owner__repo`（默认 `$HOME/Projects/Github/Analyse` 或已 export 的 `GITHUB_REPO_EVALUATE_CLONE_ROOT`），且不得删除；需要终端则生成 `30_cli_commands.md`，否则在 `99_notes` 写明跳过理由。”
5. “我这边 `gh` 不可用且 API 限流，只能克隆后本地看提交与 README，照样出尽调报告并固化。”
6. “这是一个几乎全是 `.md` 的文档仓库，评估并固化；说明为何不生成 `30_cli_commands.md`。”

更多标准化 prompt 见本 skill 目录下 `evals/evals.json`（可用于人工回归或未来自动化评测）。

---

## 捆绑资源（渐进披露）

| 路径 | 用途 |
|------|------|
| `evals/evals.json` | 标准评估用例 prompt 列表，便于回归 |
| `references/README.md` | 预留：将来若评分细则过长，可拆出附录至此目录 |

