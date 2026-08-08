# Task 7 — Summary

Two commits. **Parts A–D**: sixteen panels redrawn at print scale, Table 2 enlarged,
Figures 1 and 3 diagnosed. **Part E**: Figure 6 converted to a table.

**Page count: 13 (after Task 6) → 14 (Parts A–D) → 13 (Part E).**
**`verify_numbers.py`: 95/2/1 → 98 PASS / 2 FAIL / 1 UNVERIFIABLE, no drift.**

---

## 1. Part A — the sixteen panels

Every panel: canvas drawn at the width it prints at, **measured placement scale 1.0000**,
**smallest type 8.00 pt**, data verified identical.

| Fig | Panel | Canvas (in) | Printed (in) | Scale | Min type | Data |
|---|---|---|---|---:|---:|---|
| 2a | `stacked_graph` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 2b | `forwardpass_8cores` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 2c | `forwardpass_bs16_range_discrete` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 2d | `batchsize_stacked_linear_labeled` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 2e | `latency_cores` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 2f | `latency_dbsize` | 2.100 × 1.460 | 2.100 | 1.0 | 8.00 | PASS |
| 4a | `4090LatencyOurs` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 4b | `4090speedupEdgeRAG` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 4c | `4090speedupFlashRAG` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 4d | `4090speedupPipeRAG` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 4e | `4080Latency_MaestroRAG` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 4f | `4080Speedup_Merged` | 2.240 × 1.580 | 2.240 | 1.0 | 8.00 | PASS |
| 5 | `JetsonThemVsUs` | 2.194 × 1.860 | 2.194 | 1.0 | 8.00 | PASS |
| 6a | `cores_allocation_stacked` | 2.240 × 1.920 | 2.240 | 1.0 | 8.00 | PASS |
| 6b | `MainLatencyResults2` | 2.240 × 1.920 | 2.240 | 1.0 | 8.00 | PASS |
| 6c | `ThroughputResults` | 2.240 × 1.920 | 2.240 | 1.0 | 8.00 | PASS |

Before and after, smallest type on the page:

| Figure | Was | Now |
|---|---:|---:|
| 2 | 3.1 pt | **8.00 pt** |
| 7 (now 6) | 3.7 pt | **8.00 pt** |
| 4 | 4.1 pt | **8.00 pt** |
| 5 | already clear | **8.00 pt** |

Measured by walking the built PDF's content streams recursively, tracking the CTM through
each nested XObject, and multiplying every `Tf` size by the accumulated scale. Side-by-side
previews at true printed size are in `reports/task07_previews/`.

**New files:** `plots/cr/_origdata.py`, `plots/cr/regen_figures.py`,
`plots/cr/verify_data.py`, `plots/cr/plotted_values.json`, and 16 PDFs in `Figs/cr/`.
Nothing under `plots/MaestroRAG/Plots/` and nothing in `Figs/` outside `Figs/cr/` was
modified. All 16 regenerate **byte-identically** across runs.

### The Figure 2 aspect decision

**I dropped the `height=1in` override and let the canvas set the aspect.**

The old inclusion was `width=0.3\linewidth, height=1in` applied to a 5 × 3 in canvas: x
scaled by 0.420, y by 0.333. Glyphs were compressed about 21% vertically on top of being
shrunk, which is why the type read worse than its nominal size. The new canvas is
2.100 × 1.460 in and the `.tex` now carries width only, so the scale is uniform at 1.0.

**Cost:** each Figure 2 panel is 0.460 in taller than the 1.000 in box it replaced, so the
two-row figure grows by about 0.92 in. That is the single largest contributor to Parts A–D
taking the paper to 14 pages.

### Panels whose labels changed (permitted by Part 0)

- `1 mil` → `1M` in the Figure 4 legends, applied consistently.
- Figure 2a's x-ticks: `Encode/Retrieve/Augment/Generate` → `E/R/A/G`. The caption already
  names the stages.
- Figure 6a: the per-bar annotation was `BS:x\nTC:y`; the `TC:` line is dropped because the
  total core count **is** the bar height on a `# Cores` axis. The per-segment Encode and
  Retrieve counts the original printed inside the bars are retained.
- Figures 6a, 6b, 6c and 5: legends moved below the axes. Inside the frame at 2.24 in they
  overlapped the tallest bars and, in 6b, the clipped-bar annotations.

---

## 2. Part B — data verification, 16/16 PASS

**Nothing was transcribed.** `plots/cr/_origdata.py` executes each original script with
`savefig`/`show` stubbed and the working directory pointed at a scratch dir, then hands back
its module globals. The regenerated panels plot those objects, so equality is structural.

`plots/cr/verify_data.py` then checks it independently: it re-loads the originals in a fresh
process, rebuilds the expected values without reference to `regen_figures.py`, and diffs
them against `plotted_values.json`, a manifest of every number handed to a plotting call.

```
16/16 panels match the original data exactly
```

Every panel: *identical to the original script's arrays*.

---

## 3. Part C — Table 2

**6.5 pt → 9.0 pt**, measured on the page. Zero overfull boxes.

The `\resizebox{\linewidth}{!}` is gone, which was the entire cause: it shrank the tabular
to fit rather than fitting the tabular. Replaced with, in order of how invasive:

1. `{\small ...}` (9.03 pt in this class);
2. `\setlength{\tabcolsep}{3pt}`;
3. units moved from every cell into the caption ("Stage-level latency **in seconds**"), so
   cells read `0.20` rather than `0.20\,s`;
4. headings abbreviated: `Encode/Retrieve/Augment/Model loads/Scheduler / sync` →
   `Enc./Retr./Aug./Model loads/Sched. / sync`;
5. model-load cells shortened: `0.73\,s (encoder)` → `0.73 enc.`, `2.20\,s (LLM)` → `2.20 LLM`.

**No value changed.** Placement unaffected: still `[t]`, still page 7.

---

## 4. Part D — Figures 1 and 3, diagnosis only

Nothing was changed. All four files inspected as they sit in the repository.

### `Figs/RAGpipegrad.pdf` — Figure 1

| | |
|---|---|
| Type | **Vector PDF**, MediaBox 1099.9 × 337.9 pt (15.28 × 4.69 in) |
| Text objects | 36 text-setting ops, 119 show-text ops, at nominal 16 pt (×24) and 18 pt (×12) |
| Effective on page | **4.22 pt** and 4.75 pt |
| Fonts | one `/Type3` (bitmap, not embedded), two `/BAAAAA+Arial-BoldMT` `/Type0` |
| Rasters inside | **12 embedded images** |
| Palette | includes `#d5e8d4`, `#82b366`, `#9673a6`, `#e1d5e7`, which is the draw.io default set |

**White on light green, located.** Fill colour `#ffffff` is present alongside the light
greens `#d4ffbd`, `#c5ecaf`, `#afd29b`, `#d5e8d4` and the mid green `#82b366`. The
complaint is white text over one of those greens.

**Verdict: editable, but not cleanly.** The Arial-BoldMT text is real text and extractable,
so Inkscape can retype and recolour it. But the `/Type3` font is a bitmap font that will not
survive editing well, and 12 embedded rasters mean parts of the diagram are pictures, not
shapes. The palette says this came out of **diagrams.net (draw.io)**. If the `.drawio`
source exists, this is a twenty-minute fix: recolour the white text, enlarge the type, and
re-export at a sane canvas size. Without it, budget a redraw.

### `diagrams/pipeline_comparison_schematic.pdf` — Figure 3c

| | |
|---|---|
| Type | **Vector PDF**, 440 × 251 pt (6.11 × 3.49 in) |
| Fonts | `Calibri` and `Calibri-Bold`, **both embedded TrueType** |
| Text objects | 117 show-text ops, `Tf 1.0` with the size carried in the text matrix (`Tm` y-scale 55.0) |
| Effective on page | **≈ 4.4 pt** |
| Rasters inside | none |

**`FlashFAG` confirmed.** `extract_text()` returns `FlashFAG`, `PipeRAG` and `EdgeRAG`;
`FlashRAG` does not appear. The typo is in a real, editable text object.

**Verdict: fully editable.** Embedded TrueType, no rasters, text extractable. Fixing the
typo and enlarging the type is an Inkscape session. Calibri points at PowerPoint or Visio as
the origin, so the source may exist too.

> **Correction to my own measurement.** The recursive scanner reports 0.08 pt for this
> figure because it tracks the CTM but not the text matrix, and this file puts the size in
> `Tm`. The true effective size is `Tf 1.0 × Tm 55.0 × CTM`, about **4.4 pt**. The 0.08 pt
> figure in the raw scan output is an artifact, not a finding.

### `diagrams/latency_oriented_pipeline.png` — Figure 3a

| | |
|---|---|
| Type | **Raster**, RGBA, 1947 × 737 px |
| Effective DPI at 2.240 in | **869 dpi** |
| Smallest text | the `Core` chip labels, ~70 px → **5.80 pt** on the page |
| Largest text | the stage letters `E`, `R`, `G`, ~110 px → 9.11 pt |

### `diagrams/throughput_oriented_pipeline.png` — Figure 3b

Same class: RGBA 1927 × 767 px, **860 dpi**, same label sizes.

**Verdict for 3a and 3b: not editable, but not urgent.** Resolution is ample; the problem
is design size, not DPI, so upsampling would not help. The main stage labels already clear
9 pt. Only the small `Core` chips fall short at 5.8 pt. If the source exists, enlarging
those chips is a small edit; if not, they are the only part that needs redrawing.

**Summary of the remaining figure work:** Figure 3c is an afternoon. Figure 1 is an
afternoon **if** the draw.io source turns up, and a redraw if it does not. Figures 3a and 3b
need only their smallest labels enlarged.

---

## 5. Part E — Figure 6 becomes Table 3

### The table

`TablesAlgos/PowerEnergy.tex`, single column, caption above, `\label{tab:power_energy}`,
`\small` at **9.0 pt**. It reproduces the brief's values exactly, with three section rules
separating power, energy and shares.

The fused-cell convention matches Table 2: FlashRAG's 79.2 and MaestroRAG's 83.2 are
`\multirow{2}{*}` cells spanning the Retrieve and Augment rows, so the spans read as
"reported together" rather than as missing data. PipeRAG reports all three separately, so
its 64.5 and 0.0 sit in their own rows.

**FlashRAG's absent encode share** is marked `n/r`, with the caption defining it as *not
separately reported*. That is the rebuttal's own asymmetry: FlashRAG has a fused
encode-plus-retrieve entry in Table 2 but no encode share in the energy figures.

The caption states the configuration (BS=2, DB=4M, top-k=5), the measurement boundary (CPU
package and GPU board; shares of idle-subtracted CPU package energy, DRAM excluded), the
EdgeRAG exclusion, the FR/PR/MR key, the `n/r` key, and the rounding note (**the shares sum
to 100.1, 100.5 and 99.9 percent**).

### Wiring

The whole `figure*` block is commented out line by line with `% CR-REPLACED:`, so the
conversion is reversible by uncommenting. **Both `Figs/cr/fig6_power_energy_breakdown.pdf`
and `plots/cr/fig6_power_energy.py` are kept**; the script remains the derivation record for
the per-query CPU and GPU split the table now reports.

Prose change, the only one:

> The power and energy measurement results are ~~plotted in `\Cref{fig:powerEnergyPlot}`~~
> **reported in `\Cref{tab:power_energy}`**.

No other sentence described the panel layout, so nothing else needed rephrasing. **No claim
and no number changed.** The Task 6 sentence "…rather than as a decomposition of the
absolute totals above" still reads correctly, since the totals now sit above the shares
within the table.

### Renumbering, verified

| | Before | After |
|---|---:|---:|
| Figure 7 (Key findings) | 7 | **6** |
| Table: power and energy | — | **3** (new) |
| Table: latency with caching | 3 | **4** |

Every `TABLE n` and `Figure n` in the built PDF was extracted with its surrounding prose and
checked against the intended target. All correct:

- `TABLE 1` caption *Platform specifications* / `TABLE 1 sets both against` in §2.1 ✅
- `TABLE 2` caption *Stage-level latency* / `TABLE 2 decomposes the per-stage cost` ✅
- `TABLE 3` caption *Power and energy* / `reported in TABLE 3. MaestroRAG significantly out…` ✅
- `TABLE 4` caption *Latency with caching* / `TABLE 4 reports the results of our caching mechanisms` ✅
- `Figure 6` caption *Key findings* / `Figure 6b reports end-to-end latencies`, `Figure 6c` throughput ✅
- Figures 1, 2a–2f, 3a–3c, 4a–4f, 5 all resolve to their own captions ✅

### Page area recovered

The `figure*` occupied **7.000 × 2.620 in = 18.34 in²** of the text block, plus a five-line
caption. The table occupies roughly **3.375 × 2.1 in ≈ 7.1 in²** of one column, plus its
caption. **Net recovery is about 11 in², a little over half a page**, and it is what takes
the paper from 14 pages back to 13.

### The consequence, for the response letter

**Shepherd Item 3's breakdown now appears as Table 3, not as an updated Figure 6.** The item
asked to "update Figure 6 to include a breakdown" and suggested a vertical rule to separate
the two y-axes. The response should say plainly that the breakdown is present and the
axis problem is dissolved rather than mitigated, because a table has no axes; and that the
stage-level decomposition the item asked for is in the third block of Table 3.

---

## 6. Verification

| Check | Result |
|---|---|
| `make` | **exit 0**, **13 pages**, 0 overfull boxes |
| Undefined references / citations | **0 / 0** |
| Type inside regenerated figures | **8.00 pt** everywhere, scale 1.0000 |
| Table 2 / Table 3 | **9.0 pt** / **9.0 pt** |
| Only figures still under 8 pt | Figure 1 (4.22 pt) and Figure 3c (≈4.4 pt), both scriptless, Part D |
| Part B data comparison | **16/16 PASS** |
| Script determinism | 16/16 byte-identical on a second run |
| `verify_numbers.py` | **98 PASS / 2 FAIL / 1 UNVERIFIABLE**, no drift |
| Revision modes | 11 pages differ, all **100% blue** at `\revmode=1`, **RGB(0,0,0)** at `=0`, zero near-white |
| `refs.bib` / `reference.bib` | byte-identical to pre-Task-2 |
| `plots/MaestroRAG/Plots/` | untouched |
| `Figs/` outside `Figs/cr/` | untouched |
| All 41 references render | ✅ |

The two remaining FAILs are still the Jetson 25–35% band and the 4080 FlashRAG truncation.
Three checks added for Table 3's total-energy row; the 28 Task 6 checks were repointed from
the figure to the table's cells so the printed literals are covered.

### Float placement

| Float | End of Task 6 | Parts A–D | **Part E** |
|---|---:|---:|---:|
| Figure 2 *Characterizations* | 4 | 4 | 4 |
| Figure 3 *MaestroRAG pipeline* | 4 | 4 | 4 |
| Figure 4 *Speedup* | 8 | 8 | 8 |
| Figure 5 *Jetson latency* | 8 | 9 | 9 |
| Figure 6 *Key findings* (was 7) | 10 | 11 | 11 |
| Table 1 *Platform specifications* | 2 | 2 | 2 |
| Table 2 *Stage-level latency* | 7 | 7 | 7 |
| Table 3 *Power and energy* | 10 (as Fig 6) | 10 | **9** |
| Table 4 *Latency with caching* | 9 | 10 | 10 |
| References begin | 12 | 12 | 12 |

### PDF

Not committed. Timestamped copy: **`reports/task07_main_20260808-1600.pdf`**.

---

## 7. Things that contradict the instructions, or that you should decide

### 7.1 Figure 5 does not print at 3.041 in; it prints at about 1.97 in

The brief computes Figure 5's width as `0.9 × \columnwidth = 3.041 in`. It is **inside a
`wrapfigure` of `0.65\linewidth`**, so `\linewidth` within it is already 0.65 × column, and
`0.9\linewidth` gives **0.9 × 0.65 × 3.375 = 1.974 in**. The measured placement scale
confirmed it: the first regenerated version came out at exactly 0.65.

I sized the canvas to the true printed width and changed the inclusion from
`width=0.9\linewidth` to `width=\linewidth` **within the wrapfigure**, giving 2.194 in,
which is the most room available without changing the wrapfigure itself. If you would
rather Figure 5 were larger, widening the `wrapfigure` from `0.65\linewidth` is the lever,
and the canvas constant in `regen_figures.py` follows it.

### 7.2 A data discrepancy in Figure 2d, reported and left

`stackedLatencyMotivation.py`, which produces Figure 2d, plots for **BS=2**: index fetch
3.36 s, similarity search 0.60 s. The `Motivation` tab records for that point **0.60 s index
fetch and 4.408 s similarity search** (`Motivation!E16`, `!F16`). The two components look
swapped, and the fetch is flat at 3.36 s for BS=4–32 in both.

This also bears on the prose: §3.2 says *"index fetch dominates latency at small batch
sizes"*, which the workbook supports and the figure contradicts.

**The regenerated panel reproduces the original script exactly**, as Part 0 requires. Not
fixed, not silently corrected. This is the master plan's conflict C1 and it needs your call.

### 7.3 Parts A–D alone take the paper to 14 pages

Legible type costs vertical space: Figure 2 grew about 0.92 in from dropping the
non-uniform scaling, and the three Figure 6 panels grew to fit their legends below the axes.
Part E gives the page back. **If you ever revert Part E, the paper returns to 14 pages.**

### 7.4 My first measurement of Figure 3c was wrong, and I have corrected it

The recursive scanner tracks the CTM but not the text matrix. Figure 3c sets `Tf 1.0` and
carries the size in `Tm`, so the raw scan reported 0.08 pt. The real figure is ≈4.4 pt. The
sixteen regenerated panels are unaffected: they set real `Tf` sizes and use an identity text
matrix, and their 8.00 pt readings are correct.

### 7.5 Figure 1 and Figure 3 remain below 8 pt

Unavoidable in this task: they have no generating scripts, and Part D is diagnosis only.
After Task 7 the paper's figure legibility is uniform at 8 pt **except** for Figure 1
(4.22 pt) and Figure 3c (≈4.4 pt), with Figure 3a/3b's small chip labels at 5.8 pt. Part D
above says what each one needs.

### 7.6 Toolchain

`matplotlib`, `pandas`, `seaborn` and `pypdf` were installed in a throwaway venv at
`/tmp/mrvenv`, because this machine's Python is PEP 668 managed and refuses `pip install`.
The venv is outside the repository and is not committed. The scripts themselves are ordinary
and have no unusual dependency, but `seaborn` is needed because the regenerated panels reuse
the originals' `pastel` palette rather than substituting colours.
