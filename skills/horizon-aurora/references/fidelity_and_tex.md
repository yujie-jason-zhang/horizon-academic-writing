# Fidelity and TeX Safety

## Purpose

Protect scientific meaning while allowing reader-oriented editing.

## 1. Claims

Preserve:

- claim object;
- scope;
- strength;
- uncertainty;
- conditions;
- exceptions;
- observation vs. interpretation.

Do not shift:

- `may improve` → `improves`;
- `suggests` → `demonstrates`;
- `associated with` → `causes`;
- `outperforms on Dataset A` → `outperforms`;
- `reduces` → `eliminates`.

Directness is allowed only when epistemic status and scope remain identical.

## 2. Agency and Causality

Preserve:

- who performs an action;
- what affects what;
- which component produces which effect;
- procedural order;
- causal direction.

Voice changes must not alter agency.

## 3. Numerical Semantic Binding

Preserve:

**value ↔ metric ↔ unit ↔ condition ↔ dataset/method ↔ comparison**

Reader-oriented edits may move a numerical statement only when all bindings remain explicit and unambiguous.

Strict mode additionally preserves surface order more strongly.

For Chinese-to-English translation, `--translation` avoids treating ordinary Chinese words such as `参见` as numeric tokens and leaves word-based quantities to manual bilingual review. Digits, recognized units/signs, math, and protected TeX remain strict. Check all Han numerals, spelled-out English numbers, contextual Roman number words, and their bindings directly against the source; the flag does not verify their equivalence.

The checker does not normalize translated unit names or digit-to-word conversions. If an equivalent translation still produces a token mismatch, document the specific manually verified equivalence and the mechanical limitation. Do not change scientific quantities to make the script pass or claim complete mechanical verification.

## 4. Mathematics

Unless the user explicitly approves notation normalization, do not alter mathematical regions.

Protect inline math, display math, equation environments, theorem/proof logic, algorithmic expressions, signs, subscripts, superscripts, accents, and math fonts.

## 5. Structural TeX

Preserve:

- `\label{...}`;
- `\ref{...}` and `\eqref{...}`;
- citation and bibliography keys;
- file paths;
- `\input`, `\include`, and related project paths;
- protected custom-command arguments;
- comments;
- verbatim, listing, and code-like source.

Do not apply prose punctuation rules inside protected forms.

Preserve the preamble byte-for-byte, along with figure/table environments, column specifications, cell separators, and row boundaries. Caption and cell prose can change without changing their structural containers. The checker recognizes alignment separators and row breaks in `tabular`, `tabular*`, `tabularx`, and `longtable`; compare other table implementations manually.

### Custom macros

Do not infer that an unknown macro argument is editable prose. Inspect its definition or usage to classify the argument. The checker does not expand arbitrary TeX or automatically protect every custom argument.

For a conventional custom command with opaque leading brace arguments, register its case-sensitive name and argument count, without a backslash:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex --reader-oriented --protect-command artifact=1
```

This protects optional arguments and the first required argument of `\artifact{path}`. Repeat `--protect-command NAME=N` for other commands; `N` can be 0–9. Existing built-in protection cannot be overridden. Later arguments remain available for prose editing, so register the full opaque prefix. Interleaved, delimited, or otherwise nonstandard arguments require manual comparison. Register only macros whose argument syntax has been established.

For unregistered custom arguments, compare source and candidate directly. Report any unresolved protection gap; a mechanical PASS does not establish that these arguments were checked.

## 6. Citations

Preserve both citation keys and the relation between citation placement and claim scope.

Do not invent, replace, or broaden citation support unless explicitly requested.

## 7. Terminology

Do not replace technical entities merely for stylistic variety.

Track canonical names for high-impact recurring entities. Report unexplained drift rather than normalizing uncertain alternatives.

## 8. Notation and Values

Check recurring high-impact symbols, frames, parameters, values, units, and experimental conditions when they materially affect interpretation.

Before reporting a conflict, distinguish legitimate changes in dataset, split, condition, aggregation, or rounding.

If the intended correction cannot be inferred safely:

> `AUTHOR DECISION REQUIRED`

## 9. Semantic Drift Review

Mechanical preservation is not enough. Manually inspect lexical changes that can alter:

- mechanism;
- degree;
- certainty;
- scope;
- causality;
- temporal meaning;
- comparison strength.

A fluent substitution can still be scientifically wrong.

## 10. Preservation Checker

Commands below assume the skill directory as the working directory. Reader-oriented, standalone files:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex --reader-oriented
```

Strict:

```bash
python3 scripts/check_preservation.py original.tex candidate.tex
```

For deliberate citation/cross-reference reordering, use `--allow-structural-reorder`, then manually verify claim attachment.

For multi-file manuscripts, preserve independent original and candidate project copies with matching relative paths:

```bash
python3 scripts/check_preservation.py original/main.tex candidate/main.tex --reader-oriented --project
```

The checker fails coverage when includes are present without `--project`, or when traversal encounters missing, cyclic, or dynamic inputs. Other protected structural events remain ordered even when citation/reference reordering is enabled.

Run these checks against the final delivered artifacts after all repairs. Style advisories about existing labels or manual numbering do not authorize changing those protected items. Authorized preamble changes require a separate approved baseline; retain the untouched original as well.

The checker detects only mechanically visible preservation risks. It does not prove semantic equivalence.
