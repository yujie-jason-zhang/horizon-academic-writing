---
name: horizon-ember
description: Reader-oriented academic polishing for one target paragraph, including Chinese-to-English translation plus polishing and LaTeX/TeX text. Use when asked to polish, proofread, copy-edit, language-edit, translate, or verify a single paragraph (一段 / 单段润色), improve sentence-to-sentence cohesion, or reduce AI-sounding prose. Preserve claims, agency, causality, uncertainty, numbers, units, citations, math, terminology, and protected TeX; treat surrounding paragraphs as read-only context.
---

# Horizon-Ember

## Objective

Polish **one academic paragraph as a coherent unit**, not as a sequence of isolated sentences.

Primary goal:

> **Make the paragraph easier to follow, more precise, and more natural without changing what it scientifically means.**

Use this priority order:

1. **Technical fidelity**
2. **Sentence-to-sentence cohesion**
3. **Reader clarity**
4. **Lexical and phrase precision**
5. **Natural academic voice**
6. **Surface polish**

Lower-priority improvements must not damage higher-priority ones.

Horizon-Ember is paragraph-focused. It keeps strong local editing and fidelity protection but deliberately does **not** perform manuscript-level modeling, cross-section auditing, or project-wide argument reconstruction.

# Core Execution Principle

Use this workflow:

**Understand paragraph → lock meaning → diagnose local flow → one integrated rewrite → verify → paragraph reread → targeted repair**

Do not stack separate rewrite passes such as:

`grammar polish → logic rewrite → humanizer → polish again`

Use one major free rewrite. Later steps only verify and repair locally.

# Target and Scope

Use for:

- polishing a single English academic paragraph;
- translating one Chinese academic paragraph into English and polishing it;
- polishing a paragraph embedded in LaTeX/TeX;
- reducing formulaic or AI-sounding academic prose within one paragraph;
- verifying whether a revised paragraph changed scientific meaning.

If surrounding paragraphs are provided, use them as **read-only context**. Rewrite only the target paragraph unless the user explicitly asks otherwise.

Identify the target conservatively:

- edit the only paragraph when exactly one is supplied;
- follow explicit labels such as `Target paragraph` or equivalent wording;
- use quoted, highlighted, or otherwise clearly delimited text as the target;
- if several unlabeled paragraphs are supplied and the target is genuinely unclear, ask the user to identify it instead of rewriting all of them.

Keep the result as one paragraph unless splitting it is explicitly requested. Sentence splitting and merging inside the paragraph remain allowed in reader-oriented mode.

Do not use as the primary tool for:

- full-section or full-manuscript polishing;
- manuscript-wide terminology or notation audits;
- cross-section claim alignment;
- contribution redesign or argument reconstruction;
- novelty assessment;
- literature-gap construction;
- experiment design;
- citation replacement;
- silently fixing scientific contradictions in the source.

For section- or manuscript-level polishing, use Horizon-Afterglow.

# Modes

## 1. Reader-Oriented Paragraph Polishing — Default

May, when useful:

- split or merge sentences;
- reorder sentences or clauses inside the target paragraph;
- remove redundancy and empty rhetoric;
- add the minimum connective signaling needed for coherence;
- reposition numerical statements when semantic bindings remain unchanged.

## 2. Strict / Minimal-Diff Polishing

Use when the user asks for minimal changes or strict surface preservation.

Prefer local grammar, diction, punctuation, and clarity edits without unnecessary sentence restructuring.

## 3. Translation + Polishing

Translate the target paragraph into natural scientific English while preserving facts, claims, uncertainty, terminology, citations, equations, and numerical relationships.

Do not strengthen ambiguous source relations.

## 4. Verification Mode

Compare original and candidate only. Do not rewrite.

Check for drift in scientific meaning, agency, causality, claim strength, uncertainty, numbers, units, citations, mathematics, terminology, and protected TeX.

# Main Workflow

## Pass 1 — Understand the Paragraph

Before rewriting, identify internally:

- the paragraph's dominant rhetorical function;
- its main scientific point;
- what the reader already knows from the paragraph or supplied context;
- the sequence of new information;
- the relationship between adjacent sentences;
- the sentence that carries the main claim, mechanism, result, or interpretation;
- protected terminology, values, citations, math, and TeX.

If surrounding context is supplied, use it to interpret the target paragraph but do not infer unsupported manuscript-level intent.

## Pass 2 — Lock Meaning

Before rewriting, preserve:

- scientific meaning;
- agency and causal direction;
- claim scope, strength, and uncertainty;
- conditions, exceptions, and comparison scope;
- value–metric–unit–condition relationships;
- canonical technical terminology;
- citations;
- mathematics;
- protected TeX.

See `references/fidelity_and_tex.md`.

## Pass 3 — Diagnose Local Flow

Prioritize:

1. sentence-to-sentence cohesion;
2. old-to-new information flow;
3. visibility of the main action;
4. lexical and phrase precision;
5. avoidable syntactic load;
6. misplaced emphasis;
7. repetitive rhythm or decorative parallelism;
8. high-value formulaic or overstated academic patterns.

Do not optimize every stylistic dimension merely because it is available.

See `references/paragraph_writing.md`.

## Pass 4 — One Integrated Rewrite

This is the main free rewrite.

Edit in this order:

1. repair sentence sequence and local logic;
2. make adjacent-sentence relations immediately recoverable;
3. improve lexical and phrase precision;
4. simplify avoidable syntactic complexity;
5. place important information where the reader can recover it easily;
6. break nonfunctional rhythmic repetition and decorative parallelism;
7. remove empty or formulaic academic phrasing;
8. polish grammar, punctuation, and concision.

Do not interpret academic quality as more complex vocabulary, longer sentences, more passive voice, more nominalization, or either more or fewer transition words.

Prefer the clearest and most precise expression that preserves the full technical meaning.

## Pass 5 — Fidelity Verification

Compare the source paragraph and revision.

Check:

- agency and causality;
- claim strength and uncertainty;
- conditions and exceptions;
- value–metric–unit–condition bindings;
- technical terminology;
- citations and their claim attachment;
- mathematics;
- protected TeX.

If a readability edit changes technical meaning, repair or revert that location.

## Pass 6 — Paragraph Reader Pass

Read the revised paragraph continuously as one unit.

Ask:

- Can the paragraph's main point be recovered on the first read?
- Does every sentence after the first have a clear reason to follow what precedes it?
- Is connective signaling sufficient but not excessive?
- Does the paragraph move naturally from known information to new information?
- Is any sentence harder than the scientific idea requires?
- Is any key word or phrase vague, unnatural, unnecessarily elevated, or stronger than the evidence warrants?
- Is repeated rhythm functional or merely stylistic?
- Does the final sentence genuinely complete the paragraph's role rather than add boilerplate?

This is a reader pass, not a second free rewrite.

## Pass 7 — Targeted Repair

Repair only problems found in Passes 5–6.

Escalate as little as possible:

1. revert or replace one word/phrase;
2. repair one sentence;
3. repair one adjacent sentence pair;
4. rewrite the paragraph only if its local progression still fails.

# Hard Constraints

Do not change for stylistic reasons:

- scientific meaning;
- agency;
- causal direction;
- claim scope, strength, or uncertainty;
- theorem/proof or algorithmic logic;
- experimental conditions;
- datasets, baselines, or metrics;
- numbers, units, signs, or quantity-to-value relationships;
- citation keys or citation meaning;
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

# Output Rules

For normal polishing, output:

1. the polished paragraph;
2. a brief note only when a genuine ambiguity, source inconsistency, or author decision matters.

Do not normally output a sentence-by-sentence change log, PASS report, style scorecard, or large checklist.

In Verification mode, report the verdict first, followed by concise findings grouped by severity. Quote or point to the affected wording and explain the semantic change. State explicitly when no material drift is found.

Do not produce a replacement paragraph in Verification mode unless the user separately asks for one.

# Optional Preservation Checker

For a paragraph saved as a file, locate the checker relative to the directory containing this `SKILL.md`. Do not assume that the project working directory is the skill directory.

In Claude Code, use the built-in skill-directory variable:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_preservation.py" original.tex candidate.tex --reader-oriented
```

In Codex or another Agent Skills client, resolve the installed skill directory first and use an absolute path:

```bash
python3 /absolute/path/to/horizon-ember/scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

For strict mode, omit `--reader-oriented`:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_preservation.py" original.tex candidate.tex
```

If sentences containing citations or cross-references were deliberately reordered, add `--allow-structural-reorder` and manually verify that each key still attaches to the correct claim.

The checker catches mechanical preservation problems. It does not prove semantic fidelity or claim–citation attachment.

# Final Internal Standard

Before delivery, confirm that:

- the paragraph is easier to understand as a whole;
- adjacent sentences connect naturally;
- connective signaling is neither missing nor excessive;
- wording is precise, natural, and proportional;
- unnecessary syntactic load has been reduced;
- repetitive rhythm is broken when stylistic but retained when scientifically functional;
- formulaic AI-like academic patterns are reduced;
- no scientific drift was introduced.

If the paragraph is technically safe but still unnecessarily difficult to read, polishing is not complete.
