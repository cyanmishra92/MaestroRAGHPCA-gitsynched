# MaestroRAG — IISWC 2026 Camera-Ready: Final Master Plan

**Supersedes blueprints v1, v2, v3.** This is the single working document.

**Sources of truth:** `/mnt/project/iiswc2026paper216.pdf` (12 pp: 10 body + 2 refs) · `/mnt/project/IISWC216.md` (reviews, rebuttal, shepherd comment) · `MaestroRAGResults.xlsx`. Nothing else is consulted.

**Due:** August 10. Today: August 8. Page relief: 1–2 pages available.

---

## Part I — Verification of every quantitative claim

### A. Verified ✅ — matches the workbook

| Claim | Paper | Workbook | |
|---|---|---|---|
| Main latency, 4090 / 4080 / Jetson | 6.50 / 3.96 / 28.56 s | 6.497 / 3.959 / 28.56 | ✅ |
| Largest case BS=16, DB=8M | ≈25 s | 25.47 | ✅ |
| 4080 at BS=16, DB=8M | 11.58 s | 11.58 | ✅ |
| 12× vs EdgeRAG @ BS=8, 8M | ≈12× | 12.081 | ✅ |
| 6.15× @ BS=16, 8M | 6.15× | 6.152 | ✅ |
| FlashRAG gains | 2–3× | 1.92–3.24 | ✅ |
| 4080 speedups @ BS=8 | 8.8 / 1.9 / 5.4 | 8.848 / 1.960 / 5.355 | ✅ |
| Jetson speedup | 1.35× @BS=8, 1.25× @BS=16 | 1.3522 / 1.2559 | ✅ |
| Latency range | 1.25×–12× | 1.233–12.081 | ✅ |
| Throughput 4090 | 1.60 / 0.29 / 0.68 / 1.19 QPS | 1.600 / 0.2876 / 0.6831 / 1.1852 | ✅ |
| Throughput Jetson | 0.43, 6.7× vs EdgeRAG, 1.16× vs PipeRAG | 0.4324, 6.70×, 1.168× | ✅ |
| Energy per query | 253.3 / 791.8 / 780.92 J | 253.28 / 792.00 / 780.92 | ✅ |
| Energy ratio | ≈3× | 3.127× | ✅ |
| Fig. 2a stage split | 6.0 / 64.7 / 0.8 / 28.5 % | 0.718 / 7.738 / 0.100 / 3.410 s | ✅ |
| BS=32 retrieval total | 227.94 s | 3.36 + 224.58 | ✅ |
| §4.2 three-stage / four-stage | 1.178 / 1.448 s | components sum exactly | ✅ |
| Mapper vs naive | 8.06× | 9.5 / 1.178 = 8.06 | ✅ |
| Multi-worker latency cost | 9% (rebuttal) | 5.347 / 4.898 = 9.2% | ✅ |
| Ablation endpoint | 6.497 s | = main result, caching off | ✅ |

**Notable good news — the tail-latency numbers are internally consistent**, which I had not previously checked. §5.4 reports P99 and P99/P50 at BS=8, DB=2M; dividing each P99 by its stated ratio reproduces the no-cache table almost exactly:

| | P99 | P99/P50 | implied P50 | table (BS=8, 2M) |
|---|---|---|---|---|
| MaestroRAG | 5.26 | 1.04 | 5.06 | **5.027** |
| FlashRAG | 14.86 | 1.14 | 13.04 | **12.96** |
| PipeRAG | 14.41 | 1.09 | 13.22 | **13.22** |

Three independent numbers landing on the table. Worth keeping in mind when the shepherd asks whether the data is sound.

### B. Corrections required ⚠️

| # | Location | Paper says | Data says | Fix |
|---|---|---|---|---|
| **B1** | §5.4 | "3–4× faster than FlashRAG (16.39 s) or PipeRAG (19.80 s)" | **2.52×** and 3.05× | "2.5× and 3.1×" |
| **B2** | §5.4 | "≥ 4× faster than EdgeRAG" | 4.37× | state 4.4× |
| **B3** | §5.2 | "6–12× latency gains over existing designs" | vs. FlashRAG it is 2–3× | "up to 12× over EdgeRAG; 2–3× over FlashRAG" |
| **B4** | §5.3 | "cut overhead relative to EdgeRAG by **25%–35%**" | **8.6% / 23.8% / 26.0% / 20.4%** at BS 2/4/8/16 | **Not supported at either end.** Say "up to 26% (BS=8)". This is the weakest unsupported claim in the paper. |
| **B5** | §5.6 | peak CPU power 16.45% / 8.22% higher | **16.36% / 8.08%** | correct both |
| **B6** | §5.8 | "one-time cold-start cost of 7 s comprising 0.36 + 3.04 + 3.36" | sums to **6.76 s** | "≈7 s, of which 0.36 s encoder, 3.04 s index, 3.36 s LLM; the remainder is process and library initialisation" |
| **B7** | §4.2 | "approximate 22% improvement" | 18.6% relative to the four-stage baseline; 22.9% relative to three-stage | ambiguous denominator — state **1.23×** instead |
| **B8** | §5.8 | "(effective) caching achieves 2.003 s" | consistent with an **80% exact-match hit rate** (0.8 × 0.92 + 0.2 × 6.497 = 2.035) | add the hit-rate qualifier inline; §5.7 already uses 80%, but the ablation reads as unconditional |
| **B9** | §5.5 / Fig. 7c | 0.29 / 0.68 / 1.19 / 0.064 | 0.288 / 0.683 / 1.185 / 0.0645 | pick a precision, apply everywhere (text and figure disagree on the Jetson EdgeRAG value) |
| **B10** | abstract, §1, §7 | 12× / 5.6× / 3× unqualified | 12× is vs. EdgeRAG @BS=8/8M; **5.6× throughput is vs. EdgeRAG — 2.34× vs. FlashRAG, 1.35× vs. PipeRAG**; 3.1× energy vs. FlashRAG | attach the operating point once per claim at first use |

B4 and B10 are the two that matter. Reviewer A's whole position is that the headline is unrepresentative; an unsupported "25–35%" on the Jetson — the platform he attacked specifically — is precisely the sentence he would check.

### C. Conflicts internal to the paper

| # | Conflict | Resolution |
|---|---|---|
| **C1** | §3.2 says index fetch dominates at small batches; Fig. 2d's BS=2 bar shows the opposite (0.60 s fetch vs. 4.408 s search, against a flat 3.36 s fetch for BS=4–32) | Point is real and caching-related (your Q2). Needs **one clause** in §3.2 giving the mechanism — **still open, F3** |
| **C2** | Fig. 7a `TC` = 4–10 total cores vs. ⟨8, 22, 1⟩ in Fig. 4 / §4.2 | Both over the full P+E budget (your Q3). Distinguish: ⟨8,22,1⟩ = **maximal latency-critical** allocation; mapper output = **minimal sufficient** allocation. Reframes Fig. 7a as *same performance on fewer cores* — a stronger result than "matches or outperforms" |
| **C3** | Fig. 7b marks Jetson PipeRAG "N/A"; §5.5 reports its Jetson throughput (0.370 QPS, 1.16×) | Footnote covering **both**: partial Jetson port sufficient for coarse steady-state throughput, not for stage-attributed latency. **Name the missing dependency — F1** |
| **C4** | §3 "24 physical cores" vs. §5.1 "32 virtual cores (8 P + 16 E)" | Both correct; state the convention once so ⟨8,22,1⟩+1 = 32 is followable |
| **C5** | §5.8 charges 3.36 s to load the generation model; `Comparison` tab records Llama-8B load at 2.27 s and the rebuttal charges FlashRAG 2.20 s | Plausible (CUDA context + transfer), but reconcile or the three numbers look arbitrary |

### D. Unverifiable — no backing cells

`15.12 s` and `11.79 s` ablation stages · `128 ms` augment-separation cost (§4.1) · `≈30 MB` cache capacity (§3.2) · `~70%` memory saving (§5.1) · indexing gains 29.27 / 28.15 / 32.18% · token-sensitivity 0.6 / 1.2 / 12% · rebuttal's PipeRAG-port QPS (1.38) and per-stage energy shares. Not errors — just note that if the shepherd asks, these have no sheet behind them.

### E. Retracted from earlier blueprints

Withdrawn because the source tabs are stale (your Q1, Q6, Q7): the 94%-vs-25% parallel-efficiency contrast, worker-count and top-k insensitivity, GPU utilization 86/62/11%, and the "plot the losing BS=16 bar on the 4090" recommendation. None of these go in the paper.

**What survives and is still unused:** the `Breakdown` tab's start-up/execution split — encode 0.46 s start-up vs. 0.258 s execution, retrieval 3.73 s vs. 4.008 s, **4.19 s of the 11.97 s pipeline is start-up**. Measured motivation for §4.3's warm workers. One sentence in §5.2.

---

## Part II — The reconciliation that anchors Item 1

Uncontended generation is **3.41 s** (`Breakdown` tab, BS=8, DB=4M, 120 tokens). Applying it to the rebuttal's breakdown:

| System | Stated components | Total | Residual | vs. 3.41 s |
|---|---|---|---|---|
| MaestroRAG | 0.20 E + 1.60 RA + 0.20 sched + **3.41 G** = 5.41 | 6.497 | **1.087 s** | 1.00× |
| FlashRAG | 7.26 E+R + 0.10 A + 0.73 enc-load + 2.20 LLM-load | 16.39 | 6.10 | **1.79×** |
| PipeRAG | 6.20 E + 5.20 R + 0.10 A + ~2.0 sync | 19.80 | ~6.30 | **1.85×** |
| EdgeRAG | 0.28 E + 25.19 RA | 28.40 | 2.93 | 0.86× ⚠️ |

Two things fall out. First, MaestroRAG's 1.087 s residual is the same ~1.1 s cross-worker handoff quoted to Reviewer C for Table 1 — two independent measurements, one constant. Second, **the baselines' generation runs ~1.8× slower than uncontended**: reserving the GPU is worth ~2.7 s at this operating point on its own, before any of the "orthogonal engineering" Reviewer A discounted. That paragraph is the strongest thing available to you and it belongs in §5.2.

Corroboration: `Comparison` tab records Llama-8B load at 2.27 s; the rebuttal charges FlashRAG 2.20 s.

EdgeRAG's 2.93 s remains the one cell I cannot defend — **F4**.

---

## Part III — Placement (confirmed)

| Now | Camera-ready | Item |
|---|---|---|
| — | **§2.1 Deployment Scope: What "Edge" Means Here** | **2** (definition) |
| 2.1, 2.2 | 2.2, 2.3 | renumber |
| — | **§3.3 Profiling Platform and Trend Portability** | **6** |
| 3.3 | 3.4 | renumber |
| 4.1 | 4.1 + context-drift paragraph | **5** |
| 4.2 | 4.2 + static-allocation sentence, B7, C2 | **5** |
| 5.1 | 5.1 + edge-criteria mapping | **2** (justification) |
| — | **§5.2 Stage-Level Latency Breakdown** (Table 2) | **1** |
| 5.2 | 5.3 **Local-Compute Platforms** | 7, B3 |
| 5.3 | 5.4 **Embedded Platform** | 7, B4 |
| 5.4 | 5.5 **End-to-End Latency** | 7, B1, B2 |
| 5.5 | 5.6 **Throughput** | 7, C3 |
| 5.6 | 5.7 **Power and Energy** | **3**, B5 |
| 5.7 | 5.8 **Software Caching** | **4** |
| 5.8 | 5.9 **Sensitivity and Ablation** | 7, B6, B8, C2 |

**Why §5.2 and not §5.5:** Reviewer B's complaint is that *Figure 4's* aggregate speedups aren't decomposed, and Figure 4 sits in §5.3. A breakdown arriving two subsections later appends to the complaint instead of answering it. Placed first, every subsequent number becomes a consequence of a mechanism already established.

**Why §2.1 and not §5.1 alone:** §3's choice of a desktop profiling platform is unjustifiable until the reader knows what "edge" means. The definition must precede §3; the platform-by-platform justification stays with the hardware table in §5.1.

**Why §3.3 and not §5.4:** the shepherd's wording is about *workload-characterization trends*, and Reviewer D asked about §3.

### Item 6 content — no new experiments needed

1. Characterization requires sweeping **past** the knee; at 15 W the Orin exposes 4 online cores and sits entirely left of saturation.
2. The Orin **confounds attribution** — unified LPDDR5 pools retrieval working set, encoder weights and KV cache, and DVFS under the cap makes frequency a dependent variable.
3. Profiling on the **most forgiving** hardware is the conservative direction: show contention on a 24 GB 4090, then show it persists at 15 W.
4. Mechanisms are architecture-independent, so knees move **left**, not away — retrieval is bound by index-footprint-to-LLC and DRAM bandwidth, both smaller on Orin.
5. **Fig. 5 already demonstrates point 4** and is unremarked: 1.09 → 1.31 → **1.35** → 1.26 across BS 2→16, peaking at BS=8 and turning over. Same shape as the 4090 at large DB, knee shifted left.

### Item 7 — exact scope

Table captions above (Tables 1, 2, ablation) · Fig. 7 caption rewritten as pure description **and the same rule applied to Figs. 4 and 1**, both of which currently carry claims rather than descriptions · fonts ≥8 pt in **all** figures, regenerated not scaled (named: 1 and 3; also needed: Fig. 2d ticks, Fig. 7a annotations, Fig. 6 axes) · no white-on-light-green in Fig. 1 · "FlashFAG" legend typo in Fig. 3c · parallel headings across §5.2–5.9 · global `\S` purge and the bare "(2.1)" cross-reference in §4.1 · the broken text wrap beside Fig. 5.

---

## Part IV — Rebuttal promises that are binding but not among the seven

The shepherd's framing — *"the rebuttal includes important additional details that must be thoroughly integrated"* — makes these binding even though they aren't numbered items.

1. **Rename desktops** to local/personal-computing platforms ("we will rename accordingly"). Folds into Item 2 but touches title, abstract, §1, headings, conclusion.
2. **EdgeRAG energy exclusion** stated as a limitation with the measurement boundary ("we will state this limitation … explicitly"). Folds into Item 3.
3. **Runtime core remapping as future work** ("which we will state clearly"). Folds into Item 5.
4. **PipeRAG-port experiment** — transferable optimizations ported to PipeRAG: 1.38 vs. 1.60 QPS, still OOM at BS=16, head-of-line blocking. This was your answer to the *common* concern, presented first in the rebuttal. **I now rate this as effectively required**, not optional as in v1. It is the direct answer to Reviewer A, the only reviewer who did not move. Place in §5.9 as a row of the ablation table with a "portable to baselines?" column.

Also cheap and gracious: one sentence acknowledging Reviewer D's point that the methodology generalizes beyond edge-scale RAG (conclusion or future work).

---

## Part V — Still open

| | Needed for | Blocks |
|---|---|---|
| **F1** | Specific missing Jetson dependency for PipeRAG | §5.6 footnote (C3) |
| **F3** | One-line caching mechanism for Fig. 2d's BS=2 point | §3.2 clause (C1) |
| **F4** | EdgeRAG's 2.93 s implied generation | Table 2 last cell |
| **F5** | LaTeX source, `.bib`, figure scripts | Everything downstream of drafting |
| **F6** | BS=8 caching run before the 10th? | Whether Item 4's amortization claim is measured or reasoned |

F5 is the real constraint now. F1/F3/F4 are one line each.

---

## Part VI — Order of work

**Today.** F1/F3/F4 answers + LaTeX. Drafting starts on: §2.1 (edge definition + tier table), §3.3 (profiling-platform argument, all five points), §4.1/§4.2 (context drift, static allocation), Table 2 and its prose. None blocked except Table 2's EdgeRAG cell.

**Aug 9 AM.** Fig. 6 redesign (CPU stacked by stage + GPU separate + divider + boundary in caption) · Table 1 rewrite · ablation table with the portability column and the PipeRAG-port row.

**Aug 9 PM.** All figure regeneration · every caption rewritten · table captions moved · the three duplicate-summary paragraph cuts (§5.3's "Two major lessons emerge…", §3.2's "Execution Breakdown Across Stages", §5.9's "Latency results insights").

**Aug 9 eve.** Corrections B1–B10 applied and re-checked against this document · reference fixes (add vLLM, HNSW, IVF-PQ; fix Indyk & Motwani and e5-base-v2; verify RAGCache / EdgeRAG / HeteRAG / REIS venues) · voice pass · one end-to-end read.

**Aug 10 AM.** Shepherd response letter. Camera-ready formatting: drop "Regular-" from the title, de-anonymize, embed fonts.

### Response letter skeleton

One table, seven rows: *Item · What we changed · Where (section, figure/table, page)*. Then a short closing paragraph noting the additional integrations from the rebuttal (Part IV items 1–4) and the terminology change from "edge device" to "local-compute platform." Shepherds read this before the PDF; it is worth thirty focused minutes.

---

## Part VII — Sign-off checklist

**Seven mandated items**
- [ ] 1 Table 2 in §5.2, every row sums to the reported total; per-baseline failure modes explained; generation-inflation paragraph present; EdgeRAG residual explained or footnoted
- [ ] 2 §2.1 defines edge by constraint with the A100 contrast; §5.1 maps each platform to the criteria; unified-memory objection answered; desktops renamed throughout
- [ ] 3 Fig. 6 shows CPU energy by stage **and** GPU separately, vertical divider, both axes labelled, boundary + config in caption; B5 fixed; EdgeRAG exclusion justified
- [ ] 4 Table 1 caption above; mechanism explained; ~1.1 s handoff named and cross-referenced to §5.2; amortization worded per F6 outcome
- [ ] 5 Context-drift discussion in §4.1 anchored to the +12% generation measurement; static allocation stated in §4.2; future work stated
- [ ] 6 §3.3 gives the reason, not just the observation; Fig. 5's turnover cited as evidence; back-reference from §5.4
- [ ] 7 All seven presentation sub-items, plus Figs. 1 and 4 captions and the Fig. 5 text wrap

**Integrity**
- [ ] B1–B10 all applied
- [ ] C1–C5 all resolved
- [ ] Every "up to N×" carries its operating point at first use
- [ ] Every CPU-only or generation-excluded figure says so in-line
- [ ] No number in the text disagrees with its own figure
- [ ] Nothing from the stale `Encode`, `Retrieval`, or `Comparison` tabs appears anywhere
- [ ] Part IV items 1–4 integrated
- [ ] Three citations added, two fixed, four verified; no `??` in the PDF
- [ ] Response letter cites section, figure and page for each of the seven items
