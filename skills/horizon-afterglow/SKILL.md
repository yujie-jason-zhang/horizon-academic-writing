---
name: horizon-afterglow
description: Reader-oriented final language polishing for English academic manuscripts, including Chinese-to-English translation plus polishing, with first-class support for LaTeX/TeX source. Use when asked to polish, proofread, copy-edit, or language-edit a paper, abstract, section, or .tex file (润色 / 语言润色) whose research content is already settled, or to reduce AI-sounding academic prose. Preserves claims, numbers, units, citations, math, and protected TeX while improving paragraph logic, information flow, and natural academic voice. Not for novelty assessment, argument redesign, or experiment design.
---

# Horizon-Afterglow

## Objective

Polish a manuscript as a scientific argument, not as a collection of isolated sentences.

Primary goal:

> **Make the paper easier for a scientific reader to follow without changing what the paper claims, measures, proves, compares, or concludes.**

Use this priority order:

1. **Technical fidelity**
2. **Discourse coherence**
3. **Reader clarity**
4. **Natural academic voice**
5. **Surface polish**

Lower-priority improvements must not damage higher-priority ones.

Horizon-Afterglow keeps the full core workflow but deliberately reduces the depth of secondary diagnostics and audits: lighter context model, high-value reader-expectation rules instead of exhaustive sentence diagnostics, concise section heuristics, one global reread, and no exhaustive ledgers by default.

# Core Execution Principle

Use this workflow:

**Understand → lock meaning → diagnose → one integrated rewrite → verify → global reread → targeted repair → optional consistency audit**

Do not stack independent rewrite passes such as:

`generic polish → logic rewrite → humanizer → another polish`

Repeated free rewrites disturb information flow, terminology, emphasis, claim strength, and numerical bindings.

Therefore:

- use one major free rewrite by default;
- combine reader clarity and natural academic style in that rewrite;
- use later passes for verification and local repair;
- do not run a separate full-text humanization pass.

# Scope

Use for:

- final academic English polishing;
- Chinese academic content translated and polished into English;
- TeX manuscript language editing;
- paragraph, section, or manuscript-level polishing;
- source-to-output fidelity checks;
- targeted terminology, notation, or numerical consistency checks.

Do not use as the primary tool for:

- novelty assessment;
- redesigning contributions;
- literature-gap construction;
- experiment design;
- large-scale argument reconstruction;
- citation replacement;
- silently fixing scientific contradictions in the source.

If the scientific argument itself is unstable, upstream reasoning work should be completed first.

# Modes

## 1. Reader-Oriented Polishing — Default

May, when useful:

- split or merge sentences;
- reorder clauses or sentences;
- remove redundancy and empty rhetoric;
- add light transitions supported by the source logic;
- reposition numerical statements.

Scientific semantic bindings must remain unchanged. Reordering a sentence that carries a citation or cross-reference is permitted, but each `\cite`/`\ref` must still attach to the claim it supports; see the checker notes below.

## 2. Strict Token-Preservation Polishing

Use when the user asks for minimal diff or strict surface preservation.

This mode sacrifices some expressive freedom for stronger mechanical preservation.

## 3. Translation + Polishing

Preserve facts, claims, uncertainty, terminology, citations, equations, and numerical relationships while using natural scientific information structure in English.

Do not strengthen ambiguous source relations.

## 4. Verification Mode

Compare original and candidate only. Do not rewrite.

Check major changes in: technical meaning; agency and causality; claim scope and strength; uncertainty; numbers and units; mathematics; citations; protected TeX.

## 5. Consistency Audit Mode

Use when requested or when a long manuscript shows clear signs of inconsistency.

Check terminology, notation, and important numerical relationships. Do not silently normalize uncertain conflicts.

# Main Workflow

## Pass 1 — Understand the Manuscript

For a major section or manuscript, first identify:

- research problem;
- central claim or main purpose;
- major contributions;
- current section purpose;
- main method or reasoning sequence;
- canonical technical terms;
- important recurring notation and quantities.

For each important paragraph, identify what the reader already knows, the paragraph's main function, what new information it must establish, and how it connects to the next step of the argument.

Do not treat a paragraph as an isolated paraphrasing task when broader context is available.

See `references/context_and_workflow.md`.

## Pass 2 — Lock Meaning

Before rewriting, preserve:

- scientific meaning;
- agency and causal direction;
- claim scope, strength, and uncertainty;
- conditions and exceptions;
- value–metric–unit–condition relationships;
- terminology;
- equations;
- citations;
- protected TeX.

See `references/fidelity_and_tex.md`.

## Pass 3 — Unified Diagnosis

Diagnose the main sources of reading difficulty before rewriting.

Prioritize:

1. paragraph function and section progression;
2. sentence-to-sentence cohesion and old-to-new information flow;
3. visibility of the main action and avoidable syntactic load;
4. lexical and phrase precision;
5. misplaced emphasis;
6. repetitive sentence rhythm or decorative parallelism;
7. high-value formulaic or over-formal academic patterns;
8. obvious repeated or inflated claims.

Do not attempt to optimize every possible stylistic dimension in every sentence.

See `references/writing_rules.md`.

## Pass 4 — One Integrated Rewrite

This is the main free rewrite.

Edit in this order:

1. repair paragraph progression and local logic;
2. improve sentence-to-sentence cohesion and information flow;
3. improve lexical and phrase precision where wording is vague, unnatural, or overstated;
4. simplify avoidable syntactic complexity;
5. improve emphasis where it clearly helps comprehension;
6. break nonfunctional repetitive rhythm and decorative parallelism;
7. remove empty or formulaic academic phrasing;
8. polish grammar, punctuation, and concision.

Prefer the clearest and most precise wording that preserves the full technical meaning. `references/writing_rules.md` §4 defines what natural academic voice does and does not mean; apply it here rather than restating it.

## Pass 5 — Technical Fidelity Verification

After the main rewrite, compare source and revision.

Check at least:

- agency and causal direction;
- claim strength and uncertainty;
- conditions and exceptions;
- value–metric–unit–condition bindings;
- terminology;
- citations;
- mathematics;
- protected TeX.

If a readability edit changes technical meaning, repair or revert that location.

Do not regenerate the whole section because of a local fidelity failure.

## Pass 6 — Global Reader Pass

Read the revised section or manuscript continuously.

Check:

- paragraph-to-paragraph continuity;
- whether the section clearly progresses;
- abrupt sentence pairs where a valid relation is under-signaled;
- places where transitions over-explain an already obvious relation;
- repeated explanations or claims;
- abrupt topic shifts;
- obvious voice inconsistency;
- whether important claims drift in strength across sections.

When adjacent sentences feel abrupt, determine whether a real relation exists. If it does, strengthen the connection with a concise bridge or connective. If it does not, do not hide the gap with a transition word.

This is a reader pass, not a second free rewrite.

Use the failure signals in `references/quality_control.md` to decide what needs repair.

## Pass 7 — Targeted Repair

Repair only locations identified by the verification or global reader pass.

Escalate scope as little as possible:

1. delete or revert a problematic edit;
2. repair one sentence;
3. repair one adjacent sentence pair;
4. repair one paragraph;
5. reorganize multiple paragraphs only when the local progression genuinely fails.

Do not regenerate a whole section because of one local problem.

## Pass 8 — Optional Consistency Audit

For long or technically dense manuscripts, or when requested, check recurring terminology, recurring notation, and important values, units, conditions, and table/figure references.

Do not build exhaustive ledgers by default unless the manuscript complexity requires them.

# Handling Long Manuscripts and Whole Files

When the input is a full `.tex` file or a long manuscript rather than a short passage:

1. **Scan the whole source first** for structure, section relationships, canonical terminology, recurring notation, and major claims; then read the active section and the surrounding context needed to edit it safely in depth. Do not perform a full-profile deep read of every paragraph by default.
2. **Never rewrite the preamble.** Leave everything before `\begin{document}` byte-identical: package loads, custom macro definitions, `\newcommand`, journal class options, author blocks.
3. **Work section by section** in source order, carrying forward the canonical terminology and notation identified in Pass 1 so that terms do not drift between chunks.
4. **Write the result to a file rather than pasting a long manuscript into the reply.** Keep the original untouched and write a sibling file, for example `paper_polished.tex`. A whole-manuscript rewrite pasted inline will be truncated.
5. **Run the preservation checker on the file pair** before reporting completion, and report what the checker found.
6. **Leave figures, tables, and `\begin{...}` environments structurally intact.** Caption prose may be polished; the environment, `\label`, column specifications, and cell alignment must not be restructured.

If the manuscript is too long to polish in one turn, polish complete sections at a time and say which sections have been covered so far. Do not silently skip material.

# Hard Constraints

Do not change for stylistic reasons:

- scientific meaning;
- agency;
- causal direction;
- claim scope, strength, or uncertainty;
- theorem/proof logic;
- algorithm steps;
- experimental settings;
- datasets, baselines, or metrics;
- numbers, units, or signs;
- quantity-to-value relationships;
- citations;
- mathematics;
- protected TeX;
- canonical technical meaning.

Do not invent experiments, evidence, mechanisms, causal relations, limitations, or conclusions not supported by the source.

# Soft Preferences

Use only when they improve comprehension:

- active vs. passive voice;
- sentence length;
- nominalization;
- transitions;
- em dashes and semicolons;
- sentence-opening variation;
- clause order;
- parallelism;
- rhythm and cadence.

Do not convert a soft preference into an absolute ban unless the user or target style explicitly requires it.

Note on dashes: dash usage is a style preference, not a preservation property. The preservation checker does not fail a candidate for em dashes. If desired, run its optional `--style-check` to surface dash-heavy prose as an advisory only. Numeric ranges such as `5--10` and `pp.~12--18` remain normal LaTeX and are ignored by that advisory.

# Output Rules

For normal polishing, output:

1. the polished authoritative text or TeX;
2. a brief note only when a genuine ambiguity, source inconsistency, coverage limitation, or author decision matters.

Do not normally output long change logs, PASS reports for every rule, style scorecards, or large checklists that merely prove the workflow ran.

Use structured findings only in Verification or Audit modes.

# Preservation Checker

Paths below are relative to this skill's directory. Adjust the prefix if invoking from elsewhere.

Reader-oriented mode:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

Strict mode:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex
```

Requires Python 3.9+. No third-party dependencies. Exit code `0` means every enabled check passed; `1` means at least one failed.

## Expected findings that are not errors

- **Reordered citations or cross-references.** The structural check compares `\cite`/`\ref` events in document order. If sentences containing them were deliberately reordered during Pass 4, the default run reports a structural FAIL even though nothing was lost. Re-run with `--allow-structural-reorder`, which compares keys and counts as a multiset instead, then manually confirm that each citation still attaches to the claim it supports:

  ```bash
  python3 scripts/check_preservation.py original.tex candidate.tex \
      --reader-oriented --allow-structural-reorder
  ```

  This flag verifies structural inventory only: missing, added, or duplicated keys still fail, but claim–citation attachment is not machine-verified. A citation moved to the wrong claim can therefore pass the multiset check and must be caught by manual semantic review.

- **Numeric order in reader-oriented mode.** Values, units, and signs stay strict, but their document order is relaxed. Verify manually that a moved number kept its metric, condition, dataset, and comparison.

The checker detects syntactic preservation problems. It does not prove semantic fidelity.

# Final Internal Standard

Before delivery, confirm that:

- the main argument is easier to recover than in the source;
- unnecessary sentence complexity has been reduced;
- paragraph flow and sentence-to-sentence cohesion are clear enough for a technical reader;
- connective signaling is sufficient but not excessive;
- wording is precise, natural, and proportional rather than needlessly elevated;
- repetitive rhythm is broken when stylistic, but functional parallelism is preserved;
- major AI-like academic templates have been reduced;
- claims remain proportional to evidence;
- no unintended scientific drift was introduced.

Work through the Final Reader Test in `references/quality_control.md` if any of these is uncertain.

If the prose is technically safe but still unnecessarily difficult to read, polishing is not complete.
