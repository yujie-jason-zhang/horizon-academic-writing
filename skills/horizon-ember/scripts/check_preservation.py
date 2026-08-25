#!/usr/bin/env python3
"""Check TeX preservation and hard polishing constraints between two TeX files."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


STRUCTURAL_COMMAND_RE = re.compile(
    r"\\(label|ref|pageref|eqref|cref|Cref|autoref|autopageref|nameref|subref|vref|cpageref|"
    r"includegraphics|citep|citet|cite|nocite|textcite|parencite|autocite|footcite|"
    r"bibitem|bibliography|addbibresource)\*?\s*"
    r"(?:\[[^\[\]]*\]\s*)*\{([^{}]*)\}"
)

BIBTEX_ENTRY_RE = re.compile(r"@\s*([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,")

INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics(?P<star>\*)?\s*"
    r"(?P<options>(?:\[[^\[\]]*\]\s*)*)\{(?P<path>[^{}]*)\}"
)

CAPTION_RE = re.compile(r"\\caption\s*(?:\[[^\[\]]*\]\s*)?\{([^{}]*)\}", re.DOTALL)

DISPLAY_NUMBER_RE = r"(?:\d+(?:\.\d+)*|[IVXLCDM]+)"

NUMBERED_CAPTION_PREFIX_RE = re.compile(
    rf"^\s*(?:fig(?:ure)?\.?|table|tab\.?|algorithm|alg\.?)\s*~?\s*{DISPLAY_NUMBER_RE}\b",
    re.IGNORECASE,
)

HARDCODED_REFERENCE_RE = re.compile(
    rf"\b(?:fig(?:ure)?s?\.?|tables?|tabs?\.?|eq(?:uation)?s?\.?|sections?|secs?\.?|"
    rf"alg(?:orithm)?s?\.?|appendices|appendix)\s*~?\s*{DISPLAY_NUMBER_RE}\b",
    re.IGNORECASE,
)

MANUAL_REFERENCE_STYLE_RE = re.compile(
    r"\b(?P<name>figs?\.|figures?|tabs?\.|tables?|eqs?\.|equations?|secs?\.|sections?)"
    r"\s*~?\s*\\(?P<command>ref|eqref|autoref|cref|Cref|subref)\s*\{",
    re.IGNORECASE,
)

REFERENCE_NAME_STYLES = {
    "fig.": ("figure", "abbr"),
    "figs.": ("figure", "abbr"),
    "figure": ("figure", "full"),
    "figures": ("figure", "full"),
    "tab.": ("table", "abbr"),
    "tabs.": ("table", "abbr"),
    "table": ("table", "full"),
    "tables": ("table", "full"),
    "eq.": ("equation", "abbr"),
    "eqs.": ("equation", "abbr"),
    "equation": ("equation", "full"),
    "equations": ("equation", "full"),
    "sec.": ("section", "abbr"),
    "secs.": ("section", "abbr"),
    "section": ("section", "full"),
    "sections": ("section", "full"),
}

PLACEHOLDER_KEYS = {
    "",
    "alg",
    "algorithm",
    "app",
    "appendix",
    "eq",
    "equation",
    "fig",
    "figure",
    "image",
    "img",
    "label",
    "pic",
    "picture",
    "sec",
    "section",
    "subsec",
    "subsection",
    "tab",
    "table",
    "temp",
    "thm",
    "theorem",
    "tmp",
}

REFERENCE_COMMANDS = {
    "label",
    "ref",
    "pageref",
    "eqref",
    "cref",
    "Cref",
    "autoref",
    "autopageref",
    "nameref",
    "subref",
    "vref",
    "cpageref",
}
MULTI_KEY_REFERENCE_COMMANDS = {"cref", "Cref"}

NUMERIC_GROUP_SEPARATOR_RE = r"[,\uff0c\u066c]"
NUMERIC_DECIMAL_SEPARATOR_RE = r"[.\uff0e\u066b]"
NUMBER_MAGNITUDE_RE = (
    rf"(?:\d{{1,3}}(?:{NUMERIC_GROUP_SEPARATOR_RE}\d{{3}})+"
    rf"(?:{NUMERIC_DECIMAL_SEPARATOR_RE}\d+)?|"
    rf"\d+{NUMERIC_DECIMAL_SEPARATOR_RE}\d+|"
    rf"{NUMERIC_DECIMAL_SEPARATOR_RE}\d+|\d+)"
    r"(?:[eE][+\-\u2212]?\d+)?"
)
NUMERIC_SPACING_TOKEN_RE = (
    r"(?:\s|~|\\(?:[,;:! ]|quad|qquad|enspace|thinspace|medspace|thickspace|"
    r"enskip|negthinspace|negmedspace|negthickspace))"
)
NUMERIC_PARAMETERIZED_SPACING_RE = (
    r"(?:\\(?:hspace|mspace)\*?\s*"
    r"\{(?:[^{}\r\n]|\{[^{}\r\n]*\})*\}|"
    r"\\(?:kern|hskip|mkern|mskip)\s*"
    r"[+\-\u2212]?(?:(?:\d+(?:\.\d*)?|\.\d+)\s*)?"
    r"[A-Za-z\u00b5\u03bc]*)"
)
NUMERIC_COMMENT_JOIN_RE = r"(?:%[^\r\n]*(?:\r\n|\r|\n)[ \t]*)"
NUMERIC_BASE_CONNECTOR_TOKEN_RE = (
    rf"(?:{NUMERIC_SPACING_TOKEN_RE}|{NUMERIC_PARAMETERIZED_SPACING_RE}|"
    rf"{NUMERIC_COMMENT_JOIN_RE})"
)
NUMERIC_EMPTY_GROUP_RE = r"(?:\{\s*\})"
NUMERIC_GROUPED_CONNECTOR_LEVEL_1_RE = (
    rf"(?:\{{(?:{NUMERIC_BASE_CONNECTOR_TOKEN_RE}|{NUMERIC_EMPTY_GROUP_RE})*\}})"
)
NUMERIC_GROUPED_CONNECTOR_LEVEL_2_RE = (
    rf"(?:\{{(?:{NUMERIC_BASE_CONNECTOR_TOKEN_RE}|"
    rf"{NUMERIC_GROUPED_CONNECTOR_LEVEL_1_RE})*\}})"
)
NUMERIC_GROUPED_CONNECTOR_RE = (
    rf"(?:{NUMERIC_GROUPED_CONNECTOR_LEVEL_1_RE}|"
    rf"{NUMERIC_GROUPED_CONNECTOR_LEVEL_2_RE})"
)
NUMERIC_CONNECTOR_TOKEN_RE = (
    rf"(?:{NUMERIC_BASE_CONNECTOR_TOKEN_RE}|{NUMERIC_GROUPED_CONNECTOR_RE})"
)
NUMERIC_SIGN_SPACING_RE = rf"(?:{NUMERIC_CONNECTOR_TOKEN_RE})*"
NUMERIC_SIGN_CLASS_RE = (
    r"+\-\u2212\u00b1\u2213\u207a\u207b\u208a\u208b\uff0b\uff0d\ufe62\ufe63"
)
AMBIGUOUS_NUMERIC_SIGN_CLASS_RE = (
    r"+\-\u2212\u207a\u207b\u208a\u208b\uff0b\uff0d\ufe62\ufe63"
)
UNAMBIGUOUS_NUMERIC_SIGN_CLASS_RE = r"\u00b1\u2213"
NUMERIC_SIGN_CHARS = (
    "+-\u2212\u00b1\u2213\u207a\u207b\u208a\u208b\uff0b\uff0d\ufe62\ufe63"
)
SIGNED_NUMBER_PREFIX_RE = (
    rf"(?:[{UNAMBIGUOUS_NUMERIC_SIGN_CLASS_RE}]|"
    rf"(?<![A-Za-z0-9_{NUMERIC_SIGN_CLASS_RE}\u2012\u2013\u2014\u2015])"
    rf"[{AMBIGUOUS_NUMERIC_SIGN_CLASS_RE}])"
)
NUMBER_CORE_RE = (
    rf"(?:{SIGNED_NUMBER_PREFIX_RE}{NUMERIC_SIGN_SPACING_RE})?{NUMBER_MAGNITUDE_RE}"
)
SIGNIFICANCE_MARKER_RE = (
    r"(?:\*+|\u2020+|\u2021+|\u00a7+|[\u1d2c-\u1d6a]+|"
    r"\\(?:ast|dagger|ddagger)|"
    r"\\textsuperscript\s*\{(?:\*+|\u2020+|\u2021+|\u00a7+|[A-Za-z]+|"
    r"\\(?:ast|dagger|ddagger))\}|"
    r"\^\{(?:\*+|\u2020+|\u2021+|\u00a7+|[A-Za-z]+|"
    r"\\(?:ast|dagger|ddagger))\})"
)
SIGNIFICANCE_MARKER_SPACING_RE = NUMERIC_SIGN_SPACING_RE
CURRENCY_UNIT_RE = (
    r"(?:[A-Z]{2}\\\$|USD|EUR|GBP|JPY|CNY|RMB|INR|AUD|CAD|CHF|HKD|SGD|KRW|NZD|SEK|"
    r"\$|\u20ac|\u00a3|\u00a5|\u20b9|\u20bd|\u20a9|\u00a2)"
)
UNAMBIGUOUS_MAPPING_QUANTITY_PATTERN = re.compile(
    rf"(?:\\%|%|(?<![A-Za-z])(?:{CURRENCY_UNIT_RE}|percent|"
    rf"percentage\s+points?|pp)(?![A-Za-z]))",
    re.IGNORECASE,
)
ENGLISH_NUMBER_WORD_RE = (
    r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
    r"million|billion|trillion|dozen|half|quarter|single|double|triple|"
    r"both|pair|twice|thrice|"
    r"onefold|twofold|threefold|fourfold|fivefold|sixfold|sevenfold|eightfold|"
    r"ninefold|tenfold|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|"
    r"eighteenth|nineteenth|twentieth|thirtieth|fortieth|fiftieth|sixtieth|"
    r"seventieth|eightieth|ninetieth|hundredth|thousandth|millionth|billionth)"
)

# A deliberately conservative unit vocabulary. Values are always protected even
# when no unit is recognized; this suffix binds common units to their value so a
# change such as ``10 ms`` -> ``10 s`` cannot pass as an unchanged number.
COMMON_COMPOUND_UNIT_ATOM_RE = (
    r"(?:kg|mg|mol|kPa|MPa|Pa|kW|MW|W|mV|V|mA|A|kJ|J|kN|N|"
    r"km|cm|mm|nm|\u00b5m|\u03bcm|m|ms|ns|\u00b5s|\u03bcs|s|h|Hz|K|bar|psi)"
)
COMPOUND_UNIT_RE = (
    rf"(?:{COMMON_COMPOUND_UNIT_ATOM_RE}"
    rf"(?:{NUMERIC_CONNECTOR_TOKEN_RE})+"
    rf"{COMMON_COMPOUND_UNIT_ATOM_RE}|"
    r"(?:Pa|N|J|W|V|A|C|F|S|T|H|Hz)(?:m|s))"
)
COUNT_UNIT_CORE_RE = (
    r"(?:epochs?|iterations?|samples?|trials?|runs?|batches?|steps?|folds?|times)"
)
COUNT_UNIT_RE = (
    rf"(?:{COUNT_UNIT_CORE_RE})"
    r"(?=\s*(?:[.,;:)\]]|$)|\s+(?:of|from|for|were|was|are|is|have|has|"
    r"with|per|each|completed|converged|failed|succeeded)\b)"
)
UNIT_WORD_RE = (
    rf"(?:{COMPOUND_UNIT_RE}|{COUNT_UNIT_RE}|"
    rf"[A-Za-z\u00b5\u03bc\u03a9]{{1,5}}(?:\s+|~)"
    rf"[A-Za-z\u00b5\u03bc\u03a9]{{1,5}}"
    rf"(?:/[A-Za-z\u00b5\u03bc\u03a9]{{1,5}})?"
    rf"(?:[\u207a\u207b\u208a\u208b]?[\u00b2\u00b3\u00b9\u2070-\u2079]+|"
    rf"\^(?:[+\-\u2212]?\d+|\{{[+\-\u2212]?\d+\}}))|"
    rf"[A-Za-z\u00b5\u03bc\u00b0\u03a9]+[/^\u00b7\u22c5]"
    rf"[A-Za-z0-9\u00b5\u03bc\u00b0\u03a9/%^{{}}+\-\u00b7\u22c5\u00b2\u00b3\u2070-\u2079\u207b]*|"
    rf"[\u3300-\u33ff]|{CURRENCY_UNIT_RE}|dollars?|euros?|pounds?|yen|yuan|"
    rf"\\%|%|percent|percentage\s+points?|pp|"
    r"\u00b0C|\u00b0F|\u00b0|degrees?\s+Celsius|degrees?\s+Fahrenheit|degrees?|radians?|"
    r"ns|us|\u00b5s|\u03bcs|ms|milliseconds?|s|seconds?|min|minutes?|h|hours?|days?|"
    r"weeks?|months?|years?|"
    r"Hz|kHz|MHz|GHz|THz|fps|FLOPs?|TFLOPs?|GFLOPs?|"
    r"dB|dBm|B|KB|MB|GB|TB|KiB|MiB|GiB|bytes?|bits?|bps|kbps|Mbps|Gbps|"
    r"m/s|km/h|mm|cm|km|m|nm|\u00b5m|\u03bcm|meters?|metres?|inches?|"
    r"in(?=\s*(?:[.,;:)]|$))|ft|"
    r"mg|kg|g|mol|K|Pa|kPa|MPa|W|kW|MW|V|mV|A|mA|J|kJ|"
    r"(?:q|r|y|z|a|f|p|n|\u00b5|\u03bc|m|c|d|da|h|k|M|G|T|P|E|Z|Y|R|Q)?"
    r"(?:Hz|N|Pa|J|W|C|V|F|S|Wb|T|H|lm|lx|eV|L|\u03a9|Ohm)|"
    r"mps|rpm|rps|psi|bar|pixels?|px|newtons?|kilonewtons?|joules?|kilojoules?|watts?|kilowatts?|"
    r"volts?|amperes?|amps?|pascals?|kilopascals?|megapascals?|hertz|"
    r"grams?|kilograms?|liters?|litres?|milliliters?|millilitres?|"
    r"yards?|miles?|furlongs?|parsecs?|feet|foot|"
    r"(?:square|cubic|nautical)\s+[A-Za-z]+|"
    r"[a-z\u00b5\u03bc]{1,5}[A-Z\u03a9]"
    r"[A-Za-z0-9\u00b5\u03bc\u00b0\u03a9/%^{}+\-\u00b7\u22c5\u00b2\u00b3\u2070-\u2079\u207b]*|"
    r"[A-Za-z\u00b5\u03bc\u00b0\u03a9]+[/^\u00b7\u22c5]"
    r"[A-Za-z0-9\u00b5\u03bc\u00b0\u03a9/%^{}+\-\u00b7\u22c5\u00b2\u00b3\u2070-\u2079\u207b]*)"
)

NUMBER_RE = re.compile(
    rf"(?P<value>{SIGNED_NUMBER_PREFIX_RE}{NUMERIC_SIGN_SPACING_RE}{NUMBER_MAGNITUDE_RE}|"
    rf"(?<!\d){NUMBER_MAGNITUDE_RE})(?!\d)"
)

NUMERIC_OCCURRENCE_RE = re.compile(
    rf"(?:(?P<prefix_unit>{CURRENCY_UNIT_RE})(?![A-Za-z]){NUMERIC_SIGN_SPACING_RE})?"
    rf"(?P<value>{SIGNED_NUMBER_PREFIX_RE}{NUMERIC_SIGN_SPACING_RE}{NUMBER_MAGNITUDE_RE}|"
    rf"(?<!\d){NUMBER_MAGNITUDE_RE})"
    rf"(?:(?:{NUMERIC_CONNECTOR_TOKEN_RE})*"
    rf"(?P<unit>{UNIT_WORD_RE})(?![A-Za-z0-9_]))?"
    rf"(?P<marker>{SIGNIFICANCE_MARKER_SPACING_RE}{SIGNIFICANCE_MARKER_RE})?"
    rf"(?!\d)"
)

UNIT_AFTER_NUMBER_RE = re.compile(
    rf"(?:(?:{NUMERIC_CONNECTOR_TOKEN_RE})*"
    rf"(?P<unit>{UNIT_WORD_RE})(?![A-Za-z0-9_]))"
)

SIGNIFICANCE_MARKER_PATTERN = re.compile(
    SIGNIFICANCE_MARKER_SPACING_RE + SIGNIFICANCE_MARKER_RE
)
SIGNIFICANCE_MARKER_BEFORE_NUMBER_PATTERN = re.compile(
    rf"(?P<marker>{SIGNIFICANCE_MARKER_RE}){NUMERIC_SIGN_SPACING_RE}$"
)
CURRENCY_BEFORE_NUMBER_PATTERN = re.compile(
    rf"(?<![A-Za-z])(?P<unit>{CURRENCY_UNIT_RE})(?![A-Za-z])"
    rf"{NUMERIC_SIGN_SPACING_RE}$"
)
NUMERIC_SPACING_SUFFIX_PATTERN = re.compile(
    rf"{NUMERIC_SIGN_SPACING_RE}$"
)
TEXTUAL_NUMBER_PATTERN = re.compile(
    rf"\b(?P<value>{ENGLISH_NUMBER_WORD_RE})\b", re.IGNORECASE
)
CONTEXTUAL_ROMAN_NUMBER_PATTERN = re.compile(
    r"\b(?:type|phase|stage|class|level|part|section|appendix|chapter|case|"
    r"group|cohort|tier|generation|version)\s+"
    r"(?P<value>[IVXLCDM]+)\b",
    re.IGNORECASE,
)
COMMENT_SPLICED_MARKER_PATTERN = re.compile(
    rf"(?P<value>{NUMBER_MAGNITUDE_RE}|\b{ENGLISH_NUMBER_WORD_RE}\b)"
    rf"{NUMERIC_COMMENT_JOIN_RE}"
    rf"(?P<marker>{SIGNIFICANCE_MARKER_RE})"
)
DELIMITED_TECHNICAL_TOKEN_PATTERN = re.compile(
    rf"(?<![A-Za-z])(?P<opening>[([])\s*"
    rf"(?P<token>{CURRENCY_UNIT_RE}|{UNIT_WORD_RE}|"
    rf"[{NUMERIC_SIGN_CLASS_RE}]|{SIGNIFICANCE_MARKER_RE})"
    rf"(?![A-Za-z0-9_])\s*(?P<closing>[)\]])"
)
STANDALONE_UNIT_CUE_PATTERN = re.compile(
    rf"(?i:\b(?:measured|reported|expressed|given)\s+in\s+)"
    rf"(?P<unit>{UNIT_WORD_RE})(?![A-Za-z0-9_])"
)
STANDALONE_CURRENCY_CUE_PATTERN = re.compile(
    rf"(?i:\bcurrency\s*(?:is|=|:)?\s*)"
    rf"(?P<unit>{CURRENCY_UNIT_RE})(?![A-Za-z])"
)
STANDALONE_SIGN_CUE_PATTERN = re.compile(
    rf"(?i:\b(?:uncertainty|sign)\b[^\r\n:;.]{{0,40}}?"
    rf"(?:by|as|=|:)\s*)"
    rf"(?P<sign>[{NUMERIC_SIGN_CLASS_RE}])"
)
STANDALONE_MARKER_CUE_PATTERN = re.compile(
    rf"(?i:\b(?:significance|marker|legend)\b[^\r\n:;.]{{0,40}}?"
    rf"(?:is\s+(?:denoted|marked|represented)\s+(?:by|as)|"
    rf"is|means|=|:)\s*)"
    rf"(?P<marker>{SIGNIFICANCE_MARKER_RE})"
)

PLAIN_INCLUDE_COMMANDS = {"input", "include", "subfile", "subfileinclude"}
RESET_IMPORT_COMMANDS = {"import", "inputfrom", "includefrom"}
RELATIVE_IMPORT_COMMANDS = {"subimport", "subinputfrom", "subincludefrom"}
IMPORT_COMMANDS = RESET_IMPORT_COMMANDS | RELATIVE_IMPORT_COMMANDS
ALL_INCLUDE_COMMANDS = PLAIN_INCLUDE_COMMANDS | IMPORT_COMMANDS

INCLUDE_COMMAND_RE = re.compile(
    r"\\(?P<command>input|include|subfile|subfileinclude)(?P<star>\*)?"
    r"(?![A-Za-z@])\s*"
    r"(?:\{(?P<braced>[^{}]*)\}|(?P<unbraced>[^\s%{}]+))"
)

IMPORT_COMMAND_RE = re.compile(
    r"\\(?P<command>import|subimport|inputfrom|includefrom|subinputfrom|subincludefrom)"
    r"(?P<star>\*)?(?![A-Za-z@])\s*"
    r"\{(?P<directory>[^{}]*)\}\s*\{(?P<filename>[^{}]*)\}"
)

INCLUDE_COMMAND_START_RE = re.compile(
    r"\\(?P<command>input|include|subfile|subfileinclude|import|subimport|inputfrom|includefrom|"
    r"subinputfrom|subincludefrom)(?P<star>\*)?(?![A-Za-z@])"
)

PROHIBITED_UNICODE_DASHES = "\u2012\u2013\u2014\u2015\u2e3a\u2e3b"
PROHIBITED_DASH_RE = re.compile(rf"[{PROHIBITED_UNICODE_DASHES}]|-{{2,}}")

# En-length dashes between numeric endpoints are standard range notation in TeX
# (`5--10`, `pp.~12--18`, `0.5--1.0`, `Figs.~3a--3c`), not the parenthetical dash
# punctuation this profile discourages. Exempt them so that a byte-identical
# candidate cannot fail the dash check.
RANGE_ENDPOINT_RE = r"\d+(?:\.\d+)?[A-Za-z]?"
EN_RANGE_DASH_RE = r"(?<!-)--(?!-)|[\u2012\u2013]"
NUMERIC_RANGE_DASH_RE = re.compile(
    rf"(?<![A-Za-z0-9]){RANGE_ENDPOINT_RE}\s*(?P<dash>{EN_RANGE_DASH_RE})\s*"
    rf"{RANGE_ENDPOINT_RE}(?![A-Za-z0-9])"
)

BEGIN_ENVIRONMENT_RE = re.compile(r"\\begin\s*\{\s*(?P<name>[^{}\s]+)\s*\}")
ENVIRONMENT_MARKER_RE = re.compile(
    r"\\(?P<action>begin|end)\s*\{\s*(?P<name>[^{}\s]+)\s*\}"
)
INLINE_LITERAL_COMMAND_RE = re.compile(
    r"\\(?P<name>verb|Verb|SaveVerb|lstinline|mintinline|mint)(?:\*)?"
    r"(?![A-Za-z@])"
)
TEX_COMMAND_RE = re.compile(r"\\(?P<name>[A-Za-z@]+)(?:\*)?")
ENSUREMATH_RE = re.compile(r"\\ensuremath(?![A-Za-z@])\s*\{")

LITERAL_ENVIRONMENTS = {
    "BVerbatim",
    "LVerbatim",
    "SaveVerbatim",
    "Verbatim",
    "alltt",
    "asy",
    "comment",
    "filecontents",
    "filecontents*",
    "lstlisting",
    "luacode",
    "luacode*",
    "minted",
    "pgfpicture",
    "pspicture",
    "pycode",
    "sageblock",
    "tikzpicture",
    "verbatim",
    "verbatim*",
}

MATH_SCAN_LITERAL_ENVIRONMENTS = LITERAL_ENVIRONMENTS - {
    "pgfpicture",
    "pspicture",
    "tikzpicture",
}

# Diagram source is active TeX and must participate in structural comparison.
# Truly verbatim/code-like environments remain opaque.
STRUCTURAL_LITERAL_ENVIRONMENTS = MATH_SCAN_LITERAL_ENVIRONMENTS

OPAQUE_ENVIRONMENTS = {"thebibliography"}

MATH_ENVIRONMENTS = {
    "Bmatrix",
    "IEEEeqnarray",
    "IEEEeqnarray*",
    "Vmatrix",
    "align",
    "align*",
    "alignat",
    "alignat*",
    "aligned",
    "alignedat",
    "array",
    "bmatrix",
    "cases",
    "displaymath",
    "equation",
    "equation*",
    "eqnarray",
    "eqnarray*",
    "flalign",
    "flalign*",
    "gather",
    "gather*",
    "gathered",
    "math",
    "matrix",
    "multline",
    "multline*",
    "pmatrix",
    "smallmatrix",
    "split",
    "vmatrix",
    "xalignat",
    "xalignat*",
    "xxalignat",
}

TEXT_MODE_MATH_COMMANDS = {
    "emph",
    "hbox",
    "intertext",
    "operatorname",
    "mbox",
    "shortintertext",
    "text",
    "textbf",
    "textit",
    "textmd",
    "textnormal",
    "textrm",
    "textsc",
    "textsf",
    "textsl",
    "texttt",
    "textup",
    "mathrm",
}

MATH_MODE_TEXT_COMMANDS = {"ensuremath"}

COMMENT_LITERAL_COMMANDS = {"nolinkurl", "path", "url"}

# These arguments contain protected keys, identifiers, URLs, paths, or source-code
# metadata rather than prose. Counts refer to required brace arguments. For
# commands such as \href, only the opaque target is masked; visible link text is
# deliberately left available for the prose check.
OPAQUE_COMMAND_ARGUMENT_COUNTS = {
    "addbibresource": 1,
    "autocite": 1,
    "autopageref": 1,
    "autoref": 1,
    "begin": 1,
    "bibliography": 1,
    "bibliographystyle": 1,
    "bibitem": 1,
    "cite": 1,
    "citealp": 1,
    "citealt": 1,
    "citeauthor": 1,
    "citefield": 2,
    "citep": 1,
    "citet": 1,
    "citetitle": 1,
    "citeurl": 1,
    "citeyear": 1,
    "citeyearpar": 1,
    "cpageref": 1,
    "cpagerefrange": 2,
    "cref": 1,
    "crefrange": 2,
    "declaregraphicsextensions": 1,
    "documentclass": 1,
    "doi": 1,
    "end": 1,
    "eqref": 1,
    "footcite": 1,
    "fullcite": 1,
    "graphicspath": 1,
    "href": 1,
    "hyperref": 0,
    "hyperlink": 1,
    "hypertarget": 1,
    "include": 1,
    "includegraphics": 1,
    "includeonly": 1,
    "includefrom": 2,
    "import": 2,
    "input": 1,
    "inputfrom": 2,
    "inputminted": 2,
    "label": 1,
    "lstinputlisting": 1,
    # Only the layout arguments are protected; the final cell text remains
    # visible prose and can still be polished.
    "multicolumn": 2,
    "multirow": 2,
    "nocite": 1,
    "nolinkurl": 1,
    "nameref": 1,
    "pageref": 1,
    "pagerefrange": 2,
    "parencite": 1,
    "path": 1,
    "ref": 1,
    "refrange": 2,
    "requirepackage": 1,
    "smartcite": 1,
    "subfile": 1,
    "subfileinclude": 1,
    "subimport": 2,
    "subincludefrom": 2,
    "subinputfrom": 2,
    "subref": 1,
    "supercite": 1,
    "textcite": 1,
    "url": 1,
    "useverb": 1,
    "useverbatim": 1,
    "buseverbatim": 1,
    "luseverbatim": 1,
    "usepackage": 1,
    "volcite": 2,
    "vref": 1,
    "vrefrange": 2,
}

VARIABLE_PROTECTED_ARGUMENT_COMMANDS = {
    "autocites",
    "cites",
    "footcites",
    "parencites",
    "smartcites",
    "supercites",
    "textcites",
    "volcites",
}

VISIBLE_OPTION_ARGUMENT_COMMANDS = {
    "autocite",
    "cite",
    "citealp",
    "citealt",
    "citeauthor",
    "citep",
    "citet",
    "citeyear",
    "footcite",
    "parencite",
    "textcite",
    "volcite",
}

UNBRACED_PATH_COMMANDS = {"include", "input", "subfile", "subfileinclude"}

CASE_SENSITIVE_PROTECTED_ARGUMENT_COUNTS = {
    "SI": 2,
    "SIlist": 2,
    "SIrange": 3,
    "ang": 1,
    "num": 1,
    "numlist": 1,
    "numrange": 2,
    "qty": 2,
    "qtylist": 2,
    "qtyrange": 3,
    "si": 1,
    "unit": 1,
}

NUMERIC_VALUE_COMMANDS = {
    "SI",
    "SIlist",
    "SIrange",
    "ang",
    "num",
    "numlist",
    "numrange",
    "qty",
    "qtylist",
    "qtyrange",
}

NUMERIC_TEXT_ARGUMENT_COMMANDS = {
    "mbox",
    "text",
    "textnormal",
    "textrm",
    "textsf",
    "texttt",
}

ENVIRONMENT_REQUIRED_ARGUMENT_COUNTS = {
    "array": 1,
    "longtable": 1,
    "minipage": 1,
    "multicols": 1,
    "tabular": 1,
    "tabular*": 2,
    "tabularx": 2,
    "thebibliography": 1,
}

VISIBLE_ENVIRONMENT_OPTION_NAMES = {
    "corollary",
    "definition",
    "example",
    "lemma",
    "proof",
    "proposition",
    "remark",
    "theorem",
}

CLI_LONG_OPTION_RE = re.compile(
    r"(?<![A-Za-z0-9_-])"
    r"--[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*"
    r"(?:=(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|[^\s,;)}\]]+))?"
)

COMMENT_JOINER = "\ue000"
OPAQUE_MATH_CHAR_ESCAPES = {
    "$": "\ue001",
    "\\": "\ue002",
    "{": "\ue003",
    "}": "\ue004",
    " ": "\ue005",
    "\t": "\ue006",
    "\r": "\ue007",
    "\n": "\ue008",
}


@dataclass(frozen=True)
class MathRegion:
    """A normalized TeX math region with source-location metadata."""

    kind: str
    tokens: tuple[str, ...]
    line_number: int
    source: str
    start_index: int
    end_index: int

    @property
    def signature(self) -> tuple[str, tuple[str, ...]]:
        return self.kind, self.tokens


@dataclass(frozen=True)
class MathParseIssue:
    """A malformed math delimiter or environment that prevents safe comparison."""

    line_number: int
    message: str


@dataclass(frozen=True)
class TexGroupIssue:
    """An unmatched active TeX grouping brace."""

    line_number: int
    message: str


@dataclass(frozen=True)
class TexEnvironmentIssue:
    """A mismatched active TeX environment marker."""

    line_number: int
    message: str


@dataclass(frozen=True)
class StructuralEvent:
    """An active TeX command, environment marker, or protected key in order."""

    signature: tuple[object, ...]
    line_number: int
    source: str


@dataclass(frozen=True)
class NumericOccurrence:
    """A protected numeric value, adjacent quantity token, and significance marker."""

    value: str
    unit: str
    marker: str
    line_number: int
    source: str

    @property
    def signature(self) -> tuple[str, str, str]:
        return self.value, self.unit, self.marker


@dataclass(frozen=True)
class ApprovedSymbolMap:
    """An explicitly authorized token-for-token mathematical symbol mapping."""

    source: str
    target: str
    source_tokens: tuple[str, ...]
    target_tokens: tuple[str, ...]


@dataclass(frozen=True)
class ProjectLoadIssue:
    """A project include that prevents complete deterministic traversal."""

    path: Path
    line_number: int
    message: str


@dataclass(frozen=True)
class IncludeDirective:
    """A statically resolved TeX include/import directive."""

    start: int
    end: int
    command: str
    target: str
    line_number: int
    directory: str | None = None


def strip_comments(text: str) -> str:
    """Remove TeX comments while preserving escaped and URL-like literal percent signs."""
    excluded_spans = sorted(
        collect_opaque_command_argument_spans(
            text, included_commands=COMMENT_LITERAL_COMMANDS
        )
    )
    excluded_index = 0
    cleaned: list[str] = []
    cursor = 0

    while cursor < len(text):
        while excluded_index < len(excluded_spans) and excluded_spans[excluded_index][1] <= cursor:
            excluded_index += 1
        if excluded_index < len(excluded_spans):
            excluded_start, excluded_end = excluded_spans[excluded_index]
            if excluded_start <= cursor < excluded_end:
                cleaned.append(text[cursor:excluded_end])
                cursor = excluded_end
                continue

        if text[cursor] == "%" and not is_escaped(text, cursor):
            line_end = text.find("\n", cursor)
            if line_end == -1:
                break
            cleaned.append("\n")
            cursor = line_end + 1
            continue

        cleaned.append(text[cursor])
        cursor += 1

    return "".join(cleaned)


def is_escaped(text: str, index: int) -> bool:
    """Return whether the token starting at index is escaped by a backslash."""
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def mask_span(buffer: list[str], start: int, end: int) -> None:
    """Blank a span without changing offsets or line numbers."""
    for index in range(max(start, 0), min(end, len(buffer))):
        if buffer[index] not in "\r\n":
            buffer[index] = " "


def find_balanced_end(text: str, start: int, opening: str, closing: str) -> int | None:
    """Return the exclusive end of a balanced TeX argument."""
    if start >= len(text) or text[start] != opening:
        return None

    depth = 0
    for index in range(start, len(text)):
        if is_escaped(text, index):
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index + 1
    return None


def find_environment_end(text: str, name: str, start: int) -> int:
    end_re = re.compile(rf"\\end\s*\{{\s*{re.escape(name)}\s*\}}")
    match = end_re.search(text, start)
    return match.end() if match else len(text)


def find_inline_literal_end(text: str, match: re.Match[str]) -> int | None:
    """Find the end of a supported inline verbatim or code command."""
    command = match.group("name")
    cursor = match.end()

    if command in {"Verb", "SaveVerb", "lstinline", "mintinline", "mint"}:
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1
        if cursor < len(text) and text[cursor] == "[":
            option_end = find_balanced_end(text, cursor, "[", "]")
            if option_end is None:
                return text.find("\n", cursor) if "\n" in text[cursor:] else len(text)
            cursor = option_end
            while cursor < len(text) and text[cursor] in " \t":
                cursor += 1

    if command in {"mintinline", "mint", "SaveVerb"}:
        if cursor >= len(text) or text[cursor] != "{":
            return text.find("\n", cursor) if "\n" in text[cursor:] else len(text)
        argument_end = find_balanced_end(text, cursor, "{", "}")
        if argument_end is None:
            return text.find("\n", cursor) if "\n" in text[cursor:] else len(text)
        cursor = argument_end
        while cursor < len(text) and text[cursor] in " \t":
            cursor += 1

    if cursor >= len(text) or text[cursor] in "\r\n" or text[cursor].isspace():
        return None

    delimiter = text[cursor]
    if delimiter == "{" and command in {"lstinline", "mintinline", "mint"}:
        return find_balanced_end(text, cursor, "{", "}")

    line_end = text.find("\n", cursor + 1)
    search_end = len(text) if line_end == -1 else line_end
    closing = text.find(delimiter, cursor + 1, search_end)
    return closing + 1 if closing != -1 else search_end


def mask_comments_and_literal_regions(
    text: str,
    buffer: list[str],
    literal_environments: set[str] | None = None,
    join_comment_lines: bool = False,
    comment_excluded_spans: list[tuple[int, int]] | None = None,
    recorded_spans: list[tuple[str, int, int]] | None = None,
) -> None:
    """Mask comments, literal code, listings, and source-only environments."""
    literal_names = LITERAL_ENVIRONMENTS if literal_environments is None else literal_environments
    excluded_spans = sorted(comment_excluded_spans or [])
    excluded_index = 0
    cursor = 0
    while cursor < len(text):
        while excluded_index < len(excluded_spans) and excluded_spans[excluded_index][1] <= cursor:
            excluded_index += 1
        if excluded_index < len(excluded_spans):
            excluded_start, excluded_end = excluded_spans[excluded_index]
            if excluded_start <= cursor < excluded_end:
                cursor = excluded_end
                continue

        if text[cursor] == "\\" and not is_escaped(text, cursor):
            environment = BEGIN_ENVIRONMENT_RE.match(text, cursor)
            if environment and environment.group("name") in literal_names:
                end = find_environment_end(text, environment.group("name"), environment.end())
                if recorded_spans is not None:
                    recorded_spans.append(("literal-environment", cursor, end))
                mask_span(buffer, cursor, end)
                cursor = end
                continue

            inline_literal = INLINE_LITERAL_COMMAND_RE.match(text, cursor)
            if inline_literal:
                end = find_inline_literal_end(text, inline_literal)
                if end is not None:
                    if recorded_spans is not None:
                        recorded_spans.append(("inline-literal", cursor, end))
                    mask_span(buffer, cursor, end)
                    cursor = end
                    continue

        if text[cursor] == "%" and not is_escaped(text, cursor):
            line_end = text.find("\n", cursor)
            end = len(text) if line_end == -1 else line_end
            if recorded_spans is not None:
                recorded_spans.append(("comment", cursor, end))
            if join_comment_lines:
                join_end = end
                if line_end != -1:
                    join_end = line_end + 1
                    while join_end < len(text) and text[join_end] in " \t":
                        join_end += 1
                for index in range(cursor, join_end):
                    buffer[index] = COMMENT_JOINER
                cursor = join_end
            else:
                mask_span(buffer, cursor, end)
                cursor = end
            continue

        cursor += 1


def tokenize_math(text: str) -> tuple[str, ...]:
    """Tokenize TeX math, preserving normalized whitespace in text-mode arguments."""
    tokens: list[str] = []
    mode_stack: list[tuple[str, bool, str | None]] = [("root", False, None)]
    pending_argument_mode: bool | None = None
    after_control_word = False
    cursor = 0
    while cursor < len(text):
        char = text[cursor]
        if char == COMMENT_JOINER:
            cursor += 1
            continue
        if char.isspace():
            end = cursor + 1
            while end < len(text) and text[end].isspace():
                end += 1
            in_text_mode = mode_stack[-1][1]
            if in_text_mode and pending_argument_mode is None and not after_control_word:
                if not tokens or tokens[-1] != " ":
                    tokens.append(" ")
            after_control_word = False
            cursor = end
            continue

        in_text_mode = mode_stack[-1][1]
        if char == "{":
            tokens.append(char)
            argument_mode = in_text_mode if pending_argument_mode is None else pending_argument_mode
            mode_stack.append(("brace", argument_mode, None))
            pending_argument_mode = None
            after_control_word = False
            cursor += 1
            continue

        if char == "}":
            tokens.append(char)
            if len(mode_stack) > 1 and mode_stack[-1][0] == "brace":
                mode_stack.pop()
            pending_argument_mode = None
            after_control_word = False
            cursor += 1
            continue

        if char == "$":
            delimiter = "$$" if text.startswith("$$", cursor) else "$"
            tokens.append(delimiter)
            if mode_stack[-1][0] == "delimiter" and mode_stack[-1][2] == delimiter:
                mode_stack.pop()
            elif in_text_mode:
                mode_stack.append(("delimiter", False, delimiter))
            pending_argument_mode = None
            after_control_word = False
            cursor += len(delimiter)
            continue

        if char != "\\":
            tokens.append(char)
            if pending_argument_mode is not None and char != "*":
                pending_argument_mode = None
            after_control_word = False
            cursor += 1
            continue

        if cursor + 1 >= len(text):
            tokens.append(char)
            pending_argument_mode = None
            after_control_word = False
            cursor += 1
            continue

        next_char = text[cursor + 1]
        if next_char.isalpha() or next_char == "@":
            end = cursor + 2
            while end < len(text) and (text[end].isalpha() or text[end] == "@"):
                end += 1
            token = text[cursor:end]
            tokens.append(token)
            command = token[1:]
            if command in TEXT_MODE_MATH_COMMANDS:
                pending_argument_mode = True
            elif command in MATH_MODE_TEXT_COMMANDS:
                pending_argument_mode = False
            else:
                pending_argument_mode = None
            after_control_word = True
            cursor = end
            continue

        token = text[cursor : cursor + 2]
        tokens.append(token)
        if mode_stack[-1][0] == "delimiter" and mode_stack[-1][2] == token:
            mode_stack.pop()
        elif in_text_mode and token in {r"\(", r"\["}:
            closing = r"\)" if token == r"\(" else r"\]"
            mode_stack.append(("delimiter", False, closing))
        pending_argument_mode = None
        after_control_word = False
        cursor += 2

    return tuple(tokens)


def find_unescaped_single_dollar(text: str, start: int) -> int:
    """Find a single-dollar delimiter, skipping escaped dollars and $$ pairs."""
    cursor = text.find("$", start)
    while cursor != -1:
        if is_escaped(text, cursor):
            cursor = text.find("$", cursor + 1)
            continue
        if (cursor > 0 and text[cursor - 1] == "$") or (
            cursor + 1 < len(text) and text[cursor + 1] == "$"
        ):
            cursor = text.find("$", cursor + 2)
            continue
        return cursor
    return -1


def find_math_environment_end(
    text: str, opening: re.Match[str]
) -> tuple[tuple[int, int] | None, MathParseIssue | None]:
    """Find a math environment's matching end while validating nested environments."""
    stack = [opening.group("name")]
    for marker in ENVIRONMENT_MARKER_RE.finditer(text, opening.end()):
        action = marker.group("action")
        name = marker.group("name")
        if action == "begin":
            stack.append(name)
            continue

        if not stack or stack[-1] != name:
            expected = stack[-1] if stack else "no open environment"
            return None, MathParseIssue(
                text.count("\n", 0, marker.start()) + 1,
                f"mismatched \\end{{{name}}}; expected \\end{{{expected}}}",
            )

        stack.pop()
        if not stack:
            return (marker.start(), marker.end()), None

    name = opening.group("name")
    return None, MathParseIssue(
        text.count("\n", 0, opening.start()) + 1,
        f"unclosed math environment \\begin{{{name}}}",
    )


def make_math_region(
    raw_text: str,
    masked_text: str,
    kind: str,
    region_start: int,
    content_start: int,
    content_end: int,
    region_end: int,
) -> MathRegion:
    """Create a normalized math region while retaining its original source excerpt."""
    return MathRegion(
        kind=kind,
        tokens=tokenize_math(masked_text[content_start:content_end]),
        line_number=raw_text.count("\n", 0, region_start) + 1,
        source=raw_text[region_start:region_end],
        start_index=region_start,
        end_index=region_end,
    )


def extract_math_regions(text: str) -> tuple[list[MathRegion], list[MathParseIssue]]:
    """Extract outermost TeX math regions and report malformed delimiters."""
    opaque_spans = collect_opaque_command_argument_spans(
        text,
        excluded_commands={"begin", "end"},
        included_commands=COMMENT_LITERAL_COMMANDS,
    )
    base_buffer = list(text)
    mask_comments_and_literal_regions(
        text,
        base_buffer,
        literal_environments=MATH_SCAN_LITERAL_ENVIRONMENTS,
        join_comment_lines=True,
        comment_excluded_spans=opaque_spans,
    )
    scan_buffer = base_buffer.copy()
    mask_opaque_command_arguments(scan_buffer, excluded_commands={"begin", "end"})
    masked_text = "".join(scan_buffer)
    content_buffer = base_buffer.copy()
    escape_opaque_command_arguments_for_math(
        content_buffer, excluded_commands={"begin", "end"}
    )
    content_text = "".join(content_buffer)
    regions: list[MathRegion] = []
    issues: list[MathParseIssue] = []
    cursor = 0

    while cursor < len(masked_text):
        if masked_text.startswith("$$", cursor) and not is_escaped(masked_text, cursor):
            closing = find_unescaped_token(masked_text, "$$", cursor + 2)
            if closing == -1:
                issues.append(
                    MathParseIssue(
                        text.count("\n", 0, cursor) + 1,
                        "unclosed display-math delimiter $$",
                    )
                )
                break
            region_end = closing + 2
            regions.append(
                make_math_region(
                    text,
                    content_text,
                    "display:$$",
                    cursor,
                    cursor + 2,
                    closing,
                    region_end,
                )
            )
            cursor = region_end
            continue

        if masked_text[cursor] == "$" and not is_escaped(masked_text, cursor):
            closing = find_unescaped_single_dollar(masked_text, cursor + 1)
            if closing == -1:
                issues.append(
                    MathParseIssue(
                        text.count("\n", 0, cursor) + 1,
                        "unclosed inline-math delimiter $",
                    )
                )
                break
            regions.append(
                make_math_region(
                    text,
                    content_text,
                    "inline:$",
                    cursor,
                    cursor + 1,
                    closing,
                    closing + 1,
                )
            )
            cursor = closing + 1
            continue

        delimiter = None
        for opening, closing, kind in (
            (r"\(", r"\)", r"inline:\("),
            (r"\[", r"\]", r"display:\["),
        ):
            if masked_text.startswith(opening, cursor) and not is_escaped(masked_text, cursor):
                delimiter = opening, closing, kind
                break

        if delimiter is not None:
            opening, closing_token, kind = delimiter
            closing = find_unescaped_token(masked_text, closing_token, cursor + len(opening))
            if closing == -1:
                issues.append(
                    MathParseIssue(
                        text.count("\n", 0, cursor) + 1,
                        f"unclosed math delimiter {opening}",
                    )
                )
                break
            region_end = closing + len(closing_token)
            regions.append(
                make_math_region(
                    text,
                    content_text,
                    kind,
                    cursor,
                    cursor + len(opening),
                    closing,
                    region_end,
                )
            )
            cursor = region_end
            continue

        ensuremath = None
        if masked_text[cursor] == "\\" and not is_escaped(masked_text, cursor):
            ensuremath = ENSUREMATH_RE.match(masked_text, cursor)
        if ensuremath is not None:
            opening_brace = ensuremath.end() - 1
            argument_end = find_balanced_end(masked_text, opening_brace, "{", "}")
            if argument_end is None:
                issues.append(
                    MathParseIssue(
                        text.count("\n", 0, cursor) + 1,
                        "unclosed \\ensuremath argument",
                    )
                )
                break
            regions.append(
                make_math_region(
                    text,
                    content_text,
                    r"command:\ensuremath",
                    cursor,
                    opening_brace + 1,
                    argument_end - 1,
                    argument_end,
                )
            )
            cursor = argument_end
            continue

        environment = None
        if masked_text[cursor] == "\\" and not is_escaped(masked_text, cursor):
            environment = BEGIN_ENVIRONMENT_RE.match(masked_text, cursor)
        if environment is not None and environment.group("name") in MATH_ENVIRONMENTS:
            matched_end, issue = find_math_environment_end(masked_text, environment)
            if issue is not None:
                issues.append(issue)
                break
            assert matched_end is not None
            content_end, region_end = matched_end
            regions.append(
                make_math_region(
                    text,
                    content_text,
                    f"env:{environment.group('name')}",
                    cursor,
                    environment.end(),
                    content_end,
                    region_end,
                )
            )
            cursor = region_end
            continue

        if masked_text.startswith((r"\)", r"\]"), cursor) and not is_escaped(masked_text, cursor):
            issues.append(
                MathParseIssue(
                    text.count("\n", 0, cursor) + 1,
                    f"unmatched math delimiter {masked_text[cursor:cursor + 2]}",
                )
            )
            cursor += 2
            continue

        if masked_text[cursor] == "\\" and not is_escaped(masked_text, cursor):
            marker = ENVIRONMENT_MARKER_RE.match(masked_text, cursor)
            if (
                marker is not None
                and marker.group("action") == "end"
                and marker.group("name") in MATH_ENVIRONMENTS
            ):
                issues.append(
                    MathParseIssue(
                        text.count("\n", 0, cursor) + 1,
                        f"unmatched \\end{{{marker.group('name')}}}",
                    )
                )
                cursor = marker.end()
                continue

        cursor += 1

    return regions, issues


def mask_named_environments(buffer: list[str], names: set[str]) -> None:
    text = "".join(buffer)
    cursor = 0
    while True:
        environment = BEGIN_ENVIRONMENT_RE.search(text, cursor)
        if environment is None:
            return
        if environment.group("name") not in names:
            cursor = environment.end()
            continue

        end = find_environment_end(text, environment.group("name"), environment.end())
        mask_span(buffer, environment.start(), end)
        cursor = end


def find_unescaped_token(text: str, token: str, start: int) -> int:
    cursor = text.find(token, start)
    while cursor != -1 and is_escaped(text, cursor):
        cursor = text.find(token, cursor + 1)
    return cursor


def mask_delimited_regions(buffer: list[str], opening: str, closing: str) -> None:
    text = "".join(buffer)
    cursor = 0
    while True:
        start = find_unescaped_token(text, opening, cursor)
        if start == -1:
            return
        end_start = find_unescaped_token(text, closing, start + len(opening))
        end = len(text) if end_start == -1 else end_start + len(closing)
        mask_span(buffer, start, end)
        cursor = end


def mask_ensuremath_regions(buffer: list[str]) -> None:
    text = "".join(buffer)
    cursor = 0
    while True:
        match = ENSUREMATH_RE.search(text, cursor)
        if match is None:
            return
        if is_escaped(text, match.start()):
            cursor = match.end()
            continue
        opening_brace = match.end() - 1
        argument_end = find_balanced_end(text, opening_brace, "{", "}")
        end = len(text) if argument_end is None else argument_end
        mask_span(buffer, match.start(), end)
        cursor = end


def mask_math_regions(buffer: list[str]) -> None:
    mask_named_environments(buffer, MATH_ENVIRONMENTS)
    mask_ensuremath_regions(buffer)
    mask_delimited_regions(buffer, r"\[", r"\]")
    mask_delimited_regions(buffer, r"\(", r"\)")
    mask_delimited_regions(buffer, "$$", "$$")
    mask_delimited_regions(buffer, "$", "$")


def skip_tex_whitespace(text: str, start: int) -> int:
    cursor = start
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    return cursor


def collect_opaque_command_argument_spans(
    text: str,
    excluded_commands: set[str] | None = None,
    included_commands: set[str] | None = None,
) -> list[tuple[int, int]]:
    """Locate protected TeX arguments that must not be parsed as prose or math."""
    spans: list[tuple[int, int]] = []

    for match in TEX_COMMAND_RE.finditer(text):
        if is_escaped(text, match.start()):
            continue
        command = match.group("name").lower()
        if excluded_commands and command in excluded_commands:
            continue
        if included_commands is not None and command not in included_commands:
            continue
        argument_count = OPAQUE_COMMAND_ARGUMENT_COUNTS.get(command)
        if argument_count is None:
            continue

        cursor = skip_tex_whitespace(text, match.end())
        while cursor < len(text) and text[cursor] == "[":
            option_end = find_balanced_end(text, cursor, "[", "]")
            if option_end is None:
                spans.append((cursor, len(text)))
                cursor = len(text)
                break
            if command not in VISIBLE_OPTION_ARGUMENT_COMMANDS:
                spans.append((cursor, option_end))
            cursor = skip_tex_whitespace(text, option_end)

        for _ in range(argument_count):
            if cursor >= len(text):
                break
            if text[cursor] == "{":
                argument_end = find_balanced_end(text, cursor, "{", "}")
                if argument_end is None:
                    spans.append((cursor, len(text)))
                    break
                spans.append((cursor, argument_end))
                cursor = skip_tex_whitespace(text, argument_end)
                continue

            if command in UNBRACED_PATH_COMMANDS:
                argument_end = cursor
                while argument_end < len(text) and not text[argument_end].isspace():
                    argument_end += 1
                spans.append((cursor, argument_end))
            break

    return spans


def mask_opaque_command_arguments(
    buffer: list[str], excluded_commands: set[str] | None = None
) -> None:
    text = "".join(buffer)
    spans = collect_opaque_command_argument_spans(text, excluded_commands)

    for start, end in spans:
        mask_span(buffer, start, end)


def escape_opaque_command_arguments_for_math(
    buffer: list[str], excluded_commands: set[str] | None = None
) -> None:
    """Escape TeX syntax inside protected arguments without hiding exact content."""
    text = "".join(buffer)
    spans = collect_opaque_command_argument_spans(text, excluded_commands)
    for start, end in spans:
        for index in range(start, end):
            replacement = OPAQUE_MATH_CHAR_ESCAPES.get(buffer[index])
            if replacement is not None:
                buffer[index] = replacement


def mask_cli_long_options(buffer: list[str]) -> None:
    text = "".join(buffer)
    for match in CLI_LONG_OPTION_RE.finditer(text):
        mask_span(buffer, match.start(), match.end())


def mask_nonprose_for_dash_check(text: str) -> str:
    """Return a same-length copy with non-prose TeX regions blanked."""
    buffer = list(text)
    opaque_spans = collect_opaque_command_argument_spans(
        text, included_commands=COMMENT_LITERAL_COMMANDS
    )
    mask_comments_and_literal_regions(
        text, buffer, comment_excluded_spans=opaque_spans
    )
    mask_named_environments(buffer, OPAQUE_ENVIRONMENTS)
    mask_math_regions(buffer)
    mask_opaque_command_arguments(buffer)
    mask_cli_long_options(buffer)
    return "".join(buffer)


def line_context(text: str, index: int, width: int = 120) -> tuple[int, str]:
    line_number = text.count("\n", 0, index) + 1
    line_start = text.rfind("\n", 0, index) + 1
    line_end = text.find("\n", index)
    if line_end == -1:
        line_end = len(text)

    half_width = max(width // 2, 1)
    context_start = max(line_start, index - half_width)
    context_end = min(line_end, index + half_width)
    context = " ".join(text[context_start:context_end].strip().split())
    if context_start > line_start:
        context = "... " + context
    if context_end < line_end:
        context += " ..."
    return line_number, context


def collect_prohibited_dashes(text: str) -> list[tuple[int, str, str]]:
    masked_text = mask_nonprose_for_dash_check(text)
    range_spans = [
        match.span("dash") for match in NUMERIC_RANGE_DASH_RE.finditer(masked_text)
    ]
    issues: list[tuple[int, str, str]] = []
    for match in PROHIBITED_DASH_RE.finditer(masked_text):
        if any(
            start <= match.start() and match.end() <= end for start, end in range_spans
        ):
            continue
        line_number, context = line_context(text, match.start())
        issues.append((line_number, match.group(0), context))
    return issues


def mask_inactive_tex(text: str, *, mask_math: bool = False) -> str:
    """Mask comments and literal regions while keeping source offsets stable."""
    buffer = list(text)
    comment_excluded_spans = collect_opaque_command_argument_spans(
        text, included_commands=COMMENT_LITERAL_COMMANDS
    )
    mask_comments_and_literal_regions(
        text,
        buffer,
        literal_environments=STRUCTURAL_LITERAL_ENVIRONMENTS,
        comment_excluded_spans=comment_excluded_spans,
    )
    if mask_math:
        mask_math_regions(buffer)
    return "".join(buffer)


def parse_structural_command_arguments(
    text: str,
    match: re.Match[str],
    command: str,
    argument_count: int,
) -> tuple[tuple[object, ...], tuple[str, ...], int]:
    """Parse protected options/arguments and return normalized signatures."""
    cursor = skip_tex_whitespace(text, match.end())
    options: list[object] = []
    while cursor < len(text) and text[cursor] == "[":
        option_end = find_balanced_end(text, cursor, "[", "]")
        if option_end is None:
            return ("<malformed>",), (), len(text)
        if command.lower() in (
            VISIBLE_OPTION_ARGUMENT_COMMANDS | VISIBLE_ENVIRONMENT_OPTION_NAMES
        ):
            option_text = text[cursor + 1 : option_end - 1]
            nested_signatures = tuple(
                event.signature for event in collect_structural_events(option_text)
            )
            options.append(("visible-option", nested_signatures))
        else:
            options.append(" ".join(text[cursor + 1 : option_end - 1].split()))
        cursor = skip_tex_whitespace(text, option_end)

    arguments: list[str] = []
    for _ in range(argument_count):
        if cursor >= len(text):
            arguments.append("<missing>")
            break
        if text[cursor] == "{":
            argument_end = find_balanced_end(text, cursor, "{", "}")
            if argument_end is None:
                arguments.append("<malformed>")
                cursor = len(text)
                break
            arguments.append(text[cursor + 1 : argument_end - 1].strip())
            cursor = skip_tex_whitespace(text, argument_end)
            continue
        if command.lower() in UNBRACED_PATH_COMMANDS:
            argument_end = cursor
            while argument_end < len(text) and not text[argument_end].isspace():
                argument_end += 1
            arguments.append(text[cursor:argument_end].strip())
            cursor = argument_end
            continue
        arguments.append("<missing>")
        break
    return tuple(options), tuple(arguments), cursor


def parse_all_structural_command_groups(
    text: str, match: re.Match[str]
) -> tuple[tuple[tuple[str, object], ...], int]:
    """Parse variable-length citation groups without losing any citation key."""
    cursor = skip_tex_whitespace(text, match.end())
    groups: list[tuple[str, object]] = []
    while cursor < len(text) and text[cursor] in "([{":
        opening = text[cursor]
        closing = {
            "(": ")",
            "[": "]",
            "{": "}",
        }[opening]
        group_end = find_balanced_end(text, cursor, opening, closing)
        if group_end is None:
            groups.append((opening, "<malformed>"))
            return tuple(groups), len(text)
        group_text = text[cursor + 1 : group_end - 1]
        value: object
        if opening in "([":
            value = (
                "visible-option",
                tuple(
                    event.signature
                    for event in collect_structural_events(group_text)
                ),
            )
        else:
            value = group_text.strip()
        groups.append((opening, value))
        cursor = skip_tex_whitespace(text, group_end)
    if not groups:
        groups.append(("", "<missing>"))
    return tuple(groups), cursor


def parse_volcite_groups(
    text: str, match: re.Match[str], *, plural: bool
) -> tuple[tuple[tuple[str, object], ...], int]:
    """Parse biblatex volume citations with interleaved notes and locators."""
    cursor = skip_tex_whitespace(text, match.end())
    groups: list[tuple[str, object]] = []

    def consume(
        opening: str,
        closing: str,
        label: str,
        *,
        visible: bool,
        required: bool = False,
    ) -> bool:
        nonlocal cursor
        if cursor >= len(text) or text[cursor] != opening:
            if required:
                groups.append((label, "<missing>"))
            return False
        group_end = find_balanced_end(text, cursor, opening, closing)
        if group_end is None:
            groups.append((label, "<malformed>"))
            cursor = len(text)
            return True
        group_text = text[cursor + 1 : group_end - 1]
        value: object
        if visible:
            value = (
                "visible-option",
                tuple(
                    event.signature
                    for event in collect_structural_events(group_text)
                ),
            )
        else:
            value = group_text.strip()
        groups.append((label, value))
        cursor = skip_tex_whitespace(text, group_end)
        return True

    if plural:
        consume("(", ")", "multiprenote", visible=True)
        consume("(", ")", "multipostnote", visible=True)

    item_index = 0
    while cursor < len(text):
        item_index += 1
        consume("[", "]", f"prenote:{item_index}", visible=True)
        if not consume(
            "{", "}", f"volume:{item_index}", visible=False, required=True
        ):
            break
        consume("[", "]", f"pages:{item_index}", visible=False)
        if not consume(
            "{", "}", f"key:{item_index}", visible=False, required=True
        ):
            break
        if not plural:
            break
        if cursor >= len(text) or text[cursor] not in "[{":
            break

    if not groups:
        groups.append(("", "<missing>"))
    return tuple(groups), cursor


def parse_multirow_layout_arguments(
    text: str, match: re.Match[str]
) -> tuple[tuple[tuple[str, str], ...], int]:
    """Parse multirow's interleaved protected options and layout arguments."""
    cursor = skip_tex_whitespace(text, match.end())
    groups: list[tuple[str, str]] = []

    def consume(opening: str, closing: str, label: str) -> bool:
        nonlocal cursor
        if cursor >= len(text) or text[cursor] != opening:
            return False
        end = find_balanced_end(text, cursor, opening, closing)
        if end is None:
            groups.append((label, "<malformed>"))
            cursor = len(text)
            return True
        groups.append((label, text[cursor + 1 : end - 1].strip()))
        cursor = skip_tex_whitespace(text, end)
        return True

    consume("[", "]", "vpos")
    if not consume("{", "}", "nrows"):
        groups.append(("nrows", "<missing>"))
        return tuple(groups), cursor
    consume("[", "]", "bigstruts")
    if not consume("{", "}", "width"):
        groups.append(("width", "<missing>"))
        return tuple(groups), cursor
    consume("[", "]", "vmove")
    return tuple(groups), cursor


def collect_structural_events(text: str) -> list[StructuralEvent]:
    """Collect protected TeX plus exact comments/literal source in document order."""
    inactive_buffer = list(text)
    comment_excluded_spans = collect_opaque_command_argument_spans(
        text, included_commands=COMMENT_LITERAL_COMMANDS
    )
    inactive_spans: list[tuple[str, int, int]] = []
    mask_comments_and_literal_regions(
        text,
        inactive_buffer,
        literal_environments=STRUCTURAL_LITERAL_ENVIRONMENTS,
        comment_excluded_spans=comment_excluded_spans,
        recorded_spans=inactive_spans,
    )
    mask_math_regions(inactive_buffer)
    active = "".join(inactive_buffer)
    indexed_events: list[tuple[int, StructuralEvent]] = []
    for kind, start, end in inactive_spans:
        signature: tuple[object, ...] = (
            "inactive-source",
            kind,
            text[start:end],
        )
        if kind == "comment":
            line_start = text.rfind("\n", 0, start) + 1
            placement = (
                "inline-comment"
                if text[line_start:start].strip()
                else "whole-line-comment"
            )
            newline = (
                "crlf"
                if text.startswith("\r\n", end)
                else "newline"
                if end < len(text) and text[end] in "\r\n"
                else "end-of-file"
            )
            signature = (*signature, placement, newline)
        indexed_events.append(
            (
                start,
                StructuralEvent(
                    signature,
                    text.count("\n", 0, start) + 1,
                    " ".join(text[start:end].split()),
                ),
            )
        )

    # Math content is checked separately (and may undergo an approved mapping),
    # but its boundary must remain ordered relative to comments, literal source,
    # and active TeX.  A kind-only event keeps that order without blocking an
    # explicitly authorized symbol substitution inside the region.
    math_regions, _ = extract_math_regions(text)
    for region in math_regions:
        indexed_events.append(
            (
                region.start_index,
                StructuralEvent(
                    ("math-boundary", region.kind),
                    region.line_number,
                    concise_math_source(region),
                ),
            )
        )
    cursor = 0
    while cursor < len(active):
        command_start = active.find("\\", cursor)
        if command_start == -1:
            break
        if is_escaped(active, command_start):
            cursor = command_start + 1
            continue

        environment = ENVIRONMENT_MARKER_RE.match(active, command_start)
        if environment is not None:
            action = environment.group("action")
            name = environment.group("name")
            event_end = environment.end()
            options: tuple[str, ...] = ()
            arguments: tuple[str, ...] = ()
            if action == "begin":
                options, arguments, event_end = parse_structural_command_arguments(
                    active,
                    environment,
                    name,
                    ENVIRONMENT_REQUIRED_ARGUMENT_COUNTS.get(name, 0),
                )
            source = " ".join(text[command_start:event_end].split())
            indexed_events.append(
                (
                    command_start,
                    StructuralEvent(
                        (
                            "environment",
                            action,
                            name,
                            options,
                            arguments,
                        ),
                        text.count("\n", 0, command_start) + 1,
                        source,
                    ),
                )
            )
            cursor = event_end
            continue

        command_match = TEX_COMMAND_RE.match(active, command_start)
        if command_match is None:
            end = min(command_start + 2, len(active))
            source = text[command_start:end]
            indexed_events.append(
                (
                    command_start,
                    StructuralEvent(
                        ("control-symbol", source),
                        text.count("\n", 0, command_start) + 1,
                        source,
                    ),
                )
            )
            cursor = end
            continue

        command = command_match.group("name")
        starred = text[command_match.start() : command_match.end()].endswith("*")
        if command.lower() == "multirow":
            groups, event_end = parse_multirow_layout_arguments(
                active, command_match
            )
            indexed_events.append(
                (
                    command_start,
                    StructuralEvent(
                        ("protected-command", command, starred, groups),
                        text.count("\n", 0, command_start) + 1,
                        " ".join(text[command_start:event_end].split()),
                    ),
                )
            )
            cursor = max(command_match.end(), event_end)
            continue
        lower_command = command.lower()
        is_singular_volcite = lower_command.endswith("volcite")
        is_plural_volcite = lower_command.endswith("volcites")
        is_citation_command = "cite" in lower_command
        if (
            lower_command in VARIABLE_PROTECTED_ARGUMENT_COMMANDS
            or is_citation_command
            or is_singular_volcite
            or is_plural_volcite
        ):
            if is_singular_volcite or is_plural_volcite:
                groups, event_end = parse_volcite_groups(
                    active, command_match, plural=is_plural_volcite
                )
            else:
                groups, event_end = parse_all_structural_command_groups(
                    active, command_match
                )
            signature = (
                "protected-command",
                command,
                starred,
                groups,
            )
            source_end = max(command_match.end(), event_end)
            indexed_events.append(
                (
                    command_start,
                    StructuralEvent(
                        signature,
                        text.count("\n", 0, command_start) + 1,
                        " ".join(text[command_start:source_end].split()),
                    ),
                )
            )
            cursor = source_end
            continue

        argument_count = CASE_SENSITIVE_PROTECTED_ARGUMENT_COUNTS.get(command)
        if argument_count is None:
            argument_count = OPAQUE_COMMAND_ARGUMENT_COUNTS.get(command.lower())

        if argument_count is None:
            signature: tuple[object, ...] = ("command", command, starred)
            event_end = command_match.end()
        else:
            options, arguments, event_end = parse_structural_command_arguments(
                active, command_match, command, argument_count
            )
            signature = (
                "protected-command",
                command,
                starred,
                options,
                arguments,
            )

        source_end = max(command_match.end(), event_end)
        indexed_events.append(
            (
                command_start,
                StructuralEvent(
                    signature,
                    text.count("\n", 0, command_start) + 1,
                    " ".join(text[command_start:source_end].split()),
                ),
            )
        )
        cursor = source_end

    for match in BIBTEX_ENTRY_RE.finditer(active):
        indexed_events.append(
            (
                match.start(),
                StructuralEvent(
                    ("bibtex", match.group(1).lower(), match.group(2).strip()),
                    text.count("\n", 0, match.start()) + 1,
                    match.group(0),
                ),
            )
        )

    return [event for _, event in sorted(indexed_events, key=lambda item: item[0])]


def structural_event_sequence_delta(
    original: list[StructuralEvent], polished: list[StructuralEvent]
) -> tuple[list[StructuralEvent], list[StructuralEvent]]:
    original_signatures = [event.signature for event in original]
    polished_signatures = [event.signature for event in polished]
    if original_signatures == polished_signatures:
        return [], []
    prefix = 0
    while (
        prefix < len(original_signatures)
        and prefix < len(polished_signatures)
        and original_signatures[prefix] == polished_signatures[prefix]
    ):
        prefix += 1
    suffix = 0
    while (
        suffix < len(original_signatures) - prefix
        and suffix < len(polished_signatures) - prefix
        and original_signatures[-1 - suffix] == polished_signatures[-1 - suffix]
    ):
        suffix += 1
    original_trim_end = len(original) - suffix if suffix else len(original)
    polished_trim_end = len(polished) - suffix if suffix else len(polished)
    matcher = SequenceMatcher(
        None,
        original_signatures[prefix:original_trim_end],
        polished_signatures[prefix:polished_trim_end],
        autojunk=False,
    )
    missing: list[StructuralEvent] = []
    added: list[StructuralEvent] = []
    for tag, original_start, original_end, polished_start, polished_end in matcher.get_opcodes():
        if tag in {"delete", "replace"}:
            missing.extend(original[prefix + original_start : prefix + original_end])
        if tag in {"insert", "replace"}:
            added.extend(polished[prefix + polished_start : prefix + polished_end])
    return missing, added


def select_events_for_signatures(
    events: list[StructuralEvent], signature_counts: Counter[str]
) -> list[StructuralEvent]:
    remaining = Counter(signature_counts)
    selected: list[StructuralEvent] = []
    for event in events:
        if remaining.get(event.signature, 0) > 0:
            selected.append(event)
            remaining[event.signature] -= 1
    return selected


def structural_event_multiset_delta(
    original: list[StructuralEvent], polished: list[StructuralEvent]
) -> tuple[list[StructuralEvent], list[StructuralEvent]]:
    """Compare structural events ignoring document order.

    Used only when the caller has explicitly authorized sentence reordering.
    Every citation, cross-reference, and protected argument must still be
    present exactly as many times as in the original.
    """
    original_counts = Counter(event.signature for event in original)
    polished_counts = Counter(event.signature for event in polished)
    missing = select_events_for_signatures(original, original_counts - polished_counts)
    added = select_events_for_signatures(polished, polished_counts - original_counts)
    return missing, added


def collect_tex_group_issues(text: str) -> list[TexGroupIssue]:
    """Validate active TeX grouping braces outside comments and literal code."""
    active = mask_inactive_tex(text)
    openings: list[int] = []
    issues: list[TexGroupIssue] = []
    for index, char in enumerate(active):
        if is_escaped(active, index):
            continue
        if char == "{":
            openings.append(index)
        elif char == "}":
            if openings:
                openings.pop()
            else:
                issues.append(
                    TexGroupIssue(
                        text.count("\n", 0, index) + 1,
                        "unmatched closing group brace '}'",
                    )
                )
    for index in openings:
        issues.append(
            TexGroupIssue(
                text.count("\n", 0, index) + 1,
                "unclosed opening group brace '{'",
            )
        )
    return issues


def print_tex_group_issues(
    title: str, issues: list[TexGroupIssue], limit: int
) -> None:
    if not issues:
        return
    print(title)
    for issue in issues[:limit]:
        print(f"  line {issue.line_number}: {issue.message}")
    if len(issues) > limit:
        print(f"  ... {len(issues) - limit} more")


def collect_tex_environment_issues(text: str) -> list[TexEnvironmentIssue]:
    """Validate statically visible begin/end nesting outside literal source."""
    active = mask_inactive_tex(text)
    stack: list[tuple[str, int]] = []
    issues: list[TexEnvironmentIssue] = []
    for marker in ENVIRONMENT_MARKER_RE.finditer(active):
        if is_escaped(active, marker.start()):
            continue
        action = marker.group("action")
        name = marker.group("name")
        line_number = text.count("\n", 0, marker.start()) + 1
        if action == "begin":
            stack.append((name, line_number))
            continue
        if not stack:
            issues.append(
                TexEnvironmentIssue(
                    line_number, f"unmatched \\end{{{name}}}"
                )
            )
            continue
        expected, _ = stack[-1]
        if expected != name:
            issues.append(
                TexEnvironmentIssue(
                    line_number,
                    f"mismatched \\end{{{name}}}; expected \\end{{{expected}}}",
                )
            )
            continue
        stack.pop()
    for name, line_number in stack:
        issues.append(
            TexEnvironmentIssue(
                line_number, f"unclosed \\begin{{{name}}}"
            )
        )
    return issues


def print_tex_environment_issues(
    title: str, issues: list[TexEnvironmentIssue], limit: int
) -> None:
    if not issues:
        return
    print(title)
    for issue in issues[:limit]:
        print(f"  line {issue.line_number}: {issue.message}")
    if len(issues) > limit:
        print(f"  ... {len(issues) - limit} more")


def check_structural_preservation(
    original_text: str,
    polished_text: str,
    limit: int,
    allow_reordering: bool = False,
) -> bool:
    original_events = collect_structural_events(original_text)
    polished_events = collect_structural_events(polished_text)
    reordered = False
    if allow_reordering:
        missing, added = structural_event_multiset_delta(
            original_events, polished_events
        )
        reordered = (
            not missing
            and not added
            and [event.signature for event in original_events]
            != [event.signature for event in polished_events]
        )
    else:
        missing, added = structural_event_sequence_delta(
            original_events, polished_events
        )
    original_group_issues = collect_tex_group_issues(original_text)
    polished_group_issues = collect_tex_group_issues(polished_text)
    original_environment_issues = collect_tex_environment_issues(original_text)
    polished_environment_issues = collect_tex_environment_issues(polished_text)
    passed = (
        not missing
        and not added
        and not original_group_issues
        and not polished_group_issues
        and not original_environment_issues
        and not polished_environment_issues
    )
    print(f"TeX structures and protected arguments: {'PASS' if passed else 'FAIL'}")
    if reordered:
        print(
            "  Structural event order changed but the multiset is unchanged "
            "(reorder mode). This verifies inventory, not semantic attachment; "
            "manually confirm that each citation/reference remains attached to the intended claim."
        )
    print_tex_group_issues(
        "Original TeX grouping issues:", original_group_issues, limit
    )
    print_tex_group_issues(
        "Candidate TeX grouping issues:", polished_group_issues, limit
    )
    print_tex_environment_issues(
        "Original TeX environment issues:", original_environment_issues, limit
    )
    print_tex_environment_issues(
        "Candidate TeX environment issues:", polished_environment_issues, limit
    )
    for title, events in (
        ("Missing or changed original structural events:", missing),
        ("Added or changed candidate structural events:", added),
    ):
        if not events:
            continue
        print(title)
        for event in events[:limit]:
            print(f"  line {event.line_number}: {event.source or event.signature}")
        if len(events) > limit:
            print(f"  ... {len(events) - limit} more")
    return passed


def collect_structural_keys(text: str) -> dict[str, Counter[str]]:
    text = mask_inactive_tex(text)
    keys: dict[str, Counter[str]] = defaultdict(Counter)
    for match in STRUCTURAL_COMMAND_RE.finditer(text):
        command, value = match.groups()
        keys[command][value.strip()] += 1
    for match in INCLUDEGRAPHICS_RE.finditer(text):
        star = match.group("star") or ""
        options = match.group("options")
        path = match.group("path")
        option_text = " ".join(options.split())
        prefix = f"{star}{option_text}" if option_text else star
        signature = f"{prefix}{{{path.strip()}}}"
        keys["includegraphics_options"][signature] += 1
    for entry_type, value in BIBTEX_ENTRY_RE.findall(text):
        keys[f"bibtex:{entry_type.lower()}"][value.strip()] += 1
    return dict(keys)


def split_reference_keys(command: str, value: str) -> list[str]:
    if command in MULTI_KEY_REFERENCE_COMMANDS:
        return [key.strip() for key in value.split(",")]
    return [value.strip()]


def collect_placeholder_reference_keys(text: str) -> dict[str, Counter[str]]:
    keys = collect_structural_keys(text)
    placeholders: dict[str, Counter[str]] = {}
    for command in sorted(REFERENCE_COMMANDS):
        command_placeholders: Counter[str] = Counter()
        for value, count in keys.get(command, Counter()).items():
            for key in split_reference_keys(command, value):
                if key.lower() in PLACEHOLDER_KEYS:
                    command_placeholders[key] += count
        if command_placeholders:
            placeholders[command] = command_placeholders
    return placeholders


def collect_numbered_caption_prefixes(text: str) -> Counter[str]:
    text = mask_intrinsic_prose_exclusions(text)
    captions: Counter[str] = Counter()
    for caption in CAPTION_RE.findall(text):
        caption_text = " ".join(caption.split())
        if NUMBERED_CAPTION_PREFIX_RE.search(caption_text):
            captions[caption_text] += 1
    return captions


def remove_caption_commands(text: str) -> str:
    return CAPTION_RE.sub(r"\\caption", text)


def mask_intrinsic_prose_exclusions(text: str) -> str:
    """Mask source regions that are preserved metadata rather than manuscript prose."""
    buffer = list(mask_inactive_tex(text))
    mask_named_environments(buffer, OPAQUE_ENVIRONMENTS)
    return "".join(buffer)


def collect_hardcoded_display_references(text: str) -> Counter[str]:
    text = remove_caption_commands(mask_intrinsic_prose_exclusions(text))
    return Counter(match.group(0) for match in HARDCODED_REFERENCE_RE.finditer(text))


def collect_reference_name_styles(text: str) -> dict[str, Counter[str]]:
    text = remove_caption_commands(mask_intrinsic_prose_exclusions(text))
    styles: dict[str, Counter[str]] = defaultdict(Counter)
    for match in MANUAL_REFERENCE_STYLE_RE.finditer(text):
        name = match.group("name").lower()
        object_type, style = REFERENCE_NAME_STYLES[name]
        styles[object_type][style] += 1
    return dict(styles)


def collect_numeric_occurrences(text: str) -> list[NumericOccurrence]:
    """Collect every source-level numerical value and adjacent quantity token in order."""
    indexed_occurrences: list[tuple[int, NumericOccurrence]] = []
    covered = bytearray(len(text))

    def normalize_value(value: str) -> str:
        return re.sub(rf"(?:{NUMERIC_SPACING_TOKEN_RE})+", "", value)

    def normalize_unit(unit: str) -> str:
        return " ".join(unit.split())

    def normalize_marker(marker: str) -> str:
        return re.sub(rf"(?:{NUMERIC_SPACING_TOKEN_RE})+", "", marker)

    def mark_group_covered(match: re.Match[str], group: str) -> None:
        start, end = match.span(group)
        if start < 0:
            return
        for index in range(start, end):
            covered[index] = 1

    def looks_pronominal(match: re.Match[str]) -> bool:
        value = match.group("value")
        preceding = text[: match.start("value")]
        following = text[match.end("value") :]
        if value.lower() == "one":
            modal_use = re.match(
                r"\s+(?:cannot|can|could|may|might|must|should|would|will)\s+"
                r"(?!of\b)[A-Za-z]",
                following,
                re.IGNORECASE,
            )
            direct_use = re.match(
                r"\s+(?:(?:often|readily|generally|typically|therefore|clearly)\s+)?"
                r"(?:observes?|infers?|notes?|sees?|finds?|concludes?|"
                r"derives?|obtains?|writes?|defines?|assumes?|considers?|"
                r"recognizes?|verifies?)\b",
                following,
                re.IGNORECASE,
            )
            auxiliary_use = re.match(
                r"\s+(?:(?:does|did)\s+(?:not\s+)?[A-Za-z]|"
                r"is\s+(?:able|likely|unlikely|required|expected|tempted)\s+to\b)",
                following,
                re.IGNORECASE,
            )
            reciprocal_use = re.match(r"\s+another\b", following, re.IGNORECASE)
            if modal_use or direct_use or auxiliary_use or reciprocal_use:
                return True
        if value.lower() == "second":
            return bool(
                re.match(
                    r"\s+(?:this|that|these|those|the|our|your|their)\b",
                    following,
                    re.IGNORECASE,
                )
                or re.search(r"\b(?:we|they|i|you)\s+$", preceding, re.IGNORECASE)
            )
        if value.lower() == "pair":
            return bool(
                re.match(
                    r"\s+(?:each|the|these|those|inputs?|samples?|observations?)\b",
                    following,
                    re.IGNORECASE,
                )
                or re.search(r"\b(?:we|they|i|you)\s+$", preceding, re.IGNORECASE)
            )
        return bool(
            value.lower() == "single"
            and (
                re.match(r"\s+out\b", following, re.IGNORECASE)
                or re.search(
                    r"\b(?:we|they|i|you)\s+$", preceding, re.IGNORECASE
                )
            )
        )

    def source_contains_number(source: str) -> bool:
        return (
            any(char.isnumeric() for char in source)
            or TEXTUAL_NUMBER_PATTERN.search(source) is not None
            or CONTEXTUAL_ROMAN_NUMBER_PATTERN.search(source) is not None
        )

    def add_adjacent_quantity(
        anchor_start: int, anchor_end: int, anchor_value: str
    ) -> None:
        source_start = anchor_start
        source_end = anchor_end
        sign = ""
        prefix_unit = ""
        suffix_unit = ""
        prefix_marker = ""
        marker = ""

        spacing_match = NUMERIC_SPACING_SUFFIX_PATTERN.search(text[:anchor_start])
        spacing_start = (
            spacing_match.start() if spacing_match is not None else anchor_start
        )
        sign_index = spacing_start - 1
        if sign_index >= 0 and text[sign_index] in NUMERIC_SIGN_CHARS:
            sign = text[sign_index]
            source_start = sign_index

        prefix_match = CURRENCY_BEFORE_NUMBER_PATTERN.search(text[:source_start])
        if prefix_match is not None:
            prefix_unit = normalize_unit(prefix_match.group("unit") or "")
            source_start = prefix_match.start()

        prefix_marker_match = SIGNIFICANCE_MARKER_BEFORE_NUMBER_PATTERN.search(
            text[:source_start]
        )
        if prefix_marker_match is not None:
            prefix_marker = normalize_marker(
                prefix_marker_match.group("marker") or ""
            )
            source_start = prefix_marker_match.start()

        unit_match = UNIT_AFTER_NUMBER_RE.match(text, anchor_end)
        if unit_match is not None:
            suffix_unit = normalize_unit(unit_match.group("unit") or "")
            if suffix_unit:
                source_end = unit_match.end()

        marker_match = SIGNIFICANCE_MARKER_PATTERN.match(text, source_end)
        if marker_match is not None:
            marker = normalize_marker(marker_match.group(0))
            source_end = marker_match.end()

        marker = " ".join(
            part for part in (prefix_marker, marker) if part
        )
        unit = " ".join(
            part for part in (prefix_unit, suffix_unit) if part
        )
        if not sign and not unit and not marker:
            return
        indexed_occurrences.append(
            (
                source_start,
                NumericOccurrence(
                    value=sign + anchor_value,
                    unit=unit,
                    marker=marker,
                    line_number=text.count("\n", 0, source_start) + 1,
                    source=" ".join(text[source_start:source_end].split()),
                ),
            )
        )

    # Deliberately scan the raw source.  Numbers in comments, literal examples,
    # identifiers, URLs, and protected arguments are still numbers and must not
    # be changed by Horizon-Ember.
    for match in NUMERIC_OCCURRENCE_RE.finditer(text):
        value = normalize_value(match.group("value"))
        prefix_unit = normalize_unit(match.group("prefix_unit") or "")
        suffix_unit = normalize_unit(match.group("unit") or "")
        occurrence_end = match.end()
        class_count_match: re.Match[str] | None = None
        if len(suffix_unit) == 1 and suffix_unit.isupper():
            class_count_match = re.match(
                rf"\s+(?P<count>{COUNT_UNIT_RE})(?![A-Za-z0-9_])",
                text[match.end() :],
            )
            if class_count_match is not None:
                suffix_unit = class_count_match.group("count")
                occurrence_end = match.end() + class_count_match.end()
        unit = " ".join(part for part in (prefix_unit, suffix_unit) if part)
        marker = normalize_marker(match.group("marker") or "")
        occurrence = NumericOccurrence(
            value=value,
            unit=unit,
            marker=marker,
            line_number=text.count("\n", 0, match.start()) + 1,
            source=" ".join(text[match.start() : occurrence_end].split()),
        )
        indexed_occurrences.append((match.start(), occurrence))
        groups_to_mark = ["prefix_unit", "value", "marker"]
        if class_count_match is None:
            groups_to_mark.append("unit")
        for group in groups_to_mark:
            mark_group_covered(match, group)
        if class_count_match is not None:
            count_start, count_end = class_count_match.span("count")
            for index in range(
                match.end() + count_start,
                match.end() + count_end,
            ):
                covered[index] = 1

    for pattern, canonicalizer in (
        (TEXTUAL_NUMBER_PATTERN, str.lower),
        (CONTEXTUAL_ROMAN_NUMBER_PATTERN, str.upper),
    ):
        for match in pattern.finditer(text):
            number_start, number_end = match.span("value")
            if any(covered[number_start:number_end]):
                continue
            if pattern is TEXTUAL_NUMBER_PATTERN and looks_pronominal(match):
                # Pronominal/verb uses such as ``one can observe`` and
                # ``we second this`` are not numerical tokens.  Keep genuinely
                # quantitative uses such as ``one model`` protected.
                continue
            source_start = number_start
            source_end = number_end
            sign = ""
            prefix_unit = ""
            prefix_marker = ""
            suffix_unit = ""
            marker = ""

            spacing_match = NUMERIC_SPACING_SUFFIX_PATTERN.search(
                text[:number_start]
            )
            spacing_start = (
                spacing_match.start()
                if spacing_match is not None
                else number_start
            )
            sign_index = spacing_start - 1
            if sign_index >= 0 and text[sign_index] in NUMERIC_SIGN_CHARS:
                sign = text[sign_index]
                source_start = sign_index

            prefix_match = CURRENCY_BEFORE_NUMBER_PATTERN.search(
                text[:source_start]
            )
            if prefix_match is not None:
                prefix_unit = normalize_unit(prefix_match.group("unit") or "")
                source_start = prefix_match.start()

            prefix_marker_match = SIGNIFICANCE_MARKER_BEFORE_NUMBER_PATTERN.search(
                text[:source_start]
            )
            if prefix_marker_match is not None:
                prefix_marker = normalize_marker(
                    prefix_marker_match.group("marker") or ""
                )
                source_start = prefix_marker_match.start()

            unit_match = UNIT_AFTER_NUMBER_RE.match(text, number_end)
            if unit_match is not None:
                suffix_unit = normalize_unit(unit_match.group("unit") or "")
                if suffix_unit:
                    source_end = unit_match.end()
            marker_match = SIGNIFICANCE_MARKER_PATTERN.match(text, source_end)
            if marker_match is not None:
                marker = normalize_marker(marker_match.group(0))
                source_end = marker_match.end()
            unit = " ".join(
                part for part in (prefix_unit, suffix_unit) if part
            )
            marker = " ".join(
                part for part in (prefix_marker, marker) if part
            )
            indexed_occurrences.append(
                (
                    source_start,
                    NumericOccurrence(
                        value=sign + canonicalizer(match.group("value")),
                        unit=unit,
                        marker=marker,
                        line_number=text.count("\n", 0, source_start) + 1,
                        source=" ".join(text[source_start:source_end].split()),
                    ),
                )
            )
            for index in range(number_start, number_end):
                covered[index] = 1
            if unit_match is not None and unit:
                for index in range(*unit_match.span("unit")):
                    covered[index] = 1
            if marker_match is not None and marker:
                for index in range(marker_match.start(), marker_match.end()):
                    covered[index] = 1

    # Python's ``str.isnumeric`` additionally covers superscripts, vulgar
    # fractions, circled numbers, CJK numerals, and Unicode Roman numerals.
    # These forms are not part of the decimal/scientific regex above.
    cursor = 0
    while cursor < len(text):
        if covered[cursor] or not text[cursor].isnumeric():
            cursor += 1
            continue
        number_start = cursor
        while (
            cursor < len(text)
            and not covered[cursor]
            and text[cursor].isnumeric()
        ):
            cursor += 1
        number_end = cursor

        source_start = number_start
        sign = ""
        spacing_match = NUMERIC_SPACING_SUFFIX_PATTERN.search(text[:number_start])
        spacing_start = spacing_match.start() if spacing_match is not None else number_start
        sign_index = spacing_start - 1
        if sign_index >= 0 and text[sign_index] in NUMERIC_SIGN_CHARS:
            sign = text[sign_index]
            source_start = sign_index

        prefix_match = CURRENCY_BEFORE_NUMBER_PATTERN.search(text[:source_start])
        prefix_unit = ""
        if prefix_match is not None:
            prefix_unit = normalize_unit(prefix_match.group("unit"))
            source_start = prefix_match.start()

        unit = prefix_unit
        marker = ""
        source_end = number_end
        unit_match = UNIT_AFTER_NUMBER_RE.match(text, number_end)
        if unit_match is not None:
            suffix_unit = normalize_unit(unit_match.group("unit") or "")
            if suffix_unit:
                unit = " ".join(part for part in (unit, suffix_unit) if part)
                source_end = unit_match.end()
        marker_match = SIGNIFICANCE_MARKER_PATTERN.match(text, source_end)
        if marker_match is not None:
            marker = normalize_marker(marker_match.group(0))
            source_end = marker_match.end()

        indexed_occurrences.append(
            (
                source_start,
                NumericOccurrence(
                    value=sign + text[number_start:number_end],
                    unit=unit,
                    marker=marker,
                    line_number=text.count("\n", 0, source_start) + 1,
                    source=" ".join(text[source_start:source_end].split()),
                ),
            )
        )

    # A number may be enclosed by a math delimiter or a supported numeric
    # macro while its unit or significance marker remains immediately outside.
    # Bind those adjacent tokens to a stable placeholder; the anchor content is
    # already checked by the math/structural comparison.
    math_regions, _ = extract_math_regions(text)
    for region in math_regions:
        if source_contains_number(region.source):
            add_adjacent_quantity(
                region.start_index,
                region.end_index,
                f"<numeric-{region.kind}>",
            )

    for command_match in TEX_COMMAND_RE.finditer(text):
        command = command_match.group("name")
        if command not in NUMERIC_VALUE_COMMANDS:
            continue
        argument_count = CASE_SENSITIVE_PROTECTED_ARGUMENT_COUNTS[command]
        _, _, command_end = parse_structural_command_arguments(
            text, command_match, command, argument_count
        )
        if source_contains_number(text[command_match.start() : command_end]):
            add_adjacent_quantity(
                command_match.start(),
                command_end,
                f"<numeric-command:{command}>",
            )

    literal_buffer = list(text)
    literal_spans: list[tuple[str, int, int]] = []
    literal_comment_exclusions = collect_opaque_command_argument_spans(
        text, included_commands=COMMENT_LITERAL_COMMANDS
    )
    mask_comments_and_literal_regions(
        text,
        literal_buffer,
        literal_environments=STRUCTURAL_LITERAL_ENVIRONMENTS,
        comment_excluded_spans=literal_comment_exclusions,
        recorded_spans=literal_spans,
    )
    for kind, start, end in literal_spans:
        if kind != "comment" and source_contains_number(text[start:end]):
            add_adjacent_quantity(start, end, f"<numeric-{kind}>")

    for command_match in TEX_COMMAND_RE.finditer(text):
        command = command_match.group("name")
        if command.lower() not in NUMERIC_TEXT_ARGUMENT_COMMANDS:
            continue
        _, _, command_end = parse_structural_command_arguments(
            text, command_match, command, 1
        )
        if source_contains_number(text[command_match.start() : command_end]):
            add_adjacent_quantity(
                command_match.start(),
                command_end,
                f"<numeric-text-command:{command.lower()}>",
            )

    for match in COMMENT_SPLICED_MARKER_PATTERN.finditer(text):
        raw_value = match.group("value")
        normalized_value = normalize_value(raw_value)
        if any(char.isalpha() for char in raw_value):
            normalized_value = normalized_value.lower()
        indexed_occurrences.append(
            (
                match.start(),
                NumericOccurrence(
                    value=normalized_value,
                    unit="",
                    marker=normalize_marker(match.group("marker")),
                    line_number=text.count("\n", 0, match.start()) + 1,
                    source=" ".join(text[match.start() : match.end()].split()),
                ),
            )
        )

    for match in DELIMITED_TECHNICAL_TOKEN_PATTERN.finditer(text):
        token = match.group("token")
        value = "<standalone-token>"
        unit = ""
        marker = ""
        if token in NUMERIC_SIGN_CHARS:
            value = token + value
        elif re.fullmatch(SIGNIFICANCE_MARKER_RE, token):
            marker = normalize_marker(token)
        else:
            unit = normalize_unit(token)
        indexed_occurrences.append(
            (
                match.start(),
                NumericOccurrence(
                    value=value,
                    unit=unit,
                    marker=marker,
                    line_number=text.count("\n", 0, match.start()) + 1,
                    source=" ".join(match.group(0).split()),
                ),
            )
        )

    for pattern, group, field in (
        (STANDALONE_UNIT_CUE_PATTERN, "unit", "unit"),
        (STANDALONE_CURRENCY_CUE_PATTERN, "unit", "unit"),
        (STANDALONE_SIGN_CUE_PATTERN, "sign", "sign"),
        (STANDALONE_MARKER_CUE_PATTERN, "marker", "marker"),
    ):
        for match in pattern.finditer(text):
            token = match.group(group)
            indexed_occurrences.append(
                (
                    match.start(group),
                    NumericOccurrence(
                        value=(token if field == "sign" else "")
                        + "<standalone-cue>",
                        unit=normalize_unit(token) if field == "unit" else "",
                        marker=(
                            normalize_marker(token) if field == "marker" else ""
                        ),
                        line_number=text.count("\n", 0, match.start(group)) + 1,
                        source=" ".join(match.group(0).split()),
                    ),
                )
            )

    return [
        occurrence
        for _, occurrence in sorted(indexed_occurrences, key=lambda item: item[0])
    ]


def collect_numbers(text: str) -> Counter[str]:
    return Counter(
        f"{occurrence.value} {occurrence.unit}{occurrence.marker}".rstrip()
        for occurrence in collect_numeric_occurrences(text)
    )


def numeric_sequence_delta(
    original: list[NumericOccurrence], polished: list[NumericOccurrence]
) -> tuple[list[NumericOccurrence], list[NumericOccurrence]]:
    original_signatures = [occurrence.signature for occurrence in original]
    polished_signatures = [occurrence.signature for occurrence in polished]
    if original_signatures == polished_signatures:
        return [], []
    prefix = 0
    while (
        prefix < len(original_signatures)
        and prefix < len(polished_signatures)
        and original_signatures[prefix] == polished_signatures[prefix]
    ):
        prefix += 1
    suffix = 0
    while (
        suffix < len(original_signatures) - prefix
        and suffix < len(polished_signatures) - prefix
        and original_signatures[-1 - suffix] == polished_signatures[-1 - suffix]
    ):
        suffix += 1
    original_trim_end = len(original) - suffix if suffix else len(original)
    polished_trim_end = len(polished) - suffix if suffix else len(polished)
    matcher = SequenceMatcher(
        None,
        original_signatures[prefix:original_trim_end],
        polished_signatures[prefix:polished_trim_end],
        autojunk=False,
    )
    missing: list[NumericOccurrence] = []
    added: list[NumericOccurrence] = []
    for tag, original_start, original_end, polished_start, polished_end in matcher.get_opcodes():
        if tag in {"delete", "replace"}:
            missing.extend(original[prefix + original_start : prefix + original_end])
        if tag in {"insert", "replace"}:
            added.extend(polished[prefix + polished_start : prefix + polished_end])
    return missing, added


def numeric_multiset_delta(
    original: list[NumericOccurrence], polished: list[NumericOccurrence]
) -> tuple[list[NumericOccurrence], list[NumericOccurrence]]:
    """Compare recognized numeric occurrences without requiring document order."""
    original_counts = Counter(occurrence.signature for occurrence in original)
    polished_counts = Counter(occurrence.signature for occurrence in polished)
    missing_counts = original_counts - polished_counts
    added_counts = polished_counts - original_counts

    missing: list[NumericOccurrence] = []
    added: list[NumericOccurrence] = []

    remaining = missing_counts.copy()
    for occurrence in original:
        if remaining[occurrence.signature] > 0:
            missing.append(occurrence)
            remaining[occurrence.signature] -= 1

    remaining = added_counts.copy()
    for occurrence in polished:
        if remaining[occurrence.signature] > 0:
            added.append(occurrence)
            remaining[occurrence.signature] -= 1

    return missing, added


def check_numeric_preservation(
    original_text: str, polished_text: str, limit: int, allow_reordering: bool = False
) -> bool:
    """Require exact recognized numeric content; optionally ignore document order."""
    original = collect_numeric_occurrences(original_text)
    polished = collect_numeric_occurrences(polished_text)
    if allow_reordering:
        missing, added = numeric_multiset_delta(original, polished)
        label = "Recognized numeric/unit/sign/marker multiset"
    else:
        missing, added = numeric_sequence_delta(original, polished)
        label = "Recognized numeric/unit/sign/marker sequence"
    passed = not missing and not added
    print(f"{label}: {'PASS' if passed else 'FAIL'}")
    if allow_reordering:
        print(
            "Numeric occurrence order: NOT ENFORCED (reader-oriented mode; "
            "manually verify metric/condition/value bindings)."
        )
    for title, occurrences in (
        ("Missing or changed original numeric occurrences:", missing),
        ("Added or changed candidate numeric occurrences:", added),
    ):
        if not occurrences:
            continue
        print(title)
        for occurrence in occurrences[:limit]:
            unit = f" {occurrence.unit}" if occurrence.unit else ""
            marker = occurrence.marker
            print(
                f"  line {occurrence.line_number}: "
                f"{occurrence.value}{unit}{marker} ({occurrence.source})"
            )
        if len(occurrences) > limit:
            print(f"  ... {len(occurrences) - limit} more")
    return passed


def math_region_sequence_delta(
    original: list[MathRegion], polished: list[MathRegion]
) -> tuple[list[MathRegion], list[MathRegion]]:
    """Return removed/changed and added/changed regions while preserving document order."""
    original_signatures = [region.signature for region in original]
    polished_signatures = [region.signature for region in polished]
    if original_signatures == polished_signatures:
        return [], []
    prefix = 0
    while (
        prefix < len(original_signatures)
        and prefix < len(polished_signatures)
        and original_signatures[prefix] == polished_signatures[prefix]
    ):
        prefix += 1
    suffix = 0
    while (
        suffix < len(original_signatures) - prefix
        and suffix < len(polished_signatures) - prefix
        and original_signatures[-1 - suffix] == polished_signatures[-1 - suffix]
    ):
        suffix += 1
    original_trim_end = len(original) - suffix if suffix else len(original)
    polished_trim_end = len(polished) - suffix if suffix else len(polished)
    matcher = SequenceMatcher(
        None,
        original_signatures[prefix:original_trim_end],
        polished_signatures[prefix:polished_trim_end],
        autojunk=False,
    )
    missing: list[MathRegion] = []
    added: list[MathRegion] = []
    for tag, original_start, original_end, polished_start, polished_end in matcher.get_opcodes():
        if tag in {"delete", "replace"}:
            missing.extend(original[prefix + original_start : prefix + original_end])
        if tag in {"insert", "replace"}:
            added.extend(polished[prefix + polished_start : prefix + polished_end])
    return missing, added


def concise_math_source(region: MathRegion, width: int = 140) -> str:
    """Format a math region as a compact single-line diagnostic excerpt."""
    source = " ".join(region.source.split())
    if len(source) <= width:
        return source
    return source[: max(width - 3, 1)].rstrip() + "..."


def closest_math_region(region: MathRegion, candidates: list[MathRegion]) -> MathRegion | None:
    """Return the most token-similar candidate, preferring the same math kind."""
    same_kind = [candidate for candidate in candidates if candidate.kind == region.kind]
    pool = same_kind or candidates
    if not pool:
        return None
    return max(
        pool,
        key=lambda candidate: SequenceMatcher(
            None, region.tokens, candidate.tokens, autojunk=False
        ).ratio(),
    )


def print_math_regions(title: str, regions: list[MathRegion], candidates: list[MathRegion], limit: int) -> None:
    """Print changed math regions with source locations and a nearby candidate."""
    if not regions:
        return
    print(title)
    for region in regions[:limit]:
        print(f"  line {region.line_number} [{region.kind}]: {concise_math_source(region)}")
        closest = closest_math_region(region, candidates)
        if closest is not None and closest.signature != region.signature:
            print(
                f"    closest line {closest.line_number} [{closest.kind}]: "
                f"{concise_math_source(closest)}"
            )
    remaining = len(regions) - limit
    if remaining > 0:
        print(f"  ... {remaining} more")


def print_math_parse_issues(title: str, issues: list[MathParseIssue], limit: int) -> None:
    if not issues:
        return
    print(title)
    for issue in issues[:limit]:
        print(f"  line {issue.line_number}: {issue.message}")
    remaining = len(issues) - limit
    if remaining > 0:
        print(f"  ... {remaining} more")


def parse_approved_symbol_maps(values: list[str]) -> list[ApprovedSymbolMap]:
    """Parse repeatable OLD=NEW mappings and reject anything numerical."""
    mappings: list[ApprovedSymbolMap] = []
    seen: dict[tuple[str, ...], tuple[str, ...]] = {}
    for value in values:
        if value.count("=") != 1:
            raise ValueError(
                f"invalid approved symbol map {value!r}; expected OLD=NEW"
            )
        source, target = (part.strip() for part in value.split("=", 1))
        if not source or not target:
            raise ValueError(
                f"invalid approved symbol map {value!r}; both sides are required"
            )
        if (
            any(char.isnumeric() for char in source + target)
            or TEXTUAL_NUMBER_PATTERN.search(source + " " + target)
            or CONTEXTUAL_ROMAN_NUMBER_PATTERN.search(source + " " + target)
            or UNAMBIGUOUS_MAPPING_QUANTITY_PATTERN.search(source)
            or UNAMBIGUOUS_MAPPING_QUANTITY_PATTERN.search(target)
        ):
            raise ValueError(
                f"numeric, currency, or percentage content is not allowed in approved symbol map {value!r}"
            )
        if "$" in source + target or any(
            delimiter in source + target for delimiter in (r"\(", r"\)", r"\[", r"\]")
        ):
            raise ValueError(
                f"approved symbol map {value!r} must contain math fragments, not delimiters"
            )
        source_tokens = tokenize_math(source)
        target_tokens = tokenize_math(target)
        protected_sign_tokens = {
            *NUMERIC_SIGN_CHARS,
            "*",
            "\u2020",
            "\u2021",
            r"\ast",
            r"\dagger",
            r"\ddagger",
            r"\pm",
            r"\mp",
        }
        if protected_sign_tokens.intersection(source_tokens + target_tokens):
            raise ValueError(
                f"numeric or mathematical signs are not allowed in approved symbol map {value!r}"
            )
        if not source_tokens or not target_tokens or source_tokens == target_tokens:
            raise ValueError(
                f"approved symbol map {value!r} must describe a nonempty change"
            )
        previous = seen.get(source_tokens)
        if previous is not None and previous != target_tokens:
            raise ValueError(f"conflicting approved mappings for {source!r}")
        if previous is not None:
            continue
        seen[source_tokens] = target_tokens
        mappings.append(
            ApprovedSymbolMap(
                source=source,
                target=target,
                source_tokens=source_tokens,
                target_tokens=target_tokens,
            )
        )
    return mappings


def protected_mapping_flags(tokens: tuple[str, ...]) -> list[bool]:
    """Mark text-mode and opaque-argument tokens that symbol maps may not touch."""
    flags = [False] * len(tokens)
    mode_stack: list[tuple[str, bool, str | None]] = [("root", False, None)]
    pending_argument_mode: bool | None = None
    opaque_depth = 0
    opaque_open = OPAQUE_MATH_CHAR_ESCAPES["{"]
    opaque_close = OPAQUE_MATH_CHAR_ESCAPES["}"]

    for index, token in enumerate(tokens):
        if token == opaque_open:
            opaque_depth += 1
            flags[index] = True
            continue
        if token == opaque_close:
            flags[index] = True
            opaque_depth = max(opaque_depth - 1, 0)
            continue
        if opaque_depth:
            flags[index] = True
            continue

        in_text_mode = mode_stack[-1][1]
        flags[index] = in_text_mode
        if token == "{":
            argument_mode = in_text_mode if pending_argument_mode is None else pending_argument_mode
            mode_stack.append(("brace", argument_mode, None))
            pending_argument_mode = None
            continue
        if token == "}":
            if len(mode_stack) > 1 and mode_stack[-1][0] == "brace":
                mode_stack.pop()
            pending_argument_mode = None
            continue
        if token in {"$", "$$"}:
            if mode_stack[-1][0] == "delimiter" and mode_stack[-1][2] == token:
                mode_stack.pop()
            elif in_text_mode:
                mode_stack.append(("delimiter", False, token))
            pending_argument_mode = None
            continue
        if token in {r"\(", r"\["} and in_text_mode:
            closing = r"\)" if token == r"\(" else r"\]"
            mode_stack.append(("delimiter", False, closing))
            pending_argument_mode = None
            continue
        if mode_stack[-1][0] == "delimiter" and mode_stack[-1][2] == token:
            mode_stack.pop()
            pending_argument_mode = None
            continue
        if token.startswith("\\") and len(token) > 1 and token[1:].isalpha():
            command = token[1:]
            if command in TEXT_MODE_MATH_COMMANDS:
                pending_argument_mode = True
            elif command in MATH_MODE_TEXT_COMMANDS:
                pending_argument_mode = False
            else:
                pending_argument_mode = None
        elif token != " " and not (token == "*" and pending_argument_mode is not None):
            pending_argument_mode = None
    return flags


def apply_approved_symbol_maps(
    tokens: tuple[str, ...], mappings: list[ApprovedSymbolMap]
) -> tuple[tuple[str, ...], Counter[str]]:
    """Apply approved token mappings simultaneously, preferring longer sources."""
    ordered = sorted(mappings, key=lambda mapping: len(mapping.source_tokens), reverse=True)
    protected_flags = protected_mapping_flags(tokens)
    transformed: list[str] = []
    uses: Counter[str] = Counter()
    cursor = 0
    while cursor < len(tokens):
        matched: ApprovedSymbolMap | None = None
        for mapping in ordered:
            end = cursor + len(mapping.source_tokens)
            if (
                tokens[cursor:end] == mapping.source_tokens
                and not any(protected_flags[cursor:end])
            ):
                matched = mapping
                break
        if matched is None:
            transformed.append(tokens[cursor])
            cursor += 1
            continue
        transformed.extend(matched.target_tokens)
        uses[matched.source] += 1
        cursor += len(matched.source_tokens)
    return tuple(transformed), uses


def normalized_nonmath_skeleton(text: str) -> tuple[tuple[str, str], ...]:
    """Return layout-normalized prose while preserving literal source exactly."""
    regions, _ = extract_math_regions(text)
    recorded_spans: list[tuple[str, int, int]] = []
    scratch = list(text)
    mask_comments_and_literal_regions(
        text,
        scratch,
        literal_environments=STRUCTURAL_LITERAL_ENVIRONMENTS,
        recorded_spans=recorded_spans,
    )
    protected_spans: list[tuple[int, int, str, str]] = [
        (region.start_index, region.end_index, "math", region.kind)
        for region in regions
    ]
    protected_spans.extend(
        (start, end, kind, text[start:end])
        for kind, start, end in recorded_spans
    )
    protected_spans.sort(key=lambda span: (span[0], span[1]))

    signature: list[tuple[str, str]] = []
    cursor = 0
    for start, end, kind, payload in protected_spans:
        if start < cursor:
            continue
        signature.append(("layout", " ".join(text[cursor:start].split())))
        signature.append((kind, payload))
        cursor = end
    signature.append(("layout", " ".join(text[cursor:].split())))
    return tuple(signature)


def check_math_preservation(
    original_text: str,
    polished_text: str,
    limit: int,
    allow_additions: bool,
    approved_symbol_maps: list[ApprovedSymbolMap] | None = None,
) -> bool:
    """Check normalized math regions without claiming source-level semantic consistency."""
    original_regions, original_issues = extract_math_regions(original_text)
    polished_regions, polished_issues = extract_math_regions(polished_text)

    mappings = approved_symbol_maps or []
    expected_regions = original_regions
    mapping_uses: Counter[str] = Counter()
    if mappings:
        expected_regions = []
        for region in original_regions:
            transformed_tokens, uses = apply_approved_symbol_maps(region.tokens, mappings)
            mapping_uses.update(uses)
            expected_regions.append(
                MathRegion(
                    kind=region.kind,
                    tokens=transformed_tokens,
                    line_number=region.line_number,
                    source=region.source,
                    start_index=region.start_index,
                    end_index=region.end_index,
                )
            )

    # Protected math is exact in every mode. ``--allow-additions`` is retained
    # only for prose-workflow compatibility and never relaxes this comparison.
    missing, added = math_region_sequence_delta(expected_regions, polished_regions)
    unused_mappings = [mapping for mapping in mappings if not mapping_uses[mapping.source]]
    passed = (
        not original_issues
        and not polished_issues
        and not missing
        and not added
        and not unused_mappings
    )
    if mappings:
        mode_note = " (approved normalization)"
    elif allow_additions:
        mode_note = " (protected content remains strict)"
    else:
        mode_note = ""
    print(f"Math regions: {'PASS' if passed else 'FAIL'}{mode_note}")
    print_math_parse_issues("Original math parse issues:", original_issues, limit)
    print_math_parse_issues("Polished math parse issues:", polished_issues, limit)
    print_math_regions(
        "Missing or changed expected math regions:", missing, polished_regions, limit
    )
    print_math_regions("Added or changed candidate math regions:", added, expected_regions, limit)
    if mappings:
        for mapping in mappings:
            count = mapping_uses[mapping.source]
            status = "AUTHORIZED CHANGE" if count else "UNUSED MAPPING"
            print(f"  {status}: {mapping.source} -> {mapping.target} ({count} replacement(s))")
    return passed


def check_placeholder_reference_keys(polished_text: str, limit: int) -> bool:
    placeholders = collect_placeholder_reference_keys(polished_text)
    if not placeholders:
        print("Placeholder label/reference keys: PASS")
        return True

    print("Placeholder label/reference keys: FAIL")
    print("  Replace bare placeholder keys with semantic keys, such as tab:diff_methods or fig:framework.")
    for command in sorted(placeholders):
        print(f"  \\{command}:")
        for key, count in placeholders[command].most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    \\{command}{{{key}}}{suffix}")
        remaining = len(placeholders[command]) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def check_hardcoded_display_numbering(polished_text: str, limit: int) -> bool:
    numbered_captions = collect_numbered_caption_prefixes(polished_text)
    hardcoded_refs = collect_hardcoded_display_references(polished_text)
    if not numbered_captions and not hardcoded_refs:
        print("Hard-coded display numbering: PASS")
        return True

    print("Hard-coded display numbering: FAIL")
    print(
        "  Use LaTeX-generated numbering with the journal/manuscript style, "
        "such as Fig.~\\ref{fig:framework} or Figure~\\ref{fig:framework}, and omit Figure/Table numbers from captions."
    )
    if numbered_captions:
        print("  Numbered caption prefixes:")
        for caption, count in numbered_captions.most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    \\caption{{{caption}}}{suffix}")
        remaining = len(numbered_captions) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    if hardcoded_refs:
        print("  Hard-coded prose references:")
        for reference, count in hardcoded_refs.most_common(limit):
            suffix = f" x{count}" if count > 1 else ""
            print(f"    {reference}{suffix}")
        remaining = len(hardcoded_refs) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def check_reference_name_style(original_text: str, polished_text: str, limit: int) -> bool:
    original_styles = collect_reference_name_styles(original_text)
    polished_styles = collect_reference_name_styles(polished_text)
    issues: dict[str, list[str]] = {}

    for object_type, polished_counter in polished_styles.items():
        polished_style_set = set(polished_counter)
        original_style_set = set(original_styles.get(object_type, Counter()))
        if original_style_set:
            introduced_styles = sorted(polished_style_set - original_style_set)
            if introduced_styles:
                issues[object_type] = [
                    f"introduced {', '.join(introduced_styles)} style; original uses {', '.join(sorted(original_style_set))}"
                ]
        elif len(polished_style_set) > 1:
            issues[object_type] = [f"mixed {', '.join(sorted(polished_style_set))} styles without an original style baseline"]

    if not issues:
        print("Reference-name style: PASS")
        return True

    print("Reference-name style: FAIL")
    print("  Match the target journal or manuscript style, such as Fig.~\\ref{...} versus Figure~\\ref{...}, and keep it consistent.")
    for object_type, object_issues in sorted(issues.items()):
        print(f"  {object_type}:")
        for issue in object_issues[:limit]:
            print(f"    {issue}")
        remaining = len(object_issues) - limit
        if remaining > 0:
            print(f"    ... {remaining} more")
    return False


def report_dash_style_advisory(polished_text: str, limit: int) -> None:
    """Report dash-heavy prose as an optional style advisory.

    Dash style is intentionally excluded from preservation pass/fail because it does
    not indicate whether protected scientific or TeX content was preserved.
    """
    issues = collect_prohibited_dashes(polished_text)
    if not issues:
        print("Dash style advisory: no em-length prose dashes detected")
        return

    print("Dash style advisory: review em-length prose dashes if the target style disfavors them")
    for line_number, token, context in issues[:limit]:
        print(f"    line {line_number}: {token!r} in {context}")
    remaining = len(issues) - limit
    if remaining > 0:
        print(f"    ... {remaining} more")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_static_includes(
    text: str, source_path: Path
) -> tuple[list[IncludeDirective], list[ProjectLoadIssue]]:
    """Collect statically resolvable include directives from active TeX."""
    active = mask_inactive_tex(text)
    directives: list[IncludeDirective] = []
    issues: list[ProjectLoadIssue] = []
    for start_match in INCLUDE_COMMAND_START_RE.finditer(active):
        if is_escaped(active, start_match.start()):
            continue
        command = start_match.group("command")
        if command in IMPORT_COMMANDS:
            match = IMPORT_COMMAND_RE.match(active, start_match.start())
        else:
            match = INCLUDE_COMMAND_RE.match(active, start_match.start())
        line_number = text.count("\n", 0, start_match.start()) + 1
        if match is None:
            issues.append(
                ProjectLoadIssue(
                    source_path,
                    line_number,
                    f"dynamic or malformed \\{start_match.group('command')} cannot be resolved",
                )
            )
            continue
        if command in IMPORT_COMMANDS:
            directory = (match.group("directory") or "").strip()
            filename = (match.group("filename") or "").strip()
            invalid_parts = not filename
            dynamic_parts = bool(re.search(r"[\\#$]", directory + filename))
            raw_path = f"{directory}{filename}"
        else:
            directory = None
            raw_path = (
                match.group("braced") or match.group("unbraced") or ""
            ).strip()
            invalid_parts = not raw_path
            dynamic_parts = bool(re.search(r"[\\#$]", raw_path))
        if invalid_parts or dynamic_parts:
            issues.append(
                ProjectLoadIssue(
                    source_path,
                    line_number,
                    f"dynamic or empty \\{command} target {raw_path!r}",
                )
            )
            continue
        directives.append(
            IncludeDirective(
                start=match.start(),
                end=match.end(),
                command=command,
                target=filename if command in IMPORT_COMMANDS else raw_path,
                line_number=line_number,
                directory=directory,
            )
        )
    return directives, issues


def with_optional_tex_suffix(path: Path) -> list[Path]:
    """Return TeX's common explicit/implicit-extension candidates."""
    variants = [path] if path.suffix else [path, path.with_suffix(".tex")]
    candidates: list[Path] = []
    for variant in variants:
        resolved = variant.resolve()
        if resolved not in candidates:
            candidates.append(resolved)
    return candidates


def include_path_candidates(
    directive: IncludeDirective,
    project_root: Path,
    including_file: Path,
    import_bases: tuple[Path, ...],
) -> tuple[list[Path], tuple[Path, ...]]:
    """Resolve a directive using ordinary TeX and import-package lookup rules."""
    target = Path(directive.target)

    def with_current_base(base: Path) -> tuple[Path, ...]:
        resolved = base.resolve()
        return (resolved, *(item for item in import_bases if item != resolved))

    if directive.command in IMPORT_COMMANDS:
        assert directive.directory is not None
        directory = Path(directive.directory)
        if directory.is_absolute():
            import_base = directory.resolve()
        elif directive.command in RESET_IMPORT_COMMANDS:
            import_base = (project_root / directory).resolve()
        else:
            import_base = ((import_bases[0] if import_bases else project_root) / directory).resolve()
        if target.is_absolute():
            candidates = with_optional_tex_suffix(target)
        else:
            candidate_bases = [import_base]
            if directive.command in RELATIVE_IMPORT_COMMANDS:
                candidate_bases.extend(import_bases)
                candidate_bases.append(project_root)
            candidates = []
            for base in candidate_bases:
                for candidate in with_optional_tex_suffix(base / target):
                    if candidate not in candidates:
                        candidates.append(candidate)
        return candidates, with_current_base(import_base)

    if directive.command in {"subfile", "subfileinclude"}:
        if target.is_absolute():
            candidates = with_optional_tex_suffix(target)
            child_base = target.parent.resolve()
        else:
            base = import_bases[0] if import_bases else project_root
            child_base = (base / target.parent).resolve()
            candidate_bases = [child_base, *import_bases, project_root]
            candidates = []
            for candidate_base in candidate_bases:
                for candidate in with_optional_tex_suffix(
                    candidate_base / target.name
                ):
                    if candidate not in candidates:
                        candidates.append(candidate)
        return candidates, with_current_base(child_base)

    if target.is_absolute():
        return with_optional_tex_suffix(target), import_bases

    bases: list[Path] = [*import_bases, project_root, including_file.parent]
    candidates: list[Path] = []
    for base in bases:
        for candidate in with_optional_tex_suffix(base / target):
            if candidate not in candidates:
                candidates.append(candidate)
    return candidates, import_bases


def load_tex_project(root_path: Path) -> tuple[str, list[ProjectLoadIssue]]:
    """Inline supported static include/import content in TeX document order."""
    root_path = root_path.resolve()
    project_root = root_path.parent
    issues: list[ProjectLoadIssue] = []

    def expand(
        path: Path,
        stack: tuple[Path, ...],
        import_bases: tuple[Path, ...],
    ) -> str:
        resolved_path = path.resolve()
        if resolved_path in stack:
            cycle = " -> ".join(item.name for item in (*stack, resolved_path))
            issues.append(ProjectLoadIssue(resolved_path, 1, f"cyclic include: {cycle}"))
            return ""
        try:
            text = read_text(resolved_path)
        except OSError as exc:
            issues.append(ProjectLoadIssue(resolved_path, 1, f"cannot read file: {exc}"))
            return ""

        directives, directive_issues = collect_static_includes(text, resolved_path)
        issues.extend(directive_issues)
        chunks: list[str] = []
        cursor = 0
        next_stack = (*stack, resolved_path)
        for directive in directives:
            chunks.append(text[cursor : directive.end])
            candidates, child_import_bases = include_path_candidates(
                directive,
                project_root,
                resolved_path,
                import_bases,
            )
            target = next((candidate for candidate in candidates if candidate.is_file()), None)
            if target is None:
                attempted = ", ".join(str(candidate) for candidate in candidates)
                raw_target = (
                    f"{directive.directory}{directive.target}"
                    if directive.directory is not None
                    else directive.target
                )
                issues.append(
                    ProjectLoadIssue(
                        resolved_path,
                        directive.line_number,
                        f"missing \\{directive.command} target {raw_target!r}; tried {attempted}",
                    )
                )
            else:
                chunks.append("\n")
                chunks.append(expand(target, next_stack, child_import_bases))
                chunks.append("\n")
            cursor = directive.end
        chunks.append(text[cursor:])
        return "".join(chunks)

    return expand(root_path, (), ()), issues


def print_project_issues(
    title: str, issues: list[ProjectLoadIssue], limit: int
) -> None:
    if not issues:
        return
    print(title)
    for issue in issues[:limit]:
        print(f"  {issue.path}:{issue.line_number}: {issue.message}")
    if len(issues) > limit:
        print(f"  ... {len(issues) - limit} more")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check TeX preservation and hard polishing constraints."
    )
    parser.add_argument(
        "original", type=Path, help="Original or author-approved baseline TeX file"
    )
    parser.add_argument(
        "polished", type=Path, help="Candidate or normalization-result TeX file"
    )
    parser.add_argument("--limit", type=int, default=20, help="Maximum issues to print per category")
    parser.add_argument(
        "--allow-additions",
        action="store_true",
        help=(
            "Allow ordinary prose additions only. Protected TeX structures and math remain exact; numeric values and "
            "recognized unit, currency, sign, and marker tokens in supported anchored, connected, delimited, or cue "
            "contexts remain exact and in order. Other contexts require manual source comparison. Recognized comments "
            "and literal/code regions are exact protected source in "
            "every mode; custom unrecognized literal macros require manual comparison. Retained for workflow "
            "compatibility."
        ),
    )
    parser.add_argument(
        "--reader-oriented",
        action="store_true",
        help=(
            "Reader-oriented polishing mode: preserve recognized numeric values/units/signs as a multiset rather than "
            "requiring document order. Use only after manual verification that moved numerical statements retain the "
            "same metric, condition, dataset, and comparison."
        ),
    )
    parser.add_argument(
        "--style-check",
        action="store_true",
        help=(
            "Run optional advisory-only style checks. Currently this surfaces em-length dash punctuation in prose. "
            "Style advisories never affect preservation pass/fail."
        ),
    )
    parser.add_argument(
        "--allow-structural-reorder",
        action="store_true",
        help=(
            "Compare citations, cross-references, and protected arguments as a multiset rather than an ordered "
            "sequence. Use only when sentences or clauses containing \\cite/\\ref were deliberately reordered during "
            "reader-oriented polishing. Counts and keys remain exact, but semantic claim-citation attachment is not "
            "verified and must be checked manually."
        ),
    )
    parser.add_argument(
        "--approved-symbol-map",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help=(
            "Authorize an exact global math-symbol substitution. Repeat for multiple mappings. "
            "This enters normalization-only mode, rejects unambiguous numeric, currency, percentage, and sign mappings, "
            "never authorizes unit changes, and permits no other prose or protected change."
        ),
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help=(
            "Treat each positional file as a root TeX file and recursively compare statically resolvable "
            "\\input/\\include/\\subfile/\\subfileinclude and import-family content."
        ),
    )
    args = parser.parse_args()

    if args.allow_additions and args.approved_symbol_map:
        parser.error("--allow-additions cannot be combined with --approved-symbol-map")
    if args.reader_oriented and args.approved_symbol_map:
        parser.error("--reader-oriented cannot be combined with --approved-symbol-map")
    if args.allow_structural_reorder and args.approved_symbol_map:
        parser.error(
            "--allow-structural-reorder cannot be combined with --approved-symbol-map"
        )
    try:
        approved_symbol_maps = parse_approved_symbol_maps(args.approved_symbol_map)
    except ValueError as exc:
        parser.error(str(exc))

    try:
        if args.project:
            original_text, original_project_issues = load_tex_project(args.original)
            polished_text, polished_project_issues = load_tex_project(args.polished)
        else:
            original_text = read_text(args.original)
            polished_text = read_text(args.polished)
            original_project_issues = []
            polished_project_issues = []
    except OSError as exc:
        print(f"Error reading input files: {exc}", file=sys.stderr)
        return 2

    project_pass = not original_project_issues and not polished_project_issues
    if args.project:
        print(f"Project traversal: {'PASS' if project_pass else 'FAIL'}")
        print_project_issues("Original project issues:", original_project_issues, args.limit)
        print_project_issues("Candidate project issues:", polished_project_issues, args.limit)

    if args.allow_additions:
        print(
            "Additions mode: ordinary prose may be added; protected TeX, math, and numeric content remains strict."
        )
    if args.reader_oriented:
        print(
            "Reader-oriented mode: numeric occurrence order is relaxed, but values/units/signs remain strict."
        )

    if args.allow_structural_reorder:
        print(
            "Structural reorder mode: citation and cross-reference order is relaxed, but keys and counts remain "
            "strict. Semantic claim attachment is not machine-verified; review it manually."
        )

    structures_pass = check_structural_preservation(
        original_text, polished_text, args.limit, allow_reordering=args.allow_structural_reorder
    )
    math_pass = check_math_preservation(
        original_text,
        polished_text,
        args.limit,
        args.allow_additions,
        approved_symbol_maps,
    )
    numbers_pass = check_numeric_preservation(
        original_text, polished_text, args.limit, allow_reordering=args.reader_oriented
    )

    normalization_text_pass = True
    if approved_symbol_maps:
        normalization_text_pass = (
            normalized_nonmath_skeleton(original_text)
            == normalized_nonmath_skeleton(polished_text)
        )
        print(
            "Normalization-only non-math content: "
            f"{'PASS' if normalization_text_pass else 'FAIL'}"
        )
        if not normalization_text_pass:
            print("  Non-math prose or structure changed outside the approved symbol mapping.")
        print("Intrinsic polishing-style checks: NOT APPLIED (normalization-only mode)")
        placeholder_pass = True
        numbering_pass = True
        reference_style_pass = True
    else:
        placeholder_pass = check_placeholder_reference_keys(polished_text, args.limit)
        numbering_pass = check_hardcoded_display_numbering(polished_text, args.limit)
        reference_style_pass = check_reference_name_style(
            original_text, polished_text, args.limit
        )
        if args.style_check:
            report_dash_style_advisory(polished_text, args.limit)

    return (
        0
        if project_pass
        and structures_pass
        and placeholder_pass
        and numbering_pass
        and reference_style_pass
        and math_pass
        and numbers_pass
        and normalization_text_pass
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
