# Horizon Academic Writing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-4B5563.svg)](https://agentskills.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A growing family of agent skills for rigorous, context-aware academic writing, peer review, and scholarly publishing workflows.

Horizon treats scholarly writing as technical communication rather than generic prose generation. Its skills are designed to improve readability and workflow quality while preserving claims, evidence, uncertainty, numerical relationships, citations, mathematics, and protected LaTeX.

## Skills

| Skill | Status | Focus |
|---|---|---|
| **Horizon-Ember** | Planned | Focused, paragraph-level academic polishing |
| **Horizon-Afterglow** | Available | Balanced, reader-oriented manuscript polishing |
| **Horizon-Aurora** | Planned | Exhaustive manuscript-level polishing and consistency review |

Only released skills are included in `skills/`; planned skills do not have placeholder directories.

## Horizon-Afterglow

Horizon-Afterglow is the balanced profile in the Horizon family. It polishes English academic manuscripts, translates and polishes Chinese academic text into English, and works directly with LaTeX/TeX source.

It addresses two common failure modes:

1. **Cosmetic copy-editing** that fixes grammar but leaves paragraph logic and information flow unchanged.
2. **Overenthusiastic rewriting** that produces fluent prose while quietly changing claim strength, causality, scope, numerical bindings, or citation attachment.

Afterglow uses one integrated rewrite followed by fidelity verification, a global reader pass, and targeted repair. It does not assess novelty, redesign contributions, construct literature gaps, or repair a scientifically unstable argument.

### Modes

| Mode | Use case |
|---|---|
| **Reader-oriented** | General academic polishing with paragraph and sentence restructuring when useful |
| **Strict token-preservation** | Minimal-diff editing with stronger mechanical preservation |
| **Translation + polishing** | Chinese academic source to natural English without semantic strengthening |
| **Verification** | Compare an original and revision without rewriting |
| **Consistency audit** | Check terminology, notation, numerical relationships, and references |

## Install

### Codex

Ask the built-in installer to install the skill from its GitHub subdirectory:

```text
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-afterglow
```

After installation, Codex can select the skill automatically when a request matches its description. You can also invoke it explicitly:

```text
$horizon-afterglow
```

### Claude Code

Clone the repository and copy the skill directory into your personal skills directory:

```bash
git clone https://github.com/yujie-jason-zhang/horizon-academic-writing.git
cp -r horizon-academic-writing/skills/horizon-afterglow ~/.claude/skills/
```

For a project-local installation, copy it to `.claude/skills/` instead.

### Packaged-skill clients

For clients that accept a skill folder or ZIP archive, package only `skills/horizon-afterglow/`. The archive should contain a top-level `horizon-afterglow/` directory with `SKILL.md`, `references/`, `scripts/`, and `agents/` inside it—not the entire repository.

The skill itself is Markdown. Its optional preservation checker requires Python 3.9 or later and has no third-party dependencies.

## Usage

Use ordinary task requests; no rigid command syntax is required.

```text
Polish the Methods section of this paper.
帮我润色这篇论文的引言部分。
Language-edit main.tex for journal submission. Keep the diff minimal.
Translate this Chinese abstract into English and polish it.
Fix the AI-sounding voice without changing any claims.
Check whether this revision changed any numbers, citations, or equations.
```

## Preservation checker

`check_preservation.py` compares an original with a candidate and reports changes in the protected layer. It catches mechanical loss; it does not prove semantic fidelity or replace a careful diff review.

```bash
# Reader-oriented polishing
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex --reader-oriented

# Strict token preservation
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex

# Multi-file LaTeX project
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  main.tex polished_main.tex --project --reader-oriented
```

The checker covers protected TeX structures, citation and reference keys, mathematics, numerical bindings, placeholder keys, hard-coded numbering, and reference-name style. Run it with `--help` for all modes and flags.

## How Afterglow works

```text
Understand → Lock meaning → Diagnose → One integrated rewrite
           → Verify → Global reader pass → Targeted repair → Optional audit
```

Its priorities are ordered deliberately:

1. Technical fidelity
2. Discourse coherence
3. Reader clarity
4. Natural academic voice
5. Surface polish

A lower-priority improvement must never damage a higher-priority one.

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
└── skills/
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

Each released skill lives directly under `skills/`, and its directory name matches the `name` in its `SKILL.md` frontmatter.

## Versioning

The repository uses skill-scoped semantic version tags:

```text
horizon-afterglow-v1.0.0
```

This keeps releases unambiguous as more Horizon skills are added.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
