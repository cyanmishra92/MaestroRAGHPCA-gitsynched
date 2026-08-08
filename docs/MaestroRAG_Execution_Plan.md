# MaestroRAG — Execution Plan: Repo Verification + How to Run the Revision

Companion to `MaestroRAG_IISWC_Final_Master_Plan.md`. That file says *what* changes. This one says *how, in what order, and with what tooling*.

---

## Part I — Repo verification (`cyanmishra92/MaestroRAG`, main)

Pulled the tarball (166 files) and parsed the hardcoded data out of every plotting script, then compared against the workbook and the PDF.

### Verdict: the plot scripts are correct. Every series matches.

| Figure | Script → output | Data check |
|---|---|---|
| 2a | `pieChart.py` → `stacked_graph.pdf` | Exact match to `Breakdown` tab: startup [0.46, 3.73, 0, 0], execution [0.258, 4.0079, 0.1, **3.41**], total 11.9659 ✅ |
| 2b | `FwdPassBS.py` → `forwardpass_8cores.pdf` | [0.0546, 0.0989, 0.256, 0.5515, 0.9836] ✅ |
| 2c | `FwdPass.py` → `forwardpass_bs16_range_discrete.pdf` | min/max over cores [1,2,4,8,16] ✅ |
| 2d | `stackedLatencyMotivation.py` → `batchsize_stacked_linear_labeled.pdf` | see V1 below ⚠️ |
| 2e | `CharacterizationPlot1.py` → `latency_cores.pdf` | [8.77, 5.84, 4.935, 4.12, 3.72] ✅ |
| 2f | `CharacterizationPlot1.py` → `latency_dbsize.pdf` | [2.11, 3.72, 7.449, 12.069] ✅ |
| 4a–f | `SpeedUpPlot4090.py`, `SpeedUpPlot4080.py`, `latencyPlot.py` | all 16 MaestroRAG points + all baseline speedups match ✅ |
| 5 | `JetsonThemVsUs.py` | [14.14, 23.44, 38.62, 59] vs [12.923, 17.87, 28.56, 46.979] ✅ |
| 7a | `mapping.py` | matches `Mapping` tab exactly ✅ |
| 7b | `mainLatencyResult2.py` | 6.497 / 3.959 / 28.56, cache 0.92, all baselines ✅ |
| 7c | `goodput.py` | 1.6 / 0.2876 / 0.6831 / 1.1852; Jetson 0.4324 / 0.0645 / — / 0.3701 ✅ |
| **6** | **no script exists** | see V3 below ⚠️ |

### Two things the repo settles

**Your Q1 answer is independently confirmed.** `data_flash` and `data_pipe` in `SpeedUpPlot4090.py` contain **12 entries each — BS = 2, 4, 8 only**, while `data_edge` and `data_ours` contain 16. The BS=16 omission for FlashRAG and PipeRAG is deliberate in the plotting code, not an artifact. The Excel BS=16 baseline rows are stale, exactly as you said. My earlier "plot the losing bar" suggestion stays retracted.

**Generation = 3.41 s is now double-sourced.** `pieChart.py` hardcodes it and the `Breakdown` tab records it. That's the anchor of the whole Table 2 reconciliation, and it's confirmed from two independent places.

### V1 ⚠️ — Fig. 2d: two scripts, two different BS=2 values; the *paper's text is fine*

Two scripts draw this panel:

| Script | Index Fetch | Similarity Search |
|---|---|---|
| `CharacterizationPlot1.py` → `batchsize_stacked.pdf` | 3.36 ×5 | **4.408**, 0.7539, 1.79, 3.81, 224.58 |
| `stackedLatencyMotivation.py` → `batchsize_stacked_linear_labeled.pdf` | 3.36 ×5 | **0.60**, 0.7539, 1.79, 3.81, 224.58 |

Only `batchsize_stacked_linear_labeled.pdf` is in `InResultASPLOS26/`, so **the paper ships the SS = 0.60 version**. At BS=2 that gives index fetch 3.36 s (85% of the bar) against 0.60 s search — which makes §3.2's *"index fetch dominates latency at small batch sizes"* **correct**, and the totals monotone (3.96, 4.11, 5.15, 7.17).

So my earlier concern C1/F3 is **withdrawn — no text change needed.** What remains is a bookkeeping mismatch: the `Motivation` tab records BS=2 as (IF 0.60, SS 4.408), which matches neither script. The plotted 3.36 at BS=2 is imputed from the constant-fetch assumption rather than taken from that row. Nothing in the paper is wrong, but if anyone asks for raw data the row won't line up. Worth a 30-second re-run or a note in your records. **Not a camera-ready blocker.**

Also dormant: `FwdPassBS.py` has a second DataFrame with cores `[1, 2, 4, 8, 10]` and the [1,2,4,8,16] latency values. It writes `forwardpass_bs16_range.pdf`, which is **not** in `InResultASPLOS26/` — the paper uses `FwdPass.py`'s correct version. Delete the dead block so nobody regenerates from it.

### V2 — the repo workbook is a subset

`Plots/NewRAGResults.xlsx` is the same 13 tabs as your upload **minus `PowerComp`**. The uploaded file is the superset; work from that one. `CachingResults4090` is empty in both, so Table 1's data lives nowhere but the PDF — F6 stands.

### V3 ⚠️ — no source for Figures 1, 3, or 6

The repo has 47 Python scripts and **no `.pptx`, `.svg`, `.ai`, `.drawio`, `.tex`, or `.bib`**. Consequences:

- **Fig. 6** has no plotting script at all — probably an Excel chart. Item 3 asks for a stage breakdown, a vertical divider, and labelled dual axes. That figure has to be **written from scratch in matplotlib**, not edited. Budget it as a build, not a tweak. Good news: with `PowerComp` plus the rebuttal's stage shares, all the inputs exist.
- **Figs. 1 and 3** are hand-drawn and the PC named both for font size, plus the white-on-light-green in Fig. 1 and the "FlashFAG" typo in Fig. 3c. **Where are the source files?** If they don't exist anywhere, these get redrawn — and Fig. 3c in particular (the pipeline timeline grids) is the least legible element in the paper. This is now the single largest unknown in the schedule.

---

## Part II — Should this run in Claude Code?

**Yes, and it's the right call for this job specifically** — not for generic reasons.

What makes it fit: the work is ~30 discrete edits across a LaTeX tree, most of which are verifiable by compiling. Claude Code can hold the `.tex`, the `.bib`, the plot scripts, and the workbook in one place; make an edit; rebuild; and diff. In chat I'm handing you fragments to paste, which means you're the integration layer for every one of them — that's 30 opportunities for a cross-reference to break silently two days before a deadline.

The specific wins here:

- **One repo, one commit per item.** Seven mandated items → seven commits, each independently revertible. If the shepherd pushes back on one, you revert one.
- **Compile-verified cross-references.** The renumbering (two new subsections, seven renamed) touches every `\Cref`. A build catches `??` immediately; a chat paste does not.
- **The plot scripts live next to the paper.** Fig. 6 gets built, `\includegraphics` gets updated, page count gets checked, in one loop.
- **The number audit becomes executable.** Drop the verification script into `tools/`; it reads the workbook and greps the `.tex` for the claimed values. Run it before you submit. This is what stops B1–B10 from recurring.

Where chat stays better: the judgment calls. Placement decisions, what Item 6's argument should actually *say*, whether the EdgeRAG residual is defensible. Do that here, execute there.

**Suggested split:** we finish deciding content in this thread (Items 2, 5, 6 are argument-shaped and mostly settled); you open Claude Code on the paper repo for execution; you bring anything contentious back here.

### Repo layout worth setting up first

```
paper/           main.tex, sections/, figs/, refs.bib
plots/           the 47 scripts, unchanged, + newer fig6_power_energy.py
data/            MaestroRAGResults.xlsx  (single source of truth)
tools/           verify_numbers.py       (workbook ↔ .tex audit)
docs/            the master plan + this file + shepherd_response.md
```

Splitting `main.tex` into `sections/*.tex` if it isn't already is worth the 20 minutes — it makes "one task, one file" possible and keeps diffs readable.

---

## Part III — Task sequence

Your instinct — text first, then graphs, then figures — is right, with one amendment: **Table 2 comes before everything.**

Table 2 is the only artifact whose content is still uncertain (the EdgeRAG cell, F4). Everything else is either decided or mechanical. If it turns out the EdgeRAG row can't be defended, §5.2's framing changes, and §5.5's and §5.9's cross-references change with it. Better to discover that in hour 2 than hour 20.

### Phase 0 — setup (~30 min)
Repo scaffold · split `main.tex` if needed · add the diff switch (Part IV) · drop in `verify_numbers.py` · baseline build, record the page count.

### Phase 1 — text, no figures (7 tasks, one commit each)

| T | Task | Item | Blocked on |
|---|---|---|---|
| **T1** | **§5.2 Stage-Level Latency Breakdown** + Table 2 | 1 | **F4** (EdgeRAG 2.93 s) |
| T2 | §2.1 Deployment Scope + tier table; §5.1 criteria mapping; global "edge device" → "local-compute platform" | 2 | — |
| T3 | §3.3 Profiling Platform and Trend Portability (the five-point argument) | 6 | — |
| T4 | §4.1 context-drift paragraph; §4.2 static-allocation sentence + B7 + C2 | 5 | — |
| T5 | §5.8 Table 1 analysis rewrite; caption above | 4 | F6 (BS=8 run — changes wording only) |
| T6 | §5.9 ablation table + portability column + PipeRAG-port row; B6, B8 | Part IV of master plan | — |
| T7 | Corrections sweep B1–B5, B9, B10; conflicts C3–C5; renumbering + `\S` purge | 7 + integrity | **F1** (Jetson dependency) |

T2–T4 and T6 are unblocked right now. T7 last, because it touches lines the others create.

### Phase 2 — plots (regenerate from scripts)

| T | Task |
|---|---|
| **T8** | **Build `fig6_power_energy.py` from scratch** — CPU energy stacked by stage, GPU energy adjacent, power panel behind a vertical rule, both axes labelled. The big one. |
| T9 | Font pass across all matplotlib figures: bump the shared `rc` block (currently 10–12 pt) and regenerate. Fig. 2d ticks, Fig. 7a in-bar annotations, Fig. 6 axes. |
| T10 | Caption rewrites: Fig. 7 (named by the PC), plus Figs. 4 and 1 which also carry claims rather than descriptions. Explain Fig. 7b's stacked segment (0.92 + 5.58 = 6.50). |

T9 is cheap — the scripts share an `rc` dict, so it's largely one parameter and a rerun.

### Phase 3 — hand-drawn figures

| T | Task |
|---|---|
| T11 | Fig. 1 — font sizes, kill white-on-light-green |
| T12 | Fig. 3 — font sizes (esp. 3c timelines), fix "FlashFAG" → "FlashRAG" |
| T13 | Fig. 5 text-wrap fix in §5.4 |

**Highest schedule risk.** No source files in the repo. If they're only in a PowerPoint on your laptop, fine. If they don't exist, T11–T12 are redraws and should start today in parallel with Phase 1.

### Phase 4 — close
T14 run `verify_numbers.py`, resolve everything it flags · T15 voice pass (the three duplicate-summary paragraphs, the word-level list) · T16 references · T17 page count and camera-ready formatting · T18 shepherd response letter.

---

## Part IV — The diff-highlighting switch

Concept is right. One correction: **the off state should be black, not white.** White text is invisible but still selectable, copyable, and searchable — it stays in the PDF's text layer. A camera-ready with hidden text is a bad look, and some publishers' preflight tools flag it. You want the text present and normally coloured.

Also worth having: not one switch but a small mechanism, because you'll want *three* states over the next two days.

```latex
% 0 = camera-ready (black)   1 = shepherd review (blue)   2 = drafting (blue + margin bars)
\newcommand{\revmode}{1}

\usepackage{xcolor}
\usepackage[normalem]{ulem}   % only if you want strikeouts for deletions
\usepackage{changes}          % optional; heavier but gives \added/\deleted/\replaced

\ifnum\revmode=0
  \newcommand{\new}[1]{#1}
  \newcommand{\del}[1]{}
\else
  \newcommand{\new}[1]{\textcolor{blue}{#1}}
  \newcommand{\del}[1]{\textcolor{gray}{\sout{#1}}}
\fi
```

Practical notes:

- **Wrap at paragraph or sentence granularity, not word.** `\new{...}` around a fragment mid-sentence breaks across math, `\cite`, and line breaks in ways that produce ugly colour bleed. For a whole new subsection, `\begingroup\color{blue} ... \endgroup` is more robust than a macro argument.
- **Colour won't cover everything.** New *figures* and *tables* can't be blue. Give each a one-line blue note in the caption ("New in the shepherded version") or mark them in the response letter — the letter is where the shepherd actually looks.
- **A `\revmode=2` with `\marginpar` bars** helps you find your own edits while drafting, and costs nothing since you flip to 0 at the end.
- **Flip to 0 and rebuild before submitting**, then grep the PDF text for "blue" leftovers and check nothing reflowed onto a new page.

---

## Part V — What I need to start

**Blocking:** the LaTeX source + `.bib` (F5) — nothing in Phase 1 can be committed without it. And **the Fig. 1 / Fig. 3 source files**, or confirmation that they need redrawing.

**One line each:** F1 the specific missing Jetson dependency (T7) · F4 EdgeRAG's 2.93 s (T1) · F6 whether a BS=8 caching run is possible (T5 wording).

**Withdrawn, no longer needed:** F3. The repo settled it — the shipped Fig. 2d and §3.2's text agree.

Once the source lands, T2, T3, T4, and T6 can all be drafted without waiting on anything else.
