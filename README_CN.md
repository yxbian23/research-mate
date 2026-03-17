<div align="center">

# ResearchMate

**AI 研究者的 Claude Code 一键工具箱**

*你的配置 + 6 个精选第三方工具，统一管理，一键部署，自动同步。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)]()

[快速开始](#-快速开始) · [集成工具](#-集成的第三方工具) · [功能目录](#-功能目录) · [使用指南](#-使用指南)

</div>

---

## 为什么需要 ResearchMate？

| 痛点 | 现有方案 | ResearchMate |
|------|---------|--------------|
| 换电脑要重配 Claude 设置 | 手动复制，无版本管理 | **一行命令**完成全部配置 |
| 想用多个社区工具 | 各自安装，散落各处 | **统一打包**在一个仓库 |
| 社区工具更新了想跟进 | fork 后手动 merge | **GitHub Actions 自动同步** + Claude 审核 |
| 想魔改工具适配自己 | 改了就没法再同步 | **git subtree**：改了照样能合并上游 |
| 安装依赖一堆步骤 | 看 README 一步步来 | **自动检测**依赖 + 自动注册 MCP |

## 架构

```
ResearchMate
├── config/                          <- 你的配置
│   ├── 7 agents                     架构师、代码审查、论文审稿...
│   ├── 13 rules                     编码规范、GPU 安全、学术诚信...
│   ├── 24 skills                    实验管理、模型开发、论文写作...
│   └── settings.json.template       全局配置模板
│
├── third-party/ (git subtree)       <- 6 个精选工具，独立同步上游
│   ├── Auto-claude-code-research-in-sleep (ARIS)   27 skills · 3 MCP servers — AI 研究自动化
│   ├── autoresearch (Karpathy)      program.md + train.py — 单 GPU 自主 ML 迭代
│   ├── pi-autoresearch              1 skill · 1 extension — 通用自主优化循环
│   ├── academic-research-skills     4 skills (13+12+7-agent) — 13-agent 文献 · 12-agent 写作
│   ├── claude-review-loop           2 commands · 1 stop hook — 代码审查自动化
│   └── claude-scientific-skills     170+ skills · 250+ 数据源 — 科学数据库接入
│
├── install.sh                       curl | bash 远程安装
├── setup.sh                         本地安装（幂等）
├── sync-upstream.sh                 手动同步上游
└── add-tool.sh                      添加新第三方工具
```

## 核心特性

| 特性 | 说明 |
|------|------|
| **一键安装** | `curl` 一行，自动处理依赖、MCP 注册、Plugin 安装 |
| **统一管理** | 你的配置 + 6 个精选第三方工具在一个仓库 |
| **自动同步** | GitHub Actions 每周检查上游 + Claude Haiku 审核 + 自动合并 |
| **自由魔改** | 直接编辑第三方代码，上游更新时 git subtree 自动合并 |
| **研究者专属** | 覆盖论文写作、文献综述、实验管理、代码审查全流程 |
| **冲突检测** | 同名 skill/command 自动按优先级解决，安装时报告 |

## 快速开始

**支持平台**: macOS + Linux (Ubuntu/Debian/Fedora/Arch)

### 一键安装

```bash
# 自动检测 claude 路径
curl -fsSL https://raw.githubusercontent.com/yxbian23/research-mate/main/install.sh | bash
```

### 指定路径安装（Linux 常见场景）

```bash
curl -fsSL https://raw.githubusercontent.com/yxbian23/research-mate/main/install.sh | bash -s -- \
  --claude-path /path/to/claude \
  --codex-path /path/to/codex
```

### 或 clone 安装

```bash
git clone https://github.com/yxbian23/research-mate.git ~/.research-mate
cd ~/.research-mate && ./setup.sh
```

setup.sh 自动完成：备份已有配置 -> symlink 配置文件 -> 安装 skills（含冲突检测）-> 注册 MCP servers -> 安装 plugins -> 提示配置 API keys。

## 集成的第三方工具

### Auto-claude-code-research-in-sleep (ARIS) -- AI 研究自动化引擎
> [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) ![GitHub stars](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat-square)

27 skills, 3 MCP servers (Codex, LLM-chat, MiniMax)。核心亮点：**Claude + GPT 跨模型对抗审查**，避免单一模型盲区。

| 功能 | 命令 | 说明 |
|------|------|------|
| Idea 发现 | `/idea-discovery` | 文献调研 -> 头脑风暴 -> 新颖性验证 -> GPU 实验 |
| 自动审稿 | `/auto-review-loop` | 4 轮迭代，5/10 -> 7.5/10 质量提升 |
| 论文写作 | `/paper-writing` | 叙述 -> 大纲 -> 图表 -> LaTeX -> PDF |
| 实验管理 | `/run-experiment` | 远程 GPU 部署 + 监控 |
| 研究全流程 | `/research-pipeline` | 端到端自动化 |

### academic-research-skills -- 学术全流程系统
> [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) ![GitHub stars](https://img.shields.io/github/stars/Imbad0202/academic-research-skills?style=flat-square)

4 skills（13+12+7-agent 系统）。覆盖文献综述、论文写作、同行评审全流程。

| 模块 | Agent 数 | 能力 |
|------|---------|------|
| Deep Research | 13 agents | PRISMA 文献综述、risk-of-bias 评估 |
| Academic Paper | 12 agents | LaTeX 论文写作、双语摘要 |
| Paper Reviewer | 7 agents | 同行评审模拟（0-100 评分） |
| Pipeline | 10 stages | 学术诚信检查点 |

### claude-scientific-skills -- 科学数据库接入
> [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) ![GitHub stars](https://img.shields.io/github/stars/K-Dense-AI/claude-scientific-skills?style=flat-square)

- 170+ 生产就绪 skills
- 接入 250+ 数据源（PubMed, ChEMBL, UniProt, COSMIC, SEC EDGAR...）
- 19 种论文格式模板（Nature, Science, NeurIPS, ICLR...）

### autoresearch -- Karpathy 自主 ML 实验
> [karpathy/autoresearch](https://github.com/karpathy/autoresearch) ![GitHub stars](https://img.shields.io/github/stars/karpathy/autoresearch?style=flat-square)

program.md + train.py。给 AI agent 一个 GPU，让它自主修改代码、训练、评估、迭代。单文件约束 + 5 分钟预算，12 实验/小时。

### pi-autoresearch -- 通用自主优化循环
> [davebcn87/pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) ![GitHub stars](https://img.shields.io/github/stars/davebcn87/pi-autoresearch?style=flat-square)

1 skill, 1 extension。Domain-agnostic 的自主实验循环：不限于 ML，也可优化 build speed、bundle size、测试速度等。

### claude-review-loop -- 代码审查自动化
> [hamelsmu/claude-review-loop](https://github.com/hamelsmu/claude-review-loop) ![GitHub stars](https://img.shields.io/github/stars/hamelsmu/claude-review-loop?style=flat-square)

2 commands, 1 stop hook。开发完成后自动触发 Codex 独立审查，提供第三方视角的代码质量反馈。

## 功能目录

安装后可用的所有功能，按用途分类：

### 研究自动化

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `/idea-discovery` | Skill | ARIS | 文献调研 -> 新颖性验证 -> GPU 试点 |
| `/research-pipeline` | Skill | ARIS | 端到端：idea -> 实现 -> review -> 投稿 |
| `/autoresearch` | Skill | config | Karpathy 自主 ML 实验 |
| `/autoresearch-loop` | Skill | config | 通用自主优化循环 |
| `/implement-paper` | Command | config | 论文算法转 PyTorch 代码 |
| `/analyze-paper` | Command | config | 深度分析 AI 论文 |
| codex / llm-chat | MCP | ARIS | 跨模型对抗审查 |

### 论文写作

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `/paper-writing` | Skill | ARIS | 叙述 -> LaTeX，支持 ICLR/ICML/NeurIPS |
| academic-paper | Skill | academic-research | 12-agent 写作系统 + 双语摘要 |
| 19 种格式模板 | Skill | scientific-skills | Nature/Science/NeurIPS/ICLR... |
| ai-research-slides | Skill | config | 论文分析 -> 学术演示文稿 |

### 文献综述与审稿

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `/auto-review-loop` | Skill | ARIS | 4 轮 GPT 对抗审稿 |
| deep-research | Skill | academic-research | 13-agent PRISMA 文献综述 |
| academic-paper-reviewer | Skill | academic-research | 7-agent 同行评审（0-100） |
| `/review-paper` | Command | config | ICLR/ICML/NeurIPS 标准审稿 |

### 实验管理与训练

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `/run-experiment` | Skill | ARIS | 远程 GPU 部署 + 监控 |
| `/train` | Command | config | GPU 检查 -> 配置验证 -> 训练启动 |
| `/debug-cuda` | Command | config | CUDA 内存/设备问题诊断 |
| `/ablation` | Command | config | 消融实验设计与对比 |
| gpu-optimization | Skill | config | 混合精度、梯度累积、模型并行 |

### 模型开发

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| transformers-workflow | Skill | config | HuggingFace: LoRA/QLoRA、Trainer API |
| diffusers-workflow | Skill | config | 扩散模型: ControlNet、采样器 |
| unified-generation | Skill | config | 多任务架构、多模态 tokenization |

### 代码审查

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| `/review-loop` | Command | claude-review-loop | Codex 自动独立审查 |
| `/code-review` | Command | config | 代码质量审查 |
| `/test-coverage` | Command | config | 测试覆盖率检查 |
| Stop Hook | Hook | claude-review-loop | 退出时自动触发 Codex review |

### 科学数据库

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| 170+ 科学 skills | Skill | scientific-skills | PubMed, ChEMBL, UniProt 等 250+ 数据源 |

### 文档与办公

| 功能 | 类型 | 来源 | 说明 |
|------|------|------|------|
| pdf / docx / pptx / xlsx | Skill | config | PDF/Word/PPT/Excel 创建编辑分析 |

### 维护更新

| 功能 | 类型 | 说明 |
|------|------|------|
| `/sync-upstream` | Claude Code 内 | 从 Claude Code 内同步上游更新 |
| `/add-tool` | Claude Code 内 | 从 Claude Code 内添加新第三方工具 |
| `/research-mate-update` | Claude Code 内 | 更新 ResearchMate 本身 |
| `sync-upstream.sh` | Shell 脚本 | 手动同步全部或单个工具 |
| `add-tool.sh` | Shell 脚本 | 手动添加新第三方工具 |

### 统计

| 类型 | 数量 | 来源分布 |
|------|------|---------|
| **Skills** | 200+ | config: 24, ARIS: 27, academic: 4, scientific: 170+ |
| **Commands** | 23+ | config: 21, review-loop: 2 |
| **Agents** | 7 | config: 7 |
| **MCP Servers** | 3 | ARIS: codex, llm-chat, minimax |
| **Hooks** | 3 | PreToolUse: 3 (settings.json) |
| **Rules** | 13 | config: 13 |

> 维护命令：`/sync-upstream`、`/add-tool`、`/research-mate-update` 可在 Claude Code 中直接使用。

## 使用指南

### 修改自己的配置
```bash
vim config/rules/my-new-rule.md
git add . && git commit -m "feat: add new rule" && git push
```

### 修改第三方工具
```bash
vim third-party/aris/skills/auto-review-loop/SKILL.md
git add . && git commit -m "feat: customize ARIS" && git push
```

### 同步上游更新
```
# 在 Claude Code 中:
/sync-upstream

# 或通过 shell:
./sync-upstream.sh           # 全部同步
./sync-upstream.sh aris      # 单个同步

# 自动: GitHub Actions 每周一检查 → Claude Haiku 审核 → 自动合并
```

### 添加新工具
```
# 在 Claude Code 中:
/add-tool

# 或通过 shell:
./add-tool.sh <name> <git-url> [branch]
```

### 更新 ResearchMate
```
# 在 Claude Code 中:
/research-mate-update

# 或通过 shell:
cd ~/.research-mate && git pull && ./setup.sh
```

## 依赖

setup.sh 自动检测平台并给出安装提示。

| 依赖 | 必须？ | macOS | Linux (apt) |
|------|--------|-------|-------------|
| Git | 必须 | `xcode-select --install` | `sudo apt install git` |
| Node.js | 必须 | `brew install node` | `sudo apt install nodejs npm` |
| Claude Code | 推荐 | `npm i -g @anthropic-ai/claude-code` | 同左 |
| Codex CLI | ARIS 核心 | `npm i -g @openai/codex` | 同左 |
| jq | review-loop | `brew install jq` | `sudo apt install jq` |
| LaTeX | 论文写作 | `brew install --cask mactex` | `sudo apt install texlive-full` |
| Python 3 | 文献搜索 | `brew install python` | `sudo apt install python3 python3-pip` |
| uv | autoresearch | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | 同左 |
| PyTorch | autoresearch | `pip install torch` | 同左 |

> Linux 也支持 `dnf` (Fedora/RHEL) 和 `pacman` (Arch)，setup.sh 自动检测。

## 和其他方案的对比

| 能力 | everything-claude-code | dot-claude | starter-kit | **ResearchMate** |
|------|:---:|:---:|:---:|:---:|
| 存自己的配置 | ~ | ✅ | ~ | ✅ |
| 集成多个第三方工具 | ❌ | ❌ | ❌ | ✅ (6 个) |
| 各工具独立上游同步 | ❌ | ❌ | ~ (仅一个) | ✅ |
| 本地修改后仍可同步 | ❌ | N/A | ✅ | ✅ |
| 一键新电脑部署 | ✅ | ✅ | ~ | ✅ |
| AI 研究者场景 | ❌ | ❌ | ❌ | ✅ |
| Claude 自动审核同步 PR | ❌ | ❌ | ❌ | ✅ |
| Claude Code 内维护命令 | ❌ | ❌ | ❌ | ✅ |

## 设计原则

1. **一键 > 多步** -- 所有配置一条命令搞定，不需要看文档一步步来
2. **Symlink > Copy** -- 编辑仓库文件立即生效，无需重新安装
3. **你的配置 > 第三方** -- 同名冲突时你的配置永远优先
4. **自动 > 手动** -- 上游同步、冲突检测、依赖检查全部自动化
5. **备份 > 覆盖** -- 已有配置自动备份到 `~/.claude/backup/`，不丢失任何数据

## License

[MIT](LICENSE)

## 致谢

感谢以下优秀项目：

- [autoresearch](https://github.com/karpathy/autoresearch) by [@karpathy](https://github.com/karpathy)
- [pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) by [@davebcn87](https://github.com/davebcn87)
- [Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) by [@wanshuiyin](https://github.com/wanshuiyin)
- [claude-review-loop](https://github.com/hamelsmu/claude-review-loop) by [@hamelsmu](https://github.com/hamelsmu)
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by [@Imbad0202](https://github.com/Imbad0202)
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) by [@K-Dense-AI](https://github.com/K-Dense-AI)
