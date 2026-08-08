# Ground Truth Protocol — MaestroRAG IISWC 2026 Camera-Ready

**Commit this to `docs/`. Every remaining task prompt references it.**

---

## 1. Source precedence

| Rank | Source | Role |
|---|---|---|
| **1** | **The rebuttal** (`docs/`, "Rebuttal Response by Author") | **The answer.** What the authors told the reviewers they would say is what the paper must now say. |
| **2** | **The paper** (current `.tex` / PDF) | Supporting facts, existing wording, existing claims. New text must be consistent with it. |
| **3** | `data/MaestroRAGResults.xlsx` | **Verification only.** Confirms or corrects a number. Never the source of an *argument*. Authorised tabs only — `Encode`, `Retrieval`, `Comparison` are stale. |
| — | Anything else | Not evidence. Legacy `.tex`, planning docs, prior blueprints, and reasoning generated during this project are **scaffolding, not sources**. |

## 2. The rule

**Answers are borrowed from the rebuttal, not composed afresh.** The shepherd's instruction was that *"the rebuttal includes important additional details that must be thoroughly integrated into the paper."* Integration means the rebuttal's claims, in the paper's voice, with its numbers intact.

New reasoning is permitted only to **connect** rebuttal claims to paper facts, or to **make a claim readable** in the paper's register. It may not:

- introduce a mechanism, cause, or explanation the rebuttal does not assert;
- replace the rebuttal's stated reason with a better-sounding one;
- contradict the rebuttal's framing, even where the data suggests it should.

**If the data and the rebuttal disagree, stop and report it.** Do not resolve it in the text.

## 3. Numbers

Every numeral in new text must be traceable to the rebuttal, the paper, or an authorised workbook tab, and its provenance logged. No derived quantity — a ratio, a percentage, a residual, a sum — may appear unless the rebuttal or paper already states it, or it has been explicitly approved.

## 4. Rebuttal source map — what each shepherd item's answer is made of

### Item 1 — Latency breakdown
**Rebuttal supplies:** the measured table at RTX 4090, DB=4M, BS=8, *"excluding the identical generation settings"* — MaestroRAG E=0.20 s, RA=1.60 s, scheduler=0.20 s · EdgeRAG E=0.28 s, RA=25.19 s · FlashRAG E+R=7.26 s, A=0.10 s, encoder-load=0.73 s, LLM-load=2.20 s · PipeRAG E=6.20 s, R=5.20 s, A=0.10 s, ≤2 s synchronisation. The diagnosis: *"baseline bottlenecks are on-demand embedding generation (EdgeRAG), model reloads (FlashRAG), and contention/synchronization (PipeRAG)."* And: *"Caching was disabled for all of these (including the primary results given in the paper)."*
**Also supplies (common concern):** the ported-optimisation experiment — memory-mapped indices, warm encoder weights, persistent thread/core pinning applied to PipeRAG; at batch size 1 it reaches E=0.22 s, R=1.55 s, A=0.10 s; under the bursty Azure trace it achieves 1.38 QPS versus 1.60 QPS, still OOMs at BS=16, and suffers head-of-line blocking because synchronous stages cannot admit the next batch independently.
**⚠ Open decision:** the rebuttal frames generation as *identical* across systems and excludes it. Component sums therefore do not reconcile with the Fig. 7b totals. Two options — publish exactly as the rebuttal did (components only, no totals), or measure generation per system. **The second requires author input (F4) and revises the rebuttal's framing. Do not choose silently.**

### Item 2 — Definition of edge
**Rebuttal supplies:** *"We treat desktops as personal-computing edge: local compute nodes running RAG without cloud intervention under limited power and compute budgets, as clarified in Section 4. We agree they are better called local/personal-computing platforms, not embedded edge devices, and will rename accordingly."*
**Plus the unified-memory answer:** *"Unified memory removes PCIe-copy costs, it does not remove single-GPU encode/generate contention (structural hazard) or competition among the encoder, retrieval working set, and KV cache under a constrained memory/power budget."*
**Paper supplies:** `design.tex:50` — *"Our design for an edge personal computing device targets two main types of user tasks: latency-critical and throughput-critical"* — with single-user examples (the user's calendar; their e-commerce, entertainment, and banking apps). This is the *"as clarified in Section 4"* the rebuttal points at.
**Workbook supplies:** the `edge vs. server` tab, already rendered as `TablesAlgos/Jetson4090A100.tex`.

### Item 3 — Energy breakdown
**Rebuttal supplies:** *"After subtracting idle package power, stage-attributed energy shares (DRAM excluded) are FlashRAG: 79.2% R+A, 19.1% generation-driving, 1.8% other; PipeRAG: 20.4% E, 64.5% R, 0% A, 15.6% G; MaestroRAG: 5.5% E, 83.2% RA, 11.2% G. EdgeRAG is excluded because its on-demand embedding path performs additional, non-equivalent work; we will state this limitation and the measurement boundary explicitly."*
**Note:** the measurement boundary — idle package power subtracted, DRAM excluded — is part of the rebuttal's own answer and must appear in the paper. The energy is CPU package energy (author-confirmed).

### Item 4 — Table 1 similarity matching
**Rebuttal supplies, essentially in full:** *"Exact-match returns the cached final answer, skipping retrieval+generation (0.87–0.92 s). Similarity-match reuses only top-k documents and freshly generates for the new query (3.06–3.12 s); this is not a RAM-capacity effect. Our current process/thread handoff across workers adds ~1.1 s, explaining the gap versus EdgeRAG. EdgeRAG does not incur these overheads from process orchestration, thread synchronization, or similar coordination mechanisms; its execution is largely sequential and hence has lesser overhead. Our experiment is for batch size of 1 which compares our worst case against EdgeRAG's nominal. However, at larger batch sizes this orchestration cost gets amortized."*
**Note:** the amortisation claim is asserted, not measured. Keep it as the rebuttal words it — an expectation from the fixed-cost structure — unless a BS=8 measurement arrives.

### Item 5 — Adaptive batching under context drift
**Rebuttal supplies:** *"The mapper profiles generation across intended prompt lengths, but worker allocation is static within a session. Adaptive batching creates memory-safe GPU quanta; runtime core remapping under context drift is a future extension, which we will state clearly."*
**Paper may support with:** the existing §5.8 token-sensitivity numbers, if used only as corroboration.

### Item 6 — Jetson/Orin characterization trends
**Rebuttal supplies, in full:** *"Because our optimizations focus on CPU-side encoding and retrieval, the trends observed on standard devices hold true for Jetson/Orin platforms. The primary difference is the elimination of PCIe transfer overhead in unified memory systems. A similar trend is also observed across SKUs and vendors."*
**⚠ This is the whole answer.** Arguments about sweeping past the saturation knee, DVFS confounding attribution, knees shifting with cache size, or the Fig. 5 speedup turnover are **not in the rebuttal** and are not to be introduced. The shepherd asked that *"the reason behind this observation is clearly explained"* — the reason is the one the rebuttal gives: the optimisations are CPU-side, so the trends are not GPU-platform-dependent.

### Item 7 — Writing and presentation
**No rebuttal text.** Mechanical: table captions above · Fig. 7 caption descriptive · fonts ≥8 pt in all figures (Figs. 1 and 3 named) · no white-on-light-green in Fig. 1 · consistent parallel subsection headings · no unnecessary section symbols.
**Also promised in the rebuttal:** *"We will also remove redundant 'Section section-symbol' usage."*

## 5. Rebuttal promises binding beyond the seven items

1. Rename desktops to local/personal-computing platforms — *"will rename accordingly."*
2. State the EdgeRAG energy exclusion and the measurement boundary — *"we will state this limitation ... explicitly."*
3. State runtime core remapping as future work — *"which we will state clearly."*
4. The ported-optimisation experiment answering the common concern (see Item 1).

## 6. Standing checklist for every task

- [ ] Every claim traceable to a rebuttal sentence, a paper sentence, or an authorised workbook cell
- [ ] No mechanism or explanation asserted that the rebuttal does not assert
- [ ] No derived number that the rebuttal or paper does not already state
- [ ] Data/rebuttal conflicts reported, not resolved in the text
- [ ] Provenance logged per numeral in the task report
