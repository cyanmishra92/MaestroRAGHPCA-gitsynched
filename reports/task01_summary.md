# Task 1 — Summary

Scaffold, revision-mode switch, and verification harness. **No paper content changed.**

---

## 1. What changed

| Path | Change |
|---|---|
| `main.tex` | **The only `.tex` edit.** 14 inserted lines, 0 deleted — the revision-mode block, added verbatim after the existing `\red` / `makeRed` block. |
| `.gitignore` | New. LaTeX build artifacts, Office lock files, `.DS_Store`, Python caches. |
| `data/.gitkeep` | New. |
| `data/MaestroRAGResults.xlsx` | Copied in (see §5.1). |
| `tools/verify_numbers.py` | New. Verification harness. |
| `tools/checks.yaml` | New. Checks table, 38 entries. |
| `reports/verify_numbers.md` | New. Generated. |
| `reports/task01_repo_health.md` | New. |
| `reports/task01_summary.md` | New. This file. |
| `docs/` | Pre-existing, previously untracked; now committed. |

`git diff` on `*.tex` is exactly the preamble addition:

```
 main.tex | 14 ++++++++++++++
 1 file changed, 14 insertions(+)
```

No prose, section, figure, table, or number was touched.

---

## 2. Baseline build

**`make` succeeds. `main.pdf` is 12 pages** (1,076,514 bytes).

`main.log` was captured before the Makefile's `rm` by running the same four commands
manually first.

| | |
|---|---:|
| LaTeX errors | **0** |
| Undefined references | **0** |
| Undefined citations | **0** |
| Multiply-defined labels | **0** |
| Overfull boxes | **0** |
| Underfull boxes | 20 (12 at badness 10000) |
| BibTeX warnings | 1 (`empty journal in faiss`) |

Nothing was fixed. Full detail in `reports/task01_repo_health.md` §1.

---

## 3. Revision-mode switch — verified

Added at `main.tex:188–200`, currently `\revmode=1`.

**Off state renders black, not white.** Verified by pixel measurement, not by reading the
code. A full copy of the repo in `/tmp` had a test paragraph appended that wraps `\cite`,
`\Cref`, inline math, display math, nested `\textbf`/`\texttt`, and a paper macro in both
`\new{...}` and the `newtext` environment. Both modes were built and all 12 pages
rasterised at 150 dpi with Ghostscript:

| Mode | Ink colour on the changed pixels | Near-white pixels |
|---|---|---:|
| `\revmode=1` | mean RGB **(0, 0, 255)** — 100% strongly blue | **0** |
| `\revmode=0` | mean RGB **(0, 0, 0)** — 100% neutral | **0** |

Pages 1–10 and 12 were **pixel-identical** between the two builds; only the test page
differed. The switch has no side effects on the rest of the document.

**`\new` survives `\cite`, `\Cref`, and math** — the test document compiled with 0 LaTeX
errors at both settings. No name collision with any loaded package. The test lived
entirely in `/tmp`; the paper was never edited for it.

**The real paper builds identically in both modes.** Built at `\revmode=1` and `\revmode=0`:
both produce 12 pages at **1,076,514 bytes** — byte-for-byte the same size as the step-1
baseline, with the same warning set. `\revmode` was restored to `1`.

---

## 4. Verification harness

`python3 tools/verify_numbers.py` → `reports/verify_numbers.md`. Exit 0.

### Tallies

| PASS | FAIL | UNVERIFIABLE | Total |
|---:|---:|---:|---:|
| **32** | **5** | **1** | **38** |

Drift: **none**. Every check holds the status recorded as its `expect` anchor in
`checks.yaml`, so a later edit that changes any status — in either direction — surfaces
as DRIFT rather than sliding by.

Numeric literals: **216** extracted from the 9 active `.tex` files (68 of them prose
claims not covered by a check; the rest are units, config knobs, model numbers, and list
markers, all itemised in the report).

### Stale tabs — excluded and stated explicitly

The report names the three stale tabs and says in as many words that they are excluded
from all evidence. The exclusion is enforced, not just documented: the script **refuses to
run** (exit 2) if any check in `checks.yaml` points at a non-authorised sheet.

The stale scan found a real hit: **the paper's `8.22`% peak-CPU-power figure matches
`Comparison!B6` and `Comparison!K57` — stale cells — and appears in no authorised tab.**
That is direct evidence for why the `8.22` check fails.

### The known-failing checks — all FAIL, none silently fixed

| Check | Paper says | Workbook gives | Status |
|---|---:|---:|---|
| `peak_cpu_power_delta_flashrag` | 16.45 % | **16.36 %** | **FAIL** ✔ as mandated |
| `peak_cpu_power_delta_piperag` | 8.22 % | **8.08 %** | **FAIL** ✔ as mandated |
| `jetson_overhead_reduction_band` | "25–35 %" | **8.6 / 23.8 / 26.0 / 20.4 %** | **FAIL** ✔ as mandated |
| `cold_start_total` | 7 s (parts sum to 6.76 s) | no authorised tab records it | **UNVERIFIABLE** ✔ as mandated |

None were repaired. Each carries a `known_defect` note recording that it awaits its own
task.

### Two further FAILs, not in the seeded table

| Check | Paper says | Workbook gives | Where |
|---|---:|---:|---|
| `energy_per_query_flashrag` | 791.8 J | **792.00 J** — `(579.6 + 1004.4)/2` | `implementation&eval.tex:164` |
| `speedup_4080_flashrag_bs8` | 1.9× | **1.96×** — truncated, not rounded | `implementation&eval.tex:146` |

Both are small, both are real, and both are left unfixed as this task requires.

---

## 5. Anything that contradicts the instructions

### 5.1 The workbook was not in `data/` — I put it there

`data/` already existed and held **only** `~$MaestroRAGResults.xlsx`, a 165-byte Excel
owner-lock file (the workbook is open in Excel), not the workbook. The real file was at
`/Users/cyamis01/Downloads/MaestroRAGResults.xlsx`. I **copied** it to
`data/MaestroRAGResults.xlsx` — no move, no delete, original untouched — so step 4 could
actually run. Its SHA-256 is recorded at the top of `reports/verify_numbers.md`; if this is
the wrong copy, that hash is how you will know. The lock file is covered by the
`.gitignore` `~$*` rule.

### 5.2 `data/` and `docs/` already existed

The brief said to create them. `docs/` already held three files
(`MaestroRAG_Execution_Plan.md`, `MaestroRAG_IISWC_Final_Master_Plan.md`,
`Untitled document.md`), all untracked. Nothing was moved or deleted; they are now
committed.

### 5.3 `\revmode=2` is documented but not implemented

The block's comment says mode 2 = *"drafting (additions in blue + margin markers)"*, but
the code has only an `=0` branch and an `else`. **Mode 2 therefore behaves identically to
mode 1** — no margin markers. I added the block **verbatim as specified** rather than
inventing the missing branch. Flagging it so the gap is a decision, not a surprise.

### 5.4 The workbook has an 11th tab the brief does not mention

`CachingResults4090` is in the workbook but appears in neither the authorised list nor the
stale list. Since the instruction was to read **only** the ten named tabs, it is excluded —
neither read for evidence nor scanned for stale matches. It is recorded under
`tabs.unlisted` in `checks.yaml` and named in the report so the omission is visible. If it
backs the caching results in Table 1, it needs adding to the authorised list.

### 5.5 The "25–35 %" claim is live in only one place

It appears three times in `implementation&eval.tex` — lines 89, 104, and 119 — but **lines
89 and 104 are commented out**. Only `implementation&eval.tex:119` reaches the PDF. The
check points there. Whoever fixes this in a later task needs to touch one line, not three.

### 5.6 Figure 3's assets are in `diagrams/`, not `Figs/`

The brief asked which `Figs/*.pdf` lack a generating script. The expectation — Figures 1,
3 and 6 — is **confirmed exactly**, but only two of the five files live in `Figs/`:

**`Figs/*.pdf` affected — exactly two:**
- `Figs/RAGpipegrad.pdf` (Figure 1)
- `Figs/power_energy_comparison.pdf` (Figure 6)

**Under `diagrams/` — three more, all of Figure 3:**
- `diagrams/latency_oriented_pipeline.png` (3a)
- `diagrams/throughput_oriented_pipeline.png` (3b)
- `diagrams/pipeline_comparison_schematic.pdf` (3c)

All 16 other live figures map to a named script and line in `cyanmishra92/MaestroRAG`,
`Plots/`. **Figures 1 and 3 are hand-drawn schematics, so no script is expected — Figure 6
is the one that matters.** It is a *data* plot (power/energy per query) with no script in
`Plots/` and no copy in `Plots/InResultASPLOS26/`, drawn from the same `PowerComp` tab
whose peak-power claims currently FAIL. There is no reproducible path from workbook to
that image.

### 5.7 Three `\includegraphics` calls have a space before the brace

`characterization.tex:102`, `characterization.tex:108`, and `implementation&eval.tex:210`
are written `\includegraphics[...] {file}`. A regex requiring `\]\{` misses all three —
including Figure 7c, the throughput plot. My first inventory pass had exactly this bug and
undercounted by three. `verify_numbers.py` tolerates the space; any later tooling must too.

### 5.8 One orphan beyond the expected four

The brief expected `ASPLOS*.tex`, `hpca-template.tex`, `iiswc26example.tex` and
`rebuttal_text.tex` to be orphaned — **all four confirmed**. Three more were found in
`TablesAlgos/`: `FeatureTable.tex` and `AlgoCCPUMapping.tex` (commented-out `\input` sites),
and `Jetson4090A100.tex`, which is **referenced from nothing at all** — its only mention is
a commented `\input` inside the already-orphaned `ASPLOSbackground&motivation.tex:219`.
Nothing deleted.

### 5.9 Neither `openpyxl` nor `PyYAML` is installed

`python3` here is Homebrew 3.14 with neither available. Rather than add a dependency to a
harness that later tasks must be able to run, `verify_numbers.py` is **stdlib-only**: it
reads `.xlsx` with `zipfile` + `ElementTree` and parses the YAML subset `checks.yaml` uses
with a built-in parser. It uses `PyYAML` automatically if it ever becomes available.

### 5.10 `main.pdf` added to `.gitignore` — my call, easily reversed

The repo has never tracked the built PDF, so leaving it untracked made it permanent noise
in `git status`. I ignored it, with a comment on the line saying to delete that line if the
camera-ready PDF should be versioned. Say the word and it comes out.

### 5.11 Two seeded values have no text location

`speedup_edgerag_bs16_db8m` (6.152) and the five Fig. 2a stage times exist **only inside
figures**, not in any `.tex` prose. They are encoded as checks against their workbook cells
with `locations: []` and a `figure_only:` note, so they still act as regression anchors on
the data behind the plots.

---

## 6. Acceptance criteria

| | Criterion | Status |
|---|---|---|
| ☑ | `make` succeeds; page count recorded; `main.log` captured before deletion | 12 pages; log captured |
| ☑ | `git diff` on `*.tex` shows only the preamble addition | 1 file, +14/−0 |
| ☑ | Paper builds identically at `\revmode=0` and `=1`, with `=0` rendering black | identical byte size; RGB(0,0,0) measured |
| ☑ | `tools/verify_numbers.py` runs clean and produces `reports/verify_numbers.md` | exit 0 |
| ☑ | The three stale tabs are excluded and the script says so explicitly | stated in the report; enforced with a hard guard |
| ☑ | Known-failing checks appear as FAIL | 16.45/8.22 % and 25–35 % all FAIL; cold-start UNVERIFIABLE |
| ☑ | Both reports exist, are specific, and contain no invented values | every value traced to a cell, a line, or a log |
| ☑ | Committed and pushed | see `git log` |
