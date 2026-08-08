#!/usr/bin/env python3
"""
verify_numbers.py -- cross-check the MaestroRAG paper's quantitative claims against
data/MaestroRAGResults.xlsx, and inventory every numeric literal in the active .tex
files so nothing goes unexamined.

Sources of truth, and nothing else:
  * the .tex files reached from main.tex   (listed in tools/checks.yaml: tex_sources)
  * data/MaestroRAGResults.xlsx, restricted to the authorised tabs

The tabs `Encode`, `Retrieval` and `Comparison` are STALE.  They are never read for
evidence.  They ARE scanned separately, for one purpose only: if a number printed in
the paper matches a value that lives exclusively in a stale tab, the report says so.

Nothing here estimates, infers, or fills a gap.  A value that cannot be established
from the workbook is reported UNVERIFIABLE, never guessed.

Deliberately dependency-free: stdlib only, so the harness runs anywhere the paper does.
PyYAML is used when present; otherwise a built-in parser handles the YAML subset that
tools/checks.yaml is written in.

Usage:
    python3 tools/verify_numbers.py                 # write reports/verify_numbers.md
    python3 tools/verify_numbers.py --strict        # ...and exit 1 if any check DRIFTs
    python3 tools/verify_numbers.py -o other.md     # write somewhere else

Exit codes:
    0  report written; observed statuses all match their declared `expect`
    1  --strict and at least one check drifted from its declared `expect`
    2  the run could not be completed (missing workbook, unreadable config, bad cell ref)

A check in FAIL state is data, not an error.  Each one is a known defect recorded with
its `expect: FAIL` anchor and a `known_defect` note, waiting on its own task.  The point
of the anchor is that a later edit which changes the status -- in either direction --
shows up as DRIFT rather than sliding by unnoticed.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = os.path.join(REPO_ROOT, "tools", "checks.yaml")
DEFAULT_REPORT = os.path.join(REPO_ROOT, "reports", "verify_numbers.md")

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


class Problem(Exception):
    """An infrastructure failure that stops the run. Never used for a failing check."""


# --------------------------------------------------------------------------- YAML
# tools/checks.yaml sticks to a small, unambiguous YAML subset: block mappings, block
# sequences, flow lists/maps on one line, and scalars. That is all this parser handles;
# anything outside the subset raises rather than being silently misread.

def _parse_scalar(text: str):
    t = text.strip()
    if not t:
        return None
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    if t in ("null", "~", "None"):
        return None
    if t == "true":
        return True
    if t == "false":
        return False
    if t.startswith("[") and t.endswith("]"):
        return [_parse_scalar(p) for p in _split_flow(t[1:-1])] if t[1:-1].strip() else []
    if t.startswith("{") and t.endswith("}"):
        out = {}
        for part in _split_flow(t[1:-1]):
            if not part.strip():
                continue
            k, _, v = part.partition(":")
            out[_parse_scalar(k)] = _parse_scalar(v)
        return out
    try:
        return int(t)
    except ValueError:
        pass
    try:
        return float(t)
    except ValueError:
        pass
    return t


def _split_flow(text: str):
    """Split a flow collection body on commas that are not inside quotes or brackets."""
    parts, buf, depth, quote = [], [], 0, None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "[{":
            depth += 1
            buf.append(ch)
        elif ch in "]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def _strip_comment(line: str) -> str:
    """Remove a trailing '#' comment, respecting quotes."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _mini_yaml(text: str):
    lines = []
    for raw in text.splitlines():
        stripped = _strip_comment(raw).rstrip()
        if stripped.strip():
            lines.append((len(stripped) - len(stripped.lstrip()), stripped.strip()))

    pos = [0]

    def parse_block(indent: int):
        if pos[0] >= len(lines):
            return None
        if lines[pos[0]][1].startswith("- "):
            return parse_seq(indent)
        return parse_map(indent)

    def parse_seq(indent: int):
        items = []
        while pos[0] < len(lines):
            ind, content = lines[pos[0]]
            if ind < indent or not content.startswith("- "):
                break
            body = content[2:].strip()
            pos[0] += 1
            if ":" in body and not body.startswith(("[", "{", '"', "'")):
                # A mapping opened on the dash line; its remaining keys follow, indented.
                key, _, rest = body.partition(":")
                item = {}
                _absorb(item, key.strip(), rest.strip(), ind + 2)
                nxt = ind + 2
                while pos[0] < len(lines) and lines[pos[0]][0] >= nxt and not lines[pos[0]][1].startswith("- "):
                    k2, _, r2 = lines[pos[0]][1].partition(":")
                    kind = lines[pos[0]][0]
                    pos[0] += 1
                    _absorb(item, k2.strip(), r2.strip(), kind)
                items.append(item)
            else:
                items.append(_parse_scalar(body))
        return items

    def parse_map(indent: int):
        out = {}
        while pos[0] < len(lines):
            ind, content = lines[pos[0]]
            if ind < indent or content.startswith("- "):
                break
            key, _, rest = content.partition(":")
            pos[0] += 1
            _absorb(out, key.strip(), rest.strip(), ind)
        return out

    def _absorb(target: dict, key: str, rest: str, indent: int):
        if rest:
            target[key] = _parse_scalar(rest)
        elif pos[0] < len(lines) and lines[pos[0]][0] > indent:
            target[key] = parse_block(lines[pos[0]][0])
        else:
            target[key] = None

    result = parse_block(0)
    if pos[0] != len(lines):
        raise Problem(
            "checks.yaml uses YAML beyond the supported subset "
            f"(stopped at line {pos[0] + 1}: {lines[pos[0]][1]!r}). "
            "Install PyYAML or simplify the file."
        )
    return result


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        import yaml  # noqa: PLC0415 -- optional, preferred when available
        return yaml.safe_load(text)
    except ImportError:
        return _mini_yaml(text)


# ---------------------------------------------------------------------------- XLSX

class Workbook:
    """Minimal read-only .xlsx reader: sheet names, cell values, cached formula results."""

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise Problem(f"workbook not found: {path}")
        self.path = path
        self.sha256 = hashlib.sha256(open(path, "rb").read()).hexdigest()
        self._zip = zipfile.ZipFile(path)
        self._shared = self._read_shared_strings()
        self._targets = self._read_sheet_index()
        self._cache: dict[str, dict[str, object]] = {}

    @property
    def sheet_names(self):
        return list(self._targets)

    def _read_shared_strings(self):
        name = "xl/sharedStrings.xml"
        if name not in self._zip.namelist():
            return []
        root = ET.fromstring(self._zip.read(name))
        return ["".join(t.text or "" for t in si.iter(f"{{{NS_MAIN}}}t"))
                for si in root.findall(f"{{{NS_MAIN}}}si")]

    def _read_sheet_index(self):
        book = ET.fromstring(self._zip.read("xl/workbook.xml"))
        rels = ET.fromstring(self._zip.read("xl/_rels/workbook.xml.rels"))
        relmap = {r.get("Id"): r.get("Target") for r in rels}
        out = {}
        for sheet in book.find(f"{{{NS_MAIN}}}sheets"):
            target = relmap[sheet.get(f"{{{NS_REL}}}id")]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            out[sheet.get("name")] = target
        return out

    def grid(self, sheet: str) -> dict:
        """All populated cells of one sheet, keyed by A1 reference."""
        if sheet in self._cache:
            return self._cache[sheet]
        if sheet not in self._targets:
            raise Problem(f"sheet {sheet!r} is not in {os.path.basename(self.path)}")
        root = ET.fromstring(self._zip.read(self._targets[sheet]))
        cells = {}
        for cell in root.iter(f"{{{NS_MAIN}}}c"):
            ref, ctype = cell.get("r"), cell.get("t")
            v = cell.find(f"{{{NS_MAIN}}}v")
            inline = cell.find(f"{{{NS_MAIN}}}is")
            if ctype == "s" and v is not None:
                value = self._shared[int(v.text)]
            elif ctype == "inlineStr" and inline is not None:
                value = "".join(t.text or "" for t in inline.iter(f"{{{NS_MAIN}}}t"))
            elif ctype == "e" and v is not None:
                value = v.text                     # spreadsheet error, e.g. #DIV/0!
            elif v is not None:
                try:
                    value = float(v.text)
                except (TypeError, ValueError):
                    value = v.text
            else:
                continue
            cells[ref] = value
        self._cache[sheet] = cells
        return cells

    def cell(self, sheet: str, ref: str):
        return self.grid(sheet).get(ref)

    def numeric_values(self, sheet: str):
        return [v for v in self.grid(sheet).values() if isinstance(v, float)]


# ----------------------------------------------------------------- tex literal scan
# Numbers that are pure typesetting -- column widths, vspace, float placement, cite keys
# -- are masked out before extraction. What remains is classified so the "not covered by
# any check" list stays about claims rather than about \vspace{-10pt}.

_MASKS = [
    r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{[^}]*\}",
    r"\\(?:label|ref|Cref|cref|autoref|eqref|nameref|pageref)\s*\{[^}]*\}",
    r"\\cite[tp]?\*?\s*(?:\[[^\]]*\])?\s*\{[^}]*\}",
    r"\\(?:input|include|bibliography|bibliographystyle|usepackage|documentclass)\s*(?:\[[^\]]*\])?\s*\{[^}]*\}",
    r"\\(?:url|href)\s*\{[^}]*\}(?:\s*\{[^}]*\})?",
    r"\\(?:vspace|hspace|vskip|hskip|smallskip|medskip|bigskip)\s*\*?\s*\{[^}]*\}",
    r"\\(?:setlength|addtolength|settowidth|resizebox|scalebox|rotatebox)\s*(?:\{[^}]*\}\s*){1,2}",
    r"\\(?:cmidrule|midrule|toprule|bottomrule)\s*(?:\([^)]*\))?\s*(?:\{[^}]*\})?",
    r"\\(?:multicolumn|multirow)\s*\{[^}]*\}",
    r"\\(?:renewcommand|newcommand|providecommand)\s*\{[^}]*\}\s*(?:\[[^\]]*\])?",
    r"\\begin\s*\{[^}]*\}\s*(?:\[[^\]]*\])?",
    r"\\end\s*\{[^}]*\}",
    r"\\subfloat\s*\[[^\]]*\]",
    r"\\cellcolor\s*\{[^}]*\}",
    r"\\arraystretch|\\tabcolsep|\\linewidth|\\textwidth|\\columnwidth",
    # bare dimensions: 0.32\linewidth, -10pt, 0.9\linewidth, 5pt
    r"[-+]?\d*\.?\d+\s*(?:pt|cm|mm|in|em|ex|bp|sp|pc|dd|cc)\b",
    r"[-+]?\d*\.?\d+\s*\\(?:linewidth|textwidth|columnwidth|baselineskip|height|width)",
]
_MASK_RE = re.compile("|".join(_MASKS))
# Comma-grouped forms (6,000) are matched whole so they are not split into 6 and 000.
# The `-` in the lookbehind keeps the second half of an en-dash range ("2--16") from
# being read as the negative number -16.
_NUM_RE = re.compile(
    r"(?<![\w.\-])[-+]?\d{1,3}(?:,\d{3})+(?![\w.])"
    r"|(?<![\w.\-])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w.])"
)

# Every literal is reported; these patterns only decide which bucket it lands in, so the
# "uncovered" list stays about claims rather than about model numbers and list markers.
_CONFIG_RE = re.compile(
    r"(?:BS|DB|TTL|top-?k|k|batch\s+size|database\s+size|DB\s+size|#\s*cores?|"
    r"cache\s+(?:size|capacity)|number\s+of\s+(?:CPU\s+)?cores?|"
    r"(?:allocating|assigns?|assigning|uses?|use|using|upto|up\s+to)\s*)"
    r"(?:\s*(?:=|of|is|to|:))?\s*(?:\\texttt\{)?\s*$",
    re.IGNORECASE,
)
# NOTE: percentages are deliberately absent here. "16.45\%" is a claim, not a setup
# constant, and must stay in the `claim` bucket where checks and the stale scan see it.
_UNIT_RE = re.compile(
    r"^\s*(?:\\[,;: ])?\s*(?:W\b|GB\b|MB\b|KB\b|TB\b|Hz\b|mil\b|M\b|B\b|"
    r"cores?\b|bit\b|nm\b|ms\b|QPS\b|queries\b|entries\b|lines\b)",
    re.IGNORECASE,
)
# Hardware model numbers: RTX 4090, i9-14900K, Llama-3.1-8B, OPT 2.7B, e5-base-v2, A100.
_HARDWARE_RE = re.compile(
    r"(?:RTX|GTX|i[3579]-?|Xeon|A100|H100|Orin|AGX|Llama-?|LLaMA-?|OPT|e5-base-v|"
    r"Cortex-?|DDR|LPDDR|GDDR|HBM|PCIe|Ampere|Ada)"
    # allow LaTeX spacing and grouping between the model name and its number:
    # \mbox{RTX\,4090}, RTX~4090, Llama-3.1-8B
    r"(?:[-\w~]|\\[,;:!> ]|\s|\{|\})*$",
    re.IGNORECASE,
)
# List markers: "(1)", "(2)" and "(i)"-style enumerations.
_ENUM_RE = re.compile(r"\($")
_ENUM_AFTER_RE = re.compile(r"^\)")


def strip_tex_comment(line: str) -> str:
    """Everything from the first unescaped % onward is a LaTeX comment."""
    out = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if ch == "%":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def extract_literals(paths):
    """Yield every numeric literal in the given .tex files, with provenance."""
    literals, commented_count = [], 0
    for rel in paths:
        full = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(full):
            raise Problem(f"tex source listed in checks.yaml does not exist: {rel}")
        with open(full, encoding="utf-8", errors="replace") as fh:
            for lineno, raw in enumerate(fh, 1):
                live = strip_tex_comment(raw)
                commented_count += len(_NUM_RE.findall(raw)) - len(_NUM_RE.findall(live))
                if not live.strip():
                    continue
                # Blank out formatting constructs, preserving offsets.
                masked = _MASK_RE.sub(lambda m: " " * len(m.group(0)), live)
                for m in _NUM_RE.finditer(masked):
                    before = masked[max(0, m.start() - 40):m.start()]
                    after = masked[m.end():m.end() + 12]
                    if _HARDWARE_RE.search(before):
                        category = "hardware"
                    elif _ENUM_RE.search(before) and _ENUM_AFTER_RE.match(after):
                        category = "enumerator"
                    elif _CONFIG_RE.search(before):
                        category = "config"
                    elif _UNIT_RE.match(after):
                        category = "setup"
                    else:
                        category = "claim"
                    literals.append({
                        "file": rel,
                        "line": lineno,
                        "text": m.group(0),
                        "value": float(m.group(0).replace(",", "")),
                        "category": category,
                        "context": live.strip()[:160],
                    })
    return literals, commented_count


# ------------------------------------------------------------------- check engine

_SAFE_EVAL_GLOBALS = {"__builtins__": {}, "abs": abs, "max": max, "min": min, "sum": sum}


def resolve_cells(wb: Workbook, sheet: str, cells: dict):
    """Fetch each named cell. Returns (values, missing) where missing lists non-numerics."""
    values, missing = {}, []
    for name, ref in (cells or {}).items():
        raw = wb.cell(sheet, ref)
        if isinstance(raw, float):
            values[name] = raw
        else:
            missing.append((name, ref, raw))
    return values, missing


def tex_source_value(source: dict):
    """Pull one number out of a .tex file with an anchored regex.

    Used for paper-internal consistency: a value quoted in prose against the same
    value printed in a table, where no workbook cell backs either side. The regex is
    anchored on row content rather than a line number so it survives the file moving.
    """
    path = os.path.join(REPO_ROOT, source["file"])
    if not os.path.exists(path):
        return None, f"tex source not found: {source['file']}"
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    matches = re.findall(source["regex"], text)
    if not matches:
        return None, f"regex matched nothing in {source['file']}"
    if len(matches) > 1:
        return None, f"regex matched {len(matches)} times in {source['file']}; must be unique"
    try:
        return float(matches[0]), None
    except (TypeError, ValueError):
        return None, f"captured {matches[0]!r}, which is not a number"


def evaluate(check: dict, wb: Workbook):
    """Return (status, expected, delta, detail)."""
    kind = check.get("kind", "value")
    tol = float(check.get("tolerance") or 0.0)

    if kind == "unverifiable":
        return "UNVERIFIABLE", None, None, check.get("reason", "no workbook backing")

    source = check.get("source") or {}

    if source.get("file"):
        expected, err = tex_source_value(source)
        if err:
            return "UNVERIFIABLE", None, None, err
        claimed = float(check["claimed"])
        delta = claimed - expected
        ok = abs(delta) <= tol + 1e-12
        return ("PASS" if ok else "FAIL"), expected, delta, (
            f"prose {claimed:g} vs {source['file']} {expected:.6g}; "
            f"|delta| = {abs(delta):.6g} vs tolerance {tol:g}"
        )

    sheet, cells = source.get("sheet"), source.get("cells")
    if not sheet:
        return "UNVERIFIABLE", None, None, "no workbook source declared"

    values, missing = resolve_cells(wb, sheet, cells)

    if kind == "absent":
        name, ref = next(iter((cells or {}).items()))
        raw = wb.cell(sheet, ref)
        if isinstance(raw, float):
            return "FAIL", raw, None, f"{sheet}!{ref} holds a number ({raw}); expected none"
        shown = "empty" if raw is None else repr(raw)
        return "PASS", None, None, f"{sheet}!{ref} is {shown}, as expected"

    if missing:
        detail = "; ".join(
            f"{sheet}!{ref} is {'empty' if raw is None else repr(raw)}" for _, ref, raw in missing
        )
        return "UNVERIFIABLE", None, None, f"cell(s) not numeric: {detail}"

    try:
        expected = eval(source["derivation"], dict(_SAFE_EVAL_GLOBALS), dict(values))  # noqa: S307
    except Exception as exc:  # noqa: BLE001
        return "UNVERIFIABLE", None, None, f"derivation failed: {exc}"

    if kind == "range":
        lo, hi = check["claimed"]
        vals = list(expected)
        outside = [v for v in vals if not (lo - tol <= v <= hi + tol)]
        rendered = ", ".join(f"{v:.4g}" for v in vals)
        if outside:
            return ("FAIL", vals, None,
                    f"derived [{rendered}]; {len(outside)} of {len(vals)} fall outside {lo}-{hi}")
        return "PASS", vals, None, f"derived [{rendered}], all within {lo}-{hi}"

    claimed = float(check["claimed"])
    expected = float(expected)

    if kind == "at_least":
        ok = expected >= claimed - tol
        delta = expected - claimed
        return ("PASS" if ok else "FAIL"), expected, delta, (
            f"floor claim {claimed:g}; workbook gives {expected:.6g}"
        )

    delta = claimed - expected
    ok = abs(delta) <= tol + 1e-12
    return ("PASS" if ok else "FAIL"), expected, delta, (
        f"|{claimed:g} - {expected:.6g}| = {abs(delta):.6g} vs tolerance {tol:g}"
    )


# ------------------------------------------------------------------ stale-tab scan

def stale_only_matches(literals, wb: Workbook, allowed, stale, rel_tol=1e-6):
    """Paper literals whose value appears in a stale tab and in no authorised tab."""
    allowed_vals, stale_vals = set(), {}
    for name in allowed:
        for v in wb.numeric_values(name):
            allowed_vals.add(round(v, 6))
    for name in stale:
        if name not in wb.sheet_names:
            continue
        for ref, v in wb.grid(name).items():
            if isinstance(v, float):
                stale_vals.setdefault(round(v, 6), []).append(f"{name}!{ref}")

    # Scanned across every category except the two that can never carry a measurement,
    # so the warning does not depend on the literal classifier getting a bucket right.
    hits = []
    for lit in literals:
        if lit["category"] in ("enumerator", "hardware"):
            continue
        key = round(lit["value"], 6)
        if key in stale_vals and key not in allowed_vals:
            hits.append((lit, stale_vals[key][:4]))
    return hits


# ------------------------------------------------------------------------- report

def covered_keys(checks):
    """(file, line, value) triples that some check accounts for."""
    keys = set()
    for chk in checks:
        claimed = chk.get("claimed")
        for loc in chk.get("locations") or []:
            fname, _, line = loc.rpartition(":")
            if isinstance(claimed, (int, float)):
                keys.add((fname, int(line), round(float(claimed), 6)))
            elif isinstance(claimed, list):
                for c in claimed:
                    keys.add((fname, int(line), round(float(c), 6)))
    return keys


def fmt(value, places=6):
    if value is None:
        return "--"
    if isinstance(value, list):
        return "[" + ", ".join(f"{v:.4g}" for v in value) + "]"
    if isinstance(value, float):
        if value == int(value) and abs(value) < 1e15:
            return f"{int(value)}"
        return f"{value:.{places}g}"
    return str(value)


def build_report(cfg, wb, results, literals, uncovered, stale_hits, commented_count, drifts):
    allowed = cfg["tabs"]["allowed"]
    stale = cfg["tabs"]["stale"]
    unlisted = cfg["tabs"].get("unlisted") or []
    tally = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in results:
        tally[r["status"]] += 1

    L = []
    add = L.append
    add("# Numeric verification report")
    add("")
    add("Generated by `tools/verify_numbers.py` from `tools/checks.yaml`.")
    add("This report asserts nothing that is not in a source of truth. Where the workbook")
    add("cannot settle a claim, the row says UNVERIFIABLE rather than offering an estimate.")
    add("")
    add("## Inputs")
    add("")
    add(f"- **Workbook:** `{cfg['workbook']}`")
    add(f"- **SHA-256:** `{wb.sha256}`")
    add(f"- **Tabs read (authorised, {len(allowed)}):** " + ", ".join(f"`{t}`" for t in allowed))
    add(f"- **Tabs deliberately NOT read (stale, {len(stale)}):** " + ", ".join(f"`{t}`" for t in stale))
    add("  These three tabs are excluded from all evidence. They are scanned only to detect")
    add("  paper numbers that match a stale tab and nothing authoritative (see below).")
    if unlisted:
        add(f"- **Tabs outside the authorised set (neither read nor scanned):** " + ", ".join(f"`{t}`" for t in unlisted))
    missing_tabs = [t for t in allowed if t not in wb.sheet_names]
    if missing_tabs:
        add(f"- **WARNING -- authorised tabs absent from the workbook:** " + ", ".join(f"`{t}`" for t in missing_tabs))
    add(f"- **`.tex` sources scanned ({len(cfg['tex_sources'])}):** " + ", ".join(f"`{t}`" for t in cfg["tex_sources"]))
    add("")
    add("## Tally")
    add("")
    add(f"| PASS | FAIL | UNVERIFIABLE | total | drifted from `expect` |")
    add("|---:|---:|---:|---:|---:|")
    add(f"| {tally['PASS']} | {tally['FAIL']} | {tally['UNVERIFIABLE']} | {len(results)} | {len(drifts)} |")
    add("")
    if drifts:
        add("> **DRIFT DETECTED.** The listed checks no longer hold the status recorded in")
        add("> `checks.yaml`. Either the paper/workbook changed, or an anchor is stale.")
        add("")
        for d in drifts:
            add(f"> - `{d['id']}`: expected **{d['expect']}**, observed **{d['status']}**")
        add("")
    else:
        add("Every check holds the status recorded in `checks.yaml` -- no drift.")
        add("")

    add("## Checks")
    add("")
    add("`Claimed` is what the paper (or the named figure) states. `Workbook` is what the")
    add("cited cells give. Rows marked FAIL are known, unfixed defects, each awaiting its")
    add("own task; they are recorded here, not repaired.")
    add("")
    add("| Status | ID | Claimed | Workbook | Δ | Tol | Source | Where claimed |")
    add("|---|---|---:|---:|---:|---:|---|---|")
    order = {"FAIL": 0, "UNVERIFIABLE": 1, "PASS": 2}
    for r in sorted(results, key=lambda x: (order[x["status"]], x["id"])):
        chk = r["check"]
        src = chk.get("source") or {}
        if src.get("sheet"):
            refs = ", ".join(f"{src['sheet']}!{ref}" for ref in (src.get("cells") or {}).values())
            deriv = src.get("derivation", "")
            source_txt = f"`{refs}`" + (f"<br/>`{deriv}`" if deriv and deriv not in (src.get("cells") or {}) else "")
        elif src.get("file"):
            source_txt = f"`{src['file']}`" + (f"<br/>_{src['note']}_" if src.get("note") else "")
        else:
            source_txt = "_no workbook source_"
        where = ", ".join(f"`{loc}`" for loc in (chk.get("locations") or [])) or (
            f"_{chk['figure_only']}_" if chk.get("figure_only") else "_--_")
        badge = {"PASS": "PASS", "FAIL": "**FAIL**", "UNVERIFIABLE": "_UNVERIF_"}[r["status"]]
        add(f"| {badge} | `{chk['id']}` | {fmt(chk.get('claimed'))} | {fmt(r['expected'])} | "
            f"{fmt(r['delta'])} | {fmt(chk.get('tolerance'))} | {source_txt} | {where} |")
    add("")

    add("### Detail")
    add("")
    for r in sorted(results, key=lambda x: (order[x["status"]], x["id"])):
        chk = r["check"]
        add(f"**`{chk['id']}`** -- {r['status']} ({chk.get('origin', 'seed')})  ")
        add(f"{chk.get('description', '')}  ")
        add(f"{r['detail']}  ")
        if chk.get("tolerance_rationale"):
            add(f"_Tolerance:_ {chk['tolerance_rationale']}  ")
        if chk.get("known_defect"):
            add(f"_Known defect:_ {chk['known_defect']}  ")
        if chk.get("reason"):
            add(f"_Why unverifiable:_ {chk['reason']}  ")
        add("")

    add("## Stale-tab warnings")
    add("")
    if stale_hits:
        add("These numbers appear in the paper and match a value found **only** in a stale tab")
        add("(`Encode`, `Retrieval`, `Comparison`). Nothing authoritative supports them.")
        add("")
        add("| Literal | Category | Location | Stale cell(s) | Context |")
        add("|---:|---|---|---|---|")
        for lit, refs in stale_hits:
            ctx = lit["context"].replace("|", "\\|")[:90]
            add(f"| {lit['text']} | `{lit['category']}` | `{lit['file']}:{lit['line']}` | " +
                ", ".join(f"`{r}`" for r in refs) + f" | {ctx} |")
    else:
        add("None. No paper literal matches a stale-tab value that is absent from every")
        add("authorised tab.")
    add("")

    add("## Numeric literals not covered by any check")
    add("")
    by_cat = {}
    for lit in uncovered:
        by_cat.setdefault(lit["category"], []).append(lit)
    total_lits = len(literals)
    add(f"Extracted **{total_lits}** numeric literals from the active `.tex` files "
        f"(a further {commented_count} sit on commented-out lines and are ignored).")
    add(f"**{total_lits - len(uncovered)}** are accounted for by a check above; "
        f"**{len(uncovered)}** are not, broken down as:")
    add("")
    add("| Category | Count | Meaning |")
    add("|---|---:|---|")
    add(f"| `claim` | {len(by_cat.get('claim', []))} | prose numbers that no check covers -- the actionable list |")
    add(f"| `setup` | {len(by_cat.get('setup', []))} | numbers bound to a unit (15 W, 64 GB, 10 Hz, 4 M) |")
    add(f"| `config` | {len(by_cat.get('config', []))} | experiment knobs (`BS=8`, `DB=4M`, `top-k=5`, core counts) |")
    add(f"| `hardware` | {len(by_cat.get('hardware', []))} | device/model numbers (RTX 4090, i9-14900K, Llama-3.1-8B) |")
    add(f"| `enumerator` | {len(by_cat.get('enumerator', []))} | list markers -- `(1)`, `(2)`, `(3)` |")
    add("")
    add("Classification is a presentation aid only: every literal is listed somewhere below,")
    add("so nothing is dropped. Only the `claim` bucket is treated as needing attention.")
    add("")
    add("### Uncovered `claim` literals")
    add("")
    claims = by_cat.get("claim", [])
    if claims:
        add("| File:line | Literal | Context |")
        add("|---|---:|---|")
        for lit in claims:
            ctx = lit["context"].replace("|", "\\|")[:120]
            add(f"| `{lit['file']}:{lit['line']}` | {lit['text']} | {ctx} |")
    else:
        add("None.")
    add("")
    add("<details><summary>Uncovered `setup`, `config`, `hardware` and `enumerator` literals</summary>")
    add("")
    add("| File:line | Literal | Category | Context |")
    add("|---|---:|---|---|")
    for cat in ("setup", "config", "hardware", "enumerator"):
        for lit in by_cat.get(cat, []):
            ctx = lit["context"].replace("|", "\\|")[:100]
            add(f"| `{lit['file']}:{lit['line']}` | {lit['text']} | {lit['category']} | {ctx} |")
    add("")
    add("</details>")
    add("")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("-c", "--config", default=DEFAULT_CONFIG)
    ap.add_argument("-o", "--output", default=DEFAULT_REPORT)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any check drifts from its declared `expect`")
    args = ap.parse_args(argv)

    try:
        cfg = load_config(args.config)
        allowed = cfg["tabs"]["allowed"]
        stale = cfg["tabs"]["stale"]
        overlap = set(allowed) & set(stale)
        if overlap:
            raise Problem(f"tabs listed as both allowed and stale: {sorted(overlap)}")

        wb = Workbook(os.path.join(REPO_ROOT, cfg["workbook"]))

        for chk in cfg["checks"]:
            sheet = (chk.get("source") or {}).get("sheet")
            if sheet and sheet not in allowed:
                raise Problem(
                    f"check {chk['id']!r} reads sheet {sheet!r}, which is not authorised. "
                    f"Authorised tabs: {allowed}"
                )

        results, drifts = [], []
        for chk in cfg["checks"]:
            status, expected, delta, detail = evaluate(chk, wb)
            results.append({"id": chk["id"], "check": chk, "status": status,
                            "expected": expected, "delta": delta, "detail": detail})
            if chk.get("expect") and chk["expect"] != status:
                drifts.append({"id": chk["id"], "expect": chk["expect"], "status": status})

        literals, commented_count = extract_literals(cfg["tex_sources"])
        covered = covered_keys(cfg["checks"])
        uncovered = [l for l in literals
                     if (l["file"], l["line"], round(l["value"], 6)) not in covered]
        stale_hits = stale_only_matches(literals, wb, allowed, stale)

        report = build_report(cfg, wb, results, literals, uncovered,
                              stale_hits, commented_count, drifts)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report)

    except Problem as exc:
        print(f"verify_numbers: {exc}", file=sys.stderr)
        return 2

    tally = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in results:
        tally[r["status"]] += 1
    print(f"wrote {args.output}")
    print(f"  tabs read      : {len(allowed)} authorised")
    print(f"  tabs skipped   : {len(stale)} stale ({', '.join(stale)}) -- excluded from all evidence")
    print(f"  checks         : {tally['PASS']} PASS / {tally['FAIL']} FAIL / "
          f"{tally['UNVERIFIABLE']} UNVERIFIABLE")
    print(f"  literals       : {len(literals)} extracted, {len(uncovered)} uncovered "
          f"({sum(1 for l in uncovered if l['category'] == 'claim')} in prose)")
    print(f"  stale warnings : {len(stale_hits)}")
    if drifts:
        print(f"  DRIFT          : {len(drifts)} check(s) differ from their declared expect:")
        for d in drifts:
            print(f"      {d['id']}: expect {d['expect']}, observed {d['status']}")
        if args.strict:
            return 1
    else:
        print("  drift          : none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
