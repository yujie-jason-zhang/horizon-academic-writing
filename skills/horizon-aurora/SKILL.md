---
name: horizon-aurora
description: Manuscript-level academic polishing for English research papers and Chinese-to-English academic translation, with first-class LaTeX/TeX support. Use when asked to polish, proofread, copy-edit, language-edit, or reduce AI-sounding prose in a research manuscript whose scientific content is substantially settled. Reads the manuscript globally before editing, improves section and paragraph progression, reader expectations, claim-forward framing, lexical precision, and natural academic voice, while preserving claims, uncertainty, numbers, units, citations, mathematics, experimental settings, and protected TeX. Not for novelty assessment, contribution redesign, literature-gap construction, or experiment design.
---

# Horizon-Aurora

## Objective

Treat the manuscript as a scientific argument rather than a collection of sentences.

Primary objective:

> **Make the scientific argument easier to recover, more precise, and more natural to read without changing what the paper actually claims, measures, proves, compares, or concludes.**

Priority order:

1. **Technical fidelity**
2. **Argument and discourse coherence**
3. **Reader-facing clarity**
4. **Natural academic voice**
5. **Surface polish**

A lower-priority improvement must never damage a higher-priority one.

## Core Execution Principle

Use this workflow:

**Understand globally → lock scientific meaning → diagnose selectively → one integrated rewrite → fidelity verification → global reader pass → targeted repair → focused consistency audit → final verification**

Do not stack independent free rewrites such as:

`generic polish → logic rewrite → humanizer → polish again`

Repeated rewriting can damage topic chains, terminology, numerical bindings, claim strength, and uncertainty.

Therefore:

- use one major free rewrite by default;
- integrate reader expectations, natural style, and claim-forward framing inside that rewrite;
- use later passes mainly for verification and local repair;
- do not run a separate full-manuscript “humanization” pass.

# Scope

Use for:

- final academic English polishing;
- Chinese-to-English academic translation plus polishing;
- TeX/LaTeX manuscript language editing;
- paragraph, section, and full-manuscript polishing;
- source-to-output fidelity checking;
- cross-section claim-alignment review;
- targeted terminology, notation, and numerical consistency checks.

Do not use as the primary tool for:

- novelty assessment;
- contribution redesign;
- literature-gap construction;
- experiment design;
- large-scale scientific storyline reconstruction;
- independent citation replacement;
- silently repairing scientific contradictions already present in the source.

If the research argument itself is unstable, upstream scientific reasoning should be completed first.

# Hard Constraints

Do not change for stylistic reasons:

- scientific meaning;
- agency;
- causality;
- claim strength, scope, or uncertainty;
- theorem or proof logic;
- algorithm steps;
- experimental settings;
- baselines, datasets, metrics, or evaluation conditions;
- numbers, units, signs, or quantity-to-value relationships;
- citation keys or what a citation is presented as supporting;
- mathematics;
- protected TeX;
- canonical technical meaning.

Do not invent:

- experiments;
- evidence;
- mechanisms;
- causal relations;
- limitations;
- conclusions;
- citations.

# Modes

## 1. Reader-Oriented Polishing — Default

May, when useful:

- split or merge sentences;
- reorder prose-only clauses or sentences;
- remove redundancy and empty rhetoric;
- repair paragraph progression;
- add the minimum cohesive signaling needed for a genuine source-supported relation;
- reposition numerical statements when their semantic bindings remain unambiguous.

All scientific bindings must remain unchanged.

## 2. Strict Token-Preservation Polishing

Use when the user requests minimal diff, conservative copy-editing, or strong surface preservation.

This mode sacrifices some expressive freedom for stronger mechanical preservation.

## 3. Translation + Polishing

Preserve facts, claims, uncertainty, terminology, citations, mathematics, and numerical relationships while expressing them through natural scientific information structure in English.

Do not turn an ambiguous source relation into a stronger causal or argumentative relation.

For mechanical source-to-translation comparison, add `--translation` to the reader-oriented checker command. This keeps digits, recognized units/signs, math, and protected TeX strict, but leaves Han numerals, spelled-out numbers, and contextual Roman number words to bilingual semantic review. Manually verify every word-based quantity and translated unit expression. See `references/fidelity_and_tex.md`; a mechanical PASS alone is insufficient for translation fidelity.

## 4. Verification Mode

Compare source and candidate only. Do not rewrite.

Check:

- scientific meaning;
- agency and causal direction;
- claim scope, strength, and uncertainty;
- conditions and exceptions;
- numerical semantic bindings;
- terminology;
- citations;
- mathematics;
- protected TeX.

## 5. Consistency Audit Mode

Check only. Do not freely rewrite.

Focus on high-impact conflicts in:

- terminology;
- notation;
- important values, units, conditions, datasets, and methods;
- repeated major claims across Abstract, Introduction, Results, Discussion, and Conclusion.

Do not silently normalize uncertain conflicts.

## 6. Diagnosis Only

Diagnose the main reader-facing and fidelity risks without producing rewritten prose.

Report only high-value findings: location, issue, reader cost, and repair direction. Do not produce an exhaustive sentence-by-sentence scorecard.

# Workflow

## Pass 1 — Global Manuscript Context

For a major section or full manuscript, do not start by polishing Sentence 1.

Build a compact manuscript context model covering:

- research problem;
- central purpose or main claim;
- major contributions;
- method or reasoning sequence;
- section purposes;
- major claim–evidence relationships;
- canonical terminology;
- recurring notation and protected quantities;
- the manuscript’s local scientific voice.

For full manuscripts, first scan the whole source, then read the active section and the context it depends on in depth.

For important paragraphs, determine:

- what the reader already knows;
- the paragraph’s dominant function;
- what new information it must establish;
- what the next reasoning step needs from it.

Do not build an exhaustive graph of every sentence. Escalate depth only when distant sections materially constrain the edit.

See `references/context_and_workflow.md`.

## Pass 2 — Fidelity Baseline

Before rewriting, lock:

- claim object, scope, strength, uncertainty, conditions, and exceptions;
- agency and causal direction;
- value–metric–unit–condition–dataset/method relationships;
- terminology;
- equations and mathematical regions;
- citations and their claim scope;
- protected TeX.

See `references/fidelity_and_tex.md`.

## Pass 3 — Selective Unified Diagnosis

Diagnose before rewriting. Prioritize high-cost problems rather than optimizing every sentence equally.

Check, in this order:

1. **Argument** — section progression, paragraph function, major claim–evidence fit;
2. **Flow** — old-to-new information, topic continuity, under- or over-signaled relations;
3. **Sentence** — visible main action, subject–verb distance, cognitive load, emphasis;
4. **Language** — lexical and phrase precision, collocation, disciplinary register, evidence-proportional wording;
5. **Voice** — formulaic academic patterns, repetitive rhythm, decorative symmetry, redundant defensive framing.

Use section-specific expectations rather than forcing every section into the same rhetorical template.

See:

- `references/writing_rules.md`
- `references/section_guidance.md`

## Pass 4 — One Integrated Rewrite

This is the only major free rewrite in the default workflow.

Edit in this order:

1. repair paragraph and section progression;
2. improve sentence-to-sentence cohesion and information flow;
3. make supported claims more direct when they are buried under redundant defensive framing;
4. improve lexical and phrase precision;
5. simplify avoidable syntactic complexity;
6. improve emphasis where it materially helps comprehension;
7. break nonfunctional repetitive rhythm and decorative parallelism;
8. remove empty or formulaic academic language;
9. polish grammar, punctuation, and concision.

Claim-forward framing is **not** claim strengthening. Preserve all evidence-required hedges, limitations, boundary conditions, and qualifications.

Prefer the simplest structure that expresses the full technical meaning accurately.

## Pass 5 — Technical Fidelity Verification

After rewriting, compare source and revision before any further stylistic repair.

Check at least:

- agency and causal direction;
- claim strength, scope, and uncertainty;
- conditions and exceptions;
- value–metric–unit–condition bindings;
- comparison scope;
- terminology;
- citation attachment;
- mathematics;
- protected TeX.

Also review risky lexical shifts in mechanism, degree, certainty, scope, causality, temporal meaning, and comparison strength. Examples include:

- `address` → `solve`;
- `suggest` → `demonstrate`;
- `reduce` → `eliminate`;
- `higher` → `superior`.

If a readability edit changed technical meaning, repair or revert that location. Do not regenerate the whole section.

When file access permits, run the preservation checker described below. Mechanical checks are signals, not semantic proofs.

## Pass 6 — Global Reader and Claim-Alignment Pass

Read the revised material continuously.

Check three scopes:

### Between paragraphs

- continuity;
- justified topic shifts;
- abrupt adjacent pairs;
- unnecessary transitions where referential or structural continuity is already sufficient.

### Across the section

- section progression;
- repeated claims or explanations;
- density and pacing;
- voice consistency;
- whether the section fulfills its scientific function.

### Across the manuscript

For major claims only, compare how they appear in:

- Abstract;
- Introduction;
- Results;
- Discussion;
- Conclusion.

Flag meaningful drift in:

- strength;
- scope;
- certainty;
- comparison set;
- causal interpretation.

Do not perform a second free rewrite. Repair only the locations that fail.

Use the failure signals in `references/quality_control.md` to select repairs.

## Pass 7 — Targeted Repair

Escalate scope as little as possible:

1. delete or revert a problematic edit;
2. repair one phrase or sentence;
3. repair one adjacent sentence pair;
4. repair one paragraph;
5. reorganize multiple paragraphs only when local progression genuinely fails.

Do not regenerate a whole section because of one local problem.

## Pass 8 — Focused Consistency Audit

For full, long, or technically dense manuscripts, perform a focused consistency check on recurring high-impact items.

Track only what materially affects interpretation:

- canonical technical terms;
- recurring symbols and frame conventions;
- important parameter values and units;
- experimental conditions;
- table/figure references;
- major claims that recur across sections.

Build a compact temporary ledger when needed, but do not create exhaustive inventories by default.

If the source itself is inconsistent, report the conflict rather than silently selecting one version.

## Final Delivery Verification

After all repairs and consistency edits, compare the actual delivery files against the unchanged source baseline. Repeat the semantic fidelity check for repaired passages and run the preservation checker on the final file pair or project pair when file access permits. An earlier PASS does not cover later edits.

Repair introduced preservation failures before delivery. Report source problems, unresolved project traversal, and unverified custom macros as limitations; do not change protected source merely to silence a checker. If files cannot be checked mechanically, say so briefly and perform the available source-to-output comparison.

Use the Final Reader Test in `references/quality_control.md` before delivery. Any subsequent edit requires another check of the affected content.

# Section-Aware Editing

Different sections owe the reader different things. Use `references/section_guidance.md`.

At minimum:

- **Abstract:** problem/action/result/conclusion must remain evidence-proportional;
- **Introduction:** gap, consequence, present study, and contributions should form a recoverable progression;
- **Related Work:** synthesize conceptual distinctions rather than serially listing papers;
- **Methods:** prioritize dependency order, referential clarity, mechanism relationships, and reproducibility;
- **Results/Experiments:** keep observation separate from interpretation and avoid generalizing beyond the tested setting;
- **Discussion:** preserve the boundary between evidence, interpretation, possible mechanism, implication, and limitation;
- **Conclusion:** do not introduce new mechanisms, results, or broader claims.

# Handling Long Manuscripts and TeX Projects

For full `.tex` files or multi-file manuscripts:

1. Scan the whole manuscript structure before editing locally. Work through complete sections, carrying canonical terminology and notation across chunks.
2. Keep the original untouched and write the revision to a separate file. For multi-file projects, keep separate original and candidate project copies with the same relative paths; do not compare two root files that both read the same edited child files.
3. Preserve everything before `\begin{document}` byte-for-byte unless the user explicitly requests preamble edits. For authorized protected changes, keep the original and establish a separate approved baseline that includes only those changes.
4. Resolve `\input`, `\include`, and related project structure. Use the checker's `--project` mode for project roots; unresolved or dynamic inputs prevent complete mechanical coverage.
5. Keep figure/table environments, column specifications, cell alignment, equations, algorithms, bibliography keys, labels, file paths, code listings, and protected macro arguments intact. Caption and cell prose may be polished without restructuring their containers. See `references/fidelity_and_tex.md` for custom macros.
6. Deliver long manuscripts as files, with a short location/link and verification summary. If work must span turns, deliver complete sections and state what is finished and what remains; do not silently skip material or paste a manuscript that would be truncated.
7. State `Coverage: FULL MANUSCRIPT` only after all materially relevant components have been reviewed, requested editing is complete, and final fidelity verification covers the delivered manuscript. Availability alone is insufficient. Otherwise state `Coverage: PARTIAL` and identify missing, unfinished, or unverified material briefly.

# Output Rules

For normal polishing, output:

1. the polished authoritative text or TeX, delivered as files for long manuscripts and projects;
2. concise **Material Edit Notes** only when an edit deserves author attention because it touches claim-bearing language, paragraph reordering, citation movement, numerical-statement repositioning, or a genuine source ambiguity;
3. a brief note only when a source inconsistency, coverage limitation, or author decision affects delivery.

Do not output by default:

- narrated process descriptions;
- PASS reports for every rule;
- exhaustive every-edit logs;
- style scorecards;
- large checklists merely proving that the workflow ran.

# Preservation Checker

Paths are relative to this skill directory; adjust the script path when invoking from elsewhere. Requires Python 3.9+ and no third-party dependencies. Exit `0` means enabled mechanical preservation checks passed, `1` means a preservation or coverage check failed, and `2` means invalid arguments or an unreadable root input. Style advisories do not affect the exit status.

Reader-oriented mode for standalone files:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

Strict mode for standalone files:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex
```

For multi-file manuscripts, use independent project copies and enable traversal:

```bash
python3 scripts/check_preservation.py original/main.tex candidate/main.tex --reader-oriented --project
```

Without `--project`, detected include directives cause a coverage failure. Missing, cyclic, or dynamic inputs also fail project traversal; report the unresolved coverage instead of treating root-only checks as a manuscript PASS.

If citations or cross-references were deliberately reordered, `--allow-structural-reorder` compares supported citation/reference events by inventory while retaining the order of other protected structures, including labels, environments, paths, and comments. Manually verify claim–citation attachment afterward.

Register opaque custom macro arguments when their syntax is known, for example `--protect-command artifact=1` for `\artifact{path}`. Repeat the option for additional macros. Unregistered custom arguments, nonstandard macro syntax, and TeX expansion require manual comparison; see `references/fidelity_and_tex.md`.

Existing short label keys and manual figure/table numbering produce style advisories, not preservation failures. Do not rename keys or alter protected numbers to remove those advisories.

The checker protects mechanically visible structure. It does **not** prove semantic fidelity, claim equivalence, or correct scientific reasoning.

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

# Final Internal Standard

Before delivery, confirm that:

- the scientific argument is easier to recover than in the source;
- paragraph and section progression are coherent;
- wording is precise, natural, and evidence-proportional;
- important claims retain the same strength and scope across sections;
- unnecessary AI-like academic patterns are reduced without flattening the author’s technical voice;
- all required hedges, limitations, conditions, and qualifications remain intact;
- no unintended scientific drift was introduced.

If fidelity is safe but the reader still has to reconstruct the argument unnecessarily, polishing is not complete.
