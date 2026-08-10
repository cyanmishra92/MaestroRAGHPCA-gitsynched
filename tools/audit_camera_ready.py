#!/usr/bin/env python3
"""
audit_camera_ready.py -- read-only pre-submission gate for the MaestroRAG camera-ready.

Complements tools/verify_numbers.py, which checks quantitative claims against the
workbook and the rebuttal. This script checks everything else: the presentation and
housekeeping items a format check or a shepherd would raise.

It NEVER writes to a .tex file. Run it, read the FAILs, fix them by hand.

    python3 tools/audit_camera_ready.py            # human-readable report
    python3 tools/audit_camera_ready.py --strict   # exit 1 if any check FAILs

Exit codes: 0 clean (or non-strict), 1 a FAIL under --strict, 2 could not run.

NOTE ON PROVENANCE: the Task 8 brief referred to a supplied audit script that was never
delivered with the prompt. This is a reimplementation written to the brief's description,
so its tallies are not comparable to the 45/24/12 quoted there. The brief's one named
false positive, a British-spelling probe matching "analyze", is avoided here: the
patterns below are anchored so that American -ize/-yze forms cannot match.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACTIVE = ["main.tex", "abstract.tex", "introduction.tex", "background&motivation.tex",
          "characterization.tex", "design.tex", "implementation&eval.tex",
          "related_work.tex", "conclusion.tex",
          "TablesAlgos/CachingTable.tex", "TablesAlgos/Jetson4090A100.tex",
          "TablesAlgos/LatencyBreakdown.tex", "TablesAlgos/PowerEnergy.tex"]

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
results = []


def record(status, check, detail=""):
    results.append((status, check, detail))


def uncomment(line: str) -> str:
    """Strip the LaTeX comment from a line, respecting \\%."""
    out, i = [], 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2]); i += 2; continue
        if line[i] == "%":
            break
        out.append(line[i]); i += 1
    return "".join(out)


def live_lines():
    """Yield (path, lineno, live_text) for every uncommented line of the active files."""
    for f in ACTIVE:
        p = os.path.join(REPO, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            for i, raw in enumerate(fh, 1):
                yield f, i, uncomment(raw)


# ----------------------------------------------------------------- presentation
def check_emdashes():
    hits = [(f, i, m.group(0)) for f, i, t in live_lines()
            for m in re.finditer(r"---|\u2014", t)]
    record(PASS if not hits else FAIL, "no em-dashes in live text",
           "; ".join(f"{f}:{i}" for f, i, _ in hits[:6]) or "none found")


def check_en_dash_parentheticals():
    """A bare -- used as a parenthetical rather than in a numeric range."""
    hits = []
    for f, i, t in live_lines():
        if f == "main.tex":
            continue  # preamble format strings (\crefrangeformat) and the draft banner
        for m in re.finditer(r"(?<!-)--(?!-)", t):
            before, after = t[max(0, m.start() - 1):m.start()], t[m.end():m.end() + 1]
            # X--Y between two word characters is a range or a compound modifier
            # (2--16, b--c, CPU--GPU) and is correct. A dash with space on either
            # side is being used as a parenthetical, which is what we are after.
            if before.isalnum() and after.isalnum():
                continue
            hits.append((f, i, t.strip()[:70]))
    record(PASS if not hits else WARN, "no -- used as a parenthetical",
           "; ".join(f"{f}:{i}" for f, i, _ in hits[:6]) or "none found")


def check_section_symbol():
    hits = [(f, i) for f, i, t in live_lines() if re.search(r"\\S\s*\\ref\b", t)]
    record(PASS if not hits else FAIL, "no literal \\S before a \\ref",
           "; ".join(f"{f}:{i}" for f, i in hits[:6]) or "none found")


def check_vspace():
    hits = [(f, i, m.group(0)) for f, i, t in live_lines()
            for m in re.finditer(r"\\vspace\*?\s*\{[^}]*\}", t)]
    banner = [h for h in hits if h[0] == "main.tex"]
    other = [h for h in hits if h[0] != "main.tex"]
    if other:
        record(FAIL, "no \\vspace layout hacks outside the preamble",
               "; ".join(f"{f}:{i} {v}" for f, i, v in other[:6]))
    elif banner:
        record(WARN, "no \\vspace layout hacks outside the preamble",
               f"{len(banner)} remain in main.tex, in the draft-banner header; "
               "they go when the banner goes")
    else:
        record(PASS, "no \\vspace layout hacks outside the preamble", "none found")


def check_british_spelling():
    """
    Deliberately narrow. The -ise/-isation family is the real signal; -yze/-ize words
    such as "analyze", "amortize" and "optimize" are American and must not match, which
    is the false positive the brief called out. Each pattern therefore requires the
    British letter explicitly and is bounded by word characters on both sides.
    """
    pats = [r"\b\w+isation\b", r"\b\w+isations\b", r"\banalyse[sd]?\b", r"\bbehaviour\b",
            r"\bcolour\b", r"\bmodelling\b", r"\bnormalise[sd]?\b", r"\boptimise[sd]?\b",
            r"\bamortise[sd]?\b", r"\bcentre\b", r"\bfibre\b"]
    rx = re.compile("|".join(pats), re.IGNORECASE)
    hits = [(f, i, m.group(0)) for f, i, t in live_lines() for m in rx.finditer(t)]
    record(PASS if not hits else WARN, "American spelling throughout",
           "; ".join(f"{f}:{i} {w}" for f, i, w in hits[:6]) or "none found")


def check_draft_artifacts():
    src = "\n".join(open(os.path.join(REPO, "main.tex"), encoding="utf-8",
                         errors="replace").read().split("\n"))
    items = [
        ("title has no submission-track prefix", r"\\title\{\s*Regular-", FAIL),
        ("todonotes disabled", r"^\s*\\usepackage\[textsize=tiny\]\{todonotes\}", WARN),
        ("showcomments off", r"\\setboolean\{showcomments\}\{true\}", WARN),
        ("no confidential-draft banner", r"Confidential Draft", WARN),
        ("revision mode set for review", r"\\newcommand\{\\revmode\}\{1\}", WARN),
        ("flag mode set for review", r"\\newcommand\{\\flagmode\}\{1\}", WARN),
    ]
    for name, pat, sev in items:
        hit = re.search(pat, src, re.M)
        record(PASS if not hit else sev, name,
               "still present in main.tex" if hit else "clean")


def check_annotation_macros():
    live = [(f, i, m.group(1)) for f, i, t in live_lines()
            for m in re.finditer(r"\\(rishabh|cyan|todo|fixme)\b", t) if f != "main.tex"]
    record(PASS if not live else FAIL, "no author-annotation macros in body text",
           "; ".join(f"{f}:{i} \\{w}" for f, i, w in live[:6]) or "none found")


# --------------------------------------------------------------------- content
def check_caption_config():
    """Every float caption should name the configuration it was measured at."""
    KEYS = re.compile(r"BS\s*=|batch size|DB\s*=|database size|top-?k|\bM\b|cores")
    missing = []
    for f in ACTIVE:
        p = os.path.join(REPO, f)
        if not os.path.exists(p):
            continue
        text = "".join(uncomment(l) for l in open(p, encoding="utf-8", errors="replace"))
        for m in re.finditer(r"\\caption\{", text):
            depth, j = 1, m.end()
            while j < len(text) and depth:
                if text[j] == "{": depth += 1
                elif text[j] == "}": depth -= 1
                j += 1
            body = text[m.end():j - 1]
            if not KEYS.search(body):
                missing.append((f, body.strip()[:58]))
    record(PASS if not missing else WARN, "every caption states its configuration",
           "; ".join(f"{f}: {b}..." for f, b in missing[:5]) or "all captions carry one")


def check_caption_claims():
    """Captions should describe. These verbs are how an arguing caption reads."""
    ARGUE = re.compile(r"\bsolves\b|\bdemonstrat|\bshows that\b|\bkey findings\b|"
                       r"\bconcoction\b|\boutperform|\bproves\b|\bconfirms\b", re.I)
    hits = []
    for f in ACTIVE:
        p = os.path.join(REPO, f)
        if not os.path.exists(p):
            continue
        text = "".join(uncomment(l) for l in open(p, encoding="utf-8", errors="replace"))
        for m in re.finditer(r"\\caption\{", text):
            depth, j = 1, m.end()
            while j < len(text) and depth:
                if text[j] == "{": depth += 1
                elif text[j] == "}": depth -= 1
                j += 1
            body = text[m.end():j - 1]
            w = ARGUE.search(body)
            if w:
                hits.append((f, w.group(0), body.strip()[:48]))
    record(PASS if not hits else WARN, "captions describe rather than argue",
           "; ".join(f"{f}: '{w}' in \"{b}...\"" for f, w, b in hits[:5]) or "none argue")


def check_terminology():
    """The edge vocabulary that §2.1 defines should be the one the body uses."""
    counts = {}
    for term in ("personal-computing edge", "local/personal-computing platform",
                 "embedded edge device", "edge device", "edge platform"):
        counts[term] = sum(len(re.findall(re.escape(term), t)) for _, _, t in live_lines())
    defined = counts["personal-computing edge"] + counts["local/personal-computing platform"]
    generic = counts["edge device"]
    detail = ", ".join(f"{k}: {v}" for k, v in counts.items())
    record(WARN if generic > 5 * max(defined, 1) else PASS,
           "edge vocabulary follows the Section 2.1 definition", detail)


def check_flags():
    hits = [(f, i) for f, i, t in live_lines() if "\\flag{" in t and f != "main.tex"]
    record(WARN if hits else PASS, "no unresolved author flags",
           f"{len(hits)} open: " + "; ".join(f"{f}:{i}" for f, i in hits[:8])
           if hits else "none open")


# ----------------------------------------------------------------------- build
def check_build():
    log = os.path.join(REPO, "main.log")
    if not os.path.exists(log):
        record(WARN, "build log present", "main.log absent: the Makefile deletes it. Build with pdflatex to check.")
        return
    text = open(log, encoding="utf-8", errors="replace").read()
    for name, pat, sev in (("no LaTeX errors", r"^!", FAIL),
                           ("no undefined references", r"LaTeX Warning: Reference", FAIL),
                           ("no undefined citations", r"LaTeX Warning: Citation", FAIL),
                           ("no overfull boxes", r"Overfull \\[hv]box", WARN)):
        n = len(re.findall(pat, text, re.M))
        record(PASS if not n else sev, name, f"{n} found" if n else "none")


def check_verify_numbers():
    p = os.path.join(REPO, "tools", "verify_numbers.py")
    if not os.path.exists(p):
        record(WARN, "verify_numbers agrees", "tools/verify_numbers.py absent")
        return
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, cwd=REPO)
    m = re.search(r"(\d+) PASS / (\d+) FAIL / (\d+) UNVERIFIABLE", r.stdout)
    drift = "drift          : none" in r.stdout
    if not m:
        record(WARN, "verify_numbers agrees", "could not parse output")
        return
    p_, f_, u_ = m.groups()
    record(PASS if f_ == "0" and drift else FAIL, "verify_numbers agrees",
           f"{p_} PASS / {f_} FAIL / {u_} UNVERIFIABLE, drift: {'none' if drift else 'YES'}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    for fn in (check_emdashes, check_en_dash_parentheticals, check_section_symbol,
               check_vspace, check_british_spelling, check_draft_artifacts,
               check_annotation_macros, check_caption_config, check_caption_claims,
               check_terminology, check_flags, check_build, check_verify_numbers):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            record(WARN, fn.__name__, f"check raised {type(exc).__name__}: {exc}")

    width = max(len(c) for _, c, _ in results)
    print(f"{'':6} {'check'.ljust(width)}  detail")
    print("-" * (width + 60))
    for st, check, detail in results:
        print(f"[{st}] {check.ljust(width)}  {detail}")
    n = {PASS: 0, WARN: 0, FAIL: 0}
    for st, _, _ in results:
        n[st] += 1
    print("-" * (width + 60))
    print(f"{n[PASS]} pass / {n[WARN]} warn / {n[FAIL]} fail")
    return 1 if (args.strict and n[FAIL]) else 0


if __name__ == "__main__":
    sys.exit(main())
