# Horizon Academic Writing

[![中文](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87-red.svg)](README.zh-CN.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-4B5563.svg)](https://agentskills.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A growing family of agent skills for rigorous, context-aware academic writing, peer review, and scholarly publishing workflows.

Horizon treats scholarly writing as technical communication rather than generic prose generation. Its skills are designed to improve readability and workflow quality while preserving claims, evidence, uncertainty, numerical relationships, citations, mathematics, and protected LaTeX.

## Skills

| Skill | Status | Focus |
|---|---|---|
| **Horizon-Ember** | Available | Focused, paragraph-level academic polishing |
| **Horizon-Afterglow** | Available | Balanced, reader-oriented manuscript polishing |
| **Horizon-Aurora** | Available | Manuscript-level polishing, cross-section claim alignment, and final fidelity checks |
| **Horizon-Aegis** | Available | Scientific defensibility, evidence, and implementation audits |
| **Horizon-Journal-Recommender** | Available | Verified target-journal shortlisting and fit checks |

Only released skills are included in `skills/`; testing and planned skills do not have placeholder directories.

## Horizon-Ember

Horizon-Ember polishes one target academic paragraph as a coherent unit. It improves local logic, sentence-to-sentence cohesion, precision, readability, rhythm, and natural academic voice while preserving scientific meaning and protected source material.

If surrounding paragraphs are supplied, Ember uses them as read-only context and rewrites only the identified target paragraph. It is intentionally narrower than Afterglow: it does not build a manuscript-wide context model or run cross-section consistency audits.

### Modes

| Mode | Use case |
|---|---|
| **Reader-oriented** | Paragraph polishing with sentence restructuring when useful |
| **Strict / minimal-diff** | Conservative language editing with stronger surface preservation |
| **Translation + polishing** | One Chinese academic paragraph to natural English |
| **Verification** | Compare an original and revision without rewriting |

## Horizon-Afterglow

Horizon-Afterglow is the balanced profile in the Horizon family. It polishes English academic manuscripts, translates and polishes Chinese academic text into English, and works directly with LaTeX/TeX source.

It addresses two common failure modes:

1. **Cosmetic copy-editing** that fixes grammar but leaves paragraph logic and information flow unchanged.
2. **Overenthusiastic rewriting** that produces fluent prose while quietly changing claim strength, causality, scope, numerical bindings, or citation attachment.

Afterglow uses one integrated rewrite followed by fidelity verification, a global reader pass, and targeted repair. It does not assess novelty, redesign contributions, construct literature gaps, or repair a scientifically unstable argument.

Version 1.1.0, **Cinderella**, adds claim-forward framing: supported points should be stated directly when possible, while evidence-required hedges, limitations, boundary conditions, and scientifically meaningful negative formulations remain protected.

### Modes

| Mode | Use case |
|---|---|
| **Reader-oriented** | General academic polishing with paragraph and sentence restructuring when useful |
| **Strict token-preservation** | Minimal-diff editing with stronger mechanical preservation |
| **Translation + polishing** | Chinese academic source to natural English without semantic strengthening |
| **Verification** | Compare an original and revision without rewriting |
| **Consistency audit** | Check terminology, notation, numerical relationships, and references |

## Horizon-Aurora

Horizon-Aurora is the manuscript-level polishing profile in the Horizon family. It polishes English academic manuscripts, translates Chinese academic text into English, and works directly with LaTeX/TeX projects.

It addresses two manuscript-level failure modes:

1. **Isolated local edits** that improve individual passages while terminology, claim strength, or scope drifts across sections.
2. **Incomplete final verification** that checks an intermediate revision but leaves later repairs or included files unverified.

Aurora uses one integrated rewrite followed by fidelity verification, a global reader and claim-alignment pass, targeted repair, a focused consistency audit, and final verification. It preserves scientific meaning and does not assess novelty, redesign contributions, or repair a scientifically unstable argument.

Version 1.0.0 includes section-specific guidance, independent source and candidate project handling, and explicit full/partial coverage reporting. Its checker supports preamble and table protection, registered custom macros, and translation-aware quantity checks with documented manual-review boundaries.

### Modes

| Mode | Use case |
|---|---|
| **Reader-oriented** | Manuscript polishing with paragraph progression and cross-section claim alignment |
| **Strict token-preservation** | Minimal-diff editing with stronger mechanical preservation |
| **Translation + polishing** | Chinese academic source to natural English without semantic strengthening |
| **Verification** | Compare an original and revision without rewriting |
| **Consistency audit** | Check terminology, notation, numerical relationships, and recurring claims |
| **Diagnosis only** | Identify high-impact readability and fidelity problems without rewriting |

## Horizon-Aegis

Horizon-Aegis audits whether a technical paper's conclusions can withstand a skeptical reviewer before submission or major revision. It checks novelty against verified prior work, consistency across methods and reported numbers, claim-evidence alignment, baselines, ablations, and statistical rigor.

Its central distinction is **effectiveness versus attribution or necessity**: a method can work without establishing that the claimed contribution caused the improvement or was needed. Aegis evaluates each claim separately, identifies credible alternative explanations, and recommends the minimum decisive evidence, claim narrowing, or contribution reframing.

When implementation artifacts are available, it traces the manuscript specification through code, configurations, and the result-generating path. Missing code limits the audit; it is not itself a manuscript defect. Findings use severity levels S0-S4 and evidence levels E0-E5, with source locations and explicit limits on what was checked.

Aegis is read-only: it returns an assessment and repair recommendations. Language polishing belongs to Ember, Afterglow, or Aurora; target-journal selection belongs to Journal Recommender. Aegis does not draft rebuttal letters or run experiments.

### Modes

| Mode | Use case |
|---|---|
| **Full audit** | Scientific defensibility review with a claim-evidence matrix and prioritized repairs |
| **Fast audit** | Brief judgment of the largest risk, strongest alternative explanation, and minimum repair |
| **Implementation AUTO / ON / OFF** | Check supplied artifacts automatically, explicitly request implementation review, or audit the manuscript only |

## Horizon-Journal-Recommender

Horizon-Journal-Recommender builds evidence-backed submission shortlists for finished or near-finished manuscripts. It profiles the paper, filters a broad candidate pool, live-verifies the finalists, and ranks them as Reach, Core, and Backup targets.

Every recommended journal must be checked against official scope, current indexing and submission constraints, and recent related papers. OA/APC and review-speed claims remain source-attributed and explicitly uncertain when they cannot be verified.

### Modes

| Mode | Use case |
|---|---|
| **Recommendation** | Generate and rank a verified journal shortlist |
| **Verification** | Check an existing shortlist or journal-fit claim |
| **Single-journal fit** | Evaluate one named journal in depth |

## Install

### Codex

Ask the built-in installer to install a skill from its GitHub subdirectory:

```text
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-ember
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-afterglow
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-aurora
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-aegis
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-journal-recommender
```

After installation, Codex can select the appropriate skill automatically when a request matches its description. You can also invoke one explicitly:

```text
$horizon-ember
$horizon-afterglow
$horizon-aurora
$horizon-aegis
$horizon-journal-recommender
```

### Claude Code

Clone the repository and copy the skill directory into your personal skills directory:

```bash
git clone https://github.com/yujie-jason-zhang/horizon-academic-writing.git
cp -r horizon-academic-writing/skills/horizon-ember ~/.claude/skills/
cp -r horizon-academic-writing/skills/horizon-afterglow ~/.claude/skills/
cp -r horizon-academic-writing/skills/horizon-aurora ~/.claude/skills/
cp -r horizon-academic-writing/skills/horizon-aegis ~/.claude/skills/
cp -r horizon-academic-writing/skills/horizon-journal-recommender ~/.claude/skills/
```

Copy only the skill or skills you want. For a project-local installation, use the project's `.claude/skills/` directory instead.

Invoke a skill explicitly with `/horizon-ember`, `/horizon-afterglow`, `/horizon-aurora`, `/horizon-aegis`, or `/horizon-journal-recommender`, or let Claude select it from the request. The optional `agents/openai.yaml` files supply OpenAI UI metadata; Claude Code uses the shared `SKILL.md` and bundled resources and does not require that metadata.

### Packaged-skill clients

For clients that accept a skill folder or ZIP archive, package only the selected directory under `skills/`. The archive should contain a single top-level skill directory with `SKILL.md` and its applicable `agents/`, `references/`, or `scripts/` resources—not the entire repository.

The same skill directory can be installed in Codex and Claude Code; separate platform-specific copies are not required.

The skill itself is Markdown. Its optional preservation checker requires Python 3.9 or later and has no third-party dependencies.

## Usage

Use ordinary task requests; no rigid command syntax is required.

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
Audit this manuscript before submission: which central claims can the evidence defend?
请审查这篇论文的创新性、方法与数值一致性，以及证据是否足以支持结论。
Compare the supplied implementation with the paper and flag mismatches that affect its claims.
Give me a fast scientific audit without rewriting the manuscript.
Recommend and verify target journals for this manuscript.
请根据这篇论文推荐投稿期刊，并核实收录、OA/APC 和近期相关论文。
Check whether this journal is a realistic submission target for my paper.
```

## Preservation checker

`check_preservation.py` compares an original with a candidate and reports changes in the protected layer. It catches mechanical loss; it does not prove semantic fidelity or replace a careful diff review.

```bash
# One-paragraph polishing
python3 skills/horizon-ember/scripts/check_preservation.py \
  original.tex polished.tex --reader-oriented

# Reader-oriented polishing
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex --reader-oriented

# Strict token preservation
python3 skills/horizon-afterglow/scripts/check_preservation.py \
  original.tex polished.tex

# Aurora: multi-file LaTeX project with independent source/candidate copies
python3 skills/horizon-aurora/scripts/check_preservation.py \
  original/main.tex candidate/main.tex --project --reader-oriented
```

The checkers compare protected TeX structures, citation and reference keys, mathematics, and recognized numerical tokens. Semantic numerical bindings still require manual review. Aurora reports placeholder keys, hard-coded numbering, and reference-name style as advisories; it also provides `--protect-command NAME=N` and `--translation` with explicit manual-review boundaries. Run a checker's `--help` for its modes and flags.

Run Aurora's bundled regression tests with `python3 skills/horizon-aurora/scripts/test_check_preservation.py`.

## How Ember works

```text
Understand paragraph → Lock meaning → Diagnose local flow
                     → One integrated rewrite → Verify
                     → Paragraph reread → Targeted repair
```

Ember keeps the paragraph as the editing unit: sentences are changed in service of the paragraph, while surrounding text remains context only.

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

## How Aurora works

```text
Understand globally → Lock meaning → Diagnose → One integrated rewrite
    → Verify fidelity → Global reader and claim-alignment pass
    → Targeted repair → Focused consistency audit → Final verification
```

Aurora carries manuscript context across sections and verifies the final delivery after all repairs. It reports full or partial coverage according to the material actually reviewed, edited, and verified.

## How Aegis works

```text
Inventory manuscript and artifacts → Extract core claims → Verify prior work
    → Check methods and numbers → Inspect implementation when supplied
    → Map claims to evidence → Calibrate risks → Recommend minimum repairs
```

The audit distinguishes observed defects from unchecked material and tests only the evidence requirements implied by each claim. Its report prioritizes major scientific risks; it does not treat additional experiments as the only path to repair.

## Repository layout

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
    ├── horizon-afterglow/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── references/
    │   │   ├── context_and_workflow.md
    │   │   ├── fidelity_and_tex.md
    │   │   ├── quality_control.md
    │   │   └── writing_rules.md
    │   └── scripts/
    │       └── check_preservation.py
    ├── horizon-aurora/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── references/
    │   │   ├── context_and_workflow.md
    │   │   ├── fidelity_and_tex.md
    │   │   ├── quality_control.md
    │   │   ├── section_guidance.md
    │   │   └── writing_rules.md
    │   └── scripts/
    │       ├── check_preservation.py
    │       └── test_check_preservation.py
    ├── horizon-aegis/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       ├── calibration.md
    │       ├── implementation-fidelity.md
    │       ├── method-consistency.md
    │       └── validation-audit.md
    └── horizon-journal-recommender/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            └── journal_recommendation_guide.md
```

Each released skill lives directly under `skills/`, and its directory name matches the `name` in its `SKILL.md` frontmatter.

## Versioning

The repository uses skill-scoped semantic version tags:

```text
horizon-ember-v1.0.0
horizon-afterglow-v1.1.0
horizon-aegis-v1.0.0
horizon-journal-recommender-v1.0.0
```

This keeps releases unambiguous as more Horizon skills are added.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
