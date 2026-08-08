# Task 3 — Summary

Shepherd Items 5 and 6, plus the two riders. Six `.tex` files touched. All new prose written
without em-dashes, in the paper's declarative register.

---

## 1. Full text of every added or changed passage

### 1.1 Part A — Item 5, `design.tex` §4.1 (end of the *Adaptive batching* paragraph)

```latex
\new{Generation latency depends on the intended prompt length. The mapper profiles $T_{G}$
across those lengths (\Cref{subsec:resource-mapping}), and adaptive batching creates
memory-safe GPU quanta. Worker allocation is nonetheless static within a session,
following the start-up amortisation rationale of \Cref{sec:Design:Software}. Remapping
cores at run time under context drift is a future extension.}
```

Four sentences carrying the rebuttal's four claims and nothing else. Claim 1 references
§4.2's existing profiling statement rather than restating it; claim 2 references §4.3's
start-up rationale.

### 1.2 Part B — Item 6, `characterization.tex` §3.3 (new final paragraph)

```latex
\begin{newtext}
\noindent\textbf{Portability of these trends to embedded platforms:}
The characterization above was performed on the local/personal-computing platform of
\Cref{sec:BG:Scope}. Because the optimizations we derive from it target CPU-side encoding
and retrieval, the same trends hold on embedded platforms such as the Jetson AGX Orin. The
primary difference there is the elimination of PCIe transfer overhead in unified memory
systems. A similar trend is observed across SKUs and vendors.
\end{newtext}
```

Run-in heading matches the style §3.2 already uses. A `\label{sec:char:keyobs}` was added
immediately after the `\subsection{Key Observations and Motivation for Design}` line, since
that subsection carried no label and the back-reference needs a target. It resolves to
**§3.3**. That one line is the only change to existing text in this file.

### 1.3 Part B — back-reference, `implementation&eval.tex` §5.3 (Results on Jetson AGX Orin)

One clause appended to the subsection's existing second sentence:

```latex
These results confirm that minimizing CPU--GPU data transfers remains advantageous in
low-power SoCs and that judicious model and index selections are crucial in
memory-constrained scenarios\new{, consistent with the trend portability established in
\Cref{sec:char:keyobs}}.
```

The subsection is otherwise untouched; its heading is left for Item 7.

### 1.4 Part C.1 — `background&motivation.tex` §2.3

```latex
The fundamental RAG stages—encoding, retrieval, augmentation, and generation—are
consistent across datacenter servers, \new{local/personal-computing platforms, and
embedded devices}, but their execution varies widely with hardware constraints.
```

*(was: "datacenter servers, desktops, and edge devices")* — only the two-item span changed;
sentence meaning and length preserved. The list now runs along the same spectrum §2.1
defines instead of opposing desktops to edge.

### 1.5 Part C.2 — `implementation&eval.tex` §5.1 (Metrics)

```latex
To ensure that the proposed orchestration fits in the tight power and energy constraints of
\new{the personal-computing edge platforms}, we report the peak and average power (in W)
and the total energy (in J) consumed per inference query.
```

*(was: "of the edge devices")*.

### 1.6 Part D — the five em-dashes

| # | File | Before | After |
|---|---|---|---|
| 1 | `background&motivation.tex` §2.1 | `That budget is tight---at 15\,W the Orin exposes…` | `That budget is tight: at 15\,W the Orin exposes…` |
| 2 | `implementation&eval.tex` §5.1 | `…budgets---explicitly so on the Jetson, where the 15W cap leaves 4 of its 12 CPU cores available.` | `…budgets. On the Jetson the budget is explicit: the 15W cap leaves 4 of its 12 CPU cores available.` |
| 3 | `introduction.tex` | `remains challenging\new{---\Cref{sec:BG:Scope} defines…}` | `remains challenging\new{; \Cref{sec:BG:Scope} defines…}` |
| 4–5 | `TablesAlgos/Jetson4090A100.tex` | caption, two instances | rewritten, see below |

### 1.7 Part D — table caption, shortened to two sentences

```latex
\caption{\new{Platform specifications for a local/personal-computing desktop (RTX\,4090),
an embedded device (Jetson~AGX~Orin), and a datacenter accelerator (A100). Jetson Orin's
64\,GB is a \emph{single unified} LPDDR5 pool serving CPU and GPU, not memory additional to
the main-memory row.}}
```

**66 → 36 words, three sentences → two.** It now describes rather than argues, per Item 7.
The displaced observation moved into the §2.1 sentence that already introduces the contrast:

```latex
\Cref{tab:spec_comparison} sets both against a datacenter A100, which is not a personal
compute node and is included for contrast only.
```

*(added: "and is included for contrast only")*. The unified-memory merge in the Jetson
column and the caption's position above the `tabular` are unchanged.

---

## 2. Sentence-by-sentence provenance

**R** = rebuttal · **P** = paper · **S** = shepherd/reviewer question.

### Part A — Item 5 (4 sentences)

| # | Sentence | Derives from |
|---|---|---|
| 1 | "Generation latency depends on the intended prompt length." | **P** `design.tex:117`: *"For generation, we measure $T_{G}$ given the intended prompt lengths or batch sizes."* · **P** `characterization.tex:121`: *"Generation is GPU-bound but stable unless models are frequently reloaded or prompts become excessively long."* Frames the question without adopting the reviewer's bandwidth mechanism. |
| 2 | "The mapper profiles $T_G$ across those lengths (`\Cref{subsec:resource-mapping}`), and adaptive batching creates memory-safe GPU quanta." | **R:** *"The mapper profiles generation across intended prompt lengths"* (claim 1) and *"Adaptive batching creates memory-safe GPU quanta"* (claim 3, phrase kept). Cross-reference per the brief, so claim 1 is pointed at rather than restated. |
| 3 | "Worker allocation is nonetheless static within a session, following the start-up amortisation rationale of `\Cref{sec:Design:Software}`." | **R:** *"worker allocation is static within a session"* (claim 2). The rationale is **P** `design.tex:259` (*Start-up costs*): *"the number of workers can be fixed apriori and need not change during the execution of the successive batches… application requirements tend to remain consistent throughout an operational session."* |
| 4 | "Remapping cores at run time under context drift is a future extension." | **R:** *"runtime core remapping under context drift is a future extension, which we will state clearly"* (claim 4), in the rebuttal's own register. |

### Part B — Item 6 (4 sentences)

| # | Sentence | Derives from |
|---|---|---|
| 1 | "The characterization above was performed on the local/personal-computing platform of `\Cref{sec:BG:Scope}`." | **P** `characterization.tex:64`: *"Our experiments use an Intel i9-14900K processor (24 physical cores), 128 GB RAM, and an RTX 4090 GPU."* Terminology from §2.1 per the rebuttal's renaming promise. Required explicitly by the brief. |
| 2 | "Because the optimizations we derive from it target CPU-side encoding and retrieval, the same trends hold on embedded platforms such as the Jetson AGX Orin." | **R:** *"Because our optimizations focus on CPU-side encoding and retrieval, the trends observed on standard devices hold true for Jetson/Orin platforms."* (claim 1) |
| 3 | "The primary difference there is the elimination of PCIe transfer overhead in unified memory systems." | **R:** *"The primary difference is the elimination of PCIe transfer overhead in unified memory systems."* (claim 2, near-verbatim) |
| 4 | "A similar trend is observed across SKUs and vendors." | **R:** *"A similar trend is also observed across SKUs and vendors."* (claim 3, near-verbatim) |

### Parts B (back-ref), C, D

| Passage | Derives from |
|---|---|
| ", consistent with the trend portability established in `\Cref{sec:char:keyobs}`" | Cross-reference to the paragraph above; asserts nothing new. Required by the brief. |
| "local/personal-computing platforms, and embedded devices" | **R:** *"better called local/personal-computing platforms, not embedded edge devices."* |
| "the personal-computing edge platforms" | **R:** *"We treat desktops as personal-computing edge."* |
| "and is included for contrast only" | Relocated verbatim in substance from the caption sentence it replaces (Task 2). The A100 appears in no experiment. |
| Caption sentence 1 | Table columns from `edge vs. server`!F13/G13/H13; terminology from **R**. |
| Caption sentence 2 | Task 2, unchanged. `edge vs. server`!F16 and !F18 both = 64. |

**Every sentence maps.**

---

## 3. Provenance of every numeral

**No new numbers.** The Item 5 and Item 6 passages contain **no numerals at all**. The only
numerals in text touched by this task are the four Task 2/2a already traced, and they were
carried through the em-dash rewrites unchanged:

| Numeral | Where | Source |
|---|---|---|
| `15\,W` | §2.1, em-dash rewrite #1 | **P** `implementation&eval.tex:11`; `design.tex:136` footnote |
| `4` (cores) | §2.1 and §5.1, rewrites #1 and #2 | **P** `design.tex:136` footnote: *"we get 4 cores to work with"* |
| `12` (CPU cores) | §2.1 and §5.1 | `edge vs. server`!F15 = 12 |
| `64\,GB` | table caption | `edge vs. server`!F16 and !F18, both = 64 |
| `4090`, `4080` | table caption | `edge vs. server`!G13; **P** `implementation&eval.tex:11` |

`refs.bib` and `reference.bib` untouched; **no citation was needed that does not already
exist**.

---

## 4. Withheld under the "out of bounds" instructions

Nothing below is in the paper. Each is offered as a recommendation.

### From Part A (Item 5)

| # | Considered | Why withheld | Recommendation |
|---|---|---|---|
| A1 | Reviewer C's own framing, that longer contexts enlarge the KV cache and "may turn into a bandwidth problem" | The rebuttal does not adopt the bandwidth mechanism, and asserting it would introduce a cause the authors did not claim. Sentence 1 states only the prompt-length dependence, which the paper already states twice. | **Leave out** unless you want to concede the bandwidth framing. |
| A2 | The §5.8 token-sensitivity results (0.6 / 1.2 / 12 percent) as corroboration that generation dominates the response to context growth | The brief explicitly asked for this as a report recommendation rather than paper text. It would also be a *derived* corroboration the rebuttal does not draw. Master plan §D also lists these three numbers as having no backing cells. | **Your call.** If added, it needs a source for the three percentages first. |
| A3 | An argument that core rebalancing would (or would not) help under context drift | The rebuttal says only that runtime remapping is a future extension. Any claim about its benefit is unsupported. | **Leave out.** |
| A4 | Naming *where* context growth loads the pipeline (encode vs. generate) | Explicitly out of bounds; the rebuttal makes no such attribution. | **Leave out.** |

### From Part B (Item 6)

| # | Considered | Why withheld | Recommendation |
|---|---|---|---|
| B1 | That characterization requires sweeping past the saturation knee, and at 15 W the Orin sits left of it | Not in the rebuttal. Named as out of bounds. | **Leave out.** It is also a concession that the Orin *cannot* show the trend, which is the opposite of the rebuttal's claim that it does. |
| B2 | That DVFS under the power cap confounds attribution | Not in the rebuttal. | **Leave out.** |
| B3 | That knees shift left with smaller cache and DRAM bandwidth | Not in the rebuttal. | **Leave out.** |
| B4 | That the Orin exposes too few cores to observe saturation | Not in the rebuttal. Note this sits awkwardly beside §2.1's "4 of its 12 CPU cores", which is a *scope* fact, not a characterization-validity argument. | **Leave out.** |
| B5 | That Fig. 5's speedup curve (1.09 → 1.31 → 1.35 → 1.26 across BS 2→16) already demonstrates the trend turning over on the Orin | Not in the rebuttal. Named as out of bounds. | **Worth considering later** — it is the only *measured* support for portability in the paper, and it currently goes unremarked. But it is a new argument and needs your assent. |

---

## 5. Em-dash counts

| | Before Task 3 | After Task 3 |
|---|---:|---:|
| **Text added by Tasks 2, 2a, 3** — `---` | **5** | **0** ✅ |
| **Text added by Tasks 2, 2a, 3** — `—` (literal) | 0 | **0** |
| Pre-existing prose — `---` | 4 | 4 |
| Pre-existing prose — `—` (literal) | 6 | 6 |
| **Pre-existing total** | **10** | **10** |

The five removed are exactly the five the brief listed. No `--` is used as a parenthetical
in new text; the `--` occurrences that remain are numeric ranges and the compound
`CPU--GPU`, both correct.

**For the author to decide:** the 10 pre-existing instances are spread one line each across
`abstract.tex`, `introduction.tex`, `background&motivation.tex`, `characterization.tex`,
`design.tex`, and `implementation&eval.tex`. Six are the literal Unicode character `—`,
four are `---`. One of them sits in the sentence this task edited
(`background&motivation.tex` §2.3, the em-dashes bracketing "encoding, retrieval,
augmentation, and generation"); I left it, because Part D confines the sweep to Tasks 2/2a
text and the minimal-edit rule applies. **A global sweep looks like a natural fit for the
Item 7 task.**

---

## 6. Verification

### Build

| | |
|---|---|
| `make` | **exit 0**, 12 pages |
| LaTeX errors | **0** |
| Undefined references | **0** — new `sec:char:keyobs` resolves to §3.3 (p3) |
| Undefined citations | **0** |
| All 41 references render | ✅ |

### Revision modes — pixel-verified

Six pages now carry new text, up from three:

| Page | Content | Differing pixels | mode 1 | mode 0 |
|---|---|---:|---|---|
| 1 | intro clause | 1,981 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 2 | §2.1, Table 1, §2.3 platform list | 41,868 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 4 | §3.3 portability paragraph | 14,283 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 5 | §4.1 adaptive batching | 10,320 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 7 | §5.1 deployment + metrics | 12,309 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 8 | §5.3 Jetson back-reference | 1,969 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 3, 6, 9–12 | — | **0**, pixel-identical | | |

`\revmode` restored to `1`.

### `verify_numbers.py`

```
checks : 41 PASS / 5 FAIL / 1 UNVERIFIABLE
drift  : none
```

Unchanged from Task 2a. The five known FAILs and the one UNVERIFIABLE are untouched; all
nine hardware-table checks still pass.

### Page count

**12 pages, unchanged.** Growth landed as follows:

| Landmark | pre-Task 2 | Task 2a | **Task 3** |
|---|---:|---:|---:|
| §2.1 Deployment Scope | — | 2 | 2 |
| §3.3 *Portability of these trends* | — | — | **4** (new) |
| §4.1 *Generation latency depends…* | — | — | **5** (new) |
| §5 Implementation and Evaluation | 6 | 6 | **7** (+1) |
| §5.2 Results on RTX | 7 | 7 | 7 |
| §6 Related Work | 10 | 10 | **11** (+1) |
| §7 Conclusions | 10 | 11 | 11 |

The back half moved one page later; the reference list absorbed it again, still ending on
page 12. All 41 references render.

**Headroom is now the thing to watch.** Three tasks have consumed the slack that page 12
had. Item 1's Table 2 and Item 4's ablation table are still to come, and one of them will
likely push to page 13.

### Bibliography

Byte-identical to the pre-Task-2 state:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

### Diff against Task 2a (`780fcbc`)

```
 TablesAlgos/Jetson4090A100.tex |  2 +-
 background&motivation.tex      |  4 +--
 characterization.tex           |  6 ++
 design.tex                     |  1 +
 implementation&eval.tex        |  6 +--
 introduction.tex               |  2 +-
 reports/verify_numbers.md      | 66 +++---
 7 files changed, 47 insertions(+), 40 deletions(-)
```

### PDF

Not committed (gitignored). Timestamped copy: **`reports/task03_main_20260808-1356.pdf`**.

---

## 7. Things that contradict the instructions, or that you should decide

### 7.1 §3.3 had no label; I added one

The brief asks for a back-reference "pointing to this paragraph", but
`\subsection{Key Observations and Motivation for Design}` carried no `\label`. I added
`\label{sec:char:keyobs}` on the line immediately after the heading. It is a pure addition
with no rendering effect, and it resolves to §3.3. Placing the label inside the new
paragraph instead would have worked here but is fragile: `\label` binds to the last stepped
counter, so an intervening float would silently make it point at a figure.

### 7.2 The back-reference is one clause, attached to an existing sentence

The brief said "one clause". Rather than a standalone sentence, I appended
", consistent with the trend portability established in `\Cref{sec:char:keyobs}`" to the
subsection's existing second sentence, which already discusses why the Orin behaves as it
does. That is literally one clause and it does not rewrite anything. Flagging in case you
expected a separate sentence.

### 7.3 Part C.2 uses the §2.1 term without a fourth `\Cref`

The brief says the Metrics sentence "should refer to the platforms as defined in Section
2.1." I used the defined term, "the personal-computing edge platforms", without adding a
`\Cref{sec:BG:Scope}`. §2.1 is already cross-referenced twice within §5.1 on the same page;
a third pointer four lines later would be noise, and each one costs another instance of the
`Section §N` defect. Say the word and it becomes an explicit reference.

### 7.4 The `Section §N` count is now 19, up from 9 before Task 2

| State | Instances |
|---|---:|
| pre-Task 2 | 9 |
| Task 2 | 13 |
| Task 2a | 15 |
| **Task 3** | **19** |

Task 3 adds four, all required by the brief: §2.1 from the portability paragraph, §4.2 and
§4.3 from the Item 5 passage, and §3.3 from the Jetson back-reference. The rebuttal itself
promises the fix (*"We will also remove redundant 'Section section-symbol' usage"*), and
Item 7's sweep must now cover ten added instances across Tasks 2, 2a and 3. This is worth
scheduling deliberately rather than leaving to the end: it is a one-line preamble change
(`\creflabelformat`) plus a read-through.

### 7.5 The Item 5 passage sits in §4.1, which is where the brief put it, but §4.2 is where the mapper lives

The *Adaptive batching* paragraph is in §4.1 (*Pipeline Design Overview*); the mapper and
$T_G$ profiling are in §4.2 (*Resource Mapping*). The passage therefore forward-references
§4.2 from §4.1. This is what the brief specified and it reads correctly, but if you would
rather the passage sat next to the mapper it describes, §4.2's closing paragraph is the
alternative home. Purely a placement preference; no text would change.

### 7.6 One rebuttal claim is stated more weakly than the rebuttal states it

The rebuttal says *"the trends observed on standard devices hold true for Jetson/Orin
platforms"* — a claim about a platform the paper characterizes only indirectly. The paper
now says the same thing. **No measurement in the paper demonstrates it**, and item B5 above
(Fig. 5's turnover) is the only thing that would. Reporting rather than resolving, per
protocol §2: the rebuttal's framing stands, but you should know the claim is asserted, not
shown.

---

## 8. Acceptance criteria

| | Criterion | Status |
|---|---|---|
| ☑ | Item 5 passage states the four claims and nothing further | 4 sentences, mapped in §2 |
| ☑ | Runtime core remapping stated clearly as future work | sentence 4 |
| ☑ | Claim 1 references §4.2 rather than restating it | `\Cref{subsec:resource-mapping}` |
| ☑ | Item 6 paragraph states the three claims and nothing further | 4 sentences, mapped in §2 |
| ☑ | No saturation-knee, DVFS, cache-capacity, core-count, or Fig. 5 argument anywhere | 5 candidates withheld and logged in §4 |
| ☑ | States plainly that characterization was on the desktop platform, and why it carries | sentences 1 and 2 |
| ☑ | One back-reference from the Jetson results subsection | one clause, §5.3 |
| ☑ | Both Part C contradictions resolved with minimal edits | two spans changed |
| ☑ | All five em-dashes removed; zero `---` in Tasks 2/2a/3 text | verified by script, count 5 → 0 |
| ☑ | Table caption reduced to two sentences | 66 → 36 words |
| ☑ | Every sentence of new prose mapped | §2 |
| ☑ | Blue at `\revmode=1`, black at `=0` | six pages, 100% blue / RGB(0,0,0), 0 near-white |
| ☑ | `make` clean: 0 undefined refs, 0 undefined citations | exit 0 |
| ☑ | `refs.bib`, `reference.bib` byte-identical to pre-Task-2 | SHA-256 verified |
| ☑ | `verify_numbers.py` no drift | 41 / 5 / 1 |
| ☑ | `main.pdf` not committed; timestamped copy in `reports/` | `task03_main_20260808-1356.pdf` |
| ☑ | Committed, not pushed | see `git log`; no `git push` run |
