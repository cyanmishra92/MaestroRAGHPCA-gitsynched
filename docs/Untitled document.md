# IISWC 2026 Paper \#216 Reviews and Comments

Paper \#216 Regular-MaestroRAG: Orchestrated Pipeline Architecture for Efficient RAG on Edge Devices

# Review \#216A

## Overall merit

2. Weak reject

## Reviewer expertise

3. Knowledgeable

## Experimental methodology

2. Average

## Novelty

2. Incremental improvement

## Paper summary

This paper presents MaestroRAG, a three-stage CPU-GPU pipeline for RAG inference on edge devices. The system is motivated by a workload characterization showing that encoding is compute-bound and scales well on multicore CPUs, retrieval is memory/I-O-bound with diminishing returns from parallelism, and generation is GPU-bound. Based on these findings, MaestroRAG assigns encoding and retrieval+augmentation to dedicated CPU core sets and reserves the GPU exclusively for generation. An adaptive batching and resource mapping strategy profiles latency per pipeline stage across batch sizes and core allocations and solves for the optimal resource assignment for either latency-critical or throughput-critical operation.

## Strengths

The system design is grounded in a workload characterization that explicitly measures encoding batch-size scaling, retrieval memory-bandwidth sensitivity, and generation GPU boundedness. Assigning each stage to the resource it best utilizes is a clean architectural decision justified by data.

## Weaknesses

The core idea of assigning encoding to CPU and generation to GPU for RAG on edge devices is not fundamentally new.

Jetson AGX Orin results are limited.

## Comments for authors

MaestroRAG addresses a practically important problem of efficient RAG on resource-constrained edge devices. The reviewer has the following comments.

The performance improvements are dominated by orthogonal engineering, not the stated design. The paper's central idea is "put encode+retrieve on CPU, reserve GPU for generation." But ablation shows partitioning \+ adaptive batching only gets 15.12s to 11.79s (\~1.28×), while software optimizations (shared-memory model, mmap indices, warm workers) get 11.79 to 6.5, and caching gets 6.5 to 2.0. So the CPU/GPU partitioning is the smallest improvement. Most of the win is good engineering that is orthogonal to placement and could be applied to the baselines too.

Two of three platforms are an i9-14900K workstation, not edge. The evaluated edge device Jetson, the speedup collapses to 1.25–1.35×. Worse, Jetson has unified memory, so the core motivations, CPU to GPU transfer cost and GPU OOM from hosting the encoder largely don't apply on the edge target.

# Review \#216B

* Updated: Jul 17, 2026

## Overall merit

3. Weak Accept

## Reviewer expertise

3. Knowledgeable

## Experimental methodology

2. Average

## Novelty

2. Incremental improvement

## Paper summary

This paper is about making Retrieval-Augmented Generation practical on edge devices with limited compute, memory, and power, usually with only one GPU. The core idea is that current RAG systems do not use edge hardware efficiently because they overload the GPU with multiple RAG stages. MaestroRAG treats RAG as a pipeline and assigns each stage to the hardware resource that best matches its workload.

## Strengths

Making RAG practical on resource- and power-constrained edge devices.

The core insight of reserving the GPU for generation while moving encoding and retrieval to CPU cores is interesting

## Weaknesses

The characterization is not deep enough for an IISWC-style paper.

## Comments for authors

I appreciated that the paper combines a characterization study with a system design. The main design intuition is interesting, and the paper makes a reasonable case that naive GPU-centric RAG execution can create contention and pipeline bubbles on single-GPU devices. The evaluation across both consumer-grade GPUs and Jetson also helps show that the problem is relevant across a range of edge-like platforms.

That said, I found the characterization somewhat shallow relative to what I would expect from an IISWC paper. In particular, the main latency and speedup results in Figure 4 are presented as aggregate improvements, but the paper does not sufficiently break down where the speedups come from. A breakdown  along with ablations would make the paper much stronger. A similar concern applies to the power and energy analysis in Figure 6\. The paper reports large energy savings, but only for a single configuration and without a stage-level or component-level explanation. Since the paper is motivated by edge deployment, energy should be treated as a first-class characterization dimension.

More broadly, the paper sometimes overstates generality: the strongest speedups come from desktop-class RTX platforms, while the Jetson gains are more modest, and the experiments use different LLMs across platforms. The claim of model-agnosticism would be more convincing with broader sensitivity analysis across encoders, LLMs, retrieval indexes, context lengths, and query locality patterns.

I also think some presentation and framing issues should be addressed. Example: the caption of Figure 7 currently mixes findings with figure description, and only part (a) appears to correspond to the stated “key findings”; parts (b) and (c) are latency and throughput comparisons. The caption should simply describe what each subfigure shows, leaving interpretation to the main text.

---

**Post rebuttal comments:** My questions are addressed in the rebuttal (they just needed to be reflected in the final version). With that, I would increase my post-rebuttal score to 3\. Thanks\!

## Questions to prioritize for rebuttal

1- Can you provide a latency breakdown across MaestroRAG and all baselines?

2- Can you provide a more detailed power/energy breakdown for Figure 6?

3- How general are the conclusions across models, retrieval indexes, and platforms?

# Review \#216C

## Overall merit

3. Weak Accept

## Reviewer expertise

2. Some familiarity

## Experimental methodology

2. Average

## Novelty

3. New contribution

## Paper summary

This paper proposes MaestroRAG, a fine-grained, three-stage pipeline system that processes encoding, retrieval+augmentation, and generation across CPU and GPU for balanced resource utlization while achieving good performance for both latency-critical and throughput-oriented cases.

## Strengths

+ Detailed characterization of the four RAG stages to motivate MaestroRAG  
+ Balanced three-stage heterogeneous CPU-GPU pipeline with adaptive batching

## Weaknesses

- Part of the result analysis are not detailed

## Comments for authors

This paper targets RAG on edge problem and well motivate the problem through detailed introduction and characterization of the RAG stages. The proposed three-stage heterogeneous CPU-GPU pipeline balances the computation of different stages while maintaining their elastic control. The adaptive batching further adapt to improve the computation balance of different stages and achieve a better gain in latency reduction and throughput improvement.

In terms of the result, in TABLE 1, MaestroRAG incurs higher latency than EdgeRAG for similarity-match scenarios. Since both exact match and similarity match apply software caching, why exact match performs better? Is it because RAM is enough and cache all, while similarity match only cache items with high similarity? In addition, why similarity-match in MaestroRAG is worse than the one in EdgeRAG?

For the generation stage, in practice, the generation time depends on the context length for KV cache and may turn into a bandwidth problem. Can the adaptive batching adjust the allocation of the cores to the first two stages to improve the system throughput?

Minor: with Section 4, there is no need to have the section symbol, i.e., Section \\S4.

## Questions to prioritize for rebuttal

1. Please elaborate on the similarity-match result analysis of TABLE 1\.  
2. Please discuss the adaptive batching for runtime adjustment to adapt to larger context.

# Review \#216D

## Overall merit

3. Weak Accept

## Reviewer expertise

2. Some familiarity

## Experimental methodology

2. Average

## Novelty

3. New contribution

## Paper summary

This paper proposes the edge-side RAG characterization and computational pipeline that breaks down how CPU and GPU handle RAG tasks across both CPUs and GPUs for latency-critcal vs. throughput-critical tasks.

## Strengths

+ The proposed pipeline is interesting and seems to be able to leverage the observed behavior of RAG in edge GPUs to accelerate small-scale RAG systems  
+ The proposal seems effective at separating out how resources can be utilized for latency vs throughput goals.  
+ Evaluation is done on multiple types of edge GPUs, ranging from the desktop RTX 40X0 to the edge Jetson Orin GPUs

## Weaknesses

- The scope is limited to small-scale RAG systems and to somewhat older LLM models.  
- Evaluation is done on a limited set of GPUs, while the observation might also be applicable to larger-scale RAG systems.

## Comments for authors

Overall, I enjoy reading this paper and going through the characterizations provided in the paper. I believe that the work can be helpful in small-scale RAG optimization. However, I also feel like it is a missed opportunity to limit the scope to edge-side RAGs, as I believe similar methodologies and the resource management strategy can also be useful in larger-scale RAGs.

At the same time, I also find the model selection (llama3.1-8B) and configurations used for the characterization in Section 3 somewhat limited, as it does not show the extremes and is only done for the RTX 4090 and 4080, and do not include the smaller Orin.

## Questions to prioritize for rebuttal

- Are there any variations in the trends for workload characterizations on the Jetson Orin?

## Rebuttal Response by Author \[Cyan Subhra Mishra [cyan@psu.edu](mailto:cyan@psu.edu)\] (706 words)

We thank the reviewers for their constructive feedback. We address the common concerns first, followed by individual questions, and will include these details in the final version.  
**Common Concerns**

At the common configuration(RTX4090, DB=4M,BS=8), excluding the identical generation settings, measured costs are:

| System | Encode | Retrieve / Retrieve+Augment | Augment | Model loads | Scheduler / sync |
| :---- | :---- | :---- | :---- | :---- | :---- |
| MaestroRAG | E=0.20s | RA=1.60s | \- | \- | scheduler=0.20s |
| EdgeRAG | E=0.28s | RA=25.19s | \- | \- | \- |
| FlashRAG | E+R=7.26s | \- | A=0.10s | encoder-load=0.73s, LLM-load=2.20s | \- |
| PipeRAG | E=6.20s | R=5.20s | A=0.10s | \- | \<=2s synchronization/serialization/timeout |

Thus, baseline bottlenecks are on-demand embedding generation(EdgeRAG),model reloads(FlashRAG), and contention/synchronization(PipeRAG). Caching was disabled for all of these (including the primary results given in the paper).

We directly tested whether our gains are merely "orthogonal engineering" by porting all “transferable” optimizations to PipeRAG: memory-mapped indices, warm encoder weights in DRAM, and persistent thread/core pinning. For an isolated batch (size=1), optimized PipeRAG reaches E=0.22s, R=1.55s, A=0.10s,close to MaestroRAG. Under steady-state continuous load (the same bursty Azure trace), however, it achieves 1.38QPS versus our 1.60QPS, still OOMs at BS=16, and suffers head-of-line blocking because its synchronous stages cannot admit the next batch independently, resulting in significant gains at scale.

Having said, that, our “engineering optimizations”, including, but not limited to the aforementioned ones are non-trivial as they require observing the pipeline's system-software-hardware interaction, which we achieve via careful characterization and fine-grained orchestration; this results in the remaining benefits of asynchronous multi-width orchestration, worker scaling and adaptive batching.

**Reviewer-A**

1. **Novelty:** We agree CPU-encode/GPU-generate placement is not new; Figure-3c credits PipeRAG. Our contribution is finer-grained orchestration: dedicated core sets, asynchronous three-stage execution, resource mapping, and adaptive batch splitting. With identical placement, three stages reduce latency 22%(1.448s-\>1.178s, excluding generation)by cutting scheduler overhead(0.391s-\>0.188s); the mapper is 8.06x faster than naive allocation(9.5s-\>1.178s); and multi-worker execution serves 3x requests for only 9% higher batch latency(4.898s-\>5.347s).  
     
2. **Edge Scope:** We treat desktops as personal-computing edge: local compute nodes running RAG without cloud intervention under limited power and compute budgets, as clarified in Section 4\. We agree they are better called local/personal-computing platforms,not embedded edge devices, and will rename accordingly. On 15W Orin, latency improves 1.35x(BS=8)and 1.25x(BS=16), while throughput is 0.43QPS versus EdgeRAG's 0.064(6.7x) and PipeRAG's 0.37(1.16x). Unified memory removes PCIe-copy costs, it does not remove single-GPU encode/generate contention (structural hazard) or competition among the encoder, retrieval working set, and KV cache under a constrained memory/power budget.

**Reviewer-B**

1. **Latency breakdown:** refer to the table above.  
     
2. **Power breakdown:** After subtracting idle package power, stage-attributed energy shares(DRAM excluded)are FlashRAG:79.2%R+A, 19.1%generation-driving, 1.8%other; PipeRAG:20.4%E, 64.5%R, 0%A, 15.6%G; MaestroRAG:5.5%E, 83.2%RA, 11.2%G. EdgeRAG is excluded because its on-demand embedding path performs additional, non-equivalent work; we will state this limitation and the measurement boundary explicitly.  
     
3. **Generalization:** Across 3 hardware platforms, 3 models, and multiple indexing schemes, our findings generalize well; for new configurations, the mapper re-profiles when the hardware or LLM changes. Our evaluation reports sensitivity to indexing and context length: IVF-Flat/IVF-PQ/HNSW improve latency by 29.27%/28.15%/32.18%, while increasing the query to 100 tokens raises encoding and generation latency by 1.2% and 12%, respectively. Section-5.7 additionally evaluates an 80%-similar-query workload. The evaluated generation models are Llama-3.1-8B(RTX4090), OPT-2.7B(RTX4080), and Llama-3.2-1B(Orin,15W), sized to each platform's memory/power budget.

**Reviewer-C**

1. **Similarity match:** Exact-match returns the cached final answer, skipping retrieval+generation(0.87-0.92s). Similarity-match reuses only top-k documents and freshly generates for the new query(3.06-3.12s); this is not a RAM-capacity effect. Our current process/thread handoff across workers adds \~1.1s, explaining the gap versus EdgeRAG. EdgeRAG does not incur these overheads from process orchestration, thread synchronization, or similar coordination mechanisms; its execution is largely sequential and hence has lesser overhead. Our experiment is for batch size of 1 which compares our worst case against EdgeRAG’s nominal. However, at larger batch sizes this orchestration cost gets amortized.  
     
2. **Adaptive batching:** The mapper profiles generation across intended prompt lengths, but worker allocation is static within a session. Adaptive batching creates memory-safe GPU quanta; runtime core remapping under context drift is a future extension, which we will state clearly. We will also remove redundant "Section section-symbol" usage.

**Reviewer-D:**  
Because our optimizations focus on CPU-side encoding and retrieval, the trends observed on standard devices hold true for Jetson/Orin platforms. The primary difference is the elimination of PCIe transfer overhead in unified memory systems. A similar trend is also observed across SKUs and vendors.

## Comment @A1 by Reviewer B

Dear authors,

Congratulations, the PC has decided to accept your paper with shepherding\! The email from the Chairs has more details on the shepherding process. We are expecting a revised version by August 10\.

The reviewers appreciate your efforts to address their concerns in the rebuttal. Thank you\! However, because the rebuttal includes important additional details that must be thoroughly integrated into the paper, they came to the conclusion that the following seven revisions are necessary and must be added to the paper before it gets accepted:

1- Please add the latency breakdown to the paper and explain it thoroughly.

2- Please clearly define what “edge” means in the context of your paper and explain why the systems used in your evaluation fall into the edge category according to your definition.

3- Please update Figure 6 to include a breakdown. You may also consider improving the visualization—for example, by adding a vertical line to separate the energy and power sections, which use two different y-axes.

4- Please update the analysis of Table 1 to elaborate on the similarity-matching results.

5- Please add your discussion of adaptive matching to the paper.

6- Please add your clarification regarding the lack of variation in the workload-characterization trends on the Jetson/Orin platform. Make sure the reason behind this observation is clearly explained in the paper.

7- Please also improve the overall writing and presentation of the paper. In particular:

- Move all table captions above the tables.  
    
- Address Reviewer B’s comment regarding the figure captions.  
    
- Increase the font size of the text in ALL figures, especially Figures 1 and 3\.  
    
- Do not use white text on light-colored backgrounds, such as the white text on the light green background in Figure 1\.  
    
- The phrase “Results on” is redundant in several subsection headings. Please revise the headings to use a consistent, parallel structure.  
    
- Do not use section symbols when they are unnecessary.

