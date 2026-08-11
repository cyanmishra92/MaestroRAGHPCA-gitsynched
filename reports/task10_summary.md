# Task 10 — retire the untraced flags and write the shepherd changelog

**Branch** `main` · **Commits** `a204167` (A), `35b3a4f` (B) · **Not pushed.**
**PDF of record** `reports/task10_main_20260810-1807.pdf` (`\revmode=1`, `\flagmode=1`, 13 pages)

---

## Part A — the four flag removals

All four values are internal measurements never entered into `MaestroRAGResults.xlsx`, which is why Task 9's trace could not reach them. **Each is closed by author confirmation, not by a workbook trace.** That distinction is recorded here and in the commit message so the basis of the decision stays on record: if the workbook is ever reconciled against the paper, these four will still not appear in it, and the reason is that they were never entered, not that they are wrong.

| Section | Location | Value(s) removed from the flag | Basis |
|---|---|---|---|
| 3.2 | `characterization.tex:91` | ≈30 MB cache capacity | Author confirmation |
| 4.1 | `design.tex:48` | 128 ms augment-separation cost | Author confirmation |
| 5.1 | `implementation&eval.tex:9` | ~70 % memory saving | Author confirmation |
| 5.5 | `implementation&eval.tex:156` | 5.26 s (1.04), 14.86 s (1.14), 14.41 s (1.09) | Author confirmation |

**Only the `\flag{...}` spans were removed.** The removal used a brace-balanced scanner rather than a regex, and the word-diff confirms nothing outside the four spans changed: no number, no sentence, no punctuation, no hedge added. Line lengths dropped by exactly the flag text (636→538, 421→313, 1113→1018, 534→221 characters).

The `\flag` macro itself remains defined in `main.tex:220-227`, since Part B needed it.

---

## Part B — the changelog

`docs/changelog.md`. Written for the author to post to HotCRP.

### Two renumberings the shepherd would otherwise trip over

The shepherd comment cites "Figure 6" and "Table 1". **Both now point at something else.** I verified this by enumerating the submitted version's float order from `dea2501`, including the `wrapfigure` that a naive `\begin{figure}` scan misses:

| Submitted (`dea2501`) | Now |
|---|---|
| Figure 5 — `fig:JetsonThemVsUs` (wrapfigure) | Figure 5, p.9 |
| **Figure 6 — `fig:powerEnergyPlot`** | **TABLE 3, p.9** (item 3) |
| **Figure 7 — `Fig:MainLatTputFigure`** | **Figure 6, p.11** |
| **TABLE 1 — `tab:cache_results`** (the only table) | **TABLE 4, p.10** (item 4) |

This confirms the reviews independently: Reviewer B complained about "the caption of Figure 7", which is the three-panel allocation/latency/throughput figure, and Reviewer C wrote "in TABLE 1, MaestroRAG incurs higher latency than EdgeRAG for similarity-match scenarios", which is the caching table. Both map exactly as above.

The changelog states both renumberings **before** the seven items, not buried inside them.

### Coverage check against the shepherd comment

Every request is quoted **byte-for-byte** (verified programmatically, including the source's curly quotation marks and em-dash), then answered.

| # | Request | Answered at | Status |
|---|---|---|---|
| 1 | latency breakdown | TABLE 2 p.7; §5.2 heading p.7, text p.8 | Complete |
| 2 | define "edge" | §2.1 p.2; TABLE 1 p.2; §5.1 p.7 | Complete |
| 3 | update Figure 6 with a breakdown | TABLE 3 p.9; §5.7 pp.9–10 | Complete, as a table; stated plainly |
| 4 | Table 1 similarity matching | §5.8 p.10; TABLE 4 p.10 | Complete |
| 5 | adaptive batching | close of §4.1, p.6 | Complete |
| 6 | Jetson/Orin trends | §3.3 p.4; back-reference §5.4 p.9 | Complete |
| 7 | writing and presentation | six sub-items below | One incomplete |
| 7a | table captions above | TABLE 1 p.2, TABLE 2 p.7, TABLE 3 p.9, TABLE 4 p.10 | Complete |
| 7b | Reviewer B's caption comment | Figure 6 caption, p.11 | Complete |
| 7c | font size in ALL figures | Figures 2, 4, 5, 6 | **Incomplete — Figures 1 and 3** |
| 7d | no white on light backgrounds | Figure 1, p.2 | Complete |
| 7e | "Results on" headings | §5.1–§5.9 | Complete |
| 7f | section symbols | throughout | Complete |

Formatting: 19 headings, zero tables, zero nested bullets, blockquotes for the quoted requests. No `\flag`, no `revmode`/`flagmode`, no task numbers. The word "blue" appears once, in the "How to read this revision" paragraph the task specified.

---

## Item 7c — the measured figure font status

Measured by parsing the built PDF directly: expanding its object streams, walking every page content stream and Form XObject recursively, and composing the text matrix with the accumulated CTM so the reported size is the **effective on-page** size, not the nominal `Tf` operand. The method cross-validates: it returns exactly 8.00 pt for the regenerated figures, which is independently known to be correct (`BASE = 8.0` at placement scale 1.0).

### Smallest text element per page

| Page | Smallest | Where | Note |
|---|---|---|---|
| 1 | 9.96 pt | body | |
| **2** | **4.22 pt** | **Figure 1** | 44 of 44 text ops below 8 pt |
| 3 | 9.96 pt | body | |
| **4** | **4.40 pt** | **Figure 3(c)** | 117 of 117 text ops below 8 pt |
| 5 | 8.33 pt | body | |
| 6 | 7.00 pt | body | inline-math subscripts in §4.2 ($N_P$, $N_E$), normal typography |
| 7 | 8.97 pt | body | |
| 8 | 8.00 pt | Figure 4 | |
| 9 | 8.00 pt | Figure 5 | |
| 10 | 8.18 pt | body | `\resizebox` on TABLE 4 |
| 11 | 8.00 pt | Figure 6 | |
| 12 | 8.00 pt | body | |
| 13 | 8.00 pt | body | |

### Per-figure attribution on the two crowded pages

| Object | Figure | Text ops | Min | Under 8 pt |
|---|---|---|---|---|
| `/Im1` p.2 | Figure 1 | 44 | 4.22 pt | 44 |
| `/Fm1`–`/Fm6` p.4 | Figure 2(a)–(f) | 15,12,9,14,12,9 | 8.00 pt | 0 |
| `/Fm7`, `/Fm8` p.4 | Figure 3(a),(b) | — | — | raster PNG, no text layer |
| `/Fm9` p.4 | Figure 3(c) | 117 | 4.40 pt | 117 |
| `/Fm10`–`/Fm15` p.8 | Figure 4(a)–(f) | 11–14 each | 8.00 pt | 0 |
| `/Im17` p.9 | Figure 5 | 18 | 8.00 pt | 0 |
| `/Fm16`–`/Fm18` p.11 | Figure 6(a)–(c) | 37,22,20 | 8.00 pt | 0 |

**All sixteen regenerated data panels are exactly 8.00 pt. Figures 1 and 3 are not fixed.**

Why not: Figure 1 is `Figs/ShepherdedMaestro.pdf` and Figure 3 is `diagrams/latency_oriented_pipeline.png`, `diagrams/throughput_oriented_pipeline.png` and `diagrams/pipeline_comparison_schematic.pdf`. A repository-wide search for `.svg`, `.drawio`, `.pptx`, `.ai`, `.fig`, `.odg` and `.vsdx` returns nothing. These are exported artifacts with no editable source, so they cannot be regenerated. The changelog says this in those terms and does not describe the intention as an accomplishment.

### The flag raised in the paper

One `\flag{}` was added, in the Figure 1 caption (`introduction.tex:181`). It is the only flag in the paper. It records three things:

- the measured 4.22 pt and 4.40 pt against the 8 pt requested, and that no editable source exists;
- that **panel (c) of Figure 3 reads "FlashFAG" for "FlashRAG"** — a typo I found while inspecting the rendered figure, in the same untouchable asset. It is not part of any shepherd request, so it is not in the changelog, but the author should fix it when the figure is remade;
- that **7d is already resolved**: Figure 1's labels are black, from the author's own commit `f1e4c9d` ("Changed Figure1 with the new version. Text black"), not from this work.

---

## Every location cited in the changelog, and how it was verified

Ghostscript's `txtwrite` interleaves two-column text and drops spaces at kerning boundaries, so a text-layer hit alone is not proof of location. Where the extraction was ambiguous or contradicted the `.aux`, **I rendered the page to an image and read it**. That is noted below.

| Claim | Page | Verified how |
|---|---|---|
| §2.1 "Deployment Scope", definition, unified-memory answer, 15 W / 4-of-12 cores | 2 | text layer |
| TABLE 1, caption above, A100 contrast | 2 | text layer |
| Figure 1, labels black on green | 2 | **rendered and read** |
| §2.3 rename to local/personal-computing platforms | 3 | text layer |
| §3.3 "Portability of these trends to embedded platforms", PCIe reason | 4 | text layer |
| Figures 2 and 3 | 4 | **rendered and read** |
| Close of §4.1, runtime core remapping as future work | 6 | text layer |
| §4.1 three-stage vs four-stage, 1.23× | 6 | text layer |
| TABLE 2 and its caption, top of right column | 7 | **rendered and read** |
| §5.1 platform justification, "Following §2.1 … two local/personal-computing platforms and one embedded device" | 7 | **rendered and read** |
| §5.2 heading closes p.7 | 7 | **rendered and read** |
| §5.2 text, per-baseline explanation, generation excluded, caching disabled | 8 | **rendered and read** |
| Figure 4, six panels | 8 | **rendered and read** |
| §5.3 heading "Latency on Personal-Computing Platforms" | 8 | **rendered and read** |
| §5.4, back-reference to §3.3, "up to 26 %" | 9 | **rendered and read** |
| §5.5, 2.5× / 3.0× / 4.4× | 9 | **rendered and read** |
| §5.6 Throughput, 0.288 / 0.683 / 1.185 / 0.432 / 0.0645 / 0.370 | 9 | **rendered and read** |
| TABLE 3, all rows, `n/r` markers, EdgeRAG excluded | 9 | **rendered and read** |
| Figure 5 | 9 | text layer + type measurement |
| §5.7 stage shares, idle-subtracted / DRAM excluded, groupings sentence | 10 | text layer |
| §5.7 peak CPU power 16.36 % / 8.08 %, 253.28 J/query | 10 | text layer |
| §5.8 exact vs similarity analysis, "not a RAM-capacity effect" | 10 | text layer |
| TABLE 4 and its caption (BS=1, TTL 300 s, 32 entries, 5 documents) | 10 | text layer |
| §5.9 ported optimizations, 1.38 vs 1.60 QPS, head-of-line blocking | 11 | text layer |
| §5.9 caching ablation states the 80 % hit rate | 11 | text layer |
| Figure 6 and its caption | 11 | text layer + type measurement |
| No "Figure 7" anywhere in the PDF | all 13 | text layer, all pages |

### Four claims I got wrong on the first pass and corrected

Recorded because they are the reason the render-and-read step exists:

1. I wrote that TABLE 2 and Section 5.2 were "both on page 7". The table is on page 7; the section's **text is on page 8**, with only the heading closing page 7.
2. I wrote that TABLE 2 marks an unreported cost with `n/r`. That is **TABLE 3's** convention. TABLE 2 uses an **empty cell**; its caption says so.
3. I listed TABLE 3's rows and **omitted peak GPU power**.
4. My first `\cite` scan reported `simThreshold`/`simThreshold2` as orphaned bibliography entries. The scanner was truncating lines at `\%` escapes; they are cited in §5.8. No defect existed.

---

## Verification

| Check | Result |
|---|---|
| `make` (clean, 3× pdflatex + bibtex) | **0 errors** |
| Page count | **13**, unchanged by both parts |
| Undefined references / citations | **0 / 0** |
| `grep -rn '\flag{'` | **1**, the deliberately raised figure-status flag |
| `\revmode=0, \flagmode=0` | builds, 13 pages, 0 undefined |
| `\revmode=0, \flagmode=1` | builds, 13 pages, 0 undefined |
| `\revmode=1, \flagmode=0` | builds, 13 pages, 0 undefined |
| `\revmode=1, \flagmode=1` | builds, 13 pages, 0 undefined — **restored to 1/1** |
| `verify_numbers` | 100 PASS / 0 FAIL / 1 UNVERIFIABLE, **no drift** |
| All 13 requests quoted verbatim | **13/13**, byte-for-byte |
| Changelog forbidden content | 0 flags, 0 revmode/flagmode, 0 task numbers |
| Changelog formatting | 0 tables, 0 nested bullets, 19 headings |
| `main.pdf` committed | **no** — `.gitignore:4` |
| Camera-ready formatting | **untouched** — `showcomments`, `todonotes`, author block and both switches exactly as they were |

---

## What I could not state truthfully, and therefore did not

- **That item 7c is done.** It is not. Figures 1 and 3 are at 4.22 pt and 4.40 pt and the changelog says so, names the two figures, gives both measurements, and states the reason. It commits only to supplying corrected versions, which is a promise the authors can keep, rather than claiming a fix that has not happened.
- **That the white-on-light-green fix was part of this revision's work.** It was the author's own commit `f1e4c9d`. The changelog reports the outcome, which is what the shepherd needs, and the flag records the provenance for the author.
- **That the similarity-match amortization claim is measured.** It is an expectation from the fixed-cost structure. The paper words it that way and the changelog repeats that qualification rather than smoothing it over.
- **That the four Part A values are workbook-traceable.** They are not, and this report says so. The changelog does not mention them at all, because their provenance is an internal matter and no shepherd request touches them.

## Left for the author

1. **Figures 1 and 3 need remaking** at ≥8 pt, from sources not in this repository. This is the only outstanding shepherd item.
2. **"FlashFAG" → "FlashRAG"** in Figure 3(c), same asset.
3. **Camera-ready switches.** Both are 1. Set both to 0 for the final submission; at `0/0` the paper renders in pure black with zero near-white glyphs, verified in Task 9.
4. **Task 8's C1 conflict** remains open and unchanged: the master plan asked that no `§` survive in cross-references, while you asked for `§2.1`. `§2.1` is what ships.
