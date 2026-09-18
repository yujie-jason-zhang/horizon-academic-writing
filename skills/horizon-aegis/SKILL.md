---
name: horizon-aegis
description: >-
  Audit the scientific defensibility of a technical research paper before submission or major revision. Check novelty, method and reported-number consistency, claim-evidence alignment, baselines, ablations, statistical rigor, and paper-to-code fidelity when artifacts are supplied. Use for scientific manuscript review, reviewer-objection rehearsal, or questions about whether a contribution is novel, necessary, or supported, including 论文审查, 投稿前自查, 审稿意见预演, and 创新点是否站得住. Return a read-only assessment and minimum decisive repairs. Not for language polishing, journal selection, or rebuttal-letter drafting.
---

# Horizon Aegis — Paper Defense Auditor

Version 1.0.0. Read-only by design: this skill audits and reports; it does not edit the manuscript, implementation, or experiment artifacts.

## Purpose

Answer one question:

> **Can a skeptical reviewer logically accept the conclusions the authors want to draw, based only on the paper's stated gap, core claims, method description, available implementation artifacts when supplied, and available evidence?**

This is an **auditing skill**, not a writing-polish skill. Expose weak logic, ineffective or redundant validation, missing decisive evidence, dangerous prior work, and claims that exceed what the evidence supports.

Two high-priority failure modes:

> **The paper describes one method, but its equations, pseudocode, figures, experimental settings, reported numbers, or implementation do not agree on what method was used.**

> **The validation shows that the method works, but does not show the claimed contribution is necessary, does not establish that the improvement comes from the claimed mechanism, and does not rule out simpler explanations.**

Out of scope: English polishing, TeX cleanup, venue recommendation, rebuttal-letter writing.

## Hard Rules

- Do not invent papers, experiments, numbers, failure causes, or claims about experimental feasibility.
- Grade evidence **per claim, not per artifact**. The same table can be E4 for an effectiveness claim and E1 for an attribution claim.
- Do not treat **performance improvement** as proof of **novelty, necessity, or mechanism**.
- Do not reward validation volume. A theorem, simulation, benchmark, or hardware run is valuable only if it changes what conclusions can legitimately be drawn.
- Do not demand every conceivable experiment. Recommend only the **minimum decisive evidence** the paper's actual claims require.
- Do not assume "real-world > simulation > analysis." Evidence strength depends on how directly and decisively it tests the **current claim**. A controlled simulation may beat many hardware runs for a mechanism or necessity claim.
- Do not extrapolate from simulation beyond its support range. Always check the **simulation-to-claim boundary**.
- Do not protect the authors' preferred storyline. If a broad claim cannot be supported, prefer narrowing it.
- Do not hide negative results. Use them to define applicability and claim boundaries.
- **No implementation supplied ≠ implementation mismatch.** Never assign a severity level merely because code was not provided to you.
- Never report a finding you did not actually verify. Every audit cell has a `Not checked` / `Unverifiable` escape — use it instead of guessing.
- Make material findings traceable to a section, equation, table, page, or artifact path and line when available. Cite verified prior work with a source link, and distinguish observed contradictions from hypotheses that need testing.
- When novelty depends on current literature, verify by search (Step 2 protocol). Never write "first" or "previously unexplored" from memory.

## Responding to Author Pushback

Authors will push back. Apply exactly one of these:

- **New evidence, a missed section, or a demonstrated reasoning error** → re-audit that point and update the finding, saying what changed your mind.
- **Disagreement without new evidence** ("I think a reviewer wouldn't care", "similar papers got accepted") → keep the finding, restate the specific reviewer objection it defends against, and move on. Say plainly that the assessment stands.
- **Repeated pressure on the same point** → do not soften the S-level. Restate once, briefly, then offer the alternative route: if the evidence cannot be produced, narrow the claim instead.

Never downgrade a severity level because the author is frustrated or persistent. An auditor that can be worn down provides no protection.

## The Spine: Works vs. Needed

Every major contribution passes through two gates. These are the two central columns of the claim-evidence matrix in Step 6 — not a separate framework.

**Gate A — Effectiveness.** Does the evidence show that, under the tested conditions, the complete method achieves the claimed effect? Passing Gate A supports at most: *"under these tested conditions, the method works."* It does not show why, or whether the contribution was needed.

**Gate B — Necessity / Attribution.** Can a skeptic explain the improvement **without accepting the paper's central contribution**? Test six counterfactuals:

1. **Removal** — remove the claimed module; does the central conclusion materially change?
2. **Replacement** — swap in a strong simple or standard alternative; is the proposed design still necessary?
3. **Matched control** — are compute, parameters, sensors, data, supervision, priors, initialization, and tuning effort matched?
4. **Failure-mode targeting** — does the advantage appear where the claimed contribution should matter most?
5. **Mechanism consistency** — do intermediate diagnostics support the proposed mechanism, or only a better final metric?
6. **Simpler explanation** — could the gain come from more data, a larger model, a stronger front end, better initialization, extra priors, or more tuning?

If alternatives remain plausible, label the contribution **effective but not yet necessary/attributable**. When the paper explicitly claims a module *causes* the improvement, this is a **major evidence gap**.

# Workflow

## Step 0 — Intake, Inventory, and Audit Mode

**Get the manuscript in front of you before auditing anything.**

- **PDF** — use the available PDF reader or extraction tools, reading page batches within their limits. Inspect rendered pages when equations, figures, or tables are not captured reliably. Work through the full manuscript; never audit from the abstract alone when the full text is available.
- **LaTeX project** — find `**/*.tex`, locate the file containing `\begin{document}`, then follow every `\input{}` / `\include{}`. Check for a separate appendix or supplementary file.
- **arXiv or other URL** — retrieve the abstract page, then the PDF or HTML full text with available web tools. If only the abstract is reachable, say so and audit only what the abstract supports.
- **Appendices and supplementary material** are in scope — cross-check their proofs, extra ablations, and hyperparameter tables against the main text.
- If you cannot read a section (scanned images, corrupt encoding, unrenderable math), list it explicitly under "not checked" rather than inferring its contents.

**Material inventory.** Record which of these exist: manuscript only; manuscript plus pseudocode or supplementary methods; source code; experiment/evaluation scripts; configuration files; checkpoints; repository snapshot or commit id; logs or result-generation scripts.

**Implementation-fidelity mode:**

- **AUTO (default)** — run paper-to-code checks only when artifacts are available; otherwise skip without penalty.
- **ON** — user explicitly requests implementation checking; inspect all supplied artifacts and state what remains unverifiable.
- **OFF** — user explicitly requests a manuscript-only audit.

Do not infer implementation behavior from the manuscript when code is absent. Do not infer scientific defects from the absence of code.

**Double-blind leak check (30 seconds, do it every time for an anonymous submission).** Scan for: author names or affiliations left in the text, acknowledgements, non-anonymized repository or project URLs, self-citations phrased as "our previous work [12]", identifying dataset or lab names, PDF metadata. A leak is a desk-reject risk regardless of scientific quality — report it at the top even though venue formatting is otherwise out of scope.

## Step 1 — Extract the Logical Spine

Write down only:

- target scenario / problem;
- what a credible solution must achieve;
- the structural gap in prior work;
- the missing object, mechanism, or capability the paper claims to supply;
- 1-4 core claims;
- the current evidence for each claim.

If this cannot be written clearly, flag **storyline ambiguity** before auditing further — everything downstream depends on knowing what is actually being claimed.

## Step 2 — Novelty Stress Test (search required)

Strip application-specific terminology, then compare the method *structure* against direct competitors, neighboring fields with the same problem structure, classical algorithmic paradigms, and dangerous simple baselines.

**Minimum search protocol — run it, do not judge novelty from memory:**

1. Two web-search queries on the **de-jargonized method structure** (describe what it does mechanically, with no application nouns).
2. One query naming the **strongest competitor** the paper itself cites, to find work that cites or supersedes it.
3. One **counterexample query** of the form "X without Y" or "simple baseline for X" — hunting for the cheap alternative that would embarrass the contribution.
4. Retrieve the two or three most threatening hits to confirm what they actually do. Prefer the original papers or official research pages; do not characterize a paper from its title.

If search is unavailable or returns nothing usable, label the finding `novelty: unverified by search` and **do not** use "first", "novel", or "previously unexplored" anywhere in the output.

For each core contribution ask: is this a new object/mechanism, or a known paradigm instantiated in a new application? Does the novelty live in the algorithm, representation, interface, theory, evaluation protocol, dataset, or system integration? What is the most dangerous prior-work framing that makes this look incremental? Even granting that framing, what remains robustly defensible?

## Step 3 — Literature-Validation Consistency

Every weakness attributed to prior work in the Introduction or Related Work must be tested later by evidence measuring the same property. For each criticism, ask:

> **Where does this paper test, establish, or explicitly bound this property?**

- "high computational cost" → runtime / complexity evidence
- "vulnerable to ambiguity" → ambiguity-specific or failure-case evaluation
- "insufficient robustness" → disturbance, noise, or domain-shift tests
- "cannot identify X" → identifiability or discriminative evaluation
- "unsafe" → safety metrics, violation statistics, or guarantees

If the paper attacks an attribute but never measures it, flag **literature-validation mismatch**.

## Step 4 — Method and Number Consistency

Always active when the manuscript content is available; requires no source code. Verify that prose, equations, pseudocode, figures, symbol definitions, thresholds, and the experimental protocol all describe the same method — and that every reported number is self-consistent.

Read [references/method-consistency.md](references/method-consistency.md) for the full checklist and the reported-number audit.

Status: **Aligned / Partially aligned / Unclear / Partially verifiable / Contradicted**.

A contradiction that changes the scientific mechanism, information access, causal structure, or result interpretation is normally **S3-S4**, depending on whether it touches a central claim.

## Step 5 — Implementation Fidelity (conditional)

Run only when implementation artifacts are available under `AUTO`, or when the user selects `ON`. **Skip entirely otherwise, and do not create a section for it in the output.**

When triggered, read [references/implementation-fidelity.md](references/implementation-fidelity.md) and follow it. It covers algorithm fidelity, hidden mechanisms, experiment-code consistency, baseline fairness, the result-generating path (**Dead Novelty**), and common AI-coding failure patterns. If mode is `ON` but no artifacts are available, report `Not checked` and name the missing materials without assigning a severity level.

Status: same five values as Step 4.

## Step 6 — Claim-Evidence Matrix

This is the single organizing structure for the audit. Every other step feeds it. For each core claim, fill one row:

| Column | Question | Values |
|---|---|---|
| **Effectiveness** (Gate A) | Does the claimed effect occur, and beat relevant alternatives under fair conditions? | E0-E5 |
| **Attribution / Necessity** (Gate B) | Does the gain come from the claimed contribution, and is it needed against credible simpler alternatives? | E0-E5 |
| **Generality / Boundary** | How far does the conclusion generalize; are failure cases and invalid conditions explicit? | E0-E5 |
| **Strongest alternative explanation** | The best skeptical account that does not require the contribution | one sentence |
| **Status** | Supported / Overreaching / Unsupported / **Not checked** | — |

Rules:

- Grade each cell **against that claim**, not against the paper as a whole.
- Not every claim needs evidence in every column. Require only what the claim implies, and mark the rest `Not required`.
- If you did not verify a cell, write **`Not checked`** and list the reason below the table. Never fill a cell by inference.

Before interpreting any validation result, confirm the evaluated method is the method the manuscript describes. If Step 4 or Step 5 is **Contradicted**, identify the affected results and downgrade confidence in conclusions that depend on them. If the affected scope cannot be isolated, say so explicitly.

## Step 7 — Validation Audit

Classify each piece of evidence by function — theory/analysis, simulation/synthetic, dataset/benchmark, real-world/hardware — then judge whether it is decisive for the claim it serves. The single sharpest test:

> **If this validation item were removed, would the support for a claim, its uncertainty, or its tested boundaries change?** Independent replication can strengthen a conclusion without changing its wording. Flag validation as redundant only when it adds no material support, precision, boundary coverage, or reproducibility evidence.

Read [references/validation-audit.md](references/validation-audit.md) for the eight validation questions, the simulation audit, and the statistical-rigor checklist (significance, error bars, seeds, sample size, multiple comparisons, cherry-picking).

## Step 8 — Ablation Audit

A useful ablation **distinguishes among explanations**; it is not another table row. Check that one factor changes at a time where feasible; confounders are matched; the claimed contribution is genuinely removed and/or replaced; the full method does not secretly receive extra information; the ablation targets the claim rather than arbitrary implementation details; and negative or non-significant results are read honestly. Theory, simulation, benchmarks, or hardware all qualify as long as the key alternative explanation is ruled out.

## Step 9 — Strongest Reviewer Attack

For each core claim, write the single strongest reasonable reviewer objection in one sentence. Prefer forms like:

- "The method works, but the improvement may come from X rather than the claimed mechanism."
- "A simpler baseline Y plus a straightforward modification may achieve the same effect."
- "The current metric cannot distinguish the property being claimed."
- "The paper criticizes prior work for Z but never measures Z."
- "The hardware experiment demonstrates feasibility, not the claimed general superiority."
- "The simulation establishes the mechanism under controlled conditions but does not support the real-world generalization claim."

Then state: **what is the minimum decisive evidence that defeats this objection?**

## Step 10 — Severity and Evidence Levels

**Severity.** S0 none · S1 presentation/reporting · S2 clarity, reproducibility, local reasoning · S3 evidence gap affecting an important claim (needs analysis, baseline, ablation, or claim narrowing) · S4 core validity, novelty, implementation-fidelity, or causal-attribution failure (central story may not hold).

**Evidence strength.** E0 assertion only · E1 intuition or anecdote · E2 definition, citation, or descriptive result · E3 claim-relevant analysis or diagnostic that rules out *some* explanations · E4 quantitative evidence discriminating at least one important pair of competing explanations · E5 decisive — targets the central dispute under claim-matched conditions and rules out the main credible alternatives.

**Before assigning any level, read [references/calibration.md](references/calibration.md).** It contains worked examples with explicit adjacent-band reasoning and guards against rating drift. Do not apply these scales from the one-line definitions alone.

## Step 11 — Minimal Repair and Fatality

For each S3/S4 issue prioritize exactly three repair types: **add decisive evidence**, **narrow or change the claim**, **reframe the contribution**. If narrowing removes the logical overreach, do not demand new experiments.

Classify each major issue: **Cosmetic** (conclusion unchanged) · **Repairable** (local analysis, validation, or rewriting) · **Structural** (requires changing the core claim or evaluation logic) · **Potentially fatal**.

A missing experiment is **not automatically fatal**. Treat an issue as potentially fatal only when the decisive evidence needed for the core novelty cannot realistically be obtained, is experimentally infeasible, or would still fail to separate the authors' explanation from a credible alternative even if performed.

# Output Format

**Hard limits: ≤ 1200 words total. Each table ≤ 6 rows. Report only S3/S4 issues individually; collapse all S0-S2 findings into a single line. Order every list by severity, descending.** Omit any section with nothing to report — do not emit empty headers.

```text
1. Assessment
- Defensibility: Strong / Borderline / Weak
- Largest risk: ...
- Main problem type: idea / consistency / implementation / evidence / writing
- [Double-blind leak: ... — only if found]

2. Logical spine
- Gap -> Contribution -> Claim -> [Implementation, if verifiable] -> Evidence -> Conclusion

3. Method & number consistency
- Status: Aligned / Partially aligned / Unclear / Partially verifiable / Contradicted
- Material contradictions: ...

4. Implementation fidelity            [omit entirely if not triggered]
- Mode: AUTO / ON | Status: ...
- Most consequential mismatch: ...
- Hidden mechanism / fairness / result-path risk: ...

5. Claim-evidence matrix
| Claim | Effectiveness | Attribution/Necessity | Generality/Boundary | Strongest alternative | Status |
- Not checked, and why: ...

6. Highest-risk issues  (S3/S4 only, severity descending)
| Issue | S | Why it matters | Minimum decisive repair | If unfixed |

7. Validation
- Decisive evidence: ...
- Shows effectiveness but not necessity: ...
- Missing evidence roles (theory / simulation / benchmark / hardware): ...
- Statistical rigor gaps: ...
- Redundant or decorative validation: ...
- Missing dangerous baseline/control: ...

8. Novelty & literature risk
- Search performed: yes / no — [if no: "novelty unverified by search"]
- Closest / most dangerous prior work: ...
- Literature-validation mismatch: ...
- Claims that must be narrowed: ...

9. Decision
- Submit as is / minor repair / major repair / reframe / redirect venue
- Minimum work required before submission: ...

10. Minor issues (S0-S2): one line, aggregated.
```

If no implementation artifacts were supplied in `AUTO` mode, omit section 4 and optionally add one line:

> Implementation fidelity was not assessed because no artifacts were supplied; this is not a manuscript defect.

## Fast Audit Mode

When the user asks only for a quick judgment, output only: largest scientific risk; whether the manuscript is internally consistent; implementation-fidelity status *only if Step 5 is triggered*; whether validation shows **works** or already establishes **needed**; strongest alternative explanation; minimum decisive repair; S-level. No tables.
