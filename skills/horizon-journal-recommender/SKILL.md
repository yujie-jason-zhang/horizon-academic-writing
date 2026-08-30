---
name: horizon-journal-recommender
description: >-
  Recommend and verify target journals for a finished or near-finished manuscript. Use for submission shortlists, single-journal fit checks, realistic venue-level calibration, indexing/OA/APC/speed constraints, or China-context journal screening. Build a broad candidate pool, cheaply filter it, deeply verify only 8-12 finalists, then rank them as Reach, Core, and Backup with speed/OA/cost tags. Every final journal must be verified live for official scope, current constraints, and recent related papers. LetPub is auxiliary evidence for review speed and China-specific context, not an eligibility requirement. Use before paper-cover-letter.
---

# Journal Recommender

## Scope

Use this skill when a manuscript is finished or nearly finished and the user needs to decide where to submit it. Typical tasks include:

- generating a realistic journal shortlist;
- checking whether one named journal fits the manuscript;
- comparing journals by level, scope, indexing, OA/APC, language, or review speed;
- deciding which venues are Reach, Core, or Backup targets;
- verifying a shortlist produced by an advisor, another tool, or another skill.

This skill matches manuscripts to venues. It does not validate the science itself and does not draft the cover letter.

Read `references/journal_recommendation_guide.md` for the scoring rubric, source hierarchy, review-speed protocol, red-flag checks, rationale templates, and output template.

Use another skill when the primary task is novelty assessment, literature review, manuscript restructuring, language polishing, or cover-letter writing. Reuse an existing paper-level assessment when one is already available instead of re-deriving it.

## Operating Modes

### Recommendation mode

Default mode. Generate candidates, filter them, verify the finalists, and return a ranked shortlist.

### Verification mode

Use when the user already has a shortlist or a journal-fit claim.

- Preserve the supplied list unless a venue clearly violates a hard constraint or legitimacy rule.
- Verify scope, recent-content fit, level, indexing, OA/APC, speed claims, and red flags.
- Report unsupported or incorrect claims explicitly.
- Re-rank only when the user asks for ranking or when the current tier assignment is materially misleading.

### Single-journal fit mode

For one named journal, skip broad candidate generation. Verify the journal and return fit, level, constraints, recent-content evidence, risks, and any concrete adjustment needed.

## Non-Negotiable Rules

- **Live verification is mandatory for the final shortlist.** Model memory may seed search queries or candidate ideas, but no journal may appear in the final recommendation until it has been verified in the current session.
- **Never invent a journal, URL, ISSN, metric, indexing status, APC, review time, or related-paper evidence.** If a fact cannot be confirmed, label it `not found`, `unknown`, or `unverified`. Do not treat an unknown journal-specific fact as a favorable default. If required indexing, OA model, or mandatory cost cannot be verified, the journal does not pass that hard constraint for the decision-ready shortlist.
- **Official scope comes first.** Open the journal's official aims/scope or equivalent page for every finalist.
- **Recent-content fit is required.** For every finalist, verify recent papers from the journal itself and/or a scholarly index. Aims & Scope alone is not enough.
- **Hard constraints are gates.** A journal that fails required indexing, language, budget, article type, avoid-list, or another explicit non-negotiable constraint is excluded rather than down-ranked.
- **Do not select by manuscript template.** IEEE/Elsevier/Springer/other formatting is a reformatting issue, not venue-fit evidence, unless the user explicitly makes publisher family a constraint.
- **Metrics are time-sensitive.** Verify any JIF, quartile, CiteScore, indexing, APC, or fee you report, and state the relevant year/version where applicable. For work performed in 2026 or later, report a CAS partition only as the last available historical edition, state its edition year, and do not describe it as a current tier because the official partition series is no longer updated from 2026.
- **Review speed is uncertain evidence, not a promise.** Attribute it to the source, use a qualitative band, and include a confidence label. Never convert crowd-sourced timing into a guaranteed decision date.
- **LetPub is auxiliary, not a gate.** In China-oriented or speed-sensitive tasks, try to locate the mainland-China Simplified-Chinese LetPub page on `letpub.com.cn`. Use it as supporting evidence for turnaround and China-context signals. If it is absent, write `not found`; do not exclude an otherwise strong journal for that reason and do not substitute a guessed URL.
- **Screen legitimacy and warning signals.** Exclude or clearly flag predatory, hijacked, or warning-listed venues. Screen fast, OA, unfamiliar, and high-APC journals especially carefully.
- **A level estimate is not an acceptance prediction.** Reach/Core/Backup describe relative submission risk, not acceptance probability.
- **Do not pad the list.** A shorter, well-supported shortlist is better than a long weak one.

## Intake

Use information already provided before asking questions. If key information is missing, collect it in compact groups; if the user does not answer, proceed with clearly stated assumptions when reasonable. Default missing indexing requirements to SCI/SCIE and missing OA preference to non-OA / subscription-preferred.

### Hard constraints

- required indexing: SCIE / SSCI / A&HCI / EI / Scopus / 北大核心 / CSSCI / CSCD / none;
- OA preference: must be OA / optional / prefer subscription;
- APC or page-fee ceiling;
- language: English / Chinese / either;
- deadline or time sensitivity;
- avoid-list: warning lists, institutional blacklist, publishers, conflicts, or venues already rejected.

### Paper-fit inputs

- subfield and 3-6 keywords;
- abstract, or problem + method + main results;
- intended article type;
- level anchor from the user/advisor or prior publications, if available;
- current template only as an operational note.

## Workflow

### Stage A — Build and cheaply filter candidates

1. **Profile the manuscript.** Summarize the problem, method, claimed contribution, evidence strength, intended audience, article type, and likely level. Keep the level estimate hedged.
2. **Generate a broad candidate pool.** Usually target about 15-20 plausible venues from scope search, recent related literature, cited venues, user/advisor suggestions, and model recall used only as leads.
3. **Apply cheap gates before deep verification.** Remove obvious failures on scope, required indexing, language, article type, OA/budget, avoid-list, or publisher restrictions. Keep a candidate provisional when a quick check cannot resolve an important journal-specific fact; do not mark the corresponding gate as passed. Spend deep-verification effort only on provisional candidates that otherwise appear competitive.
4. **Choose a finalist pool.** Usually 8-12 journals total, with enough range to support Reach/Core/Backup. If fewer genuinely fit, return fewer.

### Stage B — Deeply verify only the finalists

5. **Verify official journal information.** Check aims/scope, article types, OA model, APC/page fees, and any journal-reported decision-time signal that matters to the user. If OA or mandatory cost remains unconfirmed and could violate a hard constraint, exclude the journal from the decision-ready shortlist and list it separately only when the unresolved option is useful to the user.
6. **Verify indexing and metrics only from appropriate sources.** Confirm required indexing for every finalist. If it remains unconfirmed after reasonable verification, exclude the journal from the decision-ready shortlist and, when useful, place it in a separate `unverified candidates` note. Verify metrics/quartiles only when they are useful to the decision; do not collect decorative metadata.
7. **Verify recent-content fit.** Search the journal archive/site and at least one scholarly search/index source when needed. Prefer the latest 3-5 years and record 1-3 representative papers or a clear `no close recent match found` caution.
8. **Check speed evidence when relevant.** If deadline or speed matters, compare official timing signals with LetPub or another available source. Record a band and confidence; disagreement between sources lowers confidence.
9. **Screen red flags.** Check warning-list, OA legitimacy, hijacking/predatory signals, and unverifiable publisher/editorial claims as appropriate.
10. **Score and tier the finalists.** Use the rubric below; do not use prestige alone.
11. **Rank within each tier.** Prefer stronger scope fit, stronger recent-content evidence, better audience/article-type fit, cleaner constraint match, and higher evidence confidence.
12. **Return a decision-ready shortlist.** Default to 8-12 total journals, not 8-12 per tier.

## Scoring and Tiering

Use the detailed rubric in the guide. At minimum record internally:

- **Constraint gate:** Pass / Fail
- **Scope fit:** 0-5
- **Recent-content fit:** 0-5
- **Audience/article-type fit:** 0-3
- **Level delta:** `+2`, `+1`, `0`, `-1`, or `-2` relative to the manuscript
- **Metadata confidence:** High / Medium / Low
- **Speed confidence:** High / Medium / Low / Unknown

Default interpretation:

- hard-constraint Fail → exclude;
- Scope fit < 3 → normally exclude;
- Recent-content fit < 2 → normally exclude unless a broad/interdisciplinary rationale clearly justifies keeping it;
- Level delta `+1` → **Reach**;
- Level delta `0` → **Core**;
- Level delta `-1` → **Backup**;
- Level delta `+2` → usually outside the shortlist; optionally show as a **Field-top reference** if useful for calibration;
- Level delta `-2` → usually omit as an undersell unless deadline/risk constraints make it strategically useful.

The scores organize evidence; they are not acceptance probabilities.

## Tiers and Tags

### Reach

A credible stretch: slightly above the manuscript's estimated level, but not several steps above it.

### Core

Best level match. These should usually be the strongest default submission targets.

### Backup

Slightly below the manuscript's estimated level or broader/less selective, while still being a defensible scientific fit.

### Optional field-top reference

At most 1-2 field-native venues above Reach, used only to calibrate the ceiling. State whether each is a realistic stretch, long-shot, or currently unrealistic, and what evidence would need to improve.

### Tags

Use tags instead of separate speed tiers, for example:

- `[Fast signal]`, `[Moderate]`, `[Slow signal]`, `[Speed unknown]`
- `[OA]`, `[Hybrid]`, `[Subscription]`
- `[No mandatory APC]`, `[APC: ...]`
- `[Deadline-friendly]` only when the evidence supports it

Do not use `[Fast]` without a cited timing signal.

## Evidence Standard for Each Final Journal

Each listed journal should have enough evidence to defend the recommendation:

- official scope/article-type fit;
- required indexing and constraint status;
- 1-3 recent related papers, or an explicit weak-evidence caution;
- OA/APC information when relevant;
- speed evidence when speed matters, with confidence;
- red-flag status;
- a short level/audience rationale;
- real source links for the facts actually used.

Do not collect every possible metric. Collect what changes the submission decision.

## Output Format

For a full recommendation, return in this order:

1. **Constraints and assumptions**
2. **Manuscript profile and estimated level**
3. **Decision summary** — best Core target, best Reach target, and best deadline-friendly option when relevant
4. **Reach / Core / Backup shortlist** — normally 8-12 journals total
5. **Evidence notes** for each listed journal: fit, recent papers, key constraints, risks, and sources
6. **Optional field-top reference** — at most 1-2
7. **Red flags / unresolved uncertainties**
8. **Suggested submission sequence** when useful

Prefer concise comparison over repetitive prose. See the guide for the detailed template.

## Rule-Conflict Handling

If the user asks for a guaranteed acceptance chance, guaranteed review time, or a factual claim that cannot be verified, state the uncertainty instead of manufacturing precision. If a requested journal shows a legitimacy or warning-list concern, surface it before treating the venue as a target.

If web/search access is unavailable, do not present a list as verified. You may provide an explicitly labeled **unverified brainstorming list** only if the user asks for one.
