# Journal Recommendation Guide

## Contents

- [Goal](#goal)
- [Intake Defaults](#intake-defaults)
- [Estimating Manuscript Level](#estimating-manuscript-level)
- [Candidate Discovery Budget](#candidate-discovery-budget)
- [Cheap Filter](#cheap-filter)
- [Scoring Rubric](#scoring-rubric)
- [Tier Logic](#tier-logic)
- [Speed as a Tag, Not a Tier](#speed-as-a-tag-not-a-tier)
- [Source Authority](#source-authority)
- [Recent-Content Verification](#recent-content-verification)
- [Red-Flag Screening](#red-flag-screening)
- [Fit Rationale Template](#fit-rationale-template)
- [Adjustment Playbook](#adjustment-playbook)
- [Recommended Output Template](#recommended-output-template)
- [Verification-Mode Output](#verification-mode-output)
- [Single-Journal Fit Output](#single-journal-fit-output)

## Goal

Produce a compact, defensible journal shortlist for a finished or near-finished manuscript. The shortlist should help the user decide where to submit, not merely name journals that sound related.

The design principle is:

```text
understand manuscript -> generate broad candidates -> cheap constraint filter -> deep-verify 8-12 finalists -> score evidence -> Reach/Core/Backup -> explain the decision
```

The skill optimizes for decision quality, not the number of journals or the amount of metadata collected.

## Intake Defaults

Use information already present in the conversation or manuscript before asking questions.

### Hard constraints

| Item | Typical values | Default when missing |
|---|---|---|
| Indexing | SCIE / SSCI / A&HCI / EI / Scopus / 北大核心 / CSSCI / CSCD / none | SCI/SCIE |
| OA | required / optional / prefer subscription | prefer non-OA / subscription route |
| Budget | APC/page-fee ceiling | unknown; do not invent a ceiling |
| Language | English / Chinese / either | English |
| Deadline | date or urgency | none |
| Avoid-list | warning list, blacklist, publisher, conflict, prior rejection | none |
| Article type | regular / letter / brief / review | regular paper |

These are defaults for interpreting missing user preferences, not defaults for unknown journal facts.

### Unknown-status handling

When a journal-specific fact remains unknown after a reasonable verification attempt:

- **Required indexing unknown → do not mark the indexing gate as passed.** Exclude the journal from the decision-ready shortlist or place it in a separate `unverified candidates` note.
- **OA model, APC, or mandatory fee unknown → do not assume subscription access, no mandatory APC, or budget compatibility.** If the unknown fact could violate a hard OA or cost constraint, exclude the journal from the decision-ready shortlist.
- When the unknown fact is not tied to a hard constraint, a journal may remain with an explicit `unknown/unverified` label, but the uncertainty must not improve its score or ranking.

### Paper-fit inputs

Prefer the full manuscript when available. Otherwise use:

- abstract;
- problem and contribution;
- method;
- main results and strongest evidence;
- 3-6 keywords and subfield;
- audience/use case;
- advisor or user level anchor.

## Estimating Manuscript Level

Estimate level from evidence, not from how sophisticated the topic sounds.

Consider:

- significance and audience breadth;
- novelty and defensibility of the main contribution;
- rigor and completeness of evaluation;
- quality and recency of baselines;
- ablations, statistics, robustness, theory, or real-world validation where relevant;
- dataset/system scale and reproducibility;
- the user's or advisor's own level anchor.

State the result as a band and confidence, for example:

```text
Estimated level: solid mid-tier / around field Q2 level (medium confidence)
Basis: moderate methodological novelty + strong real-world evaluation, but limited breadth of baselines.
```

Do not convert the estimate into an acceptance probability.

## Candidate Discovery Budget

Default search budget:

- broad pool: about 15-20 candidates;
- finalists for deep verification: about 8-12;
- final output: about 8-12 total across all tiers;
- optional field-top references: 0-2.

The broad pool may come from:

- journals publishing the most relevant recent papers;
- venues cited repeatedly by the manuscript or its close literature;
- official publisher/society journal families;
- user/advisor suggestions;
- model recall used only as a lead for live search.

Do not fully verify every broad candidate. Apply cheap gates first, then spend verification effort on finalists.

## Cheap Filter

Drop a candidate before deep verification when any of the following is already clear:

- scope is obviously unrelated;
- required indexing is verified absent or remains unconfirmed after reasonable verification;
- language is incompatible;
- article type is unavailable;
- mandatory OA or budget compatibility is verified incompatible or remains unresolved after reasonable verification;
- the venue is explicitly on the user's avoid-list;
- the publisher/venue violates another hard user constraint.

Do not reject a candidate merely because the manuscript uses another publisher's template.

## Scoring Rubric

The scoring rubric makes the recommendation repeatable without pretending that venue choice is mathematically exact.

### 1. Constraint gate — Pass / Fail

A hard-constraint failure excludes the journal.

### 2. Scope fit — 0 to 5

| Score | Interpretation |
|---|---|
| 5 | Central to the journal's stated scope and article types |
| 4 | Clearly within scope, with only minor framing adjustment |
| 3 | Plausible fit, but one important aspect is peripheral |
| 2 | Adjacent; substantial reframing needed |
| 1 | Weak connection |
| 0 | Out of scope |

Default: exclude below 3.

### 3. Recent-content fit — 0 to 5

Use recent 3-5 year content unless the field is unusually slow-moving.

| Score | Interpretation |
|---|---|
| 5 | Recurring cluster/special issue or 3+ very close recent papers |
| 4 | 2-3 close recent papers |
| 3 | 1-2 close papers plus several audience-adjacent papers |
| 2 | Only adjacent evidence; no close match |
| 1 | Very weak recent evidence |
| 0 | Recent content contradicts the proposed fit |

Default: exclude below 2 unless the journal is intentionally broad or the topic is new/interdisciplinary and the scope/audience case remains strong.

### 4. Audience/article-type fit — 0 to 3

| Score | Interpretation |
|---|---|
| 3 | Correct audience and article format |
| 2 | Correct audience with minor format/framing adjustment |
| 1 | Partial audience overlap |
| 0 | Wrong audience or article format |

### 5. Level delta — -2 to +2

Relative to the manuscript's estimated level:

| Delta | Meaning | Default treatment |
|---|---|---|
| +2 | Several steps above | omit or field-top reference only |
| +1 | Slightly above | Reach |
| 0 | Best level match | Core |
| -1 | Slightly below | Backup |
| -2 | Clear undersell | normally omit |

A `+2` venue must not be relabeled Reach merely because it is prestigious.

### 6. Evidence confidence

Record separately from fit:

- **High:** primary/authoritative sources agree; recent-content evidence is clear.
- **Medium:** core facts verified but one secondary dimension is incomplete or noisy.
- **Low:** important evidence is missing, conflicting, or only indirectly supported.

For review speed, use **High / Medium / Low / Unknown** independently from metadata confidence.

## Tier Logic

### Reach

Level delta +1 with credible scope and recent-content evidence. Reach means a plausible stretch, not a long shot several levels above the manuscript.

### Core

Level delta 0. Usually the best balance of scientific fit, paper level, and submission risk. Core should receive the most attention in the final ordering.

### Backup

Level delta -1, still with strong scientific fit. Backup is not a dumping ground for broad journals; it should remain defensible to an advisor.

### Field-top reference

Optional 0-2 field-native venues at level delta +2 or at the upper edge of +1. This lane calibrates the ceiling and must state what evidence is missing before the venue becomes a serious target.

## Speed as a Tag, Not a Tier

Review speed is orthogonal to scientific ambition. Do not create separate fast-review tiers.

Possible tags:

- `[Fast signal]`
- `[Moderate]`
- `[Slow signal]`
- `[Speed unknown]`

Use `[Deadline-friendly]` only when the available evidence reasonably supports it.

### Review-speed protocol

Prefer, in order:

1. journal-reported time to first decision or review statistics;
2. mainland-China Simplified-Chinese LetPub page on `letpub.com.cn` when available and relevant;
3. another credible field/community source if necessary.

Rules:

- attribute the timing to the source;
- crowd-sourced data is indicative only;
- source disagreement lowers confidence;
- do not convert a historical median into a guaranteed current timeline;
- if LetPub cannot be found, write `not found` and continue;
- never construct a LetPub URL from memory.

## Source Authority

Use the narrowest authoritative source for each claim.

| Fact | Preferred source | Notes |
|---|---|---|
| Aims & scope | Official journal site | Required for every finalist |
| Article types | Official journal site | Required when format matters |
| APC/page fees | Official journal/publisher site | Verify current amount/currency; note waivers only if confirmed |
| Web of Science indexing | Clarivate Master Journal List | Confirm current index |
| JIF/quartile | Clarivate JCR | State year; do not conflate with CiteScore |
| Scopus indexing/CiteScore | Scopus source records | State year where relevant |
| 中科院分区 | Last officially published CAS partition edition | The series is no longer updated from 2026; state the edition year and label it historical, not current |
| 北大核心/CSSCI/CSCD | Respective official catalogs | China-specific tasks |
| OA legitimacy | DOAJ plus official journal site | Especially useful for unfamiliar full-OA venues |
| Review speed | Official journal stats + LetPub as auxiliary evidence | No guarantees |
| Recent-content evidence | Journal archive plus scholarly index/search | Required for every finalist |
| Warning status | CAS international journal early-warning list and other reputable sources | Screen especially risky candidates |

Never guess a URL. Report only links actually found.

## Recent-Content Verification

For each finalist:

1. search the journal's own archive/site using 3-6 manuscript keywords;
2. broaden with synonyms when exact keywords are too narrow;
3. if needed, verify with Crossref, OpenAlex, PubMed, Semantic Scholar, discipline databases, or another scholarly search source;
4. record 1-3 representative papers with year and DOI/URL;
5. verify that each representative paper actually appeared in the journal.

Recent-paper evidence supports two questions:

- does the journal actually publish this technical topic or audience now?
- what kind of framing/evaluation does the journal tend to reward?

Do not count generic papers as close matches simply to increase the score.

## Red-Flag Screening

Exclude or prominently flag a venue when evidence suggests:

- hijacked/clone journal behavior;
- fabricated metrics or indexing claims;
- unclear or implausible peer-review process;
- aggressive solicitation coupled with unrealistic acceptance promises;
- unverifiable publisher/editorial-board information;
- warning-list status relevant to the user's institution/context;
- suspicious OA/APC practices or legitimacy problems.

Absence from DOAJ alone is not proof of predation. Treat signals in context.

## Fit Rationale Template

Keep each rationale compact and decision-focused:

```text
Why it fits:
- Scope: <how the manuscript maps to official scope>
- Recent content: <1-3 related papers or a caution>
- Level/audience: <why Reach/Core/Backup>
- Constraints: <indexing/OA/APC/language/deadline>
Main risk: <the biggest reason it may fail>
Adjustment: <one concrete change if borderline>
Evidence confidence: <High/Medium/Low>; speed confidence: <High/Medium/Low/Unknown>
```

## Adjustment Playbook

When a journal is close but not ideal, suggest a concrete change:

- **Scope drift:** change framing, title/keywords, introduction emphasis, or application angle.
- **Weak recent-content evidence:** align with the closest recurring theme or move the venue down the ranking.
- **Paper below venue:** add stronger baselines, ablations, theory, robustness, broader validation, or field deployment.
- **Paper above venue:** keep only if speed/risk matters; otherwise note likely underselling.
- **Article-type mismatch:** consider letter/brief/regular-paper format if genuinely offered by the journal.
- **Budget/OA strain:** check subscription route, waiver, or a nearby lower-cost journal.
- **Template mismatch:** reformat after venue selection; do not change the fit score.

## Recommended Output Template

```text
Constraints / assumptions:
- indexing: ... | OA: ... | budget: ... | language: ... | deadline: ... | avoid-list: ...

Manuscript profile:
- topic/audience: ...
- estimated level: ... (confidence: ...)
- basis: ...

Decision summary:
- Best Core target: <Journal> — <one-line reason>
- Best Reach target: <Journal> — <one-line reason>
- Best deadline-friendly target: <Journal or not applicable>

Shortlist (8-12 total):

Reach
1. <Journal> [speed tag] [OA/cost tag]
   Fit: scope X/5 · recent X/5 · audience X/3 · level +1
   Why: <concise reason>
   Recent evidence: <1-3 papers, year + DOI/URL>
   Constraints: <indexing / OA / APC / language>
   Speed: <source-backed band + confidence>
   Main risk / adjustment: <...>
   Sources: <official site>; <indexing/metric source if used>; <LetPub if used>

Core
2. ...

Backup
...

Optional field-top reference (0-2):
- <Journal> — current realism: <stretch/long-shot/unrealistic>; missing evidence: <...>

Red flags / unresolved uncertainty:
- ...

Suggested submission sequence:
1. ...
2. ...
3. ...
```

Do not force all fields into a giant table if it makes the evidence unreadable. A compact comparison table plus short evidence notes is acceptable.

## Verification-Mode Output

When checking a supplied shortlist, focus on deltas rather than regenerating everything:

```text
Verified as stated:
- ...

Needs correction:
- <Journal>: <claim> -> <verified status/source>

Tier/ranking issues:
- <Journal>: currently labeled Reach, but evidence suggests +2 / unrealistic

Missing evidence:
- <Journal>: no close recent-content match found

Red flags:
- ...
```

## Single-Journal Fit Output

```text
Verdict: Strong fit / Plausible fit / Borderline / Poor fit
Tier: Reach / Core / Backup / Outside shortlist

Evidence:
- Scope: ...
- Recent content: ...
- Level/audience: ...
- Constraints: ...
- Speed: ...
- Red flags: ...

Main risk: ...
Best adjustment before submission: ...
Confidence: ...
```
