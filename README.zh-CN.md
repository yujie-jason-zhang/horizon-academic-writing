# Horizon Academic Writing

[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-4B5563.svg)](https://agentskills.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Horizon Academic Writing 是一个持续发展的 Agent Skills 系列，面向严谨、上下文感知的学术写作、同行评审与学术出版工作流。

Horizon 将学术写作视为技术沟通，而不是一般性的文本生成。其 Skills 在改善可读性与工作流质量的同时，着重保护论断、证据、不确定性、数值关系、引文、数学内容和受保护的 LaTeX。

## Skills

| Skill | 状态 | 重点 |
|---|---|---|
| **Horizon-Ember** | 可用 | 聚焦单个段落的学术润色 |
| **Horizon-Afterglow** | 可用 | 均衡、读者导向的论文润色 |
| **Horizon-Aurora** | 测试中 | 穷尽式全文润色与一致性审查 |

`skills/` 目录只收录已经发布的 Skills；测试中和计划中的 Skills 不设置占位目录。

## Horizon-Ember

Horizon-Ember 把一个目标学术段落作为完整的连贯单元进行润色。它改善局部逻辑、句间衔接、准确性、可读性、节奏和自然学术语气，同时保护科学含义与受保护的源文本。

如果提供了相邻段落，Ember 会把它们作为只读上下文，只改写明确指定的目标段落。它有意保持比 Afterglow 更窄的范围：不建立论文级上下文模型，也不执行跨章节一致性审查。

### 模式

| 模式 | 使用场景 |
|---|---|
| **读者导向** | 在确有帮助时重构目标段落内的句子 |
| **严格／最小改动** | 更保守的语言编辑和更强的表层保留 |
| **翻译加润色** | 将一个中文学术段落转换为自然的英文 |
| **核查** | 比较原文与修订稿，不进行改写 |

## Horizon-Afterglow

Horizon-Afterglow 是 Horizon 系列中的均衡型工具。它可以润色英文学术论文，将中文学术文本翻译成英文并润色，也可以直接处理 LaTeX/TeX 源文件。

它主要解决两类常见问题：

1. **表面化文字编辑**：修复了语法，却没有改善段落逻辑和信息流。
2. **过度改写**：文本变得流畅，但论断强度、因果关系、范围、数值绑定或引文附着关系在不知不觉中发生改变。

Afterglow 先进行一次整合式改写，再执行保真核查、全局读者通读和定点修复。它不评估创新性、不重新设计贡献、不构建文献缺口，也不修复科学论证本身尚不稳定的论文。

### 模式

| 模式 | 使用场景 |
|---|---|
| **读者导向** | 一般学术润色，必要时重构段落和句子 |
| **严格 token 保留** | 最小差异编辑和更强的机械保真 |
| **翻译加润色** | 将中文学术文本转换为自然英文，但不强化原文含义 |
| **核查** | 比较原文与修订稿，不进行改写 |
| **一致性审查** | 检查术语、符号、数值关系和引用 |

## 安装

### Codex

使用内置 Skill 安装器，从 GitHub 子目录安装所需 Skill：

```text
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-ember
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-afterglow
```

安装后，当请求与 Skill 描述匹配时，Codex 可以自动选择相应 Skill；也可以显式调用：

```text
$horizon-ember
$horizon-afterglow
```

### Claude Code

克隆仓库，并将 Skill 目录复制到个人 Skills 目录：

```bash
git clone https://github.com/yujie-jason-zhang/horizon-academic-writing.git
cp -r horizon-academic-writing/skills/horizon-ember ~/.claude/skills/
cp -r horizon-academic-writing/skills/horizon-afterglow ~/.claude/skills/
```

只需复制自己需要的 Skill。若要在单个项目中安装，请改用项目内的 `.claude/skills/` 目录。

可以通过 `/horizon-ember` 显式调用 Ember，也可以让 Claude 根据请求自动选择。可选文件 `agents/openai.yaml` 用于 OpenAI 界面元数据；Claude Code 使用共用的 `SKILL.md`、references 和 scripts，不依赖该元数据文件。

### 支持 Skill 文件夹或 ZIP 的客户端

如果客户端接受 Skill 文件夹或 ZIP，只打包 `skills/` 下所选的 Skill 目录。压缩包内应包含一个顶层 Skill 目录，其中含有 `SKILL.md`、`agents/`、`references/` 和 `scripts/`，而不是整个仓库。

同一份 Horizon-Ember 目录可以同时安装到 Codex 和 Claude Code，不需要维护不同平台的副本。

Skill 本身由 Markdown 构成。可选保真检查器要求 Python 3.9 或更高版本，不依赖第三方包。

## 使用示例

直接用自然语言描述任务即可，无需固定命令格式。

```text
Polish this paragraph for journal submission.
润色这一段论文，保持技术含义不变。
Use the surrounding paragraphs as context, but rewrite only the target paragraph.
Polish the Methods section of this paper.
帮我润色这篇论文的引言部分。
Language-edit main.tex for journal submission. Keep the diff minimal.
Translate this Chinese abstract into English and polish it.
Fix the AI-sounding voice without changing any claims.
Check whether this revision changed any numbers, citations, or equations.
```

## 保真检查器

`check_preservation.py` 比较原始文本和候选文本，报告受保护层中的变化。它能够发现机械性丢失，但不能证明语义完全保真，也不能取代仔细的差异审查。

```bash
# 单段润色
python3 skills/horizon-ember/scripts/check_preservation.py \
  original.tex polished.tex --reader-oriented

# 读者导向润色
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex --reader-oriented

# 严格 token 保留
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex

# 多文件 LaTeX 项目
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  main.tex polished_main.tex --project --reader-oriented
```

检查器覆盖受保护的 TeX 结构、引文键和交叉引用键、数学内容、数值绑定、占位符键、硬编码编号以及引用名称风格。运行 `--help` 可以查看全部模式和参数。

## Ember 的工作流程

```text
理解段落 → 锁定含义 → 诊断局部信息流
         → 一次整合式改写 → 核查
         → 段落通读 → 定点修复
```

Ember 始终以段落为编辑单位：句子修改服务于整个段落，相邻文本只作为上下文。

## Afterglow 的工作流程

```text
理解 → 锁定含义 → 诊断 → 一次整合式改写
     → 核查 → 全局读者通读 → 定点修复 → 可选一致性审查
```

其优先级按以下顺序排列：

1. 技术保真
2. 语篇连贯
3. 读者理解清晰度
4. 自然的学术语气
5. 表层语言优化

低优先级的改进不得损害高优先级目标。

## 仓库结构

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CHANGELOG.md
└── skills/
    ├── horizon-ember/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── references/
    │   │   ├── fidelity_and_tex.md
    │   │   └── paragraph_writing.md
    │   └── scripts/
    │       └── check_preservation.py
    └── horizon-afterglow/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── context_and_workflow.md
        │   ├── fidelity_and_tex.md
        │   ├── quality_control.md
        │   └── writing_rules.md
        └── scripts/
            └── check_preservation.py
```

每个已发布的 Skill 都直接位于 `skills/` 下，其目录名称与 `SKILL.md` frontmatter 中的 `name` 一致。

## 版本管理

仓库使用 Skill 范围的语义化版本标签：

```text
horizon-ember-v1.0.0
horizon-afterglow-v1.0.0
```

随着 Horizon Skills 数量增加，这种方式可以让每次发布保持清晰明确。

## 变更日志

参见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT。参见 [LICENSE](LICENSE)。
