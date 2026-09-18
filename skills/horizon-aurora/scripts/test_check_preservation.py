#!/usr/bin/env python3
"""CLI regression tests. Run: python3 scripts/test_check_preservation.py"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name("check_preservation.py")


def document(body: str, preamble: str = "") -> str:
    return (
        "\\documentclass{article}\n"
        + preamble
        + "\\begin{document}\n"
        + body
        + "\n\\end{document}\n"
    )


class PreservationTests(unittest.TestCase):
    def check(self, original, candidate, expected=0, *, flags=(), children=None):
        with tempfile.TemporaryDirectory(prefix="aurora-test-") as temporary:
            root = Path(temporary)
            for index, (variant, content) in enumerate(
                (("original", original), ("candidate", candidate))
            ):
                folder = root / variant
                folder.mkdir()
                (folder / "main.tex").write_bytes(content.encode("utf-8"))
                for relative_path, pair in (children or {}).items():
                    target = folder / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(pair[index].encode("utf-8"))
            result = subprocess.run(
                [
                    sys.executable, str(CHECKER),
                    str(root / "original/main.tex"),
                    str(root / "candidate/main.tex"), *flags,
                ],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result.stdout + result.stderr

    def test_unchanged_document(self):
        source = document(r"Latency was 10 ms; we use $x+y$ and cite \cite{smith}.")
        self.check(source, source)

    def test_single_file_manuscript_polish(self):
        source = document(
            r"\begin{abstract}We performed an evaluation of the method.\end{abstract}" "\n"
            r"\section{Methods}\label{sec:methods} We use $x+y$." "\n"
            r"\section{Results}The measured latency was 10 ms on Dataset A." "\n"
            r"\begin{tabular}{cc} Method & Latency \\ Baseline & 20 ms \\ Ours & 10 ms \\ \end{tabular}" "\n"
            r"\section{Conclusion}These results suggest a benefit on Dataset A."
        )
        candidate = source.replace("performed an evaluation of", "evaluated").replace(
            "The measured latency was", "Latency was"
        )
        self.check(source, candidate, flags=("--reader-oriented",))

    def test_translation_preserves_protected_content(self):
        self.check(
            document(r"在数据集 A 上，延迟为 10 ms，采用 $x+y$，参见 \cite{smith}。"),
            document(r"On Dataset A, latency was 10 ms. We use $x+y$; see \cite{smith}."),
            flags=("--reader-oriented", "--translation"),
        )

    def test_translation_word_based_quantities_are_explicitly_manual(self):
        output = self.check(
            document("采用三种方法。"), document("We used three methods."),
            flags=("--translation",),
        )
        self.assertIn("Translation coverage: PARTIAL for quantities", output)

    def test_translation_does_not_relax_digits_units_or_math(self):
        for before, after in (("10 ms", "20 ms"), ("10 ms", "10 s"), ("$x$", "$y$"), ("²", "³")):
            with self.subTest(before=before):
                self.check(document(before), document(after), 1, flags=("--translation",))

    def test_default_still_protects_word_based_quantities(self):
        self.check(document("We used three methods."), document("We used four methods."), 1)
        self.check(document("采用三种方法。"), document("采用四种方法。"), 1)

    def test_numeric_unit_sign_and_math_damage(self):
        for before, after in (
            ("10 ms", "20 ms"), ("10 ms", "10 s"),
            ("-10 ms", "10 ms"), ("$x+y$", "$x-y$"),
        ):
            with self.subTest(before=before, after=after):
                self.check(document(before), document(after), 1, flags=("--reader-oriented",))

    def test_numeric_reordering_requires_reader_mode(self):
        original = document("Latency was 10 ms. Memory usage was 20 MB.")
        candidate = document("Memory usage was 20 MB. Latency was 10 ms.")
        self.check(original, candidate, 1)
        self.check(original, candidate, flags=("--reader-oriented",))

    def test_citation_reordering_is_explicit(self):
        original = document(r"A \cite{alpha}. B \cite{beta}.")
        candidate = document(r"B \cite{beta}. A \cite{alpha}.")
        self.check(original, candidate, 1)
        self.check(original, candidate, flags=("--allow-structural-reorder",))

    def test_cross_reference_reordering(self):
        self.check(
            document(r"See \ref{sec:a}, then \eqref{eq:b}."),
            document(r"See \eqref{eq:b}, then \ref{sec:a}."),
            flags=("--allow-structural-reorder",),
        )

    def test_citation_inventory_stays_strict(self):
        original = document(r"A \cite{alpha}. B \cite{beta}.")
        for candidate in (
            r"A. B \cite{beta}.",
            r"A \cite{alpha}. B \cite{beta,beta}.",
            r"A \cite{alpha}. B \cite{gamma}.",
        ):
            with self.subTest(candidate=candidate):
                self.check(original, document(candidate), 1, flags=("--allow-structural-reorder",))

    def test_environment_reordering_is_not_authorized(self):
        self.check(
            document(r"\begin{itemize}\item A\end{itemize}\begin{enumerate}\item B\end{enumerate}"),
            document(r"\begin{enumerate}\item A\end{enumerate}\begin{itemize}\item B\end{itemize}"),
            1, flags=("--allow-structural-reorder",),
        )

    def test_other_protected_events_cannot_reorder(self):
        for first, second in (
            (r"\label{sec:a}", r"\label{sec:b}"),
            (r"\includegraphics{first.pdf}", r"\includegraphics{second.pdf}"),
            ("% first\n", "% second\n"),
            ("$x$", "$y$"),
        ):
            with self.subTest(first=first):
                self.check(
                    document(first + "\n" + second), document(second + "\n" + first),
                    1, flags=("--allow-structural-reorder", "--reader-oriented"),
                )

    def test_comments_and_literal_code_remain_exact(self):
        for original, candidate in (
            ("% original\nBody.", "% changed\nBody."),
            (r"\verb|original|", r"\verb|changed|"),
        ):
            with self.subTest(original=original):
                self.check(document(original), document(candidate), 1)

    def test_preamble_macro_change_fails(self):
        self.check(
            document(r"We use \modelname.", r"\newcommand{\modelname}{Baseline}" "\n"),
            document(r"We use \modelname.", r"\newcommand{\modelname}{Proposed}" "\n"),
            1, flags=("--reader-oriented", "--allow-structural-reorder"),
        )

    def test_preamble_preserves_line_endings_and_whitespace(self):
        source = document("Body.")
        self.check(source.replace("\n", "\r\n"), source.replace("\n", "\r\n"))
        self.check(source.replace("\n", "\r\n"), source, 1)
        self.check(source, source.replace("{article}\n", "{article} \n"), 1)

    def test_document_marker_inside_literal_or_macro_is_not_preamble_end(self):
        preamble = (
            "% \\begin{document}\n"
            r"\newcommand{\example}{\begin{document}}" "\n"
            r"\newcommand{\modelname}{Baseline}" "\n"
        )
        self.check(
            document("Body.", preamble),
            document("Body.", preamble.replace("Baseline", "Proposed")), 1,
        )

    def test_fragments_allow_prose_changes(self):
        self.check("We performed an evaluation.", "We evaluated the method.")

    def test_table_separator_deletion_fails(self):
        for environment, arguments in (
            ("tabular", "{cc}"), ("tabular*", r"{\textwidth}{cc}"),
            ("tabularx", r"{\textwidth}{XX}"), ("longtable", "{cc}"),
        ):
            with self.subTest(environment=environment):
                body = rf"\begin{{{environment}}}{arguments} A & B \\ C & D \\ \end{{{environment}}}"
                self.check(document(body), document(body.replace("A & B", "A B")), 1)

    def test_table_separator_distribution_stays_fixed(self):
        self.check(
            document(r"\begin{tabular}{ccc} A & B & C \\ D & E \\ \end{tabular}"),
            document(r"\begin{tabular}{ccc} A & B C \\ D & E & F \\ \end{tabular}"),
            1, flags=("--allow-structural-reorder",),
        )

    def test_table_row_boundaries_and_options_stay_fixed(self):
        original = document(r"\begin{tabular}{cc} A & B \\*[2pt] C & D \\ \end{tabular}")
        for candidate in (
            original.replace(r"\\*[2pt]", r"\\[2pt]"),
            original.replace(r"\\*[2pt]", r"\\*2pt"),
            original.replace(r"\\*[2pt]", ""),
        ):
            with self.subTest(candidate=candidate):
                self.check(original, candidate, 1)

    def test_table_prose_and_escaped_ampersands(self):
        original = document(
            r"\begin{tabular}{cc} \textbf{Old description} & A \& B \\ "
            r"\href{https://example.invalid/?a=b&c=d}{Link} & \verb|a&b| \\ \end{tabular}"
        )
        self.check(original, original.replace("Old description", "Clear description"))

    def test_existing_label_and_numbering_are_advisories(self):
        for body in (
            "Figure 1 shows the method.",
            r"\section{Method}\label{sec} See Section~\ref{sec}.",
        ):
            with self.subTest(body=body):
                output = self.check(document(body), document(body))
                self.assertIn("ADVISORY", output)

    def test_style_advisory_does_not_relax_label_protection(self):
        self.check(document(r"\label{sec}"), document(r"\label{sec:method}"), 1)

    def test_reference_wording_is_advisory(self):
        output = self.check(
            document(r"Fig.~\ref{fig:method} shows the method."),
            document(r"Figure~\ref{fig:method} shows the method."),
        )
        self.assertIn("ADVISORY", output)

    def test_include_requires_project_mode(self):
        source = document(r"\input{results}")
        output = self.check(source, source, 1, children={"results.tex": ("10 ms", "20 ms")})
        self.assertIn("--project", output)

    def test_project_polishing_and_child_damage(self):
        source = document(r"\input{sections/methods}\input{sections/results}")
        children = {
            "sections/methods.tex": ("We performed an evaluation.", "We evaluated the method."),
            "sections/results.tex": ("Latency was 10 ms.", "Latency was 10 ms."),
        }
        self.check(source, source, flags=("--project", "--reader-oriented"), children=children)
        children["sections/results.tex"] = ("Latency was 10 ms.", "Latency was 20 ms.")
        self.check(source, source, 1, flags=("--project", "--reader-oriented"), children=children)

    def test_project_missing_cyclic_and_dynamic_inputs_fail(self):
        for body, children in (
            (r"\input{missing}", {}),
            (r"\input{child}", {"child.tex": (r"\input{main}", r"\input{main}")}),
            (r"\input{\partname}", {}),
        ):
            with self.subTest(body=body):
                self.check(document(body), document(body), 1, flags=("--project",), children=children)

    def test_project_included_preamble_is_protected(self):
        source = document("Body.", r"\input{settings}" "\n")
        self.check(source, source, 1, flags=("--project",), children={
            "settings.tex": (r"\newcommand{\name}{Old}", r"\newcommand{\name}{New}"),
        })

    def test_project_subfile_preamble_is_protected(self):
        root = document(r"\subfile{section}")
        section = document("Body.", r"\newcommand{\name}{Old}" "\n")
        self.check(root, root, flags=("--project",), children={"section.tex": (section, section)})
        self.check(root, root, 1, flags=("--project",), children={
            "section.tex": (section, section.replace("{Old}", "{New}")),
        })

    def test_include_in_comment_or_literal_does_not_require_traversal(self):
        source = document("% \\input{missing}\n" r"\verb|\input{also-missing}|")
        self.check(source, source)

    def test_registered_custom_arguments_are_protected(self):
        self.check(
            document(r"The source is \artifact{baseline.csv}."),
            document(r"The source is \artifact{proposed.csv}."),
            1, flags=("--protect-command", "artifact=1"),
        )

    def test_custom_optional_and_multiple_arguments(self):
        original = document(r"\artifact[raw]{dir}{source.csv}{Old description}")
        flags = ("--protect-command", "artifact=2")
        self.check(original, original.replace("Old description", "Clear description"), flags=flags)
        for candidate in (original.replace("raw", "clean"), original.replace("source.csv", "other.csv")):
            with self.subTest(candidate=candidate):
                self.check(original, candidate, 1, flags=flags)

    def test_unregistered_custom_arguments_require_manual_review(self):
        output = self.check(
            document(r"\artifact{baseline.csv}"), document(r"\artifact{proposed.csv}")
        )
        self.assertIn("Manual review required for unregistered custom macro arguments", output)

    def test_invalid_custom_registration_is_rejected(self):
        for registration in ("artifact=-1", "artifact=x", "cite=0", "SI=0"):
            with self.subTest(registration=registration):
                self.check(document("Body."), document("Body."), 2, flags=("--protect-command", registration))

    def test_symbol_normalization_keeps_other_content_strict(self):
        self.check(document("We use $x$."), document("We use $y$."), flags=("--approved-symbol-map", "x=y"))
        self.check(document("We use $x$."), document("We discard $y$."), 1, flags=("--approved-symbol-map", "x=y"))


if __name__ == "__main__":
    unittest.main()
