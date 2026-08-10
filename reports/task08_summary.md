# Task 8 — Summary

Three commits. **Parts A and B** add the flag mechanism and correct eleven numeric claims.
**Part C** does the writing pass. **Parts D and E** audit and flag, changing no prose.

| | Before | After |
|---|---|---|
| `verify_numbers.py` | 98 PASS / **2 FAIL** / 1 UNVERIFIABLE | **100 PASS / 0 FAIL** / 1 UNVERIFIABLE |
| `audit_camera_ready.py` | (script was not supplied; see §7.1) | **12 pass / 9 warn / 0 fail** |
| Live em-dashes | 10 | **0** |
| `Section §N` duplications | 0 | **0** |
| Pages | 14 | **14** |

---

## 1. Part A — the flag mechanism

Added to `main.tex` beside `\revmode`, independent of it:

```latex
%%%%% AUTHOR ATTENTION FLAGS %%%%%
% 1 = show flags in red   0 = hide entirely (camera-ready)
\newcommand{\flagmode}{1}
\ifnum\flagmode=0
  \newcommand{\flag}[1]{}
\else
  \newcommand{\flag}[1]{\textcolor{red}{\textbf{[FLAG:}~#1\textbf{]}}}
\fi
```

**Verified in the text layer, not by eye.** All four switch combinations build with zero
errors and the same page count:

| `\revmode` | `\flagmode` | Pages | Errors | `FLAG` in text layer |
|---:|---:|---:|---:|---:|
| 1 | 1 | 14 | 0 | 5 |
| 1 | 0 | 14 | 0 | **0** |
| 0 | 1 | 14 | 0 | 5 |
| 0 | 0 | 14 | 0 | **0** |

Identical page counts mean the macro is metrics-neutral: turning flags off shifts nothing.
**No flag carries content the paper needs.** Every one is a question or an observation, and
the prose reads correctly with all seven deleted.

---

## 2. Part B — numeric corrections

| | Location | Was | Now | Basis |
|---|---|---|---|---|
| **B1** | §5.5 | "3--4× faster than FlashRAG (16.39 s) or PipeRAG (19.80 s)" | "2.5× and 3.0× faster … respectively" | 16.39/6.497 = 2.523; 19.80/6.497 = 3.048 |
| **B2** | §5.5 | "≥4× faster than EdgeRAG" | "4.4× faster" | 28.40/6.497 = 4.371 |
| **B3** | §5.3 | "6--12× faster processing" | "up to 12× against EdgeRAG and 2--3× against FlashRAG" | Fig. 4c spans 1.92--3.24 |
| **B4** | §5.4 | "cut overhead … by 25%--35%" | "by up to 26%" | Jetson tab: 8.6 / 23.8 / 26.0 / 20.4 at BS 2/4/8/16 |
| **B6** | §5.9 | "cost of 7 s comprising 0.36 + 3.04 + 3.36" | "approximately 7 s, of which … the remaining 0.24 s is process creation and library initialization" | the three components sum to 6.76 s |
| **B7** | §4.2 | "approximate 22% improvement" | "1.23× improvement" | 1.448/1.178 = 1.229; 18.6% or 22.9% depending on denominator, so the ratio is the unambiguous form |
| **B8** | §5.9 | "(effective) caching achieves 2.003 s" | "caching achieves 2.003 s under the 80% hit rate described in §5.8" | 0.8×0.92 + 0.2×6.497 = 2.035 |
| **B9** | §5.6 | 0.29 / 0.68 / 1.19 / 0.43 / 0.064 / 0.37 | 0.288 / 0.683 / 1.185 / 0.432 / 0.0645 / 0.370 | three significant figures throughout; the figure's bar labels moved from `.2f` to `.3g` so text and figure now agree |
| **B11** | §5.5 | "1.9×" on the 4080 | "2.0×" | 1.960, truncated where 8.848 and 5.355 were rounded to 8.8 and 5.4 |

**B10, headline operating points, attached at first use only (the abstract):**

> MaestroRAG outperforms state-of-the-art RAG systems by up to *12×* in latency and *5.6×*
> in throughput **over EdgeRAG, the latency figure at BS=8 and DB=8M; against PipeRAG, the
> strongest baseline, the throughput gain is 1.35×**, and *3×* in energy **over FlashRAG**.

Not repeated in the introduction or conclusion, per the brief.

**Two claims flagged, not changed**, as instructed:

- **Jetson caching** (§5.8): no support in Table 4 or the workbook. Flagged with the three
  options: delete, requalify, measure.
- **1.1 s handoff** (§5.8): the rebuttal's figure, where Table 4's own columns give 1.069,
  1.058 and 0.951, averaging 1.03. Flagged, noting "approximately one second" satisfies both.

**Effect on `verify_numbers.py`:** B4 and B11 were the two remaining FAILs. Both are now
PASS, and the six throughput checks were retightened to the new precision. **100 PASS / 0
FAIL / 1 UNVERIFIABLE, no drift.** The one UNVERIFIABLE is still the cold-start total: B6
made the arithmetic close, but no sheet backs any of it.

---

## 3. Part C — writing and presentation

### C1 — adapted, and the deviation is deliberate

**The brief's premise is stale, and following it literally would undo the author's own
decision from one turn ago.**

C1 says to delete `main.tex` lines 141--142, which set `\creflabelformat` to prepend `\S`,
so that no section symbol survives. Those lines no longer exist: the previous commit
(`e099211`) replaced them with `\crefformat`, at the author's explicit instruction that
references should read **"§2.1"** rather than "Section §2.1".

Deleting the symbol now would produce "Section 2.1", which is the opposite of what was
asked for. **I kept "§2.1" and did C1's other half**, which is not in conflict:

- three literal `\S\ref{...}` in live text (`design.tex` ×2, `implementation&eval.tex` ×1)
  are now `\Cref{...}`;
- `\xref` is redefined from `\S\ref{#1}` to `\Cref{#1}` (it has zero live uses, so nothing
  renders differently; the definition no longer bypasses cleveref).

One mechanism now governs every section reference, and **zero "Section §N" duplications
remain**. **This is the one place where I did not follow the brief, and it needs your
ruling:** either "§2.1" stands as you asked last turn, or you want "Section 2.1" and I
remove the six `\crefformat` lines.

### C2 — em-dashes: 10 → 0

| File | Was | Now |
|---|---|---|
| `abstract.tex` | "three edge platforms---including an NVIDIA Jetson and consumer-grade GPUs---MaestroRAG" | "…platforms, including … GPUs, MaestroRAG" |
| `introduction.tex` | "three platforms—NVIDIA RTX 4090…" | "three platforms: NVIDIA RTX 4090…" |
| `background&motivation.tex` | "stages—encoding, retrieval, augmentation, and generation—are" | "stages (encoding, … generation) are" |
| `characterization.tex` | "four stages—*encode*, …, *generate*—each" | "four stages (*encode*, …, *generate*), each" |
| `design.tex` | "for stage G (1 worker)—yields" | "for stage G (1 worker), yields" |
| `implementation&eval.tex` | "schemes---approximate nearest neighbor … HNSW---to understand" | "schemes, namely … HNSW, to understand" |

**Zero `---` and zero U+2014 remain in live text.** Part E found four `--` appositives that
C2's list did not cover; they are flagged, not changed (§6.2).

### C3 — Section 5 headings

| | Was | Now |
|---|---|---|
| 5.3 | Results on RTX 4090 and RTX 4080 Desktop | **Latency on Personal-Computing Platforms** |
| 5.4 | Results on Jetson AGX Orin | **Latency on the Embedded Platform** |
| 5.5 | Main Latency Results | **End-to-End Latency** |
| 5.6 | Throughput Evaluation | **Throughput** |
| 5.7 | Power/energy efficiency | **Power and Energy** |

All noun phrases in title case. No heading opens with "Results on"; the slash is gone. The
5.3 and 5.4 wording uses §2.1's own vocabulary rather than inventing a third term.

### C4 — captions describe rather than argue

**Figure 1**, was: *"Classical RAG Pipeline has structural hazard and CPU under-utilization.
MaestroRAG solves it with smart orchestration."*
Now: *"Stage placement in a classical RAG pipeline and in MaestroRAG. The classical pipeline
places both encoding and generation on the GPU; MaestroRAG places encoding and retrieval on
dedicated CPU cores and reserves the GPU for generation."* The claim it made is already in
§1's body text, so nothing was lost.

**Figure 4**, was: *"All speedups observed for MaestroRAG results from a concoction of
optimizations presented in …"*
Now: *"The design elements evaluated here are described in §4.1, §4.2, and §4.3."*

**Figure 6** (the one Reviewer B named), was: *"Key findings: (a) The adaptive worker
allocation technique often results in better resource partitioning combinations …"*
Now describes all three panels and **explains 6b's stacked segment**: *"…the lower segment
of the MaestroRAG bar on the RTX 4090 is the cached latency and the upper segment is the
remainder of the uncached total."* Also states what the N/A bars mean.

### C5 — superseded paragraphs, removed in full

Deletions are invisible in the blue-text diff, so both are reproduced here.

**Removed from `implementation&eval.tex` (§5.3), four lines:**

> Two major lessons emerge from Figure 4.
> First, partitioning CPU and GPU tasks carefully is crucial: forcing both encoder and
> generative model onto the GPU triggers heavy data transfers and repeated model loads.
> Second, moderate batch sizes (BS=4--8) typically provide the most efficient balance of
> I/O and compute; pushing too high eventually saturates I/O or memory, but staying too low
> underutilizes resources.
> Overall, from a *designer's perspective*, sweet-spot batching and CPU--GPU division
> together yield 6--12× latency gains over existing designs without risking out-of-memory
> failures.

**Nothing preserved.** The paragraph immediately above already says *"Pushing both encoder
and LLM to the GPU triggers repeated data transfers and frequent model reloading, while
moderate batch sizes (BS=4--8) help balance resource use"* and now carries the B3-corrected
speedup range. The one clause not literally above it, "staying too low underutilizes
resources", is stated in §3.3 as *"encoding enjoys linear core-utilization only when the
batch size is large enough to saturate all cores."*

*Side effect:* this paragraph held the second instance of the unsupported "6--12×", so B3
needed correcting in one place rather than two.

**Removed from `characterization.tex` (§3.3), four lines:**

> **Execution Breakdown Across Stages:**
> Figure 2e shows that adding CPU cores shortens retrieval latency up to 8 cores, after
> which benefits plateau because shared-resource pressure, i.e. memory bandwidth and LLC
> capacity, dominates.
> Figure 2d further decomposes retrieval into *index fetch* (I/O-bound, once per batch) and
> *similarity search* (compute-bound, per query).
> At small batches, fixed I/O cost dictates latency; at larger batches, similarity search
> and DRAM contention take over, revealing that retrieval performance is governed primarily
> by the memory hierarchy, with compute parallelism offering only secondary gains.

**One clause preserved.** Sentences two and three duplicate §3.2 verbatim in substance
(§3.2 already defines the two components and already concludes "retrieval latency is
governed more by data movement and cache behavior than raw compute"). The first sentence's
specificity was unique, so it was folded into the §3.2 sentence that narrates the same
figure:

> Figure 2e shows sub-linear latency reductions as CPU cores are increased, suggesting
> diminishing returns from parallelism**; beyond roughly 8 cores the gains plateau as memory
> bandwidth and LLC capacity dominate**.

### C6 — title

`Regular-MaestroRAG: …` → `MaestroRAG: Orchestrated Pipeline Architecture for Efficient RAG
on Edge Devices`. Verified absent from the built PDF. `showcomments`, `todonotes` and
`\revmode` untouched.

---

## 4. Part D — rebuttal coherence, flags only

Each passage added by Tasks 2 through 7, re-read against the rebuttal now that they sit
together.

| Passage | Task | Verdict |
|---|---|---|
| §2.1 Deployment Scope | 2a | **Clean.** Three properties, no fourth. |
| §3.3 trend portability | 3 | **Clean.** Three claims, near-verbatim. |
| §4.1 adaptive batching | 3 | **Clean.** Four claims, amortization still worded as an expectation. |
| §5.1 platform justification | 2a | **Clean.** |
| §5.2 breakdown + Table 2 | 5 | **Clean on values**; one wording risk, D-2 below. |
| §5.8 caching analysis | 4 | **Clean**; the 1.1 s is flagged from Part B. |
| §5.9 ported optimizations | 5 | **Clean.** |
| §5.7 Power and Energy + Table 3 | 6 | **Clean on values**; one comparability risk, D-1 below. |

**Check 1, no claim exceeds the rebuttal:** no violations found.
**Check 2, no number differs:** none. Cross-checked the handoff, the shares, the QPS values
and the stage costs against both the rebuttal and the paper's own tables.
**Check 4, no residue of Task 2's four-criteria framing:** **confirmed absent.** Searched
live text for "four conditions", "four criteria", "criteria of", "model zoo",
"non-elastic" and "form factor". **Zero hits.** Task 2a's correction is complete.

**Check 3, same fact stated the same way:**
- The handoff cost appears **once**, in §5.8, not twice as the brief anticipated. No
  inconsistency, but see D-2.
- Edge vocabulary, counted over live text only: *personal-computing edge* 3,
  *local/personal-computing platform* 4, *embedded edge device* 1, *edge device* 7,
  *edge platform* 3. The defined terms are used where the definition matters and the
  generic class term elsewhere. **No drift.**
- Stage naming: `RA` 45, "retrieval and augmentation" 7, "Retrieve+Augment" 3. `RA` is
  defined in §4.1 and the long forms appear in prose. Acceptable.

**Check 5, table consistency → FLAG D-1.** The rebuttal fuses FlashRAG's encode and retrieve
in the latency table but its retrieve and augment in the energy shares, with no encode
category at all. Both are the rebuttal's and both stand, but the spanned-cell convention
alone does not tell a reader that the *groupings differ between the two tables*. Flagged at
`implementation&eval.tex:173`.

**FLAG D-2**, at `implementation&eval.tex:73`. Table 2's 0.20 s scheduler cost (BS=8, DB=4M)
and §5.8's approximately 1.1 s worker handoff (BS=1) are different measurements that both
read as "orchestration overhead". Suggests naming them distinctly.

---

## 5. Part E — paper-wide consistency, flags only

Grouped by severity. **No prose was changed in this part.**

### Contradiction
**None found.** No number disagrees between prose, tables and figures after Part B; no
forward reference points at material that no longer exists (searched for
`fig:powerEnergyPlot` and literal "Figure 7"); no prose describes a panel position that the
Task 7 regeneration changed.

### Unsupported claim
Both carried over from Part B and flagged there: the Jetson caching speedup, and the 1.1 s
handoff against Table 4's 1.03 s.

### Drift
**FLAG E-1**, `implementation&eval.tex:225`. Figure 6's caption describes all three panels
but does not state the operating point for (b) and (c). §5.5 gives BS=8 with 4M/4M/1M and
§5.6 gives DB=4M, BS=8. Flagged rather than fixed because Part E is audit-only, though this
is a caption I wrote in Part C and would happily amend on request.

### Cosmetic
**FLAG E-2**, `design.tex:48`. `"of the two stages --  up to 128 ms on average)"` uses `--`
as a parenthetical *inside* a parenthesis.
**FLAG E-3**, `implementation&eval.tex:18`. Three appositive `--` dashes, one after each
baseline citation: `FlashRAG~\cite{...}--presents a modular RAG framework`, and likewise for
PipeRAG and EdgeRAG.

Both are genuine style-rule violations that **C2's list did not cover**: the brief
enumerated ten instances, all `---` or U+2014, and these four are the `--` form. Four
one-character fixes whenever you want them.

### Checked and clean
Configurations are stated per float except Figure 6 (E-1) and the hardware spec table, which
is not a measurement. All 41 references render. Every `TABLE n` and `Figure n` resolves to
its intended target after the Task 7 renumbering. The abstract and conclusion make no claim
the body does not support.

---

## 6. All seven flags

| Severity | File:line | Question posed |
|---|---|---|
| Unsupported | `implementation&eval.tex:279` | Jetson caching has no support in Table 4 or the workbook. Delete, requalify, or measure? |
| Unsupported | `implementation&eval.tex:276` | 1.1 s is the rebuttal's; Table 4 averages 1.03 s. "Approximately one second" satisfies both. |
| Coherence | `implementation&eval.tex:173` | Tables 2 and 3 categorize FlashRAG two different ways, both the rebuttal's. Is that legible? |
| Coherence | `implementation&eval.tex:73` | 0.20 s scheduler cost and 1.1 s handoff both read as orchestration overhead. Name them distinctly? |
| Drift | `implementation&eval.tex:225` | Figure 6's caption omits the operating point for panels (b) and (c). |
| Cosmetic | `design.tex:48` | `--` used as a parenthetical inside a parenthesis. |
| Cosmetic | `implementation&eval.tex:18` | Three appositive `--` dashes after the baseline citations. |

---

## 7. Things that contradict the instructions, or that you should decide

### 7.1 The audit script was never supplied

The brief says `tools/audit_camera_ready.py` is "supplied separately" and quotes a baseline
of 45 pass / 24 warn / 12 fail. **It is not in `tools/`, anywhere in the repository, or in
`~/Downloads`.** I could not add or run a script I do not have.

I wrote a replacement to the brief's description: a read-only gate covering em-dashes,
section symbols, `\vspace` hacks, British spelling, draft artifacts, annotation macros,
caption configuration, arguing captions, edge vocabulary, open flags, the build log and
`verify_numbers` agreement. It is committed at `tools/audit_camera_ready.py` and its
docstring records this provenance.

**Its tallies are not comparable to 45/24/12** because it is a different script. Mine
reports **12 pass / 9 warn / 0 fail** (8/10/0 immediately after `make`, which deletes
`main.log` and so blanks the four build checks; run `pdflatex` directly for those).

The brief's named false positive is honored: the British-spelling probe is anchored so
`analyze`, `amortize` and `optimize` cannot match. I also narrowed the en-dash check to
skip `X--Y` between word characters, which was flagging `CPU--GPU` and `(b--c)`.

### 7.2 C1 conflicts with your instruction from one turn ago

Covered in §3. **This is the one instruction I did not follow**, and it needs your ruling.
Everything else in Part C is done as written.

### 7.3 The paper is 14 pages and Part C did not bring it back to 13

It went to 14 when the `\vspace` hacks came out last turn. C5 removed eight lines, but C4's
new captions are longer than the ones they replace, particularly Figure 6's, so the two
roughly cancel. **The body ends on page 12; the spill is bibliography.** The options remain
the three from last turn: accept 14 if references are excluded from the limit, cut further
prose, or revert the `\vspace` removal.

### 7.4 Section numbering in the brief no longer matches the paper

The brief refers to §5.2, §5.3, §5.4, §5.5, §5.7 and §5.8. After Task 5 inserted the
breakdown subsection, those are §5.3, §5.4, §5.5, §5.6, §5.8 and §5.9. I located each
correction by its text rather than its number; the table in §2 uses the current numbers.

### 7.5 One Part B item needed a judgment call

B9 asked for "one precision applied everywhere". Two decimal places would have rendered the
Jetson EdgeRAG value as 0.06 and broken the 6.7× ratio that follows it. I used **three
significant figures** in the text and changed the Figure 6c bar labels from `.2f` to `.3g`
so the figure agrees. That is a figure regeneration inside Part B; it is one format
specifier and the plotted values are untouched.
