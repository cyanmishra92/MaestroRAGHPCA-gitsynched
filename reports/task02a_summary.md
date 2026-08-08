# Task 2a — Summary

**Amendment to Task 2.** The definition Task 2 wrote was composed rather than borrowed: it
defined "edge" through four architectural criteria — a single shared accelerator, no cloud
offload, a fixed power/thermal budget, single-model memory — that the rebuttal never
asserts, and which a single-GPU multi-tenant server would also satisfy. Under
`docs/GROUND_TRUTH_PROTOCOL.md` §2, that is new reasoning introducing an explanation the
rebuttal does not make.

This amendment re-sources the definition from the rebuttal's own sentences and brings the
three passages that leaned on the old criteria into line. **Task 2's structural work
stands unchanged**: the subsection and its position, the label `sec:BG:Scope`, the
`\input` of the hardware table, the unified-memory merge in the Jetson column, and the
caption-above-tabular placement.

Four `.tex` files touched, one line to four lines each. `design.tex` untouched.

---

## 1. Full text of every changed passage

### 1.1 `background&motivation.tex` — §2.1 body (replaced wholesale)

The `\subsection` line, `\label{sec:BG:Scope}`, the `newtext` wrapper, and the
`\input{TablesAlgos/Jetson4090A100}` that follows are all exactly as Task 2 left them.
Only the body between `\begin{newtext}` and `\end{newtext}` changed:

```latex
We use \emph{edge} in this paper to mean \emph{personal-computing edge}: a local compute
node running RAG for a single user, without cloud intervention, under limited power and
compute budgets. The two classes of user task our design targets (\Cref{sec:04Design})
are personal-computing tasks in this sense. The desktop systems we evaluate are
accordingly better described as \emph{local/personal-computing platforms} than as
embedded edge devices, and the scope extends from those platforms through embedded
devices such as the Jetson~AGX~Orin at a 15\,W cap. \Cref{tab:spec_comparison} sets both
against a datacenter A100, which is not a personal compute node. Unified memory does not
remove the need for the orchestration we propose: it removes the PCIe-copy cost, but
neither the single-GPU encode/generate contention behind the structural hazard of
\Cref{sec:intro}, nor the competition among the encoder, the retrieval working set, and
the KV cache under a constrained memory and power budget. That budget is
tight---at 15\,W the Orin exposes 4 of its 12 CPU cores (\Cref{subsec:implementation}).
```

**213 → 173 words.** Six sentences, all mapped in §2.

### 1.2 `implementation&eval.tex` — §5.1 Deployment System

Opening clause:

```latex
\new{Following \Cref{sec:BG:Scope}, our evaluations span two local/personal-computing
platforms and one embedded device:}
```

*(was: "our evaluations span both edge tiers---two local/personal-compute platforms and
one embedded platform:")*

Appended justification, replacing Task 2's four-criteria paragraph:

```latex
\new{All three are personal-computing edge nodes in the sense of \Cref{sec:BG:Scope}:
each runs RAG locally for a single user, without cloud intervention, under limited power
and compute budgets---explicitly so on the Jetson, where the 15W cap leaves 4 of its 12
CPU cores available.}
```

**127 → 61 words.** The three numbered hardware descriptions between these two edits are
**byte-identical to their pre-Task-2 state** — no specification was touched by Task 2 or
by this amendment.

### 1.3 `introduction.tex` — forward pointer (one clause, adjusted)

```latex
However, deploying RAG efficiently on edge devices, which typically have a single GPU
shared for all  tasks, remains challenging\new{---\Cref{sec:BG:Scope} defines the
personal-computing edge setting we target}.
```

*(was: "---we define \emph{edge} by deployment constraint rather than form factor in
\Cref{sec:BG:Scope}")* — adjusted because "deployment constraint rather than form factor"
named the framing that no longer exists. Still one clause. The comma-space typo fix Task 2
made on this line stands.

### 1.4 `TablesAlgos/Jetson4090A100.tex` — caption (first sentence replaced)

```latex
\caption{\new{The personal-computing edge platforms we evaluate---a
local/personal-computing desktop (RTX\,4090) and an embedded device
(Jetson~AGX~Orin)---set against a datacenter accelerator (A100), which is not a personal
compute node. Jetson Orin's 64\,GB is a \emph{single unified} LPDDR5 pool serving CPU and
GPU, not memory additional to the main-memory row. The A100 column is shown for contrast
only and is not an evaluation platform.}}
```

Sentences 2 and 3 are Task 2's, unchanged. Only sentence 1 — which invoked "share a
single accelerator across every pipeline stage and size memory for one model" — was
replaced. **The table body, the `64 (unified)` merge, and the caption's position above the
`tabular` are all untouched.**

### 1.5 `design.tex` — confirmed unaffected

`git diff HEAD -- design.tex` is empty. Line 50 survives verbatim:

> "Our design for an edge personal computing device targets two main types of user tasks:
> latency-critical and throughput-critical. A latency-critical task involves a virtual
> assistant that provides real-time insights, such as calendar summaries. A
> throughput-critical task focuses on generating recommendations for shopping,
> entertainment, or financial investments based on data from e-commerce, entertainment,
> and banking apps."

§2.1 now points at this by reference (`\Cref{sec:04Design}`) without restating it, which
is what the rebuttal's *"as clarified in Section 4"* asks for.

---

## 2. Sentence-by-sentence provenance

**R** = rebuttal (`docs/Untitled document.md:214`, Reviewer-A #2 — the "Edge Scope" answer).
**P** = the paper.

### §2.1 — six sentences

| # | Sentence (abbreviated) | Derives from |
|---|---|---|
| 1 | "We use *edge* … to mean *personal-computing edge*: a local compute node running RAG for a single user, without cloud intervention, under limited power and compute budgets." | **R:** *"We treat desktops as personal-computing edge: local compute nodes running RAG without cloud intervention under limited power and compute budgets."* — the three properties verbatim. "for a single user" unpacks R's *personal-computing* and is carried by the single-user examples in **P** `design.tex:50` that R points at. |
| 2 | "The two classes of user task our design targets (`\Cref{sec:04Design}`) are personal-computing tasks in this sense." | **R:** *"…as clarified in Section 4."* · **P** `design.tex:50`: *"Our design for an edge personal computing device targets two main types of user tasks: latency-critical and throughput-critical."* Referenced, not restated. |
| 3 | "The desktop systems we evaluate are accordingly better described as *local/personal-computing platforms* than as embedded edge devices, and the scope extends … through embedded devices such as the Jetson AGX Orin at a 15 W cap." | **R:** *"We agree they are better called local/personal-computing platforms, not embedded edge devices, and will rename accordingly."* · Jetson/15 W from **P** `implementation&eval.tex:11`. |
| 4 | "`\Cref{tab:spec_comparison}` sets both against a datacenter A100, which is not a personal compute node." | Table content from the `edge vs. server` tab (A100 column). The predicate is sentence 1's definition applied to the A100 — no new property asserted. |
| 5 | "Unified memory … removes the PCIe-copy cost, but neither the single-GPU encode/generate contention behind the structural hazard of `\Cref{sec:intro}`, nor the competition among the encoder, the retrieval working set, and the KV cache under a constrained memory and power budget." | **R:** *"Unified memory removes PCIe-copy costs, it does not remove single-GPU encode/generate contention (structural hazard) or competition among the encoder, retrieval working set, and KV cache under a constrained memory/power budget."* — near-verbatim. The `\Cref{sec:intro}` points at **P** `introduction.tex:172`, where the paper already names the structural hazard. |
| 6 | "That budget is tight—at 15 W the Orin exposes 4 of its 12 CPU cores (`\Cref{subsec:implementation}`)." | "constrained budget" from **R** (sentence 5's source). "4 cores" from **P** `design.tex:136` footnote: *"With Jetson at a 15W power budget …, we get 4 cores to work with."* "12" from `edge vs. server`!F15. "15 W" from **P** `implementation&eval.tex:11`. |

### §5.1 — two passages

| # | Sentence | Derives from |
|---|---|---|
| 1 | "Following `\Cref{sec:BG:Scope}`, our evaluations span two local/personal-computing platforms and one embedded device:" | **R:** *"better called local/personal-computing platforms, not embedded edge devices."* |
| 2 | "All three are personal-computing edge nodes … each runs RAG locally for a single user, without cloud intervention, under limited power and compute budgets—explicitly so on the Jetson, where the 15W cap leaves 4 of its 12 CPU cores available." | **R:** the three properties, applied to the three platforms **R** already applies them to. 15 W from **P** `implementation&eval.tex:11`; 4 cores from **P** `design.tex:136`; 12 from `edge vs. server`!F15. |

### Introduction and caption

| Passage | Derives from |
|---|---|
| "`\Cref{sec:BG:Scope}` defines the personal-computing edge setting we target" | **R:** the term *personal-computing edge*. |
| Caption sentence 1 | **R:** *local/personal-computing platforms* / *embedded edge devices*; table columns from `edge vs. server`!F13/G13/H13. |
| Caption sentences 2–3 | Task 2, retained. `edge vs. server`!F16 and !F18 both = 64; **P** `implementation&eval.tex:11` ("64 GB of unified memory"). A100 appears in no experiment. |

**Every sentence maps. No numeral is new** — 15, 4, 12, 64 are the same four that Task 2
traced, all still from the same cells and lines.

---

## 3. Removal log

Thirteen claims taken out of the paper. **None was silently discarded**; each appears below
as a recommendation for you to approve or reject.

### Removed from §2.1

| # | Removed text | Why | Recommendation |
|---|---|---|---|
| 1 | "We use *edge* to denote a deployment constraint rather than a form factor." | Framing claim; not in the rebuttal. | **Drop.** The rebuttal names a *setting*, not a taxonomy of constraint-vs-form-factor. |
| 2 | Criterion (i): "a *single* accelerator is shared by every pipeline stage, making contention structural rather than a scheduling choice" | Architectural criterion the rebuttal never asserts as definitional. | **Drop as a definition.** The single-GPU structural hazard is real and already stated in §1 and in the rebuttal — but as a *property of the hardware the paper targets*, not as a test for membership in "edge". It survives in §2.1 sentence 5. |
| 3 | Criterion (ii): "no cloud offload is available, so the entire pipeline is resident locally **for privacy and latency**" | The no-cloud property is the rebuttal's and was kept. The *"for privacy and latency"* rationale and the criterion framing are not. | **Property kept, rationale dropped.** The privacy/latency motivation already exists at `introduction.tex:161` as motivation; repeating it as part of a definition over-claims. |
| 4 | Criterion (iii): "the power and **thermal** budget is **fixed and non-elastic**" | "Limited power budget" is the rebuttal's and was kept. "Thermal", "fixed", and "non-elastic" are additions. | **Drop the qualifiers.** If you want the non-elasticity argument, it needs a source. |
| 5 | Criterion (iv): "memory is provisioned for one model, not a model zoo" | Wholly invented. Appears in no source. | **Drop.** |
| 6 | "Two tiers satisfy all four and differ in scale, not in kind." | Depends on the four criteria; also asserts an equivalence the rebuttal does not. | **Drop.** |
| 7 | "…a datacenter A100, which fails (i), (iii), and (iv)." | Depends on the invented criteria. | **Replaced** with "which is not a personal compute node" — the definition applied directly. |

### Removed from §5.1

| # | Removed text | Why | Recommendation |
|---|---|---|---|
| 8 | "Each provisions a single GPU that every pipeline stage must share" | Criterion (i). | **Drop as justification.** True of the hardware, but it is not why these platforms are edge. |
| 9 | "holds enough VRAM or unified memory for one generation model rather than a resident model zoo—24 GB, 16 GB, and 64 GB shared with the host, respectively" | Criterion (iv). The three capacities remain in the untouched hardware list immediately above. | **Drop.** No information lost — the numbers are still on the page. |
| 10 | "Their power and thermal budgets are fixed rather than elastic: the desktops are bounded by a single stock chassis" | Criterion (iii), plus a chassis mechanism with no source. | **Drop.** |
| 11 | "The two tiers therefore differ in scale alone, which is why the same orchestration is evaluated unchanged across both." | Asserts a *reason* for the experimental design that no source states. | **Consider for a later task with a source.** It is a reasonable thing to say and would strengthen §5.1, but it needs the author's assent — it explains a methodological choice. |

### Removed from the introduction and the caption

| # | Removed text | Why | Recommendation |
|---|---|---|---|
| 12 | "we define *edge* by deployment constraint rather than form factor" | Same framing as #1. | **Replaced** by a pointer that names the setting instead. |
| 13 | "share a single accelerator across every pipeline stage and size memory for one model; the datacenter A100 does neither" | Criteria (i) and (iv). | **Replaced** by the personal-compute-node contrast. |

### The five arguments the brief expected to find — none were present

The brief instructed: *"Remove, do not rewrite: any argument that the definition explains
the paper's batch sizes, trace downscaling, static worker allocation, session-level cache
locality, or the throughput experiment's single-user character."*

**Task 2's version contained none of these five.** Its §2.1 and §5.1 additions never
mentioned batch sizes, trace downscaling, static worker allocation, cache locality, or the
throughput experiment. Verified by re-reading the Task 2 commit (`0dbf546`) in full.
Nothing was removed on that basis because there was nothing to remove; the log above covers
what was actually there. Flagged under §6.1 as a divergence from the brief's expectation.

---

## 4. Diff summary against Task 2 (`0dbf546`)

```
 TablesAlgos/Jetson4090A100.tex |  2 +-      caption sentence 1
 background&motivation.tex      |  2 +-      §2.1 body
 implementation&eval.tex        |  4 ++--    opening clause + justification
 introduction.tex               |  2 +-      forward-pointer clause
 reports/verify_numbers.md      | 52 +++---  regenerated
 5 files changed, 29 insertions(+), 33 deletions(-)
```

`design.tex` untouched. `refs.bib` and `reference.bib` untouched.

Prose volume:

| Passage | Task 2 | Task 2a | Δ |
|---|---:|---:|---:|
| §2.1 body | 213 words | **173** | −40 |
| §5.1 new prose | 127 words | **61** | −66 |
| Table caption | 69 words | **66** | −3 |
| **Total new prose** | **409** | **300** | **−109 (−27%)** |

Shorter, as the brief said it should be.

---

## 5. Verification

### Build

| | |
|---|---|
| `make` | **exit 0**, 12 pages |
| LaTeX errors | **0** |
| Undefined references | **0** — `sec:BG:Scope` → §2.1 (p2); `tab:spec_comparison` → Table 1 (p2) |
| Undefined citations | **0** |
| `hyperref` token warnings | 4 — unchanged from the pre-Task-2 baseline |
| All 41 references render | ✅ (markers `[1]`–`[41]` all present) |

### Revision modes — pixel-verified

| Page | Differing pixels | mode 1 | mode 0 |
|---|---:|---|---|
| 1 (intro clause) | 1,971 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 2 (§2.1 + Table 1) | 43,583 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 7 (§5.1) | 11,146 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 3–6, 8–12 | **0** — pixel-identical | | |

`\revmode` restored to `1`.

### `verify_numbers.py`

```
checks : 41 PASS / 5 FAIL / 1 UNVERIFIABLE
drift  : none
```

Identical to Task 2's result. **All nine hardware-table checks still PASS**
(`hwtable_cores_*`, `hwtable_mainmem_*`, `hwtable_vram_*`). The five known FAILs and the
one UNVERIFIABLE are untouched, exactly as Task 1 left them.

### Page count

**12 pages** — the same in all three states. But the shorter prose gave back roughly half
a page of downstream shift:

| Landmark | pre-Task 2 | Task 2 | **Task 2a** |
|---|---:|---:|---:|
| §2.1 Deployment Scope | — | 2 | **2** |
| §3 Detailed Characterization | 2 | 3 | 3 |
| §5.1 Deployment System | 6 | 7 | 7 |
| §5.2 Results on RTX | 7 | 8 | **7** ← recovered |
| §5.6 Power | 8 | 9 | 9 |
| §6 Related Work | 10 | 11 | **10** ← recovered |
| §7 Conclusions | 10 | 11 | 11 |

The reference list still begins partway down page 11 and ends on page 12, as in Task 2.

### Bibliography

Byte-identical to the **pre-Task-2** state:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

### PDF

Not committed (gitignored, untracked). Timestamped copy:
**`reports/task02a_main_20260808-1329.pdf`**.

---

## 6. Things that contradict the instructions, or that you should decide

### 6.1 Four of the five arguments the brief expected to remove did not exist

Covered in §3 above. Task 2's version argued only from the four architectural criteria; it
never connected the definition to batch sizes, trace downscaling, static worker allocation,
cache locality, or the throughput experiment. If you were remembering a draft that did make
those connections, it is not the one that got committed — worth confirming before the next
task builds on the assumption.

### 6.2 §2.1 now uses four `\Cref`s, taking the `Section §N` count from 13 to 15

The paper renders `\Cref{sec:...}` as "Section §N" — word *and* sign — a camera-ready
blocker for Item 7 that the rebuttal itself promises to fix (*"We will also remove
redundant 'Section section-symbol' usage"*).

| State | Instances |
|---|---:|
| pre-Task 2 | 9 |
| Task 2 | 13 |
| **Task 2a** | **15** |

Task 2a adds two over Task 2 because grounding the scope in Section 4 (`\Cref{sec:04Design}`)
and pointing at the paper's own structural-hazard statement (`\Cref{sec:intro}`) each cost
one. Both references were required by the brief (steps c and d). **Item 7's sweep must
cover all six added across Tasks 2 and 2a.**

### 6.3 `background&motivation.tex:50` still contradicts the definition — and now more sharply

Task 2's terminology audit flagged this line:

> "The fundamental RAG stages … are consistent across datacenter servers, **desktops, and
> edge devices**, but their execution varies widely with hardware constraints."

Under Task 2's definition it was wrong. Under the rebuttal's it is wrong in the same way
and for a cleaner reason: the rebuttal states plainly that desktops **are**
personal-computing edge. This sentence sits about four lines below §2.1 and lists them as
something else. Still out of scope here; still the first thing I would fix.

Suggested: *"…consistent across datacenter servers and the personal-computing edge
platforms of `\Cref{sec:BG:Scope}`, but their execution varies widely with hardware
constraints."*

### 6.4 "Renaming accordingly" is not yet complete

The rebuttal promises *"will rename accordingly"*, which is broader than the two passages
this task touched. Task 2's audit identified `implementation&eval.tex:19` ("the tight power
and energy constraints of **the edge devices**") as the other place the desktops are called
devices. Unchanged here — outside this amendment's scope, but it is part of the same
binding promise (protocol §5, item 1).

### 6.5 One judgement call worth naming: "for a single user"

The rebuttal says *personal-computing edge* and *local compute nodes*; it does not use the
words "single user". The brief's step (a) does, and `design.tex:50`'s examples are one
person's calendar and one person's e-commerce, entertainment, and banking apps — which is
what the rebuttal points at with *"as clarified in Section 4."* I judged this an
unpacking of *personal-computing* rather than a new property, and it is the one phrase in
§2.1 that is an interpretation rather than a transcription. Flagging it so you can strike
it if you read it differently; the sentence works without it.

---

## 7. Acceptance criteria

| | Criterion | Status |
|---|---|---|
| ☑ | Definition is the rebuttal's three properties; no architectural criteria carried over; no fourth invented | §2.1 sentence 1, verbatim from the rebuttal |
| ☑ | Desktops named local/personal-computing platforms, not embedded edge devices | §2.1 sentence 3; §5.1 opening clause |
| ☑ | Scope grounded in Section 4 by reference, without restating it | `\Cref{sec:04Design}`, §2.1 sentence 2 |
| ☑ | Unified-memory objection in the rebuttal's terms | §2.1 sentence 5, near-verbatim |
| ☑ | Every load-bearing Task 2 argument removed and logged | 13 entries in §3 |
| ☑ | §5.1 rewritten against the three properties; hardware specs untouched | 127 → 61 words; specs byte-identical to pre-Task-2 |
| ☑ | Table `\input`, unified-memory fix, caption-above-tabular all intact | only caption sentence 1 changed |
| ☑ | Every sentence of new prose mapped | §2 — all 6 + 2 + 1 + 3 |
| ☑ | `make` clean; blue at `\revmode=1`, black at `=0` | 0 errors, 0 undefined; RGB(0,0,255) / RGB(0,0,0) |
| ☑ | `refs.bib`, `reference.bib` byte-identical to pre-Task-2 | SHA-256 verified |
| ☑ | `verify_numbers.py` no drift | 41/5/1, nine hardware checks PASS |
| ☑ | `main.pdf` not committed; timestamped copy in `reports/` | `reports/task02a_main_20260808-1329.pdf` |
| ☑ | Committed, not pushed | separate commit; no `git push` run |
