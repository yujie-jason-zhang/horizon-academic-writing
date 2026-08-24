# Fidelity and TeX Safety

## Purpose

Protect the scientific content while allowing enough freedom for reader-oriented editing.

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

## 4. Mathematics

Unless explicit notation normalization is requested, do not alter mathematical regions.

Protect:

- inline and display math;
- equation environments;
- theorem/proof logic;
- algorithmic expressions;
- signs, subscripts, superscripts, accents, and math fonts.

## 5. TeX Structure

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

## 6. Citations

Preserve citation keys and the relationship between citation placement and claim scope.

Do not independently replace or invent citations unless explicitly requested.

## 7. Terminology

Do not replace technical terms merely for stylistic variety.

For long manuscripts, keep canonical names stable and report obvious term drift.

A full terminology ledger is optional rather than default in Horizon-Afterglow.

## 8. Notation and Numerical Consistency

Check important recurring symbols and values when they are central to the manuscript or show signs of conflict.

Do not silently normalize uncertain conflicts.

If the intended correction cannot be inferred safely:

> `AUTHOR DECISION REQUIRED`

Full notation and numerical ledgers are optional in this profile.

## 9. Preservation Checker

Paths are relative to the skill directory.

Reader-oriented:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

Strict:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex
```

If sentences carrying `\cite` or `\ref` were deliberately reordered, add
`--allow-structural-reorder` to compare keys and counts as a multiset rather than
in document order, then confirm claim attachment by hand. Keys and counts stay
strict under that flag; dropped, added, or duplicated citations still fail. The flag
does not verify semantic claim–citation attachment, so a citation moved to the wrong
claim can still pass the multiset check.

The checker does not replace semantic review.
