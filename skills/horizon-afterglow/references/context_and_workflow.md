# Context and Workflow

## Contents

- [Purpose](#purpose)
- [1. Manuscript Context](#1-manuscript-context)
- [2. Paragraph Context](#2-paragraph-context)
- [3. Scientific Claim Logic](#3-scientific-claim-logic)
- [4. One-Repair Principle](#4-one-repair-principle)
- [5. Minimal-Change Preference](#5-minimal-change-preference)
- [6. Source Problems](#6-source-problems)

## Purpose

Provide enough manuscript context to avoid sentence-by-sentence polishing without performing the full-profile manuscript analysis.

## 1. Manuscript Context

Before polishing a major section or manuscript, identify:

| Item | Question |
|---|---|
| Research problem | What problem is being addressed? |
| Central purpose/claim | What should the reader ultimately understand or accept? |
| Main contributions | What are the major contributions? |
| Section purpose | What job does the current section perform? |
| Method/reasoning sequence | What is the main dependency or reasoning order? |
| Canonical terminology | What names should remain stable? |
| Key notation/quantities | Which symbols and values need special protection? |

Do not build a complete claim–evidence graph unless the manuscript is complex enough to require it.


### Afterglow reading depth

For full manuscripts, use a two-level reading strategy:

1. **Global scan:** recover section structure, major claims, terminology, notation, and cross-section dependencies.
2. **Selective deep read:** read the active section and the nearby context required for safe editing in detail.

Do not perform a full-profile deep semantic analysis of every paragraph by default. Escalate only when the active section depends on distant material or when consistency problems make a deeper read necessary.

## 2. Paragraph Context

For each important paragraph, determine:

1. What does the reader already know?
2. What is this paragraph mainly doing?
3. What new information must it establish?
4. What does the next paragraph need from it?

Typical functions include:

- context;
- gap/problem;
- method motivation;
- mechanism explanation;
- definition;
- result;
- interpretation;
- qualification;
- comparison;
- transition.

Do not force all paragraphs into the same template.

## 3. Scientific Claim Logic

When a paragraph makes a substantive claim, check whether its evidence and qualification are visible enough to support it.

Distinguish:

- observation from interpretation;
- correlation from causality;
- benchmark-specific improvement from general superiority;
- empirical behavior from theoretical guarantee.

If a missing logical bridge requires new scientific content, flag it rather than inventing it.

## 4. One-Repair Principle

Use one main rewrite after diagnosis.

Later passes should verify and repair, not freely rewrite again.

This reduces:

- terminology drift;
- claim inflation;
- broken topic chains;
- unnecessary sentence reshuffling;
- unstable numerical phrasing.

## 5. Minimal-Change Preference

This ranks *kinds of edit* during the main rewrite. It is distinct from the Pass 7
repair ladder in `SKILL.md`, which ranks *how far to escalate* when repairing a
problem the verification pass found.

When several edits can solve the same problem, prefer:

1. delete redundancy;
2. adjust local order;
3. repair sentence structure;
4. split or merge sentences;
5. rewrite a sentence;
6. rewrite a whole paragraph only when needed.

## 6. Source Problems

Separate:

- **source-to-output fidelity**: did polishing introduce an error?
- **source-internal inconsistency**: was the source already inconsistent?

Do not silently resolve source conflicts unless the author has made the intended correction clear.
