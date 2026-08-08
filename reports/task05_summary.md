# Task 5 — Summary

Shepherd Item 1 (stage-level latency breakdown) and the rebuttal's answer to the common
concern (the ported-optimization experiment). One new table file, one new subsection, one
new paragraph, two one-clause back-references, 19 new rebuttal-anchored checks.

**Page count is unchanged at 13.**

---

## 1. Full text of everything added

### 1.1 The table, `TablesAlgos/LatencyBreakdown.tex` (new file)

```latex
\begin{table}[t]
\centering
\caption{\new{Stage-level latency on the RTX\,4090 at \texttt{DB=4\,M} and \texttt{BS=8},
with caching disabled. Generation is excluded because its settings are common to all four
systems. A spanned cell marks stages a system measures together: \design{} and \edgeRAG{}
fuse retrieval and augmentation (\Cref{subsec:pipeline_design}), while \flashRAG{} fuses
encoding and retrieval. An empty cell marks a cost the system does not report separately.}}
\label{tab:latency_breakdown}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lccccc}
\toprule
\textbf{System} & \textbf{Encode} & \textbf{Retrieve} & \textbf{Augment} & \makecell{\textbf{Model}\\\textbf{loads}} & \makecell{\textbf{Scheduler}\\\textbf{/ sync}} \\
\midrule
\design{}   & 0.20\,s & \multicolumn{2}{c}{1.60\,s}  &                                                & 0.20\,s \\
\edgeRAG{}  & 0.28\,s & \multicolumn{2}{c}{25.19\,s} &                                                &         \\
\flashRAG{} & \multicolumn{2}{c}{7.26\,s} & 0.10\,s  & \makecell{0.73\,s (encoder)\\2.20\,s (LLM)}    &         \\
\pipeRAG{}  & 6.20\,s & 5.20\,s & 0.10\,s            &                                                & $\leq 2$\,s \\
\bottomrule
\end{tabular}%
}
\end{table}
```

As rendered (Table 2, page 7):

```
  System        Encode   Retrieve   Augment      Model loads      Scheduler / sync
  MaestroRAG     0.20s        1.60s                                   0.20s
  EdgeRAG        0.28s       25.19s
  FlashRAG           7.26s              0.10s   0.73s (encoder)
                                                2.20s (LLM)
  PipeRAG        6.20s     5.20s      0.10s                            <= 2s
```

**On the fused-stage cells.** Rather than dashes, I used `\multicolumn` so a fused
measurement physically spans the two columns it covers: MaestroRAG's and EdgeRAG's 1.60 s
and 25.19 s span Retrieve and Augment, FlashRAG's 7.26 s spans Encode and Retrieve. The
structure carries the meaning, and the caption states it explicitly, so no cell can be
read as a missing measurement. Only genuinely-not-reported costs are blank (Model loads
for three systems, Scheduler for two), and the caption says what a blank means.

### 1.2 The subsection, `implementation&eval.tex` (new §5.2)

Placed immediately after §5.1 and before the RTX results subsection:

```latex
\subsection{\texorpdfstring{\new{Stage-Level Latency Breakdown}}{Stage-Level Latency Breakdown}}
\label{sec:breakdown}
\input{TablesAlgos/LatencyBreakdown}
\begin{newtext}
\Cref{tab:latency_breakdown} decomposes the per-stage cost of \design{} and the three
baselines at a common operating point. Generation is excluded because its settings are the
same for all four systems, so it is not a source of difference between them. Caching was
disabled for these measurements and for the primary results reported in this section.
\edgeRAG{} spends 25.19\,s in fused retrieval and augmentation, which is the cost of
generating embeddings on demand. \flashRAG{} pays 0.73\,s to load the encoder and a further
2.20\,s to load the LLM, which are model reloads. \pipeRAG{} measures the three CPU stages
separately but pays up to 2\,s in synchronization, serialization, and timeout, which is
contention between stages. \design{} reports 0.20\,s for encoding, 1.60\,s for fused
retrieval and augmentation, and 0.20\,s of scheduler cost.
\end{newtext}
```

### 1.3 Back-references (one clause each, subsections otherwise untouched)

§5.3, Results on RTX 4090:

> …yields 6--12$\times$ faster processing without risking out-of-memory problems`\new{; \Cref{sec:breakdown} decomposes these results by pipeline stage}`.

§5.5, Main Latency Results:

> On the RTX 4090, our method completes inference in 6.50 s, which is 3--4× faster than FlashRAG (16.39 s) or PipeRAG (19.80 s), and ≥4× faster than EdgeRAG`\new{, whose stage-level composition is given in \Cref{sec:breakdown}}`.

### 1.4 Part B, `implementation&eval.tex` §5.9 (Additional Insights)

Placed immediately after **Impact of optimization mechanisms**, which is the ablation
Reviewer A quoted against the paper:

```latex
\new{\noindent\textbf{Portability of optimizations to baselines: }We ported the
transferable optimizations to \pipeRAG{}: memory-mapped indices, warm encoder weights in
DRAM, and persistent thread and core pinning. For an isolated batch at \texttt{BS=1}, the
optimized \pipeRAG{} reaches 0.22\,s for encoding, 1.55\,s for retrieval, and 0.10\,s for
augmentation, close to \design{}. Under the steady-state bursty Azure trace of
\Cref{sec:throughput}, it reaches 1.38\,QPS against our 1.60\,QPS, still runs out of memory
at \texttt{BS=16}, and suffers head-of-line blocking because its synchronous stages cannot
admit the next batch independently. The remaining benefit comes from asynchronous
multi-width orchestration, worker scaling, and adaptive batching.}
```

---

## 2. Sentence-by-sentence provenance

**R** = rebuttal (`docs/Untitled document.md`, Common Concerns section, lines 195–208) ·
**P** = paper.

### §5.2 prose, seven sentences

| # | Sentence | Derives from |
|---|---|---|
| 1 | "Table 2 decomposes the per-stage cost of MaestroRAG and the three baselines at a common operating point." | **R** line 195: *"At the common configuration (RTX4090, DB=4M, BS=8), excluding the identical generation settings, measured costs are:"* |
| 2 | "Generation is excluded because its settings are the same for all four systems, so it is not a source of difference between them." | **R** line 195: *"excluding the identical generation settings."* States the settings are common; **makes no claim about generation time**, per the framing constraint. |
| 3 | "Caching was disabled for these measurements and for the primary results reported in this section." | **R** line 204: *"Caching was disabled for all of these (including the primary results given in the paper)."* |
| 4 | "EdgeRAG spends 25.19 s in fused retrieval and augmentation, which is the cost of generating embeddings on demand." | **R** line 200 (RA=25.19s) and line 204: *"baseline bottlenecks are on-demand embedding generation (EdgeRAG)."* |
| 5 | "FlashRAG pays 0.73 s to load the encoder and a further 2.20 s to load the LLM, which are model reloads." | **R** line 201 (encoder-load=0.73s, LLM-load=2.20s) and line 204: *"model reloads (FlashRAG)."* |
| 6 | "PipeRAG measures the three CPU stages separately but pays up to 2 s in synchronization, serialization, and timeout, which is contention between stages." | **R** line 202 (*"<=2s synchronization/serialization/timeout"*) and line 204: *"contention/synchronization (PipeRAG)."* |
| 7 | "MaestroRAG reports 0.20 s for encoding, 1.60 s for fused retrieval and augmentation, and 0.20 s of scheduler cost." | **R** line 199, the MaestroRAG row, read out. |

### Table caption, four sentences

| # | Sentence | Derives from |
|---|---|---|
| 1 | Configuration and caching | **R** line 195 (RTX 4090, DB=4M, BS=8) and line 204 (caching disabled) |
| 2 | Generation excluded, settings common | **R** line 195 |
| 3 | Spanned cells and which systems fuse which stages | Table shape from **R** lines 199–202; the reason MaestroRAG fuses R and A is **P** `design.tex:48`, cross-referenced |
| 4 | What an empty cell means | Reading of **R**'s `\-` entries; states the convention rather than asserting a measurement |

### Back-references and Part B

| Passage | Derives from |
|---|---|
| "; Section 5.2 decomposes these results by pipeline stage" | Cross-reference only |
| ", whose stage-level composition is given in Section 5.2" | Cross-reference only |
| Part B S1: what was ported | **R** line 206: *"porting all 'transferable' optimizations to PipeRAG: memory-mapped indices, warm encoder weights in DRAM, and persistent thread/core pinning."* |
| Part B S2: BS=1 values | **R** line 206: *"For an isolated batch (size=1), optimized PipeRAG reaches E=0.22s, R=1.55s, A=0.10s, close to MaestroRAG."* |
| Part B S3: QPS, OOM, head-of-line blocking | **R** line 206: *"it achieves 1.38QPS versus our 1.60QPS, still OOMs at BS=16, and suffers head-of-line blocking because its synchronous stages cannot admit the next batch independently."* Setup cross-referenced to §5.6 rather than restated. |
| Part B S4: conclusion | **R** line 208: *"this results in the remaining benefits of asynchronous multi-width orchestration, worker scaling and adaptive batching."* |

**Every sentence maps.** Part B carries all six required points and does not editorialize:
no "merely", no scare quotes, no characterization of the reviewer's concern, no claim of
vindication.

---

## 3. Provenance of every numeral

Every value comes from the rebuttal, and **none exists in any workbook tab** (see §7.2).

| Numeral | Where | Rebuttal line |
|---|---|---|
| 0.20 (encode), 1.60 (RA), 0.20 (scheduler) | table, §5.2 prose | line 199, MaestroRAG row |
| 0.28 (encode), 25.19 (RA) | table, §5.2 prose | line 200, EdgeRAG row |
| 7.26 (E+R), 0.10 (augment), 0.73 (encoder load), 2.20 (LLM load) | table, §5.2 prose | line 201, FlashRAG row |
| 6.20 (encode), 5.20 (retrieve), 0.10 (augment), 2 (sync ceiling) | table, §5.2 prose | line 202, PipeRAG row |
| 4090, 4 M, 8 | caption | line 195, the common configuration |
| 0.22, 1.55, 0.10 | Part B | line 206 |
| 1.38, 1.60 | Part B | line 206 |
| 1 (BS), 16 (BS) | Part B | line 206 |

The 1.60 QPS figure appears twice: from the rebuttal in Part B, and independently in §5.6
from `ThroughputResult!E4`. Both are checked, and they agree.

`refs.bib` and `reference.bib` untouched; no citation was needed that does not exist.

---

## 4. Framing confirmation: no total, no residual, no end-to-end reference

Verified by pattern search over the new subsection source **and** the table file together:

| Pattern | Occurrences |
|---|---:|
| `total` | **0** |
| `residual` | **0** |
| `end-to-end` / `end to end` | **0** |
| Figure 7b (`MainLatencyResults2`, `MainLatTputFigure`) | **0** |
| "sums to" / "adds up" | **0** |
| Any end-to-end latency value (6.50, 6.497, 16.39, 19.80, 28.40, 28.56) | **0** |

There is no total column and no total row. Generation is stated as excluded **on the
grounds that its settings are common**, and nothing is said about generation time.

The two back-references live in the *other* subsections and point inward; neither the new
subsection nor its table refers outward to an aggregate.

---

## 5. The Figure 4 core-allocation cross-reference: I did not add one

Figure 4's caption states *"we deploy one worker per pipeline stage with ⟨8, 22, 1⟩ cores
for the ⟨E, RA, G⟩ stages"*, and its sweep includes BS=8 at DB=4M, so the operating points
coincide.

**I judged that insufficient and left it out.** The rebuttal states the configuration as
*"RTX4090, DB=4M, BS=8"* and stops there. Asserting the core allocation for this table
would be asserting something the rebuttal does not, on the inference that two measurements
sharing a database size and batch size must share a deployment. That inference is probably
correct and is not mine to make. The caption is complete without it: platform, database
size, batch size, caching state, and the generation exclusion are all stated.

**If you want it**, the sentence is one clause in the caption, and Figure 4's caption is
where it would point.

---

## 6. Table renumbering, and every reference verified

The new table renumbers the sequence for the second time in this revision:

| Label | Was | Now | Page |
|---|---:|---:|---:|
| `tab:spec_comparison` (hardware, Task 2) | 1 | **1** | 2 |
| `tab:latency_breakdown` (new) | — | **2** | 7 |
| `tab:cache_results` (caching) | 2 | **3** | 9 |

**Every `TABLE n` in the built PDF checked against the prose around it.** Six occurrences,
all correct:

| Rendered | What it is | Correct? |
|---|---|---|
| `TABLE 1: Platform specifications…` | hardware table caption | ✅ |
| `…TABLE 1 sets both against a datacenter A100…` | §2.1 prose | ✅ |
| `TABLE 2: Stage-level latency on the RTX4090…` | breakdown caption | ✅ |
| `TABLE 2 decomposes the per-stage cost…` | §5.2 prose | ✅ |
| `TABLE 3: Latency with caching…` | caching caption | ✅ |
| `TABLE 3 reports the results of our caching mechanisms…` | §5.8 prose | ✅ |

Subsection renumbering within §5: Implementation Details 5.1, **Stage-Level Latency
Breakdown 5.2 (new)**, RTX results 5.3, Jetson 5.4, Main Latency 5.5, Throughput 5.6,
Power 5.7, Software Caching 5.8, Additional Insights 5.9. All `\Cref` targets updated
automatically; Part B's `\Cref{sec:throughput}` correctly renders "Section §5.6".

---

## 7. Verification

### Build

| | |
|---|---|
| `make` | **exit 0**, **13 pages** |
| LaTeX errors | **0** |
| Undefined references | **0** — `sec:breakdown` → §5.2 (p7), `tab:latency_breakdown` → Table 2 (p7) |
| Undefined citations | **0** |
| All 41 references render | ✅ |

### Revision modes — pixel-verified

Nine pages carry new text. **Every one is 100 percent blue at `\revmode=1` and pure
RGB(0,0,0) at `\revmode=0`, with zero near-white pixels**, and this time with zero non-blue
differing ink (no reflow residue):

| Page | Content | Differing px |
|---|---|---:|
| 1 | intro clause | 1,981 |
| 2 | §2.1, Table 1, §2.3 | 41,868 |
| 4 | §3.3 portability | 14,283 |
| 5 | §4.1 adaptive batching | 10,314 |
| **7** | **§5.2 + Table 2** | **48,978** |
| 8 | §5.1 justification, §5.4 back-ref | 3,734 |
| 9 | §5.5 back-ref, Table 3 caption | 4,215 |
| 10 | §5.8 caching analysis | 25,108 |
| **11** | **§5.9 Part B** | **22,276** |
| 3, 6, 12, 13 | — | 0, identical |

`\revmode` restored to `1`.

### `verify_numbers.py`

```
checks : 64 PASS / 5 FAIL / 1 UNVERIFIABLE
drift  : none
```

**The 51 pre-existing checks hold their statuses exactly.** 19 added, all PASS:

| Group | Checks | Anchored to |
|---|---:|---|
| Breakdown table, all 13 values | 13 | rebuttal lines 199–202 |
| Ported-optimization experiment, all 6 values | 6 | rebuttal line 206 |

**Harness change.** These are the first *rebuttal-anchored* checks. They reuse the
`source: {file, regex}` kind added in Task 4, pointing at `docs/Untitled document.md`, so
each paper number is tied to the rebuttal sentence it came from and neither can drift
silently. Every regex is anchored on surrounding row content and was verified to match
**exactly once** in the file before being encoded. They carry `origin: rebuttal` and a
`note` naming the row, so provenance is explicit in the report. `file_source_value` was
renamed from `tex_source_value` and its docstring now states both uses.

### Style

| | Count |
|---|---:|
| Text added by Tasks 2–5: `---` | **0** |
| Text added by Tasks 2–5: `—` | **0** |
| Text added by Tasks 2–5: non-range `--` | **0** |
| Pre-existing prose: `---` / `—` | 4 / 6 (**10**, unchanged) |

### Page count

**13 pages, unchanged from Task 4.** The new subsection, table, and Part B paragraph were
absorbed without adding a page. Where it landed:

| Landmark | Task 4 | **Task 5** |
|---|---:|---:|
| §5 Implementation | 7 | 7 |
| **§5.2 Stage-Level Latency Breakdown + Table 2** | — | **7** (new) |
| §5.3 Results on RTX | 7 | 7 |
| §5.5 Main Latency Results | 8 | **9** (+1) |
| §5.9 Additional Insights | 10 | 10 |
| §6 Related Work, §7 Conclusions | 11 | 11 |
| References begin | 11 | **12** (+1) |

The body still ends on page 11. Notably, **page 13 is now a full page of references
(65 lines) rather than the single stranded entry it held after Task 4** — the bibliography
redistributed across pages 12 and 13. That is a tidier 13 pages than Task 4 produced, but
it is still 13.

### Bibliography

Byte-identical to the pre-Task-2 state:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

### PDF

Not committed (gitignored). Timestamped copy: **`reports/task05_main_20260808-1429.pdf`**.

---

## 8. Things that contradict the instructions, or that you should decide

### 8.1 Not one of these measurements exists in the workbook

I checked every value in the new table and in Part B against all thirteen tabs, authorised
and stale:

| Value | In an authorised tab | In a stale tab |
|---|---|---|
| 0.20, 0.28, 25.19, 7.26, 0.73, 2.20, 5.20, 0.22, 1.55, 1.38 | **none** | **none** |
| 1.60 | `ThroughputResult!E4` (different quantity: QPS, not seconds) | none |
| 0.10 | `Breakdown!D5` | `Encode!B6` |
| 2 | `Motivation!D4` | `Encode!A16` |
| **6.20** | none | `Comparison!F34`, `Comparison!O110` |

Ten of the fourteen distinct values appear **nowhere in the workbook at all**. This
confirms the task's premise, and it is why the checks are anchored to the rebuttal instead.
**It also means the paper now reports a table of measurements with no exported data behind
it.** That is the author's position as stated to the reviewers, and the protocol says the
rebuttal is the answer, so I have not treated it as a problem. But if the shepherd asks for
the underlying data, it is not in `MaestroRAGResults.xlsx`.

### 8.2 A fourth stale-tab warning appeared, and it is a coincidence

`6.20` matches `Comparison!F34` and three other cells in the stale `Comparison` tab and
appears in no authorised tab, so the scanner flags it. **I checked whether this indicates
the rebuttal's breakdown was derived from the stale tab: it does not.** If it had been,
the other twelve values would show the same pattern; ten of them appear in no tab
whatsoever. One value out of fourteen landing on a stale cell is chance. No action needed,
but the count moving 3 → 4 is expected rather than a regression.

### 8.3 The `Section §N` count is now 23, up from 9 before Task 2

| State | Instances |
|---|---:|
| pre-Task 2 | 9 |
| Task 3 | 19 |
| Task 4 | 19 |
| **Task 5** | **23** |

Task 5 adds four, all required: `sec:breakdown` twice (the two back-references),
`subsec:pipeline_design` once (the caption's explanation of stage fusion), and
`sec:throughput` once (Part B's setup cross-reference). Item 7's sweep now has **fourteen
added instances** to cover, and the rebuttal itself promises the fix. As noted in Task 3,
this is a one-line `\creflabelformat` change plus a read-through, and it is now the single
largest accumulated debt in the revision.

### 8.4 Two paragraphs in §5.3 now overlap with the new §5.2

§5.3 still contains *"Two major lessons emerge from Figure 4… First, partitioning CPU and
GPU tasks carefully is crucial: forcing both encoder and generative model onto the GPU
triggers heavy data transfers and repeated model loads."* That is now a prose restatement
of what Table 2 shows quantitatively, three paragraphs later.

The master plan already lists this paragraph among the three duplicate-summary cuts. With
the breakdown in place it has become genuinely redundant rather than merely repetitive,
and cutting it would also recover the page-13 spill discussed in Task 4's report.
**Out of scope here; not touched.** Flagging because Task 5 is what made it redundant.

### 8.5 Part B's heading follows the pattern I introduced, not the pre-existing one

§5.9's existing run-in headings are all *"Impact of X:"*. I used *"Portability of
optimizations to baselines:"*, matching the *"Portability of these trends to embedded
platforms:"* heading added in Task 3 rather than the *"Impact of"* pattern. Both now exist
in the paper. Item 7 asks for parallel headings across §5.2–5.9, so whichever way you
standardize, this one and the §3.3 one should move together.
