# Task 9 — resolve flags, hallucination audit, reference audit, remove slop

**Branch** `main` · **Commits** `cde2933` (A–B), `c31d328` (C), `e1358f6` (D), `b3a3fed` (E)
**Not pushed.** The author pushes.
**PDF of record** `reports/task09_main_20260810-1742.pdf` (`\revmode=1`, `\flagmode=1`).

**Page count: 14 → 13.** The paper entered Task 9 at 14 pages and leaves at 13. The page
came back from three deletions in Part E (the §5.9 insights paragraph, four summary
sentences, and the conclusion's closing clause), not from any spacing change.

---

## Headline

| | |
|---|---|
| Flags entering Task 9 | 7 |
| Flags resolved and removed | 7 |
| Flags newly raised (untraceable numerals) | 4 |
| **Flags surviving in the paper** | **4** — all untraceable numerals, all pre-existing |
| Numerals traced to an authorised source | all but four |
| Bibliography entries | 41 → 44 |
| Fabricated references | 0 (every new entry Crossref-verified before it was written) |
| `verify_numbers` | 100 PASS / 0 FAIL / 1 UNVERIFIABLE, **no drift** — unchanged start to finish |
| Build | 0 errors, 0 overfull > 10 pt, 0 undefined refs, 0 undefined citations, 0 bibtex warnings |

**Nothing in this task was invented.** Where a fact was needed and neither the paper nor
the rebuttal contained it, a flag was left in place. Four such flags survive; that is the
correct outcome, not a shortfall.

---

## Part A — the seven author flags

Each flag is given as it stood, then what replaced it.

### A1 · §4.1 parenthetical dash

> **Before** `...latency increase of the two stages --- up to 128 ms on average)`
> **After** `...latency increase of the two stages, up to 128 ms on average)`

Punctuation only. No number, no description changed.

### A2 · §5.1 three appositive dashes

> **Before** `(1) FlashRAG~\cite{jin2024flashrag}--presents a modular RAG framework...; (2) PipeRAG~\cite{jiang2024piperag}--a server-oriented pipeline design; and (3) EdgeRAG~\cite{EdgeRAG}--mitigates memory usage by caching...`
> **After** `(1) FlashRAG~\cite{jin2024flashrag}, a modular RAG framework...; (2) PipeRAG~\cite{jiang2024piperag}, a server-oriented pipeline design; and (3) EdgeRAG~\cite{EdgeRAG}, which mitigates memory usage by caching...`

The EdgeRAG item was restructured from a fragment into a clause. The other two take a comma.

### A3 · "are these two overheads the same quantity?"

**Resolved with no prose change.** The two already carry distinct names taken from the
rebuttal itself: "scheduler cost" (§5.2) and "process and thread handoff across workers"
(§5.8). Neither is called generic orchestration overhead anywhere. Verified across
`implementation&eval.tex`, `design.tex` and `TablesAlgos/LatencyBreakdown.tex` before the
flag was removed.

### A4 · §5.7 stage groupings differ between Table 2 and Table 3

One sentence added, stating the fact and nothing more:

> **Added** `The stage groupings differ between the latency and the energy measurements because each system reports them differently.`

No speculation about why any system reports them the way it does.

### A5 · Figure 6 caption did not state its operating point

> **Added** `Panel (b) uses \texttt{BS=8} with 4\,M, 4\,M and 1\,M databases on the RTX\,4090, RTX\,4080 and Jetson respectively, and panel (c) uses \texttt{DB=4\,M} and \texttt{BS=8}. N/C marks \flashRAG{} on Jetson, which relies on vLLM and is therefore not compatible with that platform.`

Copied from §5.5 and §5.6, not derived. The N/C expansion uses §5.6's own wording.

### A6 · §5.8 "approximately 1.1 s"

> **Before** `...which adds approximately 1.1\,s.`
> **After** `...which adds approximately one second.`

Table 4's own columns give 1.069, 1.058 and 0.951 (mean 1.03). "Approximately one second"
is faithful to the rebuttal's approximation and consistent with the table on the same page.
Printing 1.1 was not.

### A7 · unsupported Jetson caching claim — **deleted in full**

> **Removed, verbatim:** `On the Jetson~AGX~Orin (15\,W power cap), caching provides consistent speedups by avoiding redundant encoder invocations and memory transfers.`

Table 4 has no Jetson column and the workbook holds no caching data at all. The surrounding
paragraph reads correctly without it.

---

## Part B — the two §5.5 corrections that never landed

Traced in Task 7.5: `git show f104a44` contains no hunk for this line, so the Task 8
correction script had aborted before writing.

> **Before** `...completes inference in 6.50\,s, which is 3--4$\times$ faster than \flashRAG{} (16.39\,s) or \pipeRAG{} (19.80\,s), and $\ge4\times$ faster than \edgeRAG{}.`
> **After** `...completes inference in 6.50\,s, which is $2.5\times$ and $3.0\times$ faster than \flashRAG{} (16.39\,s) and \pipeRAG{} (19.80\,s), respectively, and $4.4\times$ faster than \edgeRAG{}, whose stage-level composition is given in \Cref{sec:breakdown}.`

Arithmetic: 16.39 / 6.497 = 2.523; 19.80 / 6.497 = 3.048; 28.40 / 6.497 = 4.371.

**Defect introduced and fixed during Part A.** Removing the flag from inside `\caption{}`
left a whitespace-only line, which LaTeX reads as `\par`; that broke the caption with four
"Paragraph ended before `\caption@prepareanchor` was complete" errors. The remnant line was
deleted and **every** caption in the paper was then scanned for the same pattern. None other
was found.

---

## Part C — hallucination audit

### C1 · cold-start residual

> **Before** `...$3.36s$ loading the generation model onto the GPU; the remaining $0.24s$ is process creation and library initialization`
> **After** `...$3.36s$ loading the generation model onto the GPU; the remainder is process creation and library initialization`

0.24 was 7 − 6.76, arithmetic performed on a total the same sentence calls *approximate*.
Printing it to two decimals asserted a precision the word denies. The three measured
components are unchanged.

### C2 · energy per query precision

> **Before** `only consuming $253.3J/query$, compared to $792.00J$ and $780.92J/query$`
> **After** `at $253.28J/query$, compared to $792.00J$ and $780.92J/query$`

Now consistent at two decimals with Table 3 and with the two figures already in the same
sentence. The only surviving `253.3` is on a commented legacy line.

### The numeral trace

Every value in Tables 2, 3 and 4, the §5.6 throughput figures, the ablation chain and the
ported-optimization figures traces to an authorised workbook tab or to a rebuttal sentence,
and all are covered by `tools/checks.yaml`. Full per-check evidence is in
`reports/verify_numbers.md`.

Worth recording: the ablation's 2.003 s and the token-sensitivity 0.6 / 1.2 / 12 percent
**are** in the rebuttal, but in `rebuttal_text.tex` rather than under `docs/`, which is why
an earlier pass had recorded them as unverifiable. They are traced.

### The four untraceable numerals — flagged, not corrected

Correcting an untraceable number by inventing a source is the one thing this task forbids,
so each is flagged in place. **All four predate this revision.**

| # | Location | Value(s) | Status |
|---|---|---|---|
| 1 | §5.5, `implementation&eval.tex:156` | tail latency 5.26 (1.04), 14.86 (1.14), 14.41 (1.09) | No authorised tab, no rebuttal sentence. Internally consistent — each P99 divided by its stated ratio reproduces the `BS=8`, `DB=2\,M` column — but consistency is not provenance. **Supply the data or drop the sentence.** |
| 2 | §4.1, `design.tex:48` | 128 ms augment-separation cost | No authorised tab, no rebuttal sentence. |
| 3 | §3.2, `characterization.tex:91` | ≈30 MB cache capacity | No authorised tab, no rebuttal sentence. |
| 4 | §5.1, `implementation&eval.tex:9` | ~70 % memory saving | No authorised tab, no rebuttal sentence. |

These are the only four `\flag{}` occurrences in the paper. They vanish entirely at
`\flagmode=0`, verified at the pixel level.

---

## Part D — reference audit

### Three entries added, each verified against Crossref *before* being written

| Key | Entry | Canonical source |
|---|---|---|
| `vllm` | Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention", SOSP 2023, pp. 611–626 | `doi:10.1145/3600006.3613165` — confirmed via `api.crossref.org/works/` |
| `hnsw` | Malkov & Yashunin, IEEE TPAMI 42(4):824–836, 2020 | `doi:10.1109/TPAMI.2018.2889473` — confirmed via `api.crossref.org/works/` |
| `ivfpq` | Jégou, Douze & Schmid, "Product Quantization for Nearest Neighbor Search", IEEE TPAMI 33(1):117–128, 2011 | `doi:10.1109/TPAMI.2010.57` — confirmed via `api.crossref.org/works/` |

No entry was added on recall. **IVF-Flat deliberately gets no new entry**: it is a FAISS
index type rather than a published method, and `\cite{faiss}` already sits in the same
sentence. Inventing a citation for it is exactly the failure this task warns against.

### D2 · one citation moved, none dropped

`Indyk and Motwani` was attached to "a similarity metric (e.g., cosine or L2 distance)" in
§2.2, where a paper about approximate nearest neighbour search and the curse of
dimensionality does not belong. It now sits on the ANN sentence in §5.9, which is what it is
actually about. The §2.2 sentence loses the citation and keeps its wording.

### D3 · two mechanical defects

- `faiss` had an empty `journal` field, which bibtex warned about on every build. Filled as
  `arXiv preprint arXiv:2401.08281`, built from the entry's **own** `eprint` field.
- Ten cited entries had acronyms that `IEEEtranS` lowercases. `LLM`, `GPUs`, `CPUs`, `RAG`,
  `KV`, `GPU` and `BERT` are now brace-protected.

No venue was changed, because no venue change was verifiable.

### D4 · resolution

All cite keys resolve. `reference.bib` untouched. Also fixed a double period in §6, where
`\paragraph{RAG Pipeline Optimization.}` carried a period the class then repeated.

Final state: **44 cited keys = 44 bibliography entries**, none unresolved, none orphaned,
0 bibtex warnings.

---

## Part E — writing pass

### E1/E2 · unsupported intensifiers, empty summary sentences, grammar

Fourteen edits. Nothing was replaced with a different intensifier; empty sentences were
removed rather than reworded.

**Deleted in full** (each restated its own paragraph and added nothing):

| Where | Removed, verbatim |
|---|---|
| §5.3 | `These experiments highlight the importance of selecting which stages run on the GPU and which on the CPU.` |
| §5.3 | `These results confirm that CPU-driven encoding and retrieval strategies are more sustainable for mid-range GPUs while still providing significant performance gains and avoiding failures on bigger inputs.` |
| §5.5 | `These findings confirm that our pipeline achieves robust, memory-aware performance across heterogeneous platforms.` |
| §5.6 | `These gains highlight the importance of a fine-grained pipeline with minimal CPU--GPU transfers, which helps the system respond more gracefully to bursty arrivals.` |
| §5.9 | `These results clearly demonstrate the effectiveness of our layered optimizations.` |

**Rewritten, side by side:**

| Where | Before | After |
|---|---|---|
| §5.6 | `reaches 1.60\,QPS, clearly ahead of` | `reaches 1.60\,QPS, ahead of` |
| §5.6 | `Despite the overall lower speed on the Jetson, our approach clearly shows that decoupling ... increases concurrency under limited DRAM, thus sustaining higher steady-state throughput.` | `Despite the overall lower speed on the Jetson, decoupling ... increases concurrency under limited DRAM and sustains higher steady-state throughput.` |
| §5.7 | `MaestroRAG significantly outperforms FlashRAG and PipeRAG in energy efficiency, only consuming $253.28J/query$` | `MaestroRAG consumes less energy per query than FlashRAG and PipeRAG, at $253.28J/query$` |
| §5.8 | `leverages session-level query locality, yielding significant performance gains for interactive edge deployments.` | `leverages session-level query locality.` |
| §5.9 | `This demonstrates the ability of our system to trade off between retrieval accuracy and latency via configurable indexing.` | `The choice of index therefore trades retrieval accuracy against latency.` |
| §7 | `makes RAG more viable for edge deployment and sets a new benchmark for future research.` | `makes RAG more viable for edge deployment.` |

**Grammar, four defects:**

| Where | Before | After |
|---|---|---|
| §4.1 | `The rationality of our three-stage design` | `The rationale for our three-stage design` |
| §4.2 | `Our design assigns the CPU--based stages,\emph{encoding}` | `...stages, \emph{encoding}` (missing space) |
| §5.9 | `FlashRAG and EdgeRAG re-incurs this overhead` | `FlashRAG and EdgeRAG re-incur this overhead` |
| §1 | `neither systematically optimize CPU--GPU coordination and nor perform smart orchestration` | `neither systematically optimizes CPU--GPU coordination nor performs smart orchestration` |

### E3 · abstract

> **Before** `Implemented on three edge platforms, including an NVIDIA Jetson and consumer-grade GPUs, MaestroRAG outperforms state-of-the-art RAG systems by up to \emph{$12\times$} in latency and \emph{$5.6\times$} in throughput \new{over \edgeRAG{}, the latency figure at \texttt{BS=8} and \texttt{DB=8\,M}; against \pipeRAG{}, the strongest baseline, the throughput gain is $1.35\times$}, and \emph{$3\times$} in energy \new{over \flashRAG{}}.`

> **After** `Implemented on three edge platforms, including an NVIDIA Jetson and consumer-grade GPUs, \new{MaestroRAG reduces latency by up to \emph{$12\times$} over \edgeRAG{} at \texttt{BS=8} and \texttt{DB=8\,M} and improves throughput by \emph{$5.6\times$}; against \pipeRAG{}, the strongest baseline, the throughput gain is $1.35\times$. Energy per query is \emph{$3\times$} lower than \flashRAG{}.}`

**Verified mechanically:** the numeral multiset is identical before and after
(`1.35×, 12×, 3×, 5.6×, 8, 8 M`), and `\edgeRAG`, `\pipeRAG`, `\flashRAG`,
"strongest baseline", `BS=8` and `DB=8` each occur exactly once in both. **No number changed.**

*On the second half of E3:* the introduction and conclusion do **not** repeat the
qualification. `introduction.tex:185` and `conclusion.tex:3` state the bare 12× / 5.6× / 3×
against "state-of-the-art systems" with no operating point and no baseline attribution.
Since the abstract carries the qualification on first use, no change was made there.

### E4 · §5.9 "Latency results insights" — removed, nothing folded forward

**Removed, verbatim (both lines):**

> `\noindent\textbf{Latency results insights: }\design{} yields latency reductions of $1.25\times$--$12\times$ across three hardware platforms. Avoiding naive GPU offloading is crucial: we place only the generation stage on the GPU to limit data transfers and loading overheads, while CPU-driven retrieval and encoding prevent out-of-memory failures, even at \texttt{BS=16} with large databases. Furthermore, moderate batch sizes (\texttt{BS=4}--\texttt{8}) strike the best performance balance, as oversized batches saturate I/O and small ones squander concurrency.`
>
> `Although Jetson-class hardware is relatively constrained and possesses unified memory, where both encoder and generation models are stored, applying the proposed software optimizations and distributing appropriate compute over CPU and GPU resources brings a speedup of $1.35\times$ over EdgeRAG.`

**Clause-by-clause disposition. Nothing was preserved, because nothing was unique.**

| Clause | Already carried by |
|---|---|
| latency reductions of 1.25×–12× across three platforms | §5.3 (12× at `BS=8`, `DB=8\,M`) and §5.4 (1.35× at `BS=8` falling to 1.25× at `BS=16`) |
| only generation on the GPU; naive offloading triggers transfers and reloads | §5.3: *"Pushing both encoder and LLM to the GPU triggers repeated data transfers and frequent model reloading"* |
| CPU-driven retrieval and encoding prevent OOM at `BS=16` | §5.3: *"FlashRAG often runs out of memory for `BS=16`, whereas our CPU-side retrieval and encoding remain robust"* |
| moderate batch sizes `BS=4–8` balance best | §5.3: *"moderate batch sizes (`BS=4--8`) help balance resource use"* |
| Jetson unified memory holds both models | §2.1 (Deployment Scope) |
| 1.35× over EdgeRAG on Jetson | §5.4 and §5.5 |

**Verified mechanically:** exactly six numerals left the paper — `$12\times$`, `$1.35\times$`,
`$1.25\times$`, `4`, `8`, `16` — all six from this paragraph, and **zero numerals were added
anywhere**. No other numeral moved.

### E5 · Figure 5 layout — and a pre-existing splice

**The layout fix.** `\begin{wrapfigure}{r}{0.65\linewidth}` → `\begin{figure}[t]`, with
`width=\linewidth` → `width=0.65\linewidth`. Inside a `figure`, `\linewidth` equals
`\columnwidth` (3.375 in), so `0.65\linewidth` = 2.194 in — **exactly the width the figure
already printed at**. Placement scale stays 1.0, so the 8 pt type guarantee from Task 7 is
untouched. The two-to-three-word text column beside it is gone. **No wording changed.**

**The splice.** While fixing the layout, the rendered text of that paragraph read:

> "By confining encoding and retrieval to the CPU and using memory-mapped indices, Figure 5
> contrasts our pipeline with EdgeRAG on a Jetson AGX Orin limited to 4 CPU cores. **we**
> eliminate large data copies and cut overhead relative to EdgeRAG by up to 26%."

The `\Cref{fig:JetsonThemVsUs} contrasts...` sentence had been pasted into the middle of
`By confining ... indices, we eliminate ...`, leaving a dangling modifier and a sentence
beginning with a lowercase "we". `git blame` puts this in the initial import `dea2501`; it is
not something this revision introduced, and `wrapfigure` was never what caused it.

**Repaired by reordering the three existing source lines** so the figure reference opens the
paragraph and the split sentence is rejoined. **No word was added, removed, or altered** —
the fix is a permutation of text already present. Verified in the rendered PDF:

> "Figure 5 contrasts our pipeline with EdgeRAG on a Jetson AGX Orin limited to 4 CPU cores.
> Although absolute latencies on Jetson are inevitably higher..." … "By confining encoding
> and retrieval to the CPU and using memory-mapped indices, we eliminate large data copies
> and cut overhead relative to EdgeRAG by up to 26%."

This one is called out because it exceeds a literal reading of "fix the layout". It is fully
reversible: `git revert` of the reordering hunk in `b3a3fed` restores the original order.

---

## Verification

| Check | Result |
|---|---|
| `make clean` then 3× pdflatex + bibtex | **0 errors** |
| Page count | **13** (entered Task 9 at 14) |
| Overfull hbox > 10 pt | **0** |
| Undefined references / citations | **0 / 0** |
| bibtex warnings | **0** |
| `\revmode=0, \flagmode=0` | builds, 13 pages |
| `\revmode=0, \flagmode=1` | builds, 13 pages |
| `\revmode=1, \flagmode=0` | builds, 13 pages |
| `\revmode=1, \flagmode=1` | builds, 13 pages — **switches restored to 1/1** |
| Blue **glyphs** at `\revmode=0` | **0** (text-only raster, `gs -dFILTERIMAGE -dFILTERVECTOR`) |
| Blue glyphs at `\revmode=1` | 148 501 px — every `\new{}` span renders |
| Near-white glyphs, all four modes | **0** — no white text survives in the text layer |
| Red glyphs at `\flagmode=0` | 170 px, all inside Figure 6: the author's own `N/A` / `N/C` bar labels from `plots/MaestroRAG/Plots/mainLatencyResult2.py`. Not a flag leak. |
| `verify_numbers` **before** Part E (`e1358f6`) | 100 PASS / 0 FAIL / 1 UNVERIFIABLE, no drift |
| `verify_numbers` **after** Part E | 100 PASS / 0 FAIL / 1 UNVERIFIABLE, **no drift** |
| Literals extracted | 329 → 323 (the six numerals E4 removed; none added) |
| Citations | 44 cited = 44 in bibliography; 0 unresolved, 0 orphaned |
| Surviving `\flag{}` | 4, exactly the four untraceable numerals above |
| Em-dash / spaced-`--` parentheticals in compiled sources | **0** (see note below) |
| `main.pdf` committed | **no** — `.gitignore:4` |

**The one dash hit** is `main.tex:274`,
`\textbf{\#\iiswcsubmissionnumber} -- Confidential Draft -- Do NOT Distribute!!`. That is the
IISWC class's own draft banner inside `\fancypagestyle{firstpage}`, not paper prose, and it
comes out for camera-ready along with the two `\vspace` calls beside it. Left as-is
deliberately, consistent with the earlier `\vspace` sweep.

`ASPLOSbackground&motivation.tex`, `ASPLOScharacterization.tex`, `iiswc26example.tex` and
`rebuttal_text.tex` do contain em-dashes but **none is compiled** — the first three are not
`\input` anywhere and `rebuttal_text` is commented out at `main.tex:541` and `:553`.

---

## What the author must decide

1. **Four untraceable numerals** (table in Part C). Each needs either a source or a deletion.
   The tail-latency sentence in §5.5 is the most exposed: six figures, none recorded.
2. **The E5 sentence reordering.** No wording changed, but the paragraph's sentence order
   did. Revert the hunk if you disagree.
3. **Conflict C1 from Task 8 is still open** — the master plan asked that no `§` survive in
   cross-references, while you had asked one turn earlier for `§2.1`. `§2.1` is what ships
   today. Unchanged in Task 9; still needs your ruling.
4. **`\revmode` and `\flagmode` are both 1.** Set both to 0 for the camera-ready submission.
   At `0/0` the paper renders in pure black with zero near-white glyphs, verified above.
