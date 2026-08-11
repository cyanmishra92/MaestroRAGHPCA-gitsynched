# Task 7.5 — Rebase Resolution and Integrity Verification

**Rebase completed.** Three Task 8 commits replayed onto the Overleaf commit `9e8a465`
("Small changes with Deeksha"). `git rebase --skip` was never used. Nothing pushed.

```
c08e49c  Task 8 (Parts D-E): rebuttal coherence and paper-wide consistency flags
99a642a  Task 8 (Part C): section symbols, em-dashes, headings, captions, superseded paragraphs, title
af9aea9  Task 8 (Part A-B): flag mechanism; numeric corrections B1-B11 and headline operating points
9e8a465  Small changes with Deeksha          <- upstream, now the base
```

Working tree clean. **3 commits ahead of `origin/main`, 0 behind.**

**The single most important finding is in §5: corrections B1 and B2 are not in the paper,
and were never committed. That is a Task 8 defect, not a rebase loss.**

---

## 1. State on entry

| | |
|---|---|
| Rebase type | interactive, `main` onto `9e8a465` |
| Step reached | **2 of 3** |
| Applied cleanly | `f104a44` Part A-B |
| Stopped on | `00954e8` Part C, conflict in `implementation&eval.tex` |
| Remaining | `c5cf71c` Parts D-E |
| Conflicted files | `implementation&eval.tex` only |

The upstream commit touched **only** `implementation&eval.tex` (10 insertions, 6 deletions)
and made four changes: it commented out the `Results on an RTX 4080 Desktop:` run-in
heading in favour of `RTX 4080 Desktop:`, renamed `Main Latency Results` to
`Latency Analysis`, emptied the three Figure 7 subcaptions to `[~]`, and rewrote the
Figure 7 caption to drop "Key findings:".

---

## 2. Conflicted hunks, both sides, and the choice

Labels are inverted during a rebase: `HEAD` is the **upstream Overleaf** side already on
the branch, and the block after `=======` is the **commit being replayed**.

### Step 2 of 3 — `00954e8` Task 8 Part C, two hunks

**Hunk 1** — `implementation&eval.tex:146-150`, the §5.5 heading.

| Side | Content |
|---|---|
| HEAD (upstream Overleaf) | `\subsection{Latency Analysis}` |
| Incoming (Task 8 Part C) | `\subsection{\new{End-to-End Latency}}` |

**Took upstream.** The brief directs that headings go to the author's wording, which was
written and reviewed in context.

**Hunk 2** — `implementation&eval.tex:228-235`, the Figure 7 caption.

| Side | Content |
|---|---|
| HEAD (upstream Overleaf) | `\caption{\new {(a) Adaptive Worker (\#Cores) Allocation using \design{} allocator against an empirical one (b) End-to-end latency comparison … (c) Throughput comparison …}}` plus a commented-out line |
| Incoming (Task 8 Part C) | the descriptive caption written in Part C C4, which also explained the stacked segment in panel (b) and the N/A bars |

**Took upstream**, per the brief. See §5 for what this costs.

### Step 3 of 3 — `c5cf71c` Task 8 Parts D-E, one hunk

The Parts D-E commit appended the E-1 flag to the Part C caption, which no longer exists.

| Side | Content |
|---|---|
| HEAD (state after Part C replayed) | the author's caption, four lines |
| Incoming (Parts D-E) | the Part C caption **plus** `\flag{This caption does not state the operating point for panels (b) and (c) …}` |

**Combined**, and this is the one place I did not simply take a side. The caption text and
the flag are genuinely complementary: the caption is the author's, and the flag is a
separate annotation whose point still holds, because the author's caption also omits the
operating point. The result keeps the author's wording verbatim and places the flag inside
`\caption{}` after the `\new{}` group closes:

```latex
    \caption{\new {(a) Adaptive Worker (\#Cores) Allocation using \design{} allocator against an empirical one (b) End-to-end latency comparison for configurations selected by the adaptive worker allocator (c) Throughput comparison for configurations selected by the adaptive worker allocator.
    %The adaptive worker allocation technique often results in better resource partitioning combinations to achieve the same if not better latency/throughput.
    }
    \flag{This caption does not state the operating point for panels (b) and (c). \Cref{sec:main-latency-results} gives \texttt{BS=8} with 4\,M, 4\,M and 1\,M databases, and \Cref{sec:throughput} gives \texttt{DB=4\,M}, \texttt{BS=8}. Add them here if the caption should stand alone.}
    }
```

### Conflict markers

Repository-wide scan over `*.tex`, `*.md`, `*.py`, `*.yaml`, `*.bib` for `<<<<<<<`,
`=======` and `>>>>>>>`: **none remain.**

---

## 3. Step 4 — did the replayed commit's other changes survive?

Reported as found. **Nothing was re-applied.**

| # | Item | Status |
|---|---|---|
| 1 | `\creflabelformat` for `section`/`subsection` deleted from `main.tex` | **Absent ✅** (0 live occurrences) — see the note below |
| 2 | Zero section symbols before a reference; `\xref` resolved | **✅** 0 live `\S\ref`; `\xref` is `\newcommand{\xref}[1]{\Cref{#1}}` at `main.tex:237`, with 0 live uses |
| 3 | Zero em-dashes in live text | **✅ in prose** — see the note below |
| 4a | "Two major lessons emerge from Figure 4" removed | **✅** 0 live (only the pre-existing commented copy at line 56) |
| 4b | "Execution Breakdown Across Stages" removed | **✅** 0 live |
| 5 | `Regular-` gone from `\title` | **✅** `\title{MaestroRAG: Orchestrated Pipeline Architecture for Efficient RAG on Edge Devices}` |

**Note on item 1.** The `\creflabelformat` lines are absent, but they were not removed by
Part C. Commit `e099211` replaced them with six `\crefformat`/`\Crefformat` lines, at your
instruction that references read `§2.1` rather than `Section §2.1`. So references still
render with a section sign, by design. This is the open question already recorded in
`reports/task08_summary.md` §3, and it is unchanged by the rebase.

**Note on item 3.** One `---` survives in live text, at `implementation&eval.tex:18`. It is
inside the Part E flag that *describes* the pattern: *"the C2 sweep listed only the `---`
and U+2014 forms"*. It is annotation, not prose, and it disappears entirely at
`\flagmode=0`. **Zero em-dashes in actual paper prose.**

---

## 4. Step 5 — build and integrity

| Check | Result |
|---|---|
| `make` / `pdflatex` | **0 errors** |
| Undefined references | **0** |
| Undefined citations | **0** |
| Page count | **14**, unchanged from the pre-rebase Task 8 tip |
| `\includegraphics` targets | **20 live, 0 missing** |
| `refs.bib` / `reference.bib` | **byte-identical** to their pre-Task-2 state |
| `tools/verify_numbers.py` | **100 PASS / 0 FAIL / 1 UNVERIFIABLE**, no drift |
| All 41 references render | ✅ |
| `Section §N` duplications | **0** |
| Cross-references | TABLE 1–4 and Figure 6 all resolve |
| Upstream wording in the PDF | "Latency Analysis" present, "Key findings" gone ✅ |
| Flags visible | 7 `[FLAG:` markers at `\flagmode=1` |

`main.pdf` not committed. Timestamped copy: **`reports/task075_main_20260810-1707.pdf`**.

---

## 5. Two losses, neither to be re-applied here

### 5.1 B1 and B2 were never applied. This is a Task 8 defect, not a rebase loss.

`implementation&eval.tex:153` still reads:

> On the RTX 4090, our method completes inference in 6.50 s, which is **3--4×** faster than
> FlashRAG (16.39 s) or PipeRAG (19.80 s), and **≥4×** faster than EdgeRAG…

It should read 2.5× and 3.0×, and 4.4×.

**Traced to the source.** The pre-rebase tip `c5cf71c` contains the same uncorrected text,
and `git show f104a44 -- implementation&eval.tex` contains no hunk for that line. The
corrections were therefore never committed. The cause is a scripting error in Task 8: the
first correction script applied B1 and B2 in memory, then aborted on a later assertion
**before writing the file**, so the edit was discarded. The follow-up script re-applied
every other correction but omitted B1 and B2, because I had seen them report success. I
caught the identical failure mode on the C3 heading later in that task and did not go back
to re-check the earlier ones.

**Not re-applied here**, per the brief. It belongs in the next task. The replacement values
and their basis are unchanged: 16.39/6.497 = 2.523, 19.80/6.497 = 3.048, 28.40/6.497 =
4.371.

### 5.2 Figure 7b's stacked-segment explanation is gone

Taking the author's caption, as directed, discarded the sentence that explained panel (b)'s
stacked bar: *"the lower segment of the MaestroRAG bar on the RTX 4090 is the cached latency
and the upper segment is the remainder of the uncached total."* The author's caption does
not explain it, and `grep` confirms no other live text does.

That explanation was a Task 7 Part-E requirement ("explain Figure 7b's stacked segment"),
so it is now **unmet**. The E-1 flag preserved on that caption is adjacent but not the same
point. Reporting rather than restoring, since the caption is the author's.

---

## 6. Task 8 status on the branch

For scoping the revised Task 8.

| Item | Status | Where |
|---|---|---|
| **`\flagmode` mechanism** | **DONE** | `main.tex:220-226`; verified to vanish completely at `\flagmode=0` |
| **B1** 3--4× → 2.5× and 3.0× | **NOT DONE** | §5.5, `implementation&eval.tex:153`. Never committed, see §5.1 |
| **B2** ≥4× → 4.4× | **NOT DONE** | same line, same cause |
| **B3** 6--12× → up to 12× / 2--3× | **DONE** | `implementation&eval.tex` |
| **B4** 25--35% → up to 26% | **DONE** | `implementation&eval.tex` |
| **B6** cold-start 0.24 s residual | **DONE** | `implementation&eval.tex` |
| **B7** 22% → 1.23× | **DONE** | `design.tex` |
| **B8** 80% hit-rate qualifier | **DONE** | `implementation&eval.tex` |
| **B9** three-significant-figure throughput | **DONE** | `implementation&eval.tex`, and the Figure 6c bar labels were regenerated to `.3g` to match |
| **B11** 1.9× → 2.0× | **DONE** | `implementation&eval.tex:154` |
| **B10** headline operating points on 12×, 5.6×, 3× | **DONE** | `abstract.tex`, first use only |
| **Section symbols** | **DONE, with a caveat** | 0 live `\S\ref`, `\xref` routed through `\Cref`, 0 `Section §N` duplications. References still render as `§N` by your earlier instruction; whether to drop the symbol entirely is still open |
| **Em-dashes** | **DONE** | 0 in prose; 1 inside a flag that names the pattern |
| **Headings** | **DONE, upstream wins on one** | 5.3, 5.4, 5.6, 5.7 are the Task 8 wording; **5.5 is the author's "Latency Analysis"** |
| **Captions** | **PARTIAL** | Figures 1 and 4 are the Task 8 descriptive rewrites. **Figure 7 is the author's**, and its stacked-segment explanation is lost, see §5.2 |
| **Superseded paragraphs** | **DONE** | both removed |
| **Title** | **DONE** | `Regular-` gone |
| **Rebuttal coherence flags** | **DONE** | 7 flags: `design.tex:48`, `implementation&eval.tex:18, 73, 174, 229, 281, 284` |
| **`docs/changelog.md`** | **NOT DONE** | file does not exist; never created by any task so far |

### What the revised Task 8 still needs to cover

1. **B1 and B2**, the only numeric corrections outstanding.
2. **`docs/changelog.md`**, which has never been written.
3. **Figure 7b's stacked segment**, if the explanation is still wanted, now as a sentence in
   the body rather than the caption, since the caption is the author's.
4. **The section-symbol question**, if you want `Section 2.1` rather than `§2.1`.

Everything else on the list is already applied.

---

## 7. Anything contradicting the instructions

**No new commit was needed for the resolution.** The rebase produced its own commits and
both resolutions are baked into `99a642a` and `c08e49c`. The one place resolution required a
genuine change, combining the author's caption with the E-1 flag, is inside `c08e49c`. The
commit accompanying this report carries only the report and the timestamped PDF.

**The brief's expectation that only headings and the Figure 7 caption would conflict was
correct**, and the third commit's conflict was a downstream consequence of resolving the
second, not a separate disagreement.

**One item in the step 4 list needs restating rather than a simple pass.** Item 1 asks
whether Part C deleted the `\creflabelformat` lines. It did not, and could not: they were
already gone before Task 8 began. The lines are absent, but for a different reason than the
brief assumes, and the section sign still renders by your own earlier instruction.
