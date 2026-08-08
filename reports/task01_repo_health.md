# Task 1 — Repository health report

Inspection only. Nothing in this report was fixed, deleted, or reformatted; every item
is recorded for a later, separately-reviewable task. Every figure, number, and file path
below was read out of the repository, the built PDF, or the plotting repository — none
of it is inferred.

- **Repo:** `cyanmishra92/MaestroRAGHPCA-gitsynched`, branch `main`, base commit `dea2501`
- **Toolchain:** pdfTeX 3.141592653-2.6-1.40.27 (TeX Live 2025), BibTeX, macOS
- **Build command:** `make` (`pdflatex → bibtex → pdflatex → pdflatex`)

---

## 1. Build status

**`make` succeeds.** `main.pdf`, **12 pages**, 1,076,514 bytes.

The Makefile deletes `main.log`, `main.aux`, `main.bbl` and `main.blg` as its last four
steps, so the log was captured by running the same four commands manually before letting
`make` run. The captured third-pass log is the basis for everything below.

### Errors, undefined references, undefined citations

| Category | Count |
|---|---:|
| LaTeX errors (`!`) | **0** |
| Undefined references | **0** |
| Undefined citations | **0** |
| Multiply-defined labels | **0** |
| Overfull boxes (any size) | **0** |
| Underfull boxes | **20** |

Nothing is undefined and nothing is overfull. The build is clean in the senses that
matter for a camera-ready.

### Underfull boxes (all 20)

Underfull boxes are reported by TeX as a *badness* (0–10000), not as a point overflow,
so the "over 10 pt" threshold does not apply to them. All 20 are listed.

| Badness | Kind | Location |
|---:|---|---|
| 10000 | `\hbox` | `implementation&eval.tex` paragraph, lines 118–120 (×10) |
| 10000 | `\hbox` | `design.tex` paragraph, lines 232–235 (×2) |
| 10000 | `\vbox` | while `\output` is active |
| 4084 | `\hbox` | paragraph at lines 26–27 |
| 4060 | `\vbox` | while `\output` is active |
| 3861 | `\hbox` | paragraph at line 115 |
| 2573 | `\hbox` | paragraph at line 4 |
| 2269 | `\hbox` | paragraph at lines 164–172 |
| 1796 | `\hbox` | paragraph at lines 164–172 |
| 1648 | `\hbox` | paragraph at lines 40–45 |

The ten badness-10000 boxes at `implementation&eval.tex:118–120` are the narrow text
column beside the Jetson `wrapfigure` (lines 112–118) — that is the paragraph carrying
the `25\%--35\%` claim.

### Other warnings

| Warning | Count | Note |
|---|---:|---|
| `LaTeX Warning: No \author given.` | 3 | Author block is absent; `authblk` is commented out at `main.tex:47`. Camera-ready blocker. |
| `Package hyperref Warning: Token not allowed in a PDF string` | 4 | From `\mbox{RTX\,4090}` in the subsection title at `implementation&eval.tex:67`; affects PDF bookmarks only. |
| `Package caption Warning: Unknown document class` | 1 | `caption`/`subcaption` does not recognise `iiswc26.cls`; falls back to defaults. |
| `Package todonotes Warning: marginparwidth < 2cm` | 1 | Cosmetic; disappears once `todonotes` is disabled. |
| `LaTeX Font Warning: Font shape ... not available` | 84 | Libertine/`zi4` substitutions at small sizes. Cosmetic. |
| `LaTeX Warning: No positions in optional float specifier` / `'h' changed to 'ht'` | 2 | Float placement. |

### BibTeX

One warning, `Warning--empty journal in faiss`. No undefined or duplicated citations.

---

## 2. Active vs. orphaned `.tex` files

`main.tex` reaches nine files. `\input` chain, in order:

```
main.tex
├── abstract.tex
├── introduction.tex
├── background&motivation.tex     (its only \input, TablesAlgos/FeatureTable, is commented out)
├── characterization.tex
├── design.tex                    (its only \input, TablesAlgos/AlgoCCPUMapping, is commented out)
├── implementation&eval.tex ──────→ TablesAlgos/CachingTable.tex      [the one live table \input]
├── related_work.tex
└── conclusion.tex
```

**Active (10):** `main.tex`, `abstract.tex`, `introduction.tex`, `background&motivation.tex`,
`characterization.tex`, `design.tex`, `implementation&eval.tex`, `related_work.tex`,
`conclusion.tex`, `TablesAlgos/CachingTable.tex`.

**Orphaned (7)** — not reached from `main.tex` by any live `\input`. Confirmed, listed only,
nothing deleted:

| File | Size | Status |
|---|---:|---|
| `ASPLOSbackground&motivation.tex` | 40,178 B | Orphaned — **matches expectation** |
| `ASPLOScharacterization.tex` | 14,775 B | Orphaned — **matches expectation** |
| `hpca-template.tex` | 2,225 B | Orphaned — **matches expectation**. Its only `\input` site, `main.tex:476`, is commented out. |
| `iiswc26example.tex` | 14,889 B | Orphaned — **matches expectation** |
| `rebuttal_text.tex` | 7,648 B | Orphaned — **matches expectation**. Two commented `\input` sites, `main.tex:501` and `main.tex:513`. |
| `TablesAlgos/FeatureTable.tex` | 6,083 B | Orphaned — `\input` commented out at `background&motivation.tex:7` |
| `TablesAlgos/AlgoCCPUMapping.tex` | 1,029 B | Orphaned — `\input` commented out at `design.tex:237` |
| `TablesAlgos/Jetson4090A100.tex` | 580 B | Orphaned — **not referenced from any active file at all**; its only mention is a commented `\input` in the orphaned `ASPLOSbackground&motivation.tex:219` |

All four expectations in the task brief are confirmed. Three additional orphans were
found in `TablesAlgos/`, which the brief did not anticipate.

---

## 3. Figure inventory

21 live `\includegraphics` calls across the active files, resolving to 7 numbered figures
(several with subfigures). Every referenced file exists on disk.

> **Scanning note:** three of these calls are written `\includegraphics[...] {file}` — with
> a space between the option bracket and the brace (`characterization.tex:102`, `:108`,
> `implementation&eval.tex:210`). A naive `\includegraphics(\[[^\]]*\])?\{` regex misses
> them. Any later tooling over this repo must tolerate that space.

| Fig | Graphics file | `.tex` site | On disk | Generating script (`cyanmishra92/MaestroRAG`, `Plots/`) |
|---|---|---|:-:|---|
| 1 | `Figs/RAGpipegrad.pdf` | `introduction.tex:178` | yes | **NONE** |
| 2a | `Figs/stacked_graph.pdf` | `characterization.tex:5` | yes | `Plots/pieChart.py:88` |
| 2b | `Figs/forwardpass_8cores.pdf` | `characterization.tex:11` | yes | `Plots/FwdPassBS.py:50` |
| 2c | `Figs/forwardpass_bs16_range_discrete.pdf` | `characterization.tex:16` | yes | `Plots/FwdPass.py:64` |
| 2d | `Figs/batchsize_stacked_linear_labeled.pdf` | `characterization.tex:23` | yes | `Plots/stackedLatencyMotivation.py:105` |
| 2e | `Figs/latency_cores.pdf` | `characterization.tex:29` | yes | `Plots/CharacterizationPlot1.py:50` |
| 2f | `Figs/latency_dbsize.pdf` | `characterization.tex:35` | yes | `Plots/CharacterizationPlot1.py:75` |
| 3a | `diagrams/latency_oriented_pipeline.png` | `characterization.tex:96` | yes | **NONE** |
| 3b | `diagrams/throughput_oriented_pipeline.png` | `characterization.tex:102` | yes | **NONE** |
| 3c | `diagrams/pipeline_comparison_schematic.pdf` | `characterization.tex:108` | yes | **NONE** |
| 4a | `Figs/4090LatencyOurs.pdf` | `design.tex:301` | yes | `Plots/SpeedUpPlot4090.py:212` |
| 4b | `Figs/4090speedupEdgeRAG.pdf` | `design.tex:307` | yes | `Plots/SpeedUpPlot4090.py:209` |
| 4c | `Figs/4090speedupFlashRAG.pdf` | `design.tex:313` | yes | `Plots/SpeedUpPlot4090.py:210` |
| 4d | `Figs/4090speedupPipeRAG.pdf` | `design.tex:319` | yes | `Plots/SpeedUpPlot4090.py:211` |
| 4e | `Figs/4080Latency_MaestroRAG.pdf` | `design.tex:325` | yes | `Plots/AllSpeedup4080.py:193` |
| 4f | `Figs/4080Speedup_Merged.pdf` | `design.tex:331` | yes | `Plots/AllSpeedup4080.py:196` |
| 5 | `Figs/JetsonThemVsUs.pdf` | `implementation&eval.tex:114` | yes | `Plots/JetsonThemVsUs.py:128` |
| 6 | `Figs/power_energy_comparison.pdf` | `implementation&eval.tex:123` | yes | **NONE** |
| 7a | `Figs/cores_allocation_stacked.pdf` | `implementation&eval.tex:198` | yes | `Plots/mapping.py:144` |
| 7b | `Figs/MainLatencyResults2.pdf` | `implementation&eval.tex:204` | yes | `Plots/mainLatencyResult2.py:175` |
| 7c | `Figs/ThroughputResults.pdf` | `implementation&eval.tex:210` | yes | `Plots/goodput.py:111` |

### Figures with no generating script — confirmed

The expectation was Figures 1, 3 and 6. **Confirmed exactly**, with one precision worth
recording: Figure 3's three assets live in `diagrams/`, not in `Figs/`.

**`Figs/*.pdf` affected — precisely two files:**

1. `Figs/RAGpipegrad.pdf` — Figure 1
2. `Figs/power_energy_comparison.pdf` — Figure 6

**Also unscripted, but under `diagrams/` rather than `Figs/` — three files (all of Figure 3):**

3. `diagrams/latency_oriented_pipeline.png` — Figure 3a
4. `diagrams/throughput_oriented_pipeline.png` — Figure 3b
5. `diagrams/pipeline_comparison_schematic.pdf` — Figure 3c

Figures 1 and 3 are hand-drawn schematics, so the absence of a plotting script is
expected. **Figure 6 is the one that matters:** it is a *data* plot (power and energy per
query) with no script in `Plots/` and no copy in `Plots/InResultASPLOS26/`. Its underlying
numbers are in the workbook's `PowerComp` tab, and two of the four claims drawn from that
tab currently FAIL verification (see `reports/verify_numbers.md`). Figure 6 therefore has
no reproducible path from workbook to image.

### Unused assets in `Figs/`

13 of the 32 PDFs in `Figs/` are not referenced by any live `\includegraphics`. Listed
only; nothing deleted.

`4080Latency.pdf`, `4080Latency_Ours.pdf`, `MRmaindiagram.pdf`, `MainLatencyResults.pdf`,
`RAGPipelineDetailed.pdf`, `batchsize_stacked.pdf`, `forwardpass_bs16_range.pdf`,
`personalized_need_for_GenAI.pdf`, `speedupEdgeRAG.pdf`, `speedupFlashRAG.pdf`,
`speedupPipeRAG.pdf`, `speedup_vs_edgerag.pdf`, `speedup_vs_flashrag.pdf`

Note the near-duplicates: `Figs/4080Latency.pdf`, `4080Latency_Ours.pdf` and
`4080Latency_MaestroRAG.pdf` are byte-identical in size (12,076 B), and only the last is
used. Similarly `speedupEdgeRAG.pdf` and `4090speedupEdgeRAG.pdf` (13,509 B each).

---

## 4. Table inventory

`TablesAlgos/` holds four files. Only one is live.

| File | Included? | Where | Caption position |
|---|---|---|---|
| `CachingTable.tex` | **YES** | `implementation&eval.tex:229` | **ABOVE** the tabular — `\caption` at line 4, `\begin{tabular}` at line 6 |
| `FeatureTable.tex` | no — commented out | `background&motivation.tex:7` | BELOW — `\caption` at line 39, tabular ends line 38 |
| `AlgoCCPUMapping.tex` | no — commented out | `design.tex:237` | ABOVE — `\caption` at line 2, `\begin{algorithmic}` at line 4 (this is an `algorithm`, not a table) |
| `Jetson4090A100.tex` | no — never referenced from any active file | — | BELOW — `\caption` at line 17, tabular ends line 15 |

**The paper contains exactly one table.** `main.aux` records a single table label,
`tab:cache_results` → Table 1, on page 9.

The one included table already puts its caption **above** the tabular, which is the
IEEE/IISWC convention. `CachingTable.tex:17` still holds a commented-out duplicate
`\caption` below the tabular — a leftover from the move, harmless but worth removing.
The two orphaned tables would both need their captions moved above if they were ever
brought back in.

---

## 5. Camera-ready blockers in the preamble

**Reported only. None of these were changed.**

### 5.1 `showcomments`

- **Current:** `main.tex:161–162` — `\newboolean{showcomments}` / `\setboolean{showcomments}{true}`
- **Effect:** enables `\rishabh{...}` (blue "RJ:") and `\cyan{...}` (cyan "TODO Cyan:").
- **Measured:** the built PDF contains **zero** occurrences of "RJ:" or "TODO Cyan:", because
  no active `.tex` file calls either macro — the only hits are the definitions themselves
  at `main.tex:167` and `main.tex:173`.
- **Needs to become:** `false`. Note that `false` does not remove the text — both macros
  fall through to `\phantom{...}`, which still reserves the horizontal space. Setting it
  to `false` is necessary but not sufficient in general; here it is sufficient only
  because there are no call sites. Any `\rishabh`/`\cyan` added between now and the
  deadline must be deleted outright, not merely hidden.

### 5.2 `todonotes` package options

- **Current:** `main.tex:119` — `\usepackage[textsize=tiny]{todonotes}`
- **Line 118** already carries the disabled variant, commented out:
  `%\usepackage[disable,textsize=tiny]{todonotes}`
- **Effect:** `todonotes` is live and emits `Package todonotes Warning: The length
  marginparwidth is less than 2cm...`. No `\todo` call sites exist in any active file.
- **Needs to become:** the `disable` variant — swap the comment between lines 118 and 119.

### 5.3 `\creflabelformat` for `section` / `subsection`

- **Current:** `main.tex:141–142`
  ```latex
  \creflabelformat{section}{\S#2#1#3}
  \creflabelformat{subsection}{\S#2#1#3}
  ```
  together with `main.tex:137–138` (`\crefname{subsection}{section}{sections}`,
  `\Crefname{subsection}{Section}{Sections}`) and the package option `capitalise`.
- **Effect — verified two ways.** A minimal document reproducing exactly these lines
  renders `\Cref{sec:a}` as `Section §1` and `\Cref{sub:b}` as `Section §1.1`: the word
  *and* the section sign, both. Extracting the text layer of the actual `main.pdf`
  confirms **9 occurrences** of this duplication in the built paper — `Section §3` (×2),
  `Section §4`, `Section §4.`, `Section §4.1`, `Section §4.2`, `Section §4.3`,
  `Section §5.1`, `Section §5.8.`
- **Needs to become:** one of the two, not both. Either drop the two `\creflabelformat`
  lines and keep the spelled-out "Section N", or keep `§N` and remove the `\crefname` /
  `\Crefname` section naming so it renders as a bare `§N`. The existing `\xref` shorthand
  (`main.tex:197`, `\newcommand{\xref}[1]{\S\ref{#1}}`) already produces the bare `§N`
  form, so the two mechanisms currently disagree with each other.

### 5.4 `\title`

- **Current:** `main.tex:243`
  ```latex
  \title{Regular-MaestroRAG: Orchestrated Pipeline Architecture for Efficient RAG on Edge Devices\vspace{-20pt}}
  ```
- **Two problems.** The `Regular-` prefix is a submission-track marker, not part of the
  title — the built PDF's first page reads *"Regular-MaestroRAG: Orchestrated Pipeline
  Architecture for Efficient RAG on Edge Devices"*. And `\vspace{-20pt}` is embedded
  inside the title argument, so it is spacing smuggled through a semantic field.
- **Needs to become:** `\title{MaestroRAG: Orchestrated Pipeline Architecture for
  Efficient RAG on Edge Devices}`, with the vertical adjustment moved out of the title
  argument (or dropped) if it is still wanted.

### 5.5 Additional blockers found (not on the brief's list)

- **`main.tex:230–237` — the draft banner.** `\fancypagestyle{firstpage}` prints
  *"IISWC 2026 Submission #216 – Confidential Draft – Do NOT Distribute!!"* across the top
  of page 1. Verified present in the built PDF's text layer. This must go for a
  camera-ready.
- **No author block.** Three `LaTeX Warning: No \author given.`; `authblk` is commented out
  at `main.tex:47` and the author/affiliation scaffolding at `main.tex:255–268` is entirely
  commented. A camera-ready needs real authors and affiliations.
- **`main.tex:227` — `\iiswcsubmissionnumber{216}`** is only consumed by the draft banner
  above; it becomes dead once the banner goes.
- **`\red{...}` is live at `design.tex:143`.** `makeRed` is `false` (`main.tex:180`), so it
  currently renders black and is harmless — but it is a live revision marker in body text.

---

## 6. `refs.bib` vs. `reference.bib`

**`refs.bib` is the one in use.** `main.tex:508` is `\bibliography{refs}`; the Makefile's
`BIB` variable is `refs.bib`. `reference.bib` is referenced by nothing.

| | `refs.bib` | `reference.bib` |
|---|---:|---:|
| Entries | 249 | 71 |
| Unique keys | 249 | 71 |
| Duplicate keys | **0** | **0** |
| Keys shared with the other file | **0** | **0** |

**The two files have zero keys in common.** All 71 keys in `reference.bib` are named
`IEEEexample:*` (`IEEEexample:article_typical`, `IEEEexample:bibtexguide`, …) — it is the
stock IEEEtran demonstration bibliography that ships with the class, not a bibliography
for this paper. It is safe to regard as orphaned boilerplate.

### Citation integrity

41 distinct keys are cited from live (uncommented) lines in the active files. **All 41
resolve in `refs.bib`.** Zero undefined citations, zero duplicate keys.

### Malformed entry — one, in `refs.bib`

A whole-file brace count on `refs.bib` comes out unbalanced by one (2,067 `{` vs 2,068 `}`).
Traced to a single location:

```bibtex
@mastersthesis{ko94,          % refs.bib:2472
author = "Jacob Kornerup",
title = "Mapping Powerlists onto Hypercubes",
school = "The University of Texas at Austin",
note = "(In preparation)",
year = "1994"}
%month = "dec",}              % refs.bib:2478  <- stray closing brace
```

The entry itself closes correctly at line 2477. The extra `}` sits on line 2478, inside
what the author intended as a comment. **BibTeX is not affected:** `%` is not a comment
character in BibTeX, but text outside any `@entry` is ignored regardless, and `ko94` is
never cited. The build produces no error from it. Worth tidying; not urgent.

`reference.bib` is brace-balanced and has no malformed entries.

---

## 7. Summary of what was found but not changed

| # | Finding | Severity |
|---|---|---|
| 1 | `showcomments` is `true` | camera-ready blocker |
| 2 | `todonotes` loaded without `disable` | camera-ready blocker |
| 3 | `\Cref{sec:...}` renders `Section §N` — 9 occurrences in the built PDF | camera-ready blocker |
| 4 | Title carries a `Regular-` prefix and an embedded `\vspace{-20pt}` | camera-ready blocker |
| 5 | Page-1 banner reads "Confidential Draft – Do NOT Distribute!!" | camera-ready blocker |
| 6 | No `\author` block (3 warnings) | camera-ready blocker |
| 7 | Figure 6 (`power_energy_comparison.pdf`) is a data plot with no generating script | reproducibility gap |
| 8 | Figures 1 and 3a–3c have no generating script (hand-drawn — expected) | informational |
| 9 | 7 orphaned `.tex` files, 13 unused `Figs/*.pdf` | housekeeping |
| 10 | `reference.bib` is stock IEEEtran boilerplate, unused | housekeeping |
| 11 | `refs.bib:2478` stray `}` in a pseudo-comment | housekeeping |
| 12 | `CachingTable.tex:17` duplicate commented `\caption` below the tabular | housekeeping |
| 13 | 12 underfull hboxes at badness 10000, 10 of them beside the Jetson `wrapfigure` | typesetting |
| 14 | `\red{...}` live at `design.tex:143` (renders black; `makeRed` is `false`) | informational |
