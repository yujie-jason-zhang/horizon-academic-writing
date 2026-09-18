# Horizon-Aegis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yujie-jason-zhang/horizon-academic-writing/blob/main/LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-4B5563.svg)](https://agentskills.io)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

An **Agent Skill** for scientific defensibility audits of technical research papers before submission or major revision. **Aegis** is the read-only audit profile in the Horizon academic-writing series.

It treats a paper as a scientific argument: it checks novelty, method and reported-number consistency, claim-evidence alignment, baselines, ablations, and statistical rigor. When implementation artifacts are supplied, it also traces the claimed method through code, configurations, and the path that generated the results.

> **Scope.** Aegis assesses whether the available evidence supports the paper's conclusions and recommends the minimum decisive repairs. It reports findings without editing manuscripts or implementation artifacts. Language polishing, journal selection, rebuttal-letter drafting, and experiment execution are outside its scope.

---

## Contents

- [Why this exists](#why-this-exists)
- [Install](#install)
- [Usage](#usage)
- [The audit report](#the-audit-report)
- [How it works](#how-it-works)
- [Repository layout](#repository-layout)
- [Horizon series](#horizon-series)
- [Profiles](#profiles)
- [Changelog](#changelog)
- [License](#license)

---

## Why this exists

A paper can appear convincing while leaving two important problems unresolved:

1. **Inconsistent methods** — prose, equations, pseudocode, settings, reported numbers, or implementation describe different versions of the method.
2. **Unproven attribution** — the full system works, but the gain may come from extra information, compute, tuning, or a simpler mechanism rather than the claimed contribution.

Aegis separates **effectiveness** from **attribution and necessity**. It evaluates evidence against each actual claim, checks the strongest credible alternative explanation, and asks which minimum repair would resolve the objection. That repair may be a targeted analysis or experiment, a narrower claim, or a reframed contribution.

Missing code limits the audit; it is not itself a manuscript defect. Unreadable sections, unverified literature, and unchecked evidence remain explicitly marked as limits on the assessment.

## Install

### 1. Codex

Install from the skill's GitHub subdirectory:

```text
$skill-installer https://github.com/yujie-jason-zhang/horizon-academic-writing/tree/main/skills/horizon-aegis
```

For a manual installation, copy `skills/horizon-aegis/` into your Codex skills directory. Keep `SKILL.md`, `agents/`, and `references/` together.

Once installed, invoke it explicitly:

```text
$horizon-aegis
```

### 2. Claude Code

For a personal installation:

```bash
git clone https://github.com/yujie-jason-zhang/horizon-academic-writing.git
cp -r horizon-academic-writing/skills/horizon-aegis ~/.claude/skills/
```

For a project-local installation, copy the skill into the project's `.claude/skills/` directory instead.

```text
/horizon-aegis
```

### 3. Web / Desktop

For clients that accept custom skill folders or ZIP archives, package only `skills/horizon-aegis/`. The archive should contain one top-level `horizon-aegis/` folder with `SKILL.md` and its resources, rather than the full repository. Upload or enable it through the client's supported skill interface.

### Requirements

The skill is plain Markdown and has no bundled executable checker or Python dependency. Full audits need tools that can read the supplied manuscript format and retrieve primary literature. Implementation review additionally needs read access to the supplied artifacts. When a capability or source is unavailable, the report identifies what could not be checked.

## Usage

Use normal task requests rather than a rigid command syntax.

### Typical prompts

```text
Audit this manuscript before submission. Which central claims can the evidence defend?
请审查这篇论文的创新性、方法与数值一致性，以及证据是否足以支持结论。
Does this validation show that the method works, or that the proposed module is necessary?
Compare the supplied implementation with the paper and flag scientific mismatches.
Audit the manuscript only; leave implementation checking OFF.
Give me a fast audit: the largest risk, strongest alternative explanation, and minimum repair.
请预演审稿人最有力的质疑，不改写论文，也不要要求与核心论断无关的实验。
```

### Explicit invocation by platform

| Platform | Explicit invocation | Automatic use |
|---|---|---|
| **Codex** | `$horizon-aegis` | When the request matches the skill description |
| **Claude Code** | `/horizon-aegis` | When the request matches the skill description |
| **Other skill clients** | Enable or select the skill as supported | Depends on the host client |

### Modes

| Mode | When it applies | What it does |
|---|---|---|
| **Full audit** (default) | Submission or major-revision review | Builds a claim-evidence matrix and prioritizes major risks and repairs |
| **Fast audit** | You ask for a quick judgment | Returns the largest scientific risk, strongest alternative, minimum repair, and severity without tables |
| **Implementation AUTO** (default) | Artifacts are supplied | Checks paper-to-code fidelity; skips without penalty if no artifacts are available |
| **Implementation ON** | You explicitly request implementation review | Inspects available artifacts and names materials that block verification |
| **Implementation OFF** | You request a manuscript-only audit | Reviews the paper without checking implementation |

### Working with whole manuscripts

Supply the full manuscript and any appendix or supplementary methods. PDF, LaTeX projects, and accessible full-text URLs can be reviewed with the host's reading tools. For implementation review, include the relevant repository snapshot or commit, configurations, evaluation scripts, and available logs or result-generation artifacts.

Aegis inventories the material before drawing conclusions. It inspects project code without running experiment scripts and makes material findings traceable to manuscript locations or artifact paths.

## The audit report

The full report uses a claim-evidence matrix and prioritizes S3/S4 findings. Minor issues are aggregated; sections with no findings are omitted. The default limits are 1,200 words total and six rows per table.

### Checks

| Check | What it assesses |
|---|---|
| Novelty and literature | Verified prior work, structural similarity, and dangerous simple alternatives |
| Methods and numbers | Agreement among prose, equations, figures, settings, tables, and reported improvements |
| Implementation fidelity | Scientific mechanisms, hidden behavior, baseline fairness, and the result-generating path |
| Claim-evidence alignment | Effectiveness, attribution or necessity, and generality or boundary support |
| Validation and ablations | Whether tests distinguish credible explanations under fair conditions |
| Statistical rigor | Repetition, uncertainty, evaluation design, and selection or leakage risks |

### Ratings and limits

Severity runs from **S0-S4**: no issue, presentation, local clarity or reproducibility, important evidence gap, and a threat to the central scientific story. Evidence runs from **E0-E5**, from assertion alone to decisive, claim-matched evidence against the main credible alternatives.

Both scales are calibrated per finding or claim. Unchecked material is marked `Not checked`; evidence not implied by a claim is marked `Not required`. Findings identify the smallest repair that would address the objection, without assuming its result or experimental feasibility.

## How it works

```text
Inventory → Extract claims → Verify prior work → Check methods and numbers
          → Inspect supplied implementation → Map claims to evidence
          → Test alternatives → Calibrate risks → Recommend minimum repairs
```

The claim-evidence matrix organizes the audit. A strong performance table may support effectiveness while offering little support for a causal mechanism. Each conclusion is judged against the evidence it actually requires, with simulation, theory, benchmarks, and hardware evaluated by their role in that claim.

## Repository layout

```text
skills/horizon-aegis/                 # The skill directory to install
├── README.md                        # Installation, usage, and scope
├── SKILL.md                         # Workflow, modes, constraints, output rules
├── agents/
│   └── openai.yaml                  # UI metadata
└── references/
    ├── calibration.md               # Severity and evidence calibration
    ├── implementation-fidelity.md   # Conditional paper-to-code audit
    ├── method-consistency.md        # Methods and reported-number checks
    └── validation-audit.md          # Validation and statistical rigor
```

Reference files load when their audit step is needed. Implementation guidance is conditional; calibration is read before assigning ratings.

## Horizon series

- **Horizon-Ember** — paragraph-focused polishing.
- **Horizon-Afterglow** — balanced manuscript polishing.
- **Horizon-Aurora** — manuscript-level polishing and cross-section consistency review.
- **Horizon-Aegis** — scientific defensibility and evidence auditing.
- **Horizon-Journal-Recommender** — verified target-journal selection.

## Profiles

**Horizon-Aegis** is the **read-only audit** profile of the Horizon series. Choose it when the question is whether the science supports the paper's conclusions. After resolving scientific findings, use the appropriate polishing profile for language editing and Journal Recommender for submission targeting.

## Changelog

See the repository [CHANGELOG.md](https://github.com/yujie-jason-zhang/horizon-academic-writing/blob/main/CHANGELOG.md). Initial public release: **1.0.0**, tagged `horizon-aegis-v1.0.0`.

## License

MIT. See the repository [LICENSE](https://github.com/yujie-jason-zhang/horizon-academic-writing/blob/main/LICENSE).
