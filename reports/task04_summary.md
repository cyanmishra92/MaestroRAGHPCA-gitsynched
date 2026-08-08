# Task 4 — Summary

Shepherd Item 4: elaborate the similarity-match analysis for Table 1. Three `.tex` files
touched, plus two harness files. **The paper is now 13 pages, up from 12** — see §7.1,
which is the item needing your decision.

---

## 1. Full text of every added or changed passage

### 1.1 The rewritten analysis, `implementation&eval.tex` §5.7

The three configuration sentences that open the paragraph are **unchanged**:

> `\Cref{tab:cache_results}` reports the results of our caching mechanisms under exact- and
> similarity-match scenarios. All experiments use TTL of 300 s and cache capacity of 32
> entries, each storing 5 retrieved documents per prompt. For a fair comparison with
> EdgeRAG, we adopt a batch size of 1.

The explanatory sentence that followed them was replaced by:

```latex
\new{Exact matching returns the cached final answer and skips both retrieval and
generation, placing \design{} between 0.87\,s and 0.92\,s. Similarity matching reuses only
the \topk{} retrieved documents and generates afresh for the new query, placing it between
3.06\,s and 3.12\,s. The difference between the two is therefore the cost of generation,
which similarity matching still incurs; it is not a RAM-capacity effect. Against
\edgeRAG{}, the residual gap in the similarity-match case is our process and thread handoff
across workers, which adds approximately 1.1\,s. \edgeRAG{} does not incur this cost, since
its execution is largely sequential and involves no process orchestration or thread
synchronization. Because the measurement uses a batch size of 1, it compares our worst case
against \edgeRAG{}'s nominal case; the handoff is a fixed per-batch cost, so we expect it
to amortize at larger batch sizes.}
```

Six sentences carrying the seven rebuttal claims. Removed: *"For dissimilar queries falling
below the threshold, the system gracefully reverts to full flat-index lookup, slightly
increasing average latency relative to exact-match cases."* (see §4).

Left untouched in the same paragraph: the 80 percent hit-rate sentence, the Jetson caching
sentence (§5), *"Our cache management exploits temporal and semantic locality"*, the
closing *"Overall, the cache policy…"* sentence, and the Fig. 7b purple-bar reference.

### 1.2 Table 1 caption, `TablesAlgos/CachingTable.tex`

```latex
\caption{Latency with caching \new{at \texttt{BS=1}, with a TTL of 300\,s, a cache capacity
of 32 entries, and 5 retrieved documents per prompt}. \design{}: MR; EdgeRAG: ER}
```

The dead commented duplicate below the `\resizebox` was deleted:

```latex
%\caption{Latency with caching. \design{}: MR; EdgeRAG: ER}   <- removed
```

### 1.3 Spelling, `design.tex`

`amortisation` → `amortization` (introduced by Task 3). **Zero occurrences of `amortis`
remain** in any active `.tex`.

---

## 2. Sentence-by-sentence provenance

**R** = rebuttal (Reviewer-C answer, `docs/Untitled document.md`) · **P** = paper ·
**T** = Table 1 (`TablesAlgos/CachingTable.tex`).

| # | Sentence | Derives from |
|---|---|---|
| 1 | "Exact matching returns the cached final answer and skips both retrieval and generation, placing MaestroRAG between 0.87 s and 0.92 s." | **R claim 1:** *"Exact-match returns the cached final answer, skipping retrieval+generation (0.87-0.92s)."* · **T** Exact row, MR cells: 0.87, 0.92, 0.887. |
| 2 | "Similarity matching reuses only the top-k retrieved documents and generates afresh for the new query, placing it between 3.06 s and 3.12 s." | **R claim 2:** *"Similarity-match reuses only top-k documents and freshly generates for the new query (3.06-3.12s)."* · **T** Sim row, MR cells: 3.116, 3.061, 3.089. |
| 3 | "The difference between the two is therefore the cost of generation, which similarity matching still incurs; it is not a RAM-capacity effect." | First clause connects **R claims 1 and 2**: exact skips generation, similarity performs it. Second clause is **R claim 3** verbatim: *"this is not a RAM-capacity effect."* |
| 4 | "Against EdgeRAG, the residual gap in the similarity-match case is our process and thread handoff across workers, which adds approximately 1.1 s." | **R claim 4:** *"Our current process/thread handoff across workers adds ~1.1s, explaining the gap versus EdgeRAG."* |
| 5 | "EdgeRAG does not incur this cost, since its execution is largely sequential and involves no process orchestration or thread synchronization." | **R claim 5:** *"EdgeRAG does not incur these overheads from process orchestration, thread synchronization, or similar coordination mechanisms; its execution is largely sequential and hence has lesser overhead."* |
| 6 | "Because the measurement uses a batch size of 1, it compares our worst case against EdgeRAG's nominal case; the handoff is a fixed per-batch cost, so we expect it to amortize at larger batch sizes." | **R claim 6:** *"Our experiment is for batch size of 1 which compares our worst case against EdgeRAG's nominal."* · **R claim 7:** *"However, at larger batch sizes this orchestration cost gets amortized."* The "fixed per-batch cost" framing is **P** `design.tex:259` (*Start-up costs*): *"Launching workers per arrived batch leads to multiple start-up costs compared to the actual processing time."* |
| — | Caption: "at BS=1, with a TTL of 300 s, a cache capacity of 32 entries, and 5 retrieved documents per prompt" | **P** `implementation&eval.tex:263–264`, the two configuration sentences already in §5.7. Relocated into the caption, not newly asserted. |

**Every sentence maps. All seven claims present; nothing beyond them.**

Claim 7 is worded as an expectation (*"we expect it to amortize"*) grounded in the
fixed-cost structure, with **no number attached** and no implication of measurement, as
required.

---

## 3. Provenance of every numeral

| Numeral | Where | Source |
|---|---|---|
| `0.87` | sentence 1 | **R claim 1** *"(0.87-0.92s)"* · **T** Exact/MR/2 mil |
| `0.92` | sentence 1 | **R claim 1** · **T** Exact/MR/4 mil |
| `3.06` | sentence 2 | **R claim 2** *"(3.06-3.12s)"* · **T** Sim/MR/4 mil = 3.061, rounded to 2 dp |
| `3.12` | sentence 2 | **R claim 2** · **T** Sim/MR/2 mil = 3.116, rounded to 2 dp |
| **`1.1`** | sentence 4 | **R claim 4** verbatim: *"adds ~1.1s"*. **Stated by the rebuttal, not derived by me.** For information only, the table's own differences are 1.069, 1.058 and 0.951 s across the three database sizes; the paper does not compute these and neither did I. |
| `1` (batch size) | sentence 6 | **R claim 6** · **P** `implementation&eval.tex:264` |
| `300`, `32`, `5` | caption | **P** `implementation&eval.tex:263`, verbatim relocation |

No new numbers. `refs.bib` and `reference.bib` untouched; no citation was needed that does
not already exist.

---

## 4. Disposition of the "gracefully reverts to full flat-index lookup" sentence

**Removed**, not reworded.

The brief allowed either. I removed it for three reasons:

1. **Its content is already covered.** The preceding sentence in the same paragraph
   ("When 80 percent of queries exhibit strong similarity, average latency improves
   substantially despite occasional cache misses") already establishes that sub-threshold
   queries miss the cache and cost more. The removed sentence restated that with a
   mechanism.
2. **Rewording would not have removed the hazard.** Its final clause,
   *"slightly increasing average latency relative to exact-match cases"*, is precisely the
   exact-versus-similarity comparison the rebuttal explains differently. Any qualifier
   would have left two answers to the same question three lines apart, which the brief
   correctly identifies as worse than the original.
3. **It is quantitatively wrong as an account of the gap.** It calls the increase
   "slight"; the table shows similarity match at roughly 3.5 times exact match. It cannot
   be the explanation for a gap of that size.

**One thing to be aware of:** a deletion is invisible in the revision-mode diff. `\new{}`
marks additions in blue, but there is no corresponding marker for removed text, so a
shepherd comparing `\revmode=1` against the submitted PDF will not see that this sentence
went. The full text is quoted above, and in the commit message, so the record exists
outside the PDF.

---

## 5. Step 3 report: the Jetson caching claim (unchanged, as instructed)

`implementation&eval.tex` §5.7 states:

> "On the Jetson AGX Orin (15 W power cap), caching provides consistent speedups by
> avoiding redundant encoder invocations and memory transfers."

**Left exactly as written.** What I can establish about it:

| Question | Finding |
|---|---|
| Does Table 1 have a Jetson column? | **No.** Its three column groups are 2 mil, 4 mil and 8 mil database sizes, each with ER and MR. Every number in it is from the RTX 4090 configuration. |
| Does the workbook hold Jetson caching data? | **No.** `CachingResults4090` is the only caching tab, it is **empty**, and it is outside the authorised set in any case. The three Jetson tabs (`LatencyResults-NoCacheJetson` and the two other no-cache tabs) are, as named, no-cache measurements. |
| Does any other section report Jetson caching? | **No.** The only other caching numbers in the paper are the ablation's 2.003 s and the Fig. 7b purple bar, both RTX 4090. |
| Is the claim contradicted anywhere? | **No.** It is simply unsupported. |

**The options, as I see them:**

1. **Delete the sentence.** Cleanest. Costs one line and no argument; nothing else in §5.7
   depends on it.
2. **Requalify it as an expectation**, in the manner claim 7 now uses for amortization: the
   caching mechanism removes encoder invocations and memory transfers, which are costs the
   Jetson also pays, so the same benefit is expected there. This keeps the point while
   being honest that it was not measured. It is, however, **a new argument the rebuttal does
   not make**, so under the protocol it needs your explicit assent.
3. **Measure it.** A Jetson caching run at the Table 1 configuration would let the claim
   stand as written and would add a fourth column to the table. This is the only option
   that makes it a result rather than an expectation.
4. **Leave it.** Defensible only if you judge that a shepherd checking Item 4 will not
   follow the Jetson sentence back to a table that has no Jetson column. Reviewer C read
   Table 1 closely enough to ask why similarity match was slower than EdgeRAG's, so I would
   not rely on that.

I recommend 1 or 2. **This is your call, not mine, and nothing was changed.**

---

## 6. Verification

### Table 1 caption position — confirmed from the rendered PDF

**It renders above the tabular.** Extracted from the built page:

```
TABLE 2: Latency with caching at BS=1, with a TTL of 300s,
a cache capacity of 32 entries, and 5 retrieved documents
per prompt. MaestroRAG: MR; EdgeRAG: ER
                2 mil            4 mil            8 mil
  Method     ER      MR      ER       MR      ER       MR
  Exact     2.033s  0.87s   2.0326s  0.92s   2.0335s  0.887s
  Sim       2.047s  3.116s  2.003s   3.061s  2.138s   3.089s
```

The `\caption` was already before the `\resizebox` in the source and the source is what
builds, so the submitted version's caption-below must have come from a different source
state. **No fix was needed; the requirement is satisfied.** (The table is numbered Table 2
because Task 2 introduced the hardware table as Table 1.)

### A real bug caught by rendering, not by the source

The first attempt wrote `caching\new{ at \texttt{BS=1}…}`, which rendered as
**"Latency with cachingat BS=1"**. TeX strips leading spaces in a macro argument, so the
space inside `\new{ …}` vanished. Fixed by moving the space outside the braces:
`caching \new{at …}`.

I then wrote an audit over **every** `\new{}` span in the paper for the same class of
defect (leading space inside the argument, or a missing space on either side of the span).
**No other instance exists.** Worth keeping in mind for later tasks: `\new{}` swallows a
leading space silently, and the source looks correct.

*(Not a defect: Ghostscript's text extractor also drops spaces at some kerning boundaries.
"matchingstill" in the extracted §5.7 text is an artifact of the same kind as "RAMType" and
"Thefinal", both of which have real spaces in the source. Only the caption case was real,
and it was confirmed by the fix changing the output.)*

### Build

| | |
|---|---|
| `make` | **exit 0**, **13 pages** |
| LaTeX errors | **0** |
| Undefined references | **0** |
| Undefined citations | **0** |
| All 41 references render | ✅ |

### Revision modes — pixel-verified

| Page | Content | Differing px | mode 1 | mode 0 |
|---|---|---:|---|---|
| 1 | intro clause | 1,981 | 100% blue | RGB(0,0,0), 0 near-white |
| 2 | §2.1, Table 1, §2.3 | 41,868 | 100% blue | RGB(0,0,0), 0 near-white |
| 4 | §3.3 portability | 14,283 | 100% blue | RGB(0,0,0), 0 near-white |
| 5 | §4.1 adaptive batching | 10,314 | 100% blue | RGB(0,0,0), 0 near-white |
| 7 | §5.1 | 12,309 | 100% blue | RGB(0,0,0), 0 near-white |
| 8 | §5.3 back-reference | 1,969 | 100% blue | RGB(0,0,0), 0 near-white |
| 9 | **Table 2 caption** | 3,777 | 87.5% blue | RGB(0,0,0), 0 near-white |
| 10 | **§5.7 analysis** | 25,105 | 100% blue | RGB(0,0,0), 0 near-white |
| 3, 6, 11–13 | — | 0, identical | | |

Page 9's 87.5 percent is **caption reflow, not a colour failure**, and I checked it
directly: of the 3,066 ink pixels that differ, 2,682 are pure RGB(0,0,255) (the new span)
and 384 are pure RGB(0,0,0) with zero channel spread — the existing caption words
*"Latency with caching"* and *"MaestroRAG: MR; EdgeRAG: ER"*, which shift position when the
new clause is inserted between them. Zero near-white pixels in either mode.

`\revmode` restored to `1`.

### `verify_numbers.py`

```
checks : 45 PASS / 5 FAIL / 1 UNVERIFIABLE
drift  : none
```

The 41 pre-existing checks hold their statuses exactly; the four new Table 1 anchors all
pass:

| Check | Prose | Table | Tol |
|---|---:|---:|---:|
| `table1_exact_maestro_2m` | 0.87 | 0.87 | 0 |
| `table1_exact_maestro_4m` | 0.92 | 0.92 | 0 |
| `table1_sim_maestro_2m` | 3.12 | 3.116 | 0.005 |
| `table1_sim_maestro_4m` | 3.06 | 3.061 | 0.005 |

**Harness change.** These are the first *paper-internal* checks: no workbook tab holds
caching data at all, so the table itself is the only source. I added a `source: {file,
regex}` kind to `verify_numbers.py` that pulls a value out of a `.tex` file with a regex
anchored on row content rather than a line number, and requires the regex to match exactly
once. The stale-tab guard is unaffected: file sources carry no `sheet`, and a check naming
a stale sheet still aborts the run.

### Style

| | Before Task 4 | After |
|---|---:|---:|
| Text added by Tasks 2, 2a, 3, 4 — `---` | 0 | **0** ✅ |
| Text added by Tasks 2, 2a, 3, 4 — `—` | 0 | **0** ✅ |
| Text added by Tasks 2, 2a, 3, 4 — non-range `--` | 0 | **0** ✅ |
| Pre-existing prose — `---` | 4 | 4 |
| Pre-existing prose — `—` | 6 | 6 |
| **Pre-existing total** | **10** | **10** |

Still Item 7's job. `amortisation` → `amortization`; **zero occurrences of `amortis`
remain**.

### Bibliography

Byte-identical to the pre-Task-2 state:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

### Diff against Task 3 (`48941a1`)

```
 TablesAlgos/CachingTable.tex |   3 +-
 design.tex                   |   2 +-
 implementation&eval.tex      |   3 +-
 tools/checks.yaml            |  64 +++++
 tools/verify_numbers.py      |  38 +++
 reports/verify_numbers.md    | 103 +++---
```

### PDF

Not committed (gitignored). Timestamped copy: **`reports/task04_main_20260808-1411.pdf`**.

---

## 7. Things that contradict the instructions, or that you should decide

### 7.1 The paper is now 13 pages. The overflow is one reference entry.

I flagged after Task 3 that the slack was gone. It went this task.

**The body is unaffected.** Every section landmark sits on exactly the same page as in the
Task 3 build:

| Landmark | Task 3 (12 pp) | Task 4 (13 pp) |
|---|---:|---:|
| §5 Implementation | 7 | 7 |
| §5.7 Software Caching | 9 | 9 |
| §5.8 Additional Insights | 10 | 10 |
| §6 Related Work | 11 | 11 |
| §7 Conclusions | 11 | 11 |
| References begin | 11 | 11 |

**Page 13 contains one thing: reference [41]**, six lines, the OPT citation. Nothing else.
All 41 references render.

So the question is narrow: does one reference spilling to a thirteenth page matter for
IISWC's camera-ready limit? I do not know the venue's rule on whether references count
toward the limit, and I did not guess. Three ways to reclaim the six lines if it does
matter:

1. **The master plan already lists three cuts** — the duplicate-summary paragraphs at
   §5.3 ("Two major lessons emerge…"), §3.2 ("Execution Breakdown Across Stages") and §5.9
   ("Latency results insights"). Any one of them likely recovers more than six lines, and
   they are already scheduled work rather than new concessions.
2. **The Jetson caching sentence in §5 above**, if you delete it.
3. `flushend` is already loaded, so last-page column balancing is in play; a `\vspace`
   adjustment near the end of the bibliography would also do it, though that is a
   presentation hack rather than a fix.

**I did not act on any of these.** Reclaiming space by cutting content is an author's
decision, and every candidate is outside this task.

### 7.2 A third stale-tab warning appeared, and it is a false positive

The `5` I moved into the Table 1 caption ("5 retrieved documents per prompt") matches
values in `Retrieval!A17`, `!L18`, `!Q19` and `!Q31`, and appears in no authorised tab, so
the scanner flags it. It is the same coincidence already flagged for the `5` in the Fig. 6
caption. The number is the paper's own top-k configuration constant, copied verbatim from
`implementation&eval.tex:263`; it was not read off a stale tab. **No action needed**, but
the count going 2 → 3 is expected rather than a regression.

### 7.3 Deletions are invisible in the revision diff

Covered in §4. Worth deciding as policy before more removals accumulate: if the shepherd
should see what was cut, the preamble already has `\st{}` with red strike colour, and a
`\removed{}` macro alongside `\new{}` would take four lines. I did not add one, because
that changes the revision-mode contract Task 1 established and it is your call.

### 7.4 The 1.1 s figure is the rebuttal's, and the table's own numbers differ slightly

The rebuttal states *"~1.1s"*. The three per-database differences implied by Table 1 are
1.069, 1.058 and 0.951 s, averaging about 1.03 s. The rebuttal's approximation is
defensible and I used it verbatim, as the protocol requires. Recording the arithmetic here
only so that you know the number a careful reader could compute is slightly below the one
stated. Per protocol §2, I have not resolved this in the text.

### 7.5 Section 5.7 still contains one sentence I would question, outside this task's scope

*"When 80 percent of queries exhibit strong similarity, average latency improves
substantially despite occasional cache misses."* The master plan (B8) notes that the
ablation's 2.003 s is consistent with an 80 percent exact-match hit rate, and flags that
the ablation reads as unconditional. This sentence is the §5.7 counterpart. Left untouched;
noting it because it sits three lines from text I did edit.

---

## 8. Acceptance criteria

| | Criterion | Status |
|---|---|---|
| ☑ | All seven rebuttal claims present, nothing beyond them | 6 sentences, mapped in §2 |
| ☑ | Claim 3 explicit: not a RAM-capacity effect | sentence 3, verbatim from the rebuttal |
| ☑ | Claim 7 an expectation, no number, not presented as measured | "we expect it to amortize at larger batch sizes" |
| ☑ | Only one explanation stands for the gap | competing sentence removed, §4 |
| ☑ | Configuration statements retained | TTL 300 s, 32 entries, 5 documents, BS=1 all unchanged |
| ☑ | Caption verified above the tabular in the rendered PDF, and states the configuration | §6, extracted from the built page |
| ☑ | Dead commented `%\caption` removed | ✅ |
| ☑ | Jetson caching claim reported and left unchanged | §5, four options given |
| ☑ | "amortisation" → "amortization" | zero `amortis` remain |
| ☑ | Zero em-dashes of any form in Tasks 2–4 text | `---`=0, `—`=0, non-range `--`=0 |
| ☑ | Every sentence mapped | §2 |
| ☑ | Blue at `\revmode=1`, black at `=0` | 8 pages; page 9's non-blue verified as reflow |
| ☑ | `make` clean: 0 undefined refs, 0 undefined citations | exit 0 |
| ☑ | `refs.bib`, `reference.bib` byte-identical to pre-Task-2 | SHA-256 verified |
| ☑ | No drift; Table 1 checks added | 45 / 5 / 1; four new anchors PASS |
| ☑ | `main.pdf` not committed; timestamped copy in `reports/` | `task04_main_20260808-1411.pdf` |
| ☑ | Committed, not pushed | see `git log` |
