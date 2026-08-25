# Fidelity and TeX Safety

## Contents

- [Purpose](#purpose)
- [1. Claims](#1-claims)
- [2. Agency and Causality](#2-agency-and-causality)
- [3. Numerical Semantic Binding](#3-numerical-semantic-binding)
- [4. Lexical Semantic Drift](#4-lexical-semantic-drift)
- [5. Mathematics](#5-mathematics)
- [6. TeX Structure](#6-tex-structure)
- [7. Citations](#7-citations)
- [8. Terminology](#8-terminology)
- [9. Optional Preservation Checker](#9-optional-preservation-checker)

## Purpose

Protect the scientific content of the target paragraph while allowing enough freedom for reader-oriented editing.

## 1. Claims

Preserve:

- claim object;
- scope;
- strength;
- uncertainty;
- conditions;
- exceptions;
- observation vs. interpretation.

Do not make shifts such as:

- `may improve` → `improves`;
- `suggests` → `demonstrates`;
- `associated with` → `causes`;
- `outperforms on Dataset A` → `outperforms`.

## 2. Agency and Causality

Preserve:

- who performs an action;
- what affects what;
- which component produces which effect;
- procedural order;
- causal direction.

Changing active/passive voice must not change agency.

## 3. Numerical Semantic Binding

In reader-oriented mode preserve:

**value ↔ metric ↔ unit ↔ condition ↔ dataset/method ↔ comparison**

Numerical tokens may move if these relationships remain correct and unambiguous.

Strict mode additionally preserves numerical-token order.

## 4. Lexical Semantic Drift

When replacing words or phrases, verify that the substitution did not change:

- mechanism;
- degree;
- certainty;
- scope;
- causality;
- temporal meaning;
- comparison strength.

Risky examples include:

- `may help` → `improves`;
- `reduces` → `eliminates`;
- `addresses` → `solves`;
- `consistent with` → `confirms`;
- `higher` → `superior`.

## 5. Mathematics

Unless explicit notation normalization is requested, do not alter mathematical regions.

Protect inline and display math, equation environments, theorem/proof logic, algorithmic expressions, signs, subscripts, superscripts, accents, and math fonts.

## 6. TeX Structure

Preserve:

- `\label{...}`;
- `\ref{...}` and `\eqref{...}`;
- citation keys;
- bibliography keys;
- file paths;
- protected custom-command arguments;
- comments;
- verbatim/listing/code-like source.

Do not apply prose punctuation rules inside protected forms.

## 7. Citations

Preserve citation keys and the relationship between citation placement and claim scope.

Do not independently replace or invent citations unless explicitly requested.

If sentence order changes, manually confirm that each citation still attaches to the claim it supports.

## 8. Terminology

Do not replace technical terms merely for stylistic variety.

Within the target paragraph, keep canonical names stable.
If surrounding context provides a canonical term, follow it.
Do not launch a manuscript-wide terminology normalization pass.

## 9. Optional Preservation Checker

Locate the checker relative to the directory containing the skill's `SKILL.md`. Do not assume that the project working directory is the skill directory.

Claude Code reader-oriented mode:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_preservation.py" original.tex candidate.tex --reader-oriented
```

Codex or another Agent Skills client should resolve the installed skill directory and use an absolute path:

```bash
python3 /absolute/path/to/horizon-ember/scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

For strict mode, omit `--reader-oriented`:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_preservation.py" original.tex candidate.tex
```

If sentences carrying citations or cross-references were deliberately reordered, `--allow-structural-reorder` may be used to compare key inventory rather than document order. It does not verify semantic claim–citation attachment.

The checker catches mechanical preservation problems. It does not replace semantic review.
