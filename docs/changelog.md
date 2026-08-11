# MaestroRAG (Paper #216) — Summary of Revisions

**Paper #216, "MaestroRAG: Orchestrated Pipeline Architecture for Efficient RAG on Edge Devices"**
**10 August 2026**

This document lists the changes made in response to the seven required revisions, gives the location of each change in the revised PDF, and states plainly the one request that is not yet fully satisfied.

## How to read this revision

Text added during this revision is set in blue; unchanged text is black. This is a review aid only, controlled by a single switch in the source, and it will be turned off for the camera-ready so the final paper prints entirely in black. The revised paper is 13 pages.

## Two renumberings to be aware of first

The revision adds three tables and converts one figure into a table, so two of the numbers cited in the shepherd comment now refer to different objects. Please read the two items below before the rest of this document.

- **The submitted paper had a single table, TABLE 1, which was the caching table.** The revision adds three tables ahead of it, so **the caching table is now TABLE 4** (page 10). The revision request for "Table 1" is answered under item 4 below, at TABLE 4.
- **The submitted Figure 6 was the power and energy plot.** It is now **TABLE 3** (page 9); the reasoning is under item 3. As a consequence the submitted **Figure 7 is now Figure 6** (page 11). Figures 1 through 5 keep their numbers.

## 1. Latency breakdown

> Please add the latency breakdown to the paper and explain it thoroughly.

Added as **TABLE 2**, on page 7, and a new **Section 5.2, "Stage-Level Latency Breakdown"**, whose heading closes page 7 and whose text runs on page 8. The table carries the measured per-stage costs at the common operating point from the rebuttal: RTX 4090, DB=4M, BS=8. Stages that a system measures as one fused quantity are shown as spanned cells, and a cost a system does not report separately is left as an empty cell, so no cell implies a measurement that was not taken.

The text of Section 5.2, on page 8, explains each baseline individually rather than summarising them together. EdgeRAG spends 25.19 s in fused retrieval and augmentation, which is the cost of generating embeddings on demand. FlashRAG pays 0.73 s to load the encoder and a further 2.20 s to load the LLM, which are model reloads. PipeRAG measures its three CPU stages separately but pays up to 2 s in synchronization, serialization and timeout, which is contention between stages. MaestroRAG reports 0.20 s encoding, 1.60 s fused retrieval and augmentation, and 0.20 s scheduler cost.

Two scoping statements appear in both the caption and the text, because both matter for reading the table correctly. Generation is excluded because its settings are identical across all four systems and it is therefore not a source of difference between them. Caching was disabled for these measurements and for the primary results reported throughout the section.

## 2. Definition of edge

> Please clearly define what “edge” means in the context of your paper and explain why the systems used in your evaluation fall into the edge category according to your definition.

Added as a new **Section 2.1, "Deployment Scope"**, on page 2. The paper now states that it uses *edge* to mean *personal-computing edge*: a local compute node running RAG for a single user, without cloud intervention, under limited power and compute budgets. The section states that the desktop systems are better described as local/personal-computing platforms than as embedded edge devices, and that the scope runs from those platforms through embedded devices such as the Jetson AGX Orin at a 15 W cap.

The same section answers the objection that unified memory removes the need for the proposed orchestration. Unified memory removes the PCIe-copy cost, but it removes neither the single-GPU encode/generate contention behind the structural hazard nor the competition among the encoder, the retrieval working set and the KV cache under a constrained memory and power budget. The section closes with the concrete consequence of that budget: at 15 W the Orin exposes 4 of its 12 CPU cores.

**TABLE 1** on page 2 sets the evaluated platforms against a datacenter A100, which is not a personal compute node and is included for contrast only.

**Section 5.1** on page 7 now justifies the platforms against that definition, stating that the evaluation spans two local/personal-computing platforms and one embedded device, and naming each.

## 3. Energy breakdown

> Please update Figure 6 to include a breakdown. You may also consider improving the visualization—for example, by adding a vertical line to separate the energy and power sections, which use two different y-axes.

**The breakdown is now TABLE 3, on page 9, and the figure it replaces no longer exists.** We chose a table over a revised figure for two reasons. First, these are point values at a single operating point and carry no trend, so a plot adds nothing a table does not show more precisely. Second, a table removes the two-y-axes problem the request itself identifies, rather than mitigating it with a separator: power in watts and energy in joules simply become separate rows.

TABLE 3 reports average and peak CPU power, average and peak GPU power, and CPU, GPU and total energy per query for FlashRAG, PipeRAG and MaestroRAG, followed by the stage-attributed share of CPU energy for each.

**Section 5.7**, pages 9 and 10, gives the stage shares in the text and states the measurement boundary explicitly: the shares are of idle-subtracted CPU package energy with DRAM excluded, so they are reported as proportions rather than as a decomposition of the absolute totals. The section also notes that the stage groupings differ between the latency and the energy measurements because each system reports them differently, so that a reader comparing TABLE 2 with TABLE 3 is not surprised.

**Consequence for numbering:** the submitted Figure 7 is now **Figure 6**, on page 11. Its caption has also been revised; see item 7.

## 4. Table 1 similarity matching

> Please update the analysis of Table 1 to elaborate on the similarity-matching results.

The caching table is now **TABLE 4**, on page 10, and the analysis is in **Section 5.8** on the same page.

The analysis explains the mechanism rather than the numbers alone. Exact matching returns the cached final answer and skips both retrieval and generation, placing MaestroRAG between 0.87 s and 0.92 s. Similarity matching reuses only the top-k retrieved documents and generates afresh for the new query, placing it between 3.06 s and 3.12 s. The difference between the two is therefore the cost of generation, which similarity matching still incurs. The section states explicitly that this is not a RAM-capacity effect, since that was the reading offered in the review.

The remaining gap against EdgeRAG in the similarity-match case is attributed to our process and thread handoff across workers, which adds approximately one second. EdgeRAG does not incur this cost, since its execution is largely sequential and involves no process orchestration or thread synchronization. The section states that because the measurement uses a batch size of 1 it compares our worst case against EdgeRAG's nominal case, and that the handoff is a fixed per-batch cost we therefore expect to amortize at larger batch sizes. That last point is an expectation from the cost structure, not a measurement, and the paper words it that way.

TABLE 4's caption now also states the configuration the measurement used: BS=1, a TTL of 300 s, a cache capacity of 32 entries, and 5 retrieved documents per prompt.

## 5. Adaptive batching

> Please add your discussion of adaptive matching to the paper.

Added at the close of **Section 4.1**, on page 6. The passage states that the mapper profiles generation latency across the intended prompt lengths and that adaptive batching creates memory-safe GPU quanta, then states the limit honestly: worker allocation is static within a session, and remapping cores at run time under context drift is a future extension rather than something the current system does.

## 6. Jetson and Orin characterization trends

> Please add your clarification regarding the lack of variation in the workload-characterization trends on the Jetson/Orin platform. Make sure the reason behind this observation is clearly explained in the paper.

Added as a paragraph headed **"Portability of these trends to embedded platforms"** in **Section 3.3**, on page 4. The paragraph gives the reason rather than only the observation: because the optimizations target CPU-side encoding and retrieval, the trends measured on the local/personal-computing platform are not dependent on the GPU platform and therefore carry over to Jetson and Orin. The one systematic difference is named, the elimination of PCIe transfer overhead under unified memory, and the paragraph notes that a similar trend holds across SKUs and vendors.

**Section 5.4**, where the Jetson results are reported, carries a back-reference to that paragraph on page 9, so a reader who meets the Jetson numbers first is pointed to the explanation.

## 7. Writing and presentation

> Please also improve the overall writing and presentation of the paper.

Each sub-item is answered separately below.

### 7a. Table captions

> Move all table captions above the tables.

Done. All four tables carry their captions above the table body: TABLE 1 on page 2, TABLE 2 on page 7, TABLE 3 on page 9, TABLE 4 on page 10.

### 7b. Figure captions

> Address Reviewer B’s comment regarding the figure captions.

Done. The caption in question was on the submitted Figure 7, now **Figure 6** on page 11. The interpretive sentence has been removed, and the caption now describes only what each of the three panels shows. It additionally states the operating point for panels (b) and (c), which the submitted caption did not, and expands the N/C marker: it denotes FlashRAG on Jetson, which relies on vLLM and is not compatible with that platform.

### 7c. Font size in figures

> Increase the font size of the text in ALL figures, especially Figures 1 and 3.

**This one is partly done, and the part that remains is in the two figures the request names.**

Every data figure was regenerated from its source data at final print scale, so that the placement scale is exactly 1.0 and the type is not shrunk when the figure is placed. This covers all sixteen panels of Figure 2 (page 4), Figure 4 (page 8), Figure 5 (page 9) and Figure 6 (page 11). Measured in the built PDF, every text element in all sixteen panels is exactly 8.0 pt.

Figures 1 and 3 are not yet fixed. Measured in the built PDF, the smallest text is **4.2 pt in Figure 1** (page 2) and **4.4 pt in Figure 3** (page 4). Both figures are exported artwork rather than generated plots, and the editable sources are not available to us at present, so they could not be regenerated in this round. We are recreating both and will supply corrected versions; we did not want to report this item as complete when it is not.

### 7d. White text on light backgrounds

> Do not use white text on light-colored backgrounds, such as the white text on the light green background in Figure 1.

Done. Figure 1 on page 2 has been replaced with a version in which all labels on the light green stage bars are black. No white text on a light fill remains in the figure.

### 7e. Subsection headings

> The phrase “Results on” is redundant in several subsection headings. Please revise the headings to use a consistent, parallel structure.

Done. The evaluation section now reads: Implementation Details, Stage-Level Latency Breakdown, Latency on Personal-Computing Platforms, Latency on the Embedded Platform, Latency Analysis, Throughput, Power and Energy, Software Caching, Additional Insights. The phrase "Results on" no longer appears in any heading, and the headings are parallel noun phrases.

### 7f. Section symbols

> Do not use section symbols when they are unnecessary.

Done. Cross-references now render as a single section symbol followed by the number, for example §4.2, with no duplicated "Section §" anywhere in the paper.

## Additional material integrated from the rebuttal

Four commitments the rebuttal made beyond the seven items have also been honoured.

- **Desktops renamed.** The paper now calls the desktop systems local/personal-computing platforms rather than edge devices, in Section 2.1 (page 2), TABLE 1 (page 2), Section 2.3 (page 3) and the heading and body of Section 5.3 (page 8).
- **EdgeRAG energy exclusion stated as a limitation, with the measurement boundary.** Section 5.7 (page 10) states that a per-stage energy attribution for EdgeRAG would not be comparable with the other three systems because its on-demand embedding path performs additional, non-equivalent work. TABLE 3 (page 9) records the exclusion in its notes, and the measurement boundary, idle package power subtracted and DRAM excluded, is stated in the text.
- **Runtime core remapping stated as future work.** At the close of Section 4.1 (page 6), as described under item 5.
- **The ported-optimization experiment.** Added to Section 5.9 (page 11), answering the concern that the gains are orthogonal engineering. The transferable optimizations, memory-mapped indices, warm encoder weights in DRAM, and persistent thread and core pinning, were ported to PipeRAG. At an isolated BS=1 the optimized baseline comes close to MaestroRAG, but under the same bursty Azure trace it reaches 1.38 QPS against our 1.60 QPS, still runs out of memory at BS=16, and suffers head-of-line blocking because its synchronous stages cannot admit the next batch independently.

## Corrections made beyond what was asked

While integrating the above we re-derived every quantitative claim from the measurement records and tightened several that were stated loosely or rounded inconsistently. No result changed direction and no conclusion changed; these are precision improvements.

- Section 5.5 (page 9): the speedups against FlashRAG and PipeRAG were given as a "3–4×" band and "at least 4×" against EdgeRAG. They are now the computed values, 2.5×, 3.0× and 4.4×.
- Section 5.4 (page 9): the Jetson overhead reduction was given as a 25–35% range and is now stated as up to 26%.
- Section 5.7 (page 10): the peak CPU power differences are now given as 16.36% and 8.08%.
- Section 5.7 (pages 9 and 10): energy per query is now 253.28 J/query in both the table and the text, matching the two-decimal precision of the figures it is compared against.
- Section 5.9 (page 11): the cold-start total is described as approximate, so the residual is no longer printed to two decimals; the three measured components are unchanged.
- Section 4.1 (page 6): the three-stage against four-stage result was stated as "approximately 22% improvement", which is ambiguous about its denominator. It is now 1.23×, computed from the 1.448 s and 1.178 s already given in the same paragraph.
- Section 5.9 (page 11): the caching ablation figure now states the hit rate it assumes, rather than leaving it implicit.
- Section 5.6 (page 9): the throughput figures are now reported at the precision at which they were measured.
- Three works the paper named but had not cited are now cited: vLLM, HNSW and IVF-PQ.

## Other structural changes

- **Figure renumbering.** The submitted Figure 6, the power and energy plot, is now TABLE 3; the submitted Figure 7 is now Figure 6. Figures 1 through 5 are unchanged.
- **Table renumbering.** The submitted TABLE 1, the caching table, is now TABLE 4. TABLE 1, TABLE 2 and TABLE 3 are new.
- **All data figures regenerated.** Every plotted figure was rebuilt from its source data at final print scale. The plotted values are unchanged; only the rendering is new.
- **Figure 5 float.** The Jetson comparison was a text-wrapped figure, which left a text column a few words wide beside it. It is now a normal single-column float at the same printed size, on page 9.
- **Section 2.1 is new**, which shifts the numbering of the two subsections that follow it within Section 2.
- **Section 5.2 is new**, which shifts the numbering of the evaluation subsections that follow it.
