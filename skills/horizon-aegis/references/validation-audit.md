# Validation Audit (Step 7)

First determine what type of evidence each claim needs. Do not mechanically require every paper to contain theory, simulation, and hardware experiments.

## Evidence classified by function

- **Theory / Analysis** — properties, bounds, stability, complexity, identifiability, necessary mechanism relations.
- **Simulation / Synthetic** — mechanism isolation, counterfactual construction, parameter sweeps, stress testing, failure-boundary analysis.
- **Dataset / Benchmark** — comparative performance, generalization, statistical stability, fair competition with prior work.
- **Real-world / Hardware** — practical feasibility, deployment constraints, system effects, performance under real disturbance.

Before interpreting any validation result, confirm the evaluated method is the method the manuscript describes. If method consistency or implementation fidelity is **Contradicted**, downgrade confidence in conclusions that depend on the affected results. Report when that scope cannot be isolated.

## The eight questions

For each validation item:

1. Which specific claim would change if this evidence succeeded or failed?
2. Does it merely show the full system works, or does it distinguish among competing explanations?
3. Is the baseline / control strong enough to genuinely threaten the claimed contribution?
4. Are information access, compute, tuning, data, supervision, sensors, initialization, and prior knowledge fairly matched?
5. Does it test the scenarios where the proposed mechanism should matter most?
6. Do the metric and evaluation protocol actually measure the property being claimed?
7. Is the evidence modality appropriate, or is there an evidence-claim mismatch?
8. **If this item were removed, would support for the claim, its uncertainty, or its tested boundaries change?**

An unchanged conclusion does not make independent replication redundant. Flag **decorative or redundant validation** only when the item adds no material support, precision, boundary coverage, or reproducibility evidence. Explain what it fails to establish before recommending removal.

## Simulation Audit

When the paper uses simulation, synthetic data, or highly controlled virtual environments:

1. **Mechanism isolation** — does it exploit controllability to vary the key factor while holding confounders fixed?
2. **Counterfactual / necessity** — does it test "what happens without this mechanism?" or "what about a simpler replacement?"
3. **Stress & boundary** — does it systematically cover claim-relevant hard conditions: noise, occlusion, ambiguity, dynamic disturbance, initialization error, latency, sensor failure, scale changes?
4. **Simulation validity** — are dynamics, sensors, noise, latency, calibration, or environment structure unrealistically idealized? Does the method receive privileged information unavailable in deployment?
5. **Statistical validity** — see below.
6. **Simulation-to-claim boundary** — what can this simulation legitimately support? Has the paper jumped from "the mechanism works under controlled assumptions" to "the method is generally robust / superior in the real world"?

Simulation is not a lower-grade substitute for hardware testing. For claims about mechanism, necessity, identifiability, or failure boundaries, a well-designed controlled simulation is often the **most** decisive evidence available. Conversely, a simulation that merely repeats average-performance evaluation under nominal conditions has little evidential value regardless of how much of it there is.

## Statistical Rigor

Check every quantitative comparison the paper's conclusions rest on:

- **Repetition.** For any stochastic method: how many seeds, scenes, or runs? Distinguish uncertainty across training runs from uncertainty across test samples. A single run may support a result for that fixed model, but does not establish stability across runs; grade against the actual claim.
- **Dispersion.** Are standard deviations, confidence intervals, or error bars reported — and is the *type* stated (std vs. sem vs. 95% CI)? Unlabeled error bars are uninterpretable.
- **Uncertainty in the difference.** Inspect the effect size and uncertainty of the between-method difference, using paired analysis when observations are matched. Overlap of separate error bars does not by itself establish the absence of a difference. If the necessary data or summary statistics are unavailable, mark significance `Not checked`. See the [NIST formulas for confidence intervals of mean differences](https://itl.nist.gov/div898/handbook/prc/section3/prc312.htm) for paired and unpaired designs.
- **Significance testing.** Is any test reported for the headline comparison? Is the test appropriate (paired vs. unpaired, parametric assumptions plausible)?
- **Multiple comparisons.** If the paper reports many method-dataset-metric cells and highlights the wins, is any correction applied — or is the "best" result selection bias?
- **Sample size.** Is the evaluation set large enough that the reported precision is meaningful? Watch for three-decimal accuracy on a 50-item test set.
- **Seed and checkpoint selection.** Is the reported run the best of N? Is the checkpoint selected on the test set? Either is a silent evaluation leak.
- **Test-set reuse.** Were hyperparameters tuned on the test split? Is there a separate validation split at all?
- **Cherry-picked qualitative results.** Are figure examples representative or selected? Are failure cases shown anywhere?
- **Baseline numbers' provenance.** Copied from original papers or re-run under this paper's protocol? Check whether splits, metrics, data access, and evaluation settings match. Different provenance alone is not a defect; incompatible protocols can invalidate a comparison.

Missing uncertainty needed to support a central superiority or stability claim is normally **S3**; non-significance alone does not establish equivalence. Evaluation leakage — test-set tuning, test-set checkpoint selection, or best-of-N reporting presented as a single run — is normally **S4** when it undermines the central conclusion. Explain the affected claim and severity rather than assigning a level from the label alone.

## Reporting

Separate three things explicitly in the output:

- **Decisive evidence** — what genuinely establishes a claim.
- **Effective but not necessary** — what shows the system works without showing the contribution was needed.
- **Missing evidence roles** — which of theory / simulation / benchmark / hardware is absent *and required by an actual claim*. Do not list absent modalities that no claim needs.
