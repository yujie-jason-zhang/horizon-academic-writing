# Calibration: Severity (S) and Evidence (E) Levels

The one-line definitions in SKILL.md are not sufficient to grade consistently. The band boundaries matter more than the band descriptions. Read the three worked examples below before assigning any level.

## The two rules that prevent most mis-grades

**Rule 1 — Grade evidence per claim, not per artifact.** A single results table can be E4 for "the method outperforms baselines" and E1 for "the gating module is what causes the gain." Always name which claim you are grading.

**Rule 2 — Severity reflects the effect on the claim and the scope of repair.** S3 is an important evidence gap that can be repaired while preserving the central contribution. S4 puts the central scientific story at risk. Needing an experiment does not alone make an issue S4, and a cheap repair does not alone make it minor.

---

## Example A — S4 / E1

**Situation.** Contribution #1 is an attention-gating module. The paper states: *"our attention-gating module is what enables cross-domain robustness."* Evidence offered: one table where the full method beats three baselines on two datasets, plus two paragraphs of intuition about why gating should help under domain shift. There is no ablation removing or replacing the gate.

**Evidence level for the attribution claim: E1.** The only thing supporting *attribution* is a plain-language argument.

- **Not E2** — E2 requires a definition, citation, protocol detail, or descriptive result that at least clarifies the claim. The intuition paragraphs describe a hoped-for mechanism; they measure nothing. The results table is real evidence, but it is evidence for a *different* claim (effectiveness), and reusing it here is exactly the Rule 1 error.
- **Not E0** — E0 is bare assertion with no checkable support at all. There is a stated mechanism story that could in principle be tested, so it clears E0.
- For the *effectiveness* claim, that same table is roughly E3-E4 depending on baseline strength. Report both.

**Severity: S4.**

- **Not S3** — S3 covers evidence gaps repairable by added analysis, a baseline, an ablation, *or claim narrowing*. Here the claim is explicitly causal ("is what enables") and it is the paper's headline contribution. Narrowing it to "the full method is robust across domains" deletes contribution #1, which changes the paper's story rather than repairing it. When the only in-place repair guts the central claim, it is S4.
- **Not S2** — nothing about this is a clarity or reproducibility problem. The claim is clearly stated; it is just unsupported.

**Minimum decisive repair.** A replacement ablation at matched compute — swap the gate for a strong standard alternative (e.g. a plain residual path), holding other relevant factors fixed. If the proposed gate retains an advantage with adequate uncertainty estimates, this can move attribution to E4 against that alternative. If the replacement matches it, narrow or reframe the causal contribution instead; do not prescribe the result.

---

## Example B — S3 / E3

**Situation.** The paper claims robustness to sensor noise. Evidence: a simulation noise sweep showing graceful degradation up to σ = 0.1, plus a complexity analysis. Deployment noise in the target application is approximately σ = 0.3. The abstract says the method is *"robust under real-world conditions."*

**Evidence level: E3.** The sweep is genuine, claim-relevant diagnostic evidence about how the mechanism behaves as noise grows.

- **Not E4** — E4 requires discriminating between at least one important pair of competing explanations. The sweep shows *that* the method degrades gracefully; it never asks whether a trivial median filter produces the same curve. The obvious competing explanation is untested. Adding that baseline could move the evidence to E4 if the comparison reliably distinguishes the explanations; assess feasibility from the available setup.
- **Not E2** — it is more than a descriptive result: it varies the causal factor systematically and maps a boundary.

**Severity: S3.**

- **Not S4** — the evidence is real, well-constructed, and points the right way. The defect is that the abstract's claim reaches past the tested range. Narrowing the claim to "robust for σ ≤ 0.1, covering [stated conditions]" repairs it completely with no new experiments, and the paper still has a contribution. Repairable-in-place on an important claim is the definition of S3.
- **Not S2** — this is not a clarity issue. As currently written the abstract makes an unsupported empirical claim, and a reviewer who works at σ = 0.3 will reject on it.

**Minimum decisive repair.** Either narrow the claim to the tested range, or extend the sweep to σ = 0.3 with a simple-filter baseline. The latter can address both the boundary and the competing explanation if its results support those conclusions; do not assume its cost or outcome.

---

## Example C — S1 / E4

**Situation.** Table 2's caption says "+3.2% over the strongest baseline," but the table's own numbers give +3.4%. The underlying ablation is well designed: matched compute, a replacement baseline rather than mere deletion, five seeds with confidence intervals.

**Evidence level: E4.** A matched-compute replacement ablation with CIs genuinely discriminates the main alternative explanation ("it's just more capacity").

- **Not E5** — E5 requires ruling out the *main credible alternatives*, plural, under claim-matched conditions. A second live alternative remains untested here: the gain may come from the stronger front-end encoder the proposed method also uses. Until that is matched or ablated, this is E4 however clean the statistics are.
- **Not E3** — it does more than diagnose the mechanism; it puts a competing explanation on the table and knocks one down.

**Severity: S1.**

- **Not S2** — S2 is for clarity, reproducibility, or local reasoning defects. Either number supports the same conclusion, no reader is misled about the science, and nothing about reproduction changes.
- **Not S0** — it is still a real defect. A reviewer who recomputes it loses confidence in every other number in the paper, which is disproportionate damage for an arithmetic slip.

**Minimum decisive repair.** Fix the caption. Then re-check every other reported delta in the paper, since this kind of error is rarely isolated.

---

## Calibration drift guards

Check these against your finished finding list before reporting:

1. **Middle-band clustering.** Re-check adjacent-band reasoning when many findings sit at S2 or E3, but retain those levels when justified. Never force a distribution or change a score to meet a quota.
2. **Verdict consistency.** Explain how the findings support the overall defensibility verdict. Several S3 gaps can jointly justify "Weak" without inventing an S4.
3. **Repair cost versus scientific impact.** S4 requires an explicit explanation of why the central story is at risk. Judge the claim impact and required change, not experiment cost alone; a caption slip that leaves the conclusion intact remains S1.
4. **Multiple E5 ratings.** Verify independently that each claim's main credible alternatives are ruled out under claim-matched conditions. There is no per-paper quota; do not promote or demote evidence to shape the distribution.
5. **High E with `Not checked` neighbors.** If you could not verify the experimental setup, the evidence grade cannot exceed E3 regardless of how the results are presented.
6. **Severity assigned for a missing artifact.** Never. Absence of supplied code, data, or an appendix is not a defect of the manuscript — it is a limit on your audit, and belongs in `Not checked`.
