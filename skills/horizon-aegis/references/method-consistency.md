# Method and Number Consistency Audit (Step 4)

Always active when manuscript content is available. Requires no source code.

Audit the main text and appendix together; a method specification can be split across both.

## Part 1 — Do these describe the same method?

Cross-check every pair that the paper actually contains:

- prose description
- mathematical equations and objective functions
- algorithm / pseudocode
- figures, flowcharts, state diagrams
- symbol definitions and coordinate-frame conventions
- thresholds, hyperparameters, stopping conditions
- experimental setup and evaluation protocol

Look specifically for:

- contradictory parameter values or thresholds between text, table, and appendix;
- inconsistent Top-K, window length, iteration count, or update frequency;
- mismatched coordinate frames or transform direction;
- causal / online claims contradicted by use of future information;
- equations implying a different update rule than the pseudocode;
- figures introducing undeclared modules, or omitting claimed ones;
- experimental settings that quietly differ from the stated method;
- a loss or objective written one way in the method section and another in the appendix derivation;
- notation reused for two different quantities, or redefined mid-paper.

## Part 2 — Reported-number consistency

High yield, low cost, and frequently the first thing a careful reviewer checks. Verify:

- **Abstract vs. body vs. table.** Does the headline number in the abstract appear, unchanged, in the results table?
- **Deltas and percentages.** Recompute every claimed improvement from the raw numbers. Confirm the stated baseline is actually the strongest one in the table.
- **Relative vs. absolute.** Is "+3%" percentage points or a relative change? Is the convention consistent across the paper?
- **Sums and totals.** Do per-class, per-split, or per-scenario numbers reconcile with the reported totals and averages? Is the average weighted where it should be?
- **Counts.** Do dataset sizes, split sizes, trial counts, and seed counts agree everywhere they appear?
- **Bolding and "best" claims.** Is the bolded entry actually the best column value? Does any "we outperform all baselines" statement survive reading the table?
- **Units and magnitudes.** ms vs. s, degrees vs. radians, MB vs. MiB, per-frame vs. per-sequence.
- **Figures vs. tables.** Do plotted values match the tabulated ones? Do error bars in the figure match the variance reported in the text?
- **Captions vs. content.** Does each caption describe what the figure or table actually shows, including axis labels, units, and legend entries?
- **Cross-references.** Does every "see Table 3" point at the right object?

An arithmetic slip is usually **S1**. But treat it as **S3** when the corrected number changes which method wins, crosses a significance threshold, or contradicts a claim made in the abstract.

## Part 3 — Status

- **Aligned** — no material contradiction found.
- **Partially aligned** — minor or local differences, but the scientific method remains identifiable.
- **Unclear** — the manuscript does not specify enough detail to determine consistency.
- **Partially verifiable** — some components could not be read (missing appendix, unrenderable math, scanned pages). List which.
- **Contradicted** — two or more components describe materially different methods.

A contradiction that changes the scientific mechanism, information access, causal structure, or result interpretation is normally **S3-S4**, depending on whether a central claim depends on it.

When status is **Contradicted**, state which results depend on the inconsistent specification and downgrade confidence in those conclusions. If you cannot determine which method generated the reported numbers or isolate the affected results, report that uncertainty explicitly.
