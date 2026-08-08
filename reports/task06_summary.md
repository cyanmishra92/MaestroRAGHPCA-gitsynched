# Task 6 — Summary

Shepherd Item 3: Figure 6 rebuilt with a stage-level energy breakdown, a power/energy
dividing rule, explicit axis labels, and type that is 8 pt on the page. Section 5.6
rewritten with the stage shares, the measurement boundary, and the reason EdgeRAG is
excluded. Three known-failing numeric checks corrected.

**`verify_numbers.py` moves from 64/5/1 to 95 PASS / 2 FAIL / 1 UNVERIFIABLE.**
**Page count unchanged at 13.**

---

## 1. The script

**`plots/cr/fig6_power_energy.py`** (new, 231 lines). Nothing under
`plots/MaestroRAG/Plots/` was touched; `git status` on `plots/` shows only the new
untracked `plots/cr/`.

Output: **`Figs/cr/fig6_power_energy_breakdown.pdf`**, SHA-256
`2afd232a5f34e43962b48c43e1016f8c57486f9e76c8a2decd7a91e5da307136`. `git status` on
`Figs/` shows only the new untracked `Figs/cr/`; no existing figure was modified.

A rendered preview is saved alongside this report as
**`reports/task06_figure6_preview.png`**.

### Design decisions

| Decision | Reasoning |
|---|---|
| Four panels, not a redesigned dual axis | The shepherd asked for a breakdown *and* suggested separating the two axes. Four single-purpose axes remove the dual-axis problem entirely rather than annotating around it. |
| Canvas drawn at the printed size | 7.000 in canvas included at `\linewidth` inside a `figure*` gives a scale factor of exactly 1.0, so an 8 pt label prints at 8 pt. Inflating fonts on an oversized canvas, which is what the existing scripts do, also thins the line weights. |
| Promoted to `figure*` | At the old 0.8\linewidth (2.703 in), four panels would be 0.6 in each. Unreadable. See §6 for the page-flow consequence. |
| Energy per query, not per window | Section 5.6 quotes per-query joules. A figure reading 254.2 beside prose reading 253.3 invites exactly the confusion the shepherd is trying to remove. The axis says "Energy per query (J)". |
| CPU and GPU energy stacked in panel 3 | The stack totals are 792, 781 and 253 J, which are the numbers the prose quotes. The figure and the sentence now show the same quantity. |
| Composition normalized on its own axis | See §5. |
| All fills light, all text `#1a1a1a` | The white-on-light-fill complaint about Figure 1 must not be reintroduced. The script contains no white colour at all. |

### Reproducibility

`SOURCE_DATE_EPOCH` is pinned inside the script, so the PDF carries no varying
CreationDate. **Two consecutive runs produce byte-identical output** (`cmp` clean).

**One environment caveat.** This machine's Python is PEP 668 managed, so
`pip install matplotlib` is refused. I created a venv at `/tmp/mrvenv` and ran the script
with it. The script itself is unaffected and standard; it needs only `matplotlib`. The venv
is outside the repo and is not committed.

---

## 2. The figure, panel by panel

Left to right, with a vertical rule between panels 2 and 3, and bold section headings
**Power** and **Energy** above each half.

| Panel | Content | Axis |
|---|---|---|
| 1 | Average power, CPU and GPU bars per system, values labeled above each bar | "Average power (W)", 0 to ~109 |
| 2 | Peak power, CPU and GPU bars per system, values labeled | "Peak power (W)", 0 to ~328 |
| — | **Vertical rule**, full height | separates the two axis families |
| 3 | Energy per query, CPU stacked below GPU, stack total labeled above | "Energy per query (J)", 0 to ~966 |
| 4 | CPU energy composition by stage, normalized stacked bars, segments ≥ 9% labeled in-bar | "Share of attributed CPU energy (%)", 0 to 108 |

Two legends on a row above the headings: CPU/GPU on the left, the four stage categories on
the right. Below the panels, in the figure itself: *"EdgeRAG excluded: its on-demand
embedding path performs additional, non-equivalent work."* The exclusion is visible in the
figure, not only in the caption.

Plotted values, in order FlashRAG / PipeRAG / MaestroRAG:

- Average power CPU 48.3 / 62.72 / 42.37, GPU 83.67 / 58.48 / 42.06
- Peak power CPU 184.2 / 171.09 / 158.3, GPU 244.8 / 252.43 / 244.4
- Energy per query CPU 289.80 / 407.62 / 127.10, GPU 502.20 / 373.305 / 126.18, totals **792 / 781 / 253**
- Composition FlashRAG 79.2 R+A, 19.1 generation-driving, 1.8 other; PipeRAG 20.4 E, 64.5 R, 0 A, 15.6 G; MaestroRAG 5.5 E, 83.2 RA, 11.2 G

---

## 3. Scale factor and measured type size

Measured from **the built `main.pdf`**, not from the source, by walking page 10's XObject
resources with `pypdf`:

| Measurement | Value |
|---|---|
| Figure form BBox | `[0, 0, 504, 188.64]` PDF pt |
| `\textwidth` | 505.89 TeX pt = 504.000 PDF pt |
| **Placement matrix scale** | **sx = 1.00000, sy = 1.00000** |
| Distinct `Tf` font sizes inside the form | **{8.0, 8.5, 9.0}** |
| Text-setting operations counted | 67 |
| **Smallest text element on the page** | **8.0 pt** (tick labels, in-bar values, legend, the exclusion note) |

8.5 pt is used for axis labels and 9.0 pt for the two section headings. **Nothing falls
below 8 pt.** Because the scale is exactly 1.0, the sizes inside the figure are the sizes
on the page with no conversion.

For contrast, the old figure was drawn on a 5 to 7 in canvas and placed at 2.703 in, a
scale factor of roughly 0.39 to 0.54, which is what put 10 pt labels on the page at about
4 to 5 pt.

---

## 4. New caption and rewritten Section 5.6

### Figure block, `implementation&eval.tex`

```latex
\begin{figure*}[t]
    \centering
% CR-REPLACED: \includegraphics[width=0.8\linewidth]{Figs/power_energy_comparison.pdf}
    \includegraphics[width=\linewidth]{Figs/cr/fig6_power_energy_breakdown.pdf}
    \caption{\new{Power and energy on the Intel i9-14900K platform with an RTX\,4090 GPU
    at \texttt{BS=2}, \texttt{DB=4\,M}, and \texttt{top-k=5}. Left of the rule, average and
    peak power for the CPU and the GPU. Right of the rule, energy per query and the
    composition of CPU energy by pipeline stage. Power and energy are measured at the CPU
    package and at the GPU board. The composition is a share of idle-subtracted CPU package
    energy with DRAM excluded, so it is drawn on its own normalized axis rather than
    stacked onto the absolute joules beside it. \edgeRAG{} is excluded throughout.}}
    \label{fig:powerEnergyPlot}
    \vspace{-10pt}
\end{figure*}
```

The old `\includegraphics` is retained on a `% CR-REPLACED:` line, and
`Figs/power_energy_comparison.pdf` still exists untouched. `grep -rn "CR-REPLACED"` finds
every figure substitution.

### Section 5.6 changes

Corrections, each wrapped so the changed numeral is the blue span:

> …only consuming $253.3J/query$, compared to `\new{`$792.00J$`}` and $780.92J/query$ for
> FlashRAG and PipeRAG, respectively. Moreover, FlashRAG and PipeRAG exhibit
> `\new{`$16.36\%$`}` and `\new{`$8.08\%$`}` higher peak CPU power usage, respectively.

New sentences:

```latex
\new{Attributing CPU package energy to pipeline stages, after subtracting idle package
power and with DRAM excluded, gives $79.2\%$ retrieval and augmentation, $19.1\%$
generation-driving, and $1.8\%$ other for FlashRAG; $20.4\%$ encoding, $64.5\%$ retrieval,
$0\%$ augmentation, and $15.6\%$ generation for PipeRAG; and $5.5\%$ encoding, $83.2\%$
fused retrieval and augmentation, and $11.2\%$ generation for MaestroRAG. These shares are
of idle-subtracted energy, so they are reported as proportions rather than as a
decomposition of the absolute totals above.}
```

Appended to the EdgeRAG exclusion paragraph:

```latex
\new{Because that path performs additional, non-equivalent work, a per-stage energy
attribution for \edgeRAG{} would not be comparable with the other three systems.}
```

All of it verified present in the built PDF.

---

## 5. Sentence-by-sentence provenance

**R** = rebuttal · **P** = paper · **W** = `PowerComp` tab (authorised) · **T** = task brief.

| # | Sentence | Derives from |
|---|---|---|
| 1 | "…compared to $792.00J$…" | **W** `(C6 + C7)/2 = (579.60 + 1004.40)/2`. Correction directed by **T**; replaces 791.8. |
| 2 | "…exhibit $16.36\%$ and $8.08\%$ higher peak CPU power…" | **W** `(C4 - E4)/E4` = 16.36, `(D4 - E4)/E4` = 8.08. Corrections directed by **T**. |
| 3 | "Attributing CPU package energy to pipeline stages, after subtracting idle package power and with DRAM excluded, gives …" | **R**: *"After subtracting idle package power, stage-attributed energy shares (DRAM excluded) are FlashRAG: 79.2% R+A, 19.1% generation-driving, 1.8% other; PipeRAG: 20.4% E, 64.5% R, 0% A, 15.6% G; MaestroRAG: 5.5% E, 83.2% RA, 11.2% G."* All ten shares verbatim. The boundary clause is the rebuttal's own, and is the binding promise in protocol §5 item 2. |
| 4 | "These shares are of idle-subtracted energy, so they are reported as proportions rather than as a decomposition of the absolute totals above." | Connects **R**'s boundary to **W**'s idle-inclusive joules. Asserts no mechanism; states why the two are kept apart. |
| 5 | "Because that path performs additional, non-equivalent work, a per-stage energy attribution for EdgeRAG would not be comparable with the other three systems." | **R**: *"EdgeRAG is excluded because its on-demand embedding path performs additional, non-equivalent work."* The paper already described the on-demand path; this states the consequence for attribution, which is what the exclusion needed. |
| — | Caption sentences 1 and 2 (configuration, panel layout) | **P** the pre-existing caption (BS=2, DB=4M, top-k=5) plus the new panel structure |
| — | Caption sentence 3 (measurement at CPU package and GPU board) | **P** §5.6: turbostat reads *"package- and core-level"* CPU power; `nvidia-smi` reads *"on-board power sensors"* |
| — | Caption sentence 4 (composition normalized separately) | **R** boundary; the reasoning in §5 below |
| — | Caption sentence 5, and the in-figure note | **R** the exclusion sentence |

**Every sentence maps.**

### Provenance of every plotted value and prose numeral

| Value(s) | Source |
|---|---|
| 48.30, 62.72, 42.37 | **W** `PowerComp!C2, D2, E2` |
| 83.67, 58.48, 42.06 | **W** `C3, D3, E3` |
| 184.20, 171.09, 158.30 | **W** `C4, D4, E4` |
| 244.80, 252.43, 244.40 | **W** `C5, D5, E5` |
| 289.80, 407.62, 127.10 | **W** `C6/2, D6/2, E6/2` (per query, BS=2) |
| 502.20, 373.305, 126.18 | **W** `C7/2, D7/2, E7/2` |
| 792, 781, 253 (stack totals) | sums of the two rows above; 792.00 and 253.28 are already in **P** §5.6 |
| 79.2, 19.1, 1.8, 20.4, 64.5, 0, 15.6, 5.5, 83.2, 11.2 | **R**, the stage-share sentence, verbatim |
| 16.36, 8.08 | **W**, derivations above; both directed by **T** |
| BS=2, DB=4M, top-k=5 | **P**, the pre-existing caption |

All 28 are now covered by checks (§7). `refs.bib` and `reference.bib` untouched.

---

## 6. How the normalized-versus-absolute question was resolved

**Drawn normalized, in its own panel, on a percent axis.** The absolute joules stay in
panel 3 and the two are never combined.

The reasoning, which the task set out and I verified independently:

- `PowerComp` energy is **idle-inclusive**. 579.60 J / 48.30 W = 12.000 s exactly, which is
  the measurement window, so idle package draw is inside that joule figure.
- The rebuttal's shares are of **idle-subtracted** CPU energy, DRAM excluded.
- The idle-subtracted totals appear in no source, so the two cannot be reconciled.

Stacking the shares onto the joule bars would assert that they partition a quantity they do
not partition, and the error would be exactly the idle fraction, which is unknown. The
normalized panel makes the claim the rebuttal actually supports: the *proportions* of
attributed energy. Panel 4's axis says "Share of attributed CPU energy (%)", the caption
says the composition is of idle-subtracted energy, and the prose repeats it.

**A consequence worth stating.** The figure therefore does not let a reader convert a share
into joules. That is correct rather than unfortunate: the conversion is not available from
any source, and a figure that invited it would be wrong.

**The shares do not sum to 100.** FlashRAG 100.1, PipeRAG 100.5, MaestroRAG 99.9. This is
the rebuttal's own rounding. **I did not renormalize**, since that would replace the
authors' numbers with derived ones. The panel's y-limit is 108 so the over-100 bars are not
clipped. The discrepancy is at most 0.5 percentage points and is not visible at print size.

---

## 7. Verification

### Build

| | |
|---|---|
| `make` | **exit 0**, **13 pages** |
| LaTeX errors | **0** |
| Undefined references / citations | **0 / 0** |
| All 41 references render | ✅ |

### `verify_numbers.py`

```
checks : 95 PASS / 2 FAIL / 1 UNVERIFIABLE
drift  : none
```

Target was 66/2 or better. **Three checks moved FAIL → PASS**: `energy_per_query_flashrag`
(791.8 → 792.00), `peak_cpu_power_delta_flashrag` (16.45 → 16.36),
`peak_cpu_power_delta_piperag` (8.22 → 8.08). Their `known_defect` notes were removed and
their `expect` anchors updated.

**The two remaining FAILs are exactly the two that belong to the corrections task:**
`jetson_overhead_reduction_band` (the 25–35% claim) and `speedup_4080_flashrag_bs8` (the
1.9× truncation). The one UNVERIFIABLE is still the cold-start total. Untouched.

**28 checks added**, covering every value the figure plots:

| Group | Count | Anchored to |
|---|---:|---|
| Panels 1–3, power and per-query energy | 18 | `PowerComp` cells, with `v / 2` derivations for per-query |
| Panel 4, stage shares | 10 | the rebuttal sentence, by regex, `origin: rebuttal` |

**A harness characteristic worth recording.** `claimed` in `checks.yaml` is a manual
transcription of what the paper prints. Correcting the paper alone did **not** flip the
three checks to PASS; I had to update `claimed` in the YAML in lockstep. That is the
intended design (the check compares a transcribed claim against a source), but it means a
future corrections task must edit both sides, and the drift detector will not notice if
only the paper changes.

### Type size

Measured from `main.pdf`: placement scale **1.00000**, smallest `Tf` **8.0 pt**. See §3.

### Determinism

Two consecutive runs of the script produced **byte-identical** PDFs.

### Scope

```
git status --porcelain Figs/ plots/
  ?? Figs/cr/
  ?? plots/cr/
```

Nothing under `plots/MaestroRAG/Plots/` modified. No existing file in `Figs/` modified.

### Revision modes — pixel-verified

Nine pages carry new text, all **100 percent blue at `\revmode=1`, pure RGB(0,0,0) at
`\revmode=0`, zero near-white, zero non-blue ink**:

pages 1, 2, 4, 5, 7, 8, 9, **10 (Figure 6 caption)**, **11 (§5.6 prose)**.
Pages 3, 6, 12, 13 pixel-identical. `\revmode` restored to `1`.

The figure image itself cannot be colored; the `\new{}` caption is the signal that it
changed, as the brief specified.

### White text

The script specifies **no white colour anywhere**. Every fill is a light hex
(`#9ecae1`, `#fdbe85`, `#a6cee3`, `#b2df8a`, `#fdbf6f`, `#cab2d6`, `#dddddd`) and every
text element uses `INK = #1a1a1a`.

### Style

| | Count |
|---|---:|
| Text added by Tasks 2–6: `---`, `—`, non-range `--` | **0 / 0 / 0** |
| Pre-existing prose: `---` / `—` | 4 / 6 (10, unchanged) |

### Page count and float placement

**13 pages, unchanged.** The figure moved from a single-column `figure` (2.703 in wide) to
a full-width `figure*[t]` (7.000 in), landing at the top of page 10. It remains Figure 6.

| Landmark | Task 5 | **Task 6** |
|---|---:|---:|
| §5.2 Stage-Level Latency Breakdown | 7 | 7 |
| §5.5 Main Latency, §5.6 Throughput, §5.7 Power, §5.8 Caching | 9 | 9 |
| §5.9 Additional Insights | 10 | **11** (+1) |
| §6 Related Work, §7 Conclusions | 11 | **12** (+1) |
| References begin | 12 | 12 |

The back third shifted one page; the reference list absorbed it and the total held at 13.

### Bibliography

Byte-identical to the pre-Task-2 state:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

### PDF

Not committed (gitignored). Timestamped copy: **`reports/task06_main_20260808-1505.pdf`**.

---

## 8. Things that contradict the instructions, or that you should decide

### 8.1 The figure is now double-column, which is a structural change

The brief permitted it and asked for the consequence. At 0.8\linewidth the four panels
would be 0.6 in each, which cannot carry 8 pt type. **The cost:** a `figure*` can only
float to the top of a page, so it has less placement freedom, and it occupies roughly
16.4 in² against the old figure's 4.6 in². The back third of the paper moved one page
later; the total held at 13 because the reference list had room.

If you would rather keep it single-column, the workable alternative is a 2 × 2 grid on a
3.379 × 3.0 in canvas. It uses less page area but each panel is 1.5 in, so the tick labels
would need shortening. Say the word and it is a layout change in the same script.

### 8.2 matplotlib is not installable on this machine's system Python

PEP 668 refuses `pip install`. I used a venv at `/tmp/mrvenv`, which is outside the repo
and not committed. **Anyone regenerating the figure needs matplotlib available**; the
script itself is ordinary and has no other dependency. If you want the environment pinned,
a two-line `plots/cr/requirements.txt` would do it, but I did not add files the brief did
not ask for.

### 8.3 One stage share is invisible, and one is unlabeled

- **PipeRAG's Augment share is 0%.** It contributes no visible segment and I omitted it
  from the legend rather than showing a category that never appears. The prose states the
  0% explicitly, so it is not lost.
- **MaestroRAG's 5.5% Encode segment is drawn but not labeled in-bar**, because 8 pt text
  does not fit in a segment that short. The threshold is 9%. The colour, the legend and the
  prose all carry it.

### 8.4 The per-query CPU/GPU split is a derivation

The paper already reports per-query *totals* (253.3, 780.92, and now 792.00). Panel 3 also
splits each total into its CPU and GPU parts per query, which means dividing each component
by 2 rather than only the sum. The division is the same one the paper already applies, and
the brief directed the per-query basis, but it is worth naming: **the per-query CPU and GPU
components are not stated anywhere; only their sums are.** All six are checked against
`PowerComp` with an explicit `v / 2` derivation.

### 8.5 One summary sentence withheld

I considered adding "Retrieval dominates in all three systems" after the share list. It is
a true reading of 79.2, 64.5 and 83.2, but the rebuttal draws no such conclusion, and
protocol §2 forbids replacing the rebuttal's framing with a better-sounding one. **Left
out.** If you want it, it is one clause and it is defensible.

### 8.6 Figure 1 is still the other white-on-light-fill complaint

The brief told me not to reintroduce white-on-light in this figure, and I have not. But the
shepherd's original complaint named **Figure 1**, which is the hand-drawn `RAGpipegrad.pdf`
with no generating script (Task 1's report, §3). **Nothing in Tasks 1 through 6 has
addressed it**, and it cannot be fixed by a script since none exists. That is the remaining
Item 7 figure work and it needs the original drawing source.
