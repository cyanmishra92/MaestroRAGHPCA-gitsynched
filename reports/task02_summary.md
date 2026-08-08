# Task 2 — Summary

**Shepherd Item 2:** define "edge" and justify the evaluation platforms. Also discharges the
binding rebuttal promise to rename the desktops away from "embedded edge devices."

Four files edited, one table file rewritten, nine regression checks added. `refs.bib` and
`reference.bib` are byte-identical to their pre-task state.

---

## 1. Full text of every passage added

### 1.1 `background&motivation.tex` — new §2.1, inserted between the section-opening paragraph and `\subsection{Different Stages of a RAG System}`

```latex
\subsection{\texorpdfstring{\new{Deployment Scope}}{Deployment Scope}}
\label{sec:BG:Scope}
\begin{newtext}
We use \emph{edge} to denote a deployment constraint rather than a form factor. A
platform is an edge target in this work if it satisfies four conditions: (i)~a
\emph{single} accelerator is shared by every pipeline stage, making contention
structural rather than a scheduling choice; (ii)~no cloud offload is available, so the
entire pipeline is resident locally for privacy and latency; (iii)~the power and thermal
budget is fixed and non-elastic; and (iv)~memory is provisioned for one model, not a
model zoo. Two tiers satisfy all four and differ in scale, not in kind:
\emph{local/personal-compute} platforms---our \mbox{i9-14900K} desktops paired with an
RTX\,4090 or RTX\,4080---and \emph{embedded} platforms, represented here by a
Jetson~AGX~Orin held at a 15\,W cap. \Cref{tab:spec_comparison} contrasts both tiers with
a datacenter A100, which fails (i), (iii), and (iv). Unified memory does not exempt the
embedded tier from our motivation: it removes the PCIe copy, but neither the structural
hazard of a single GPU that cannot encode and generate concurrently, nor the contention
among encoder weights, the retrieval working set, and the KV cache inside one memory and
power budget. That budget binds tightly---at the 15\,W cap the Orin exposes 4 of its 12
CPU cores (\Cref{subsec:implementation}).
\end{newtext}

\input{TablesAlgos/Jetson4090A100}
```

The heading is wrapped in `\texorpdfstring` so it renders blue in the page while the PDF
bookmark stays a plain string — without it, `\textcolor` inside a section title raises
`hyperref` "Token not allowed in a PDF string" warnings. The warning count is unchanged
at 4, all pre-existing.

### 1.2 `TablesAlgos/Jetson4090A100.tex` — rewritten (caption above, memory merged)

```latex
\begin{table}[]
\centering
\caption{\new{Constraint contrast. Both evaluated edge tiers---embedded
(Jetson~AGX~Orin) and local/personal-compute (RTX\,4090 desktop)---share a single
accelerator across every pipeline stage and size memory for one model; the datacenter
A100 does neither. Jetson Orin's 64\,GB is a \emph{single unified} LPDDR5 pool serving
CPU and GPU, not memory additional to the main-memory row. The A100 column is shown for
contrast only and is not an evaluation platform.}}
\label{tab:spec_comparison}
\resizebox{\linewidth}{!}{%
\begin{tabular}{lccc}
\toprule
\textbf{Specification} & \textbf{Jetson Orin} & \textbf{RTX 4090} & \textbf{A100} \\
\midrule
\textbf{CPU} & Arm-A78AE & Intel i9-14900K & AMD 7742 \\
\textbf{CPU Cores} & 12 & 24 & 128 \\
\textbf{Main Memory (GB)} & \multirow{2}{*}{64 (unified)} & 128 & 2048 \\
\textbf{GPU VRAM (GB)} &  & 24 & 80 \\
\textbf{RAM Type} & \multirow{2}{*}{LPDDR5} & DDR5 & DDR4 \\
\textbf{VRAM Type} &  & GDDR6X & HBM2e \\
\bottomrule
\end{tabular}%
}
\end{table}
```

As rendered:

```
  Specification        Jetson Orin    RTX 4090          A100
  CPU                  Arm-A78AE      Intel i9-14900K   AMD 7742
  CPU Cores                 12               24          128
  Main Memory (GB)     64 (unified)         128         2048
  GPU VRAM (GB)                              24           80
  RAM Type               LPDDR5             DDR5         DDR4
  VRAM Type                               GDDR6X        HBM2e
```

One `64 (unified)` now bridges the two capacity rows and the Jetson VRAM cell is empty,
so the column cannot be summed to 128 GB. **No number was changed.**

### 1.3 `implementation&eval.tex` — §5.1 Deployment System

Opening clause replaced (old text struck, new in `\new{}`):

> ~~Our evaluations are conducted on 3 representative edge devices:~~
> `\new{`Following `\Cref{sec:BG:Scope}`, our evaluations span both edge tiers---two
> local/personal-compute platforms and one embedded platform:`}`

The three numbered hardware descriptions that follow are **untouched**. Appended after
them:

```latex
\new{All three meet the criteria of \Cref{sec:BG:Scope}. Each provisions a single GPU
that every pipeline stage must share, runs the complete pipeline locally with no cloud
offload, and holds enough VRAM or unified memory for one generation model rather than a
resident model zoo---24\,GB, 16\,GB, and 64\,GB shared with the host, respectively. Their
power and thermal budgets are fixed rather than elastic: the desktops are bounded by a
single stock chassis, and the Jetson is held explicitly at 15W, which leaves 4 of its 12
CPU cores online. The two tiers therefore differ in scale alone, which is why the same
orchestration is evaluated unchanged across both.}
```

### 1.4 `introduction.tex` — forward pointer, one clause

```latex
However, deploying RAG efficiently on edge devices, which typically have a single GPU
shared for all  tasks, remains challenging\new{---we define \emph{edge} by deployment
constraint rather than form factor in \Cref{sec:BG:Scope}}.
```

The paragraph is otherwise untouched. **Typo fixed on this line** (permitted, since I was
already editing it): `edge devices,which` → `edge devices, which` — a missing space after
the comma, which LaTeX was rendering as `devices,which`. Logged here as required. The
double space in `all  tasks` was left alone; LaTeX collapses it, so it is not a rendering
defect and fixing it would widen the diff for no visible gain.

---

## 2. Provenance of every numeral

**No new numbers were introduced.** Every numeral in the new prose already existed in the
paper, in an authorised workbook tab, or in both.

| Numeral | Where I used it | Source |
|---|---|---|
| `15\,W` (×2, §2.1) | Orin power cap | `implementation&eval.tex:11` ("15W"); `design.tex:136` footnote |
| `4` (cores online) | §2.1 and §5.1 | `design.tex:136` footnote: *"we get 4 cores to work with"* |
| `12` (Orin CPU cores) | §2.1 and §5.1 | `edge vs. server`!F15 = 12; hardware table row |
| `4090`, `4080` | §2.1 tier mapping | `implementation&eval.tex:11`; `edge vs. server`!G13 |
| `i9-14900K` | §2.1 tier mapping | `implementation&eval.tex:11`; `edge vs. server`!G14 |
| `64\,GB` (caption) | unified pool | `edge vs. server`!F16 **and** !F18, both = 64 |
| `24\,GB`, `16\,GB`, `64\,GB` (§5.1) | VRAM per platform | all three already in the same sentence at `implementation&eval.tex:11` |
| `A100` | contrast column | `edge vs. server`!H13 |
| `(i)`–`(iv)` | criteria labels | enumerators, not data |
| Table body: 12/24/128, 64/128/2048, 64/24/80 | unchanged | `edge vs. server`!F15–H15, F16–H16, F18–H18 — now covered by 9 checks |

**No citation was needed that did not already exist.** `refs.bib` and `reference.bib` were
not opened for writing; verified byte-identical by SHA-256 before and after:

```
7d7182d601e41c28fbc8179aae17fc4cfd6fa8fc5f2da9b9ef6f16a91fe100fe  refs.bib
152174490bf12257c1e20f8ff385da6a125615da11f34ab0257a116f334e0eb3  reference.bib
```

---

## 3. Terminology audit (Step 5)

32 live occurrences of "edge" across 23 lines in the active `.tex` files. Below is every
occurrence whose context bears on the **evaluation platforms**; the purely generic uses
(class term, motivation, related work) are summarised at the end.

**Only the §5.1 instance was changed.** Everything marked *recommend* awaits your approval.

| # | File:line | Current wording | Verdict |
|---|---|---|---|
| 1 | `background&motivation.tex:50` | "consistent across datacenter servers, **desktops, and edge devices**" | ⚠️ **Recommend changing in a later task.** This is the one real conflict: it lists desktops as *distinct from* edge devices, contradicting §2.1 four lines above, which puts desktops inside the edge class as the local/personal-compute tier. Suggested: "…across datacenter servers and the local-compute and embedded platforms of `\Cref{sec:BG:Scope}`". |
| 2 | `implementation&eval.tex:19` | "the tight power and energy constraints of **the edge devices**" | **Recommend changing in a later task.** Refers to all three evaluation platforms; "devices" is exactly the embedded framing the rebuttal promised to drop for the desktops. Suggested: "of the edge platforms". |
| 3 | `implementation&eval.tex:11` | was "3 representative **edge devices**" | ✅ **Changed in this task** → "both edge tiers---two local/personal-compute platforms and one embedded platform". |
| 4 | `abstract.tex:1` | "Implemented on **three edge platforms**---including an NVIDIA Jetson and consumer-grade GPUs" | ✅ **Correct as-is.** Already says *platforms*, not *devices*, and already distinguishes the Jetson from the consumer-grade GPUs. Optional polish only. |
| 5 | `implementation&eval.tex:120` | "meaningful benefits on **edge devices**" | ✅ **Correct as-is.** Sits inside §5.3 (Jetson), so "devices" correctly denotes the embedded tier. |
| 6 | `implementation&eval.tex:159` | "energy consumption on **edge platforms**" | ✅ **Correct as-is.** Already "platforms". |
| 7 | `design.tex:50` | "Our design for an **edge personal computing device**" | ✅ **Correct as-is.** Already uses the personal-computing framing the rebuttal promised. |
| 8 | `introduction.tex:162` | "deploying RAG efficiently on **edge devices**, which typically have a single GPU…" | ✅ **Changed in this task** — not the noun, but the forward pointer that now defines it. The phrase is the class term and the following clause scopes it. |
| 9 | `introduction.tex:172` | "On **edge devices** with single GPU, this creates a structural hazard" | ✅ **Correct as-is.** Class term, and it states criterion (i) verbatim. |
| 10 | `introduction.tex:174` | "RAG inference on **edge devices**" | ✅ **Correct as-is.** Class term. |
| 11 | `background&motivation.tex:46` | "in **edge devices**, GPUs have limited VRAM and share resources" | ✅ **Correct as-is.** Class term stating criteria (i) and (iv). |
| 12 | `conclusion.tex:3` | "performance on **edge devices**" | ✅ **Correct as-is.** Class term. |
| 13 | `main.tex:257` | title: "…Efficient RAG on **Edge Devices**" | ✅ **Correct as-is** for this task. The title needs the `Regular-` prefix dropped for camera-ready (Task 1 report §5.4), but "Edge Devices" as the class term is fine. |
| 14 | `abstract.tex:1` | "privacy- and resource-constrained **edge deployments**" | ✅ **Correct as-is.** Class term. |
| 15 | `introduction.tex:161` (×2) | "on-device or **edge**-based AI systems"; "shift inference workloads toward the **edge**" | ✅ **Correct as-is.** Class term, motivation framing. |
| 16 | `TablesAlgos/Jetson4090A100.tex:3` | "Both evaluated **edge tiers**…" | ✅ **Added in this task.** |
| 17 | `background&motivation.tex:15` (×2) | the definition itself | ✅ **Added in this task.** |

**Summary: 1 genuine conflict (#1), 1 wording improvement (#2), 4 changed/added by this
task, 11 correct as-is.** Item #1 is the one I would prioritise — it sits four lines below
the new definition and a shepherd reading §2 straight through will hit both.

---

## 4. Page count

**Unchanged: 12 → 12.** The new material is roughly half a column of body text plus a
single-column table.

Measured by rebuilding the pre-Task-2 state from `HEAD` and comparing landmark positions:

| Landmark | Before | After | Shift |
|---|---:|---:|---:|
| §1 Introduction | 1 | 1 | 0 |
| §2 Demystifying RAG Computation | 1 | 1 | 0 |
| **§2.1 Deployment Scope + Table 1** | — | **2** | *new* |
| §3 Detailed Characterization | 2 | 3 | +1 |
| §4 Proposed Pipelined Computation Model | 4 | 4 | 0 |
| §5 Implementation and Evaluation | 6 | 6 | 0 |
| §5.1 Deployment System | 6 | 7 | +1 |
| §5.6 Power | 8 | 9 | +1 |
| §6 Related Work / §7 Conclusions / §8 AI Usage | 10 | 11 | +1 |

**Where the growth landed:** the body now runs onto page 11, where the reference list
previously began at the top of the column. The references absorbed the shift because
page 12 had slack in the baseline. **All 41 references still render in both builds**
(verified by checking markers `[1]`–`[41]` are present); nothing was truncated.

Consequence to be aware of: the paper is now closer to its page budget than it was. The
master plan allows 1–2 pages of relief, so there is headroom, but later tasks adding
Table 2 and the ablation table should re-check this.

---

## 5. Verification

### Build

| | |
|---|---|
| `make` | **exit 0**, 12 pages |
| LaTeX errors | **0** |
| Undefined references | **0** — `sec:BG:Scope` → §2.1 (p2), `tab:spec_comparison` → Table 1 (p2) |
| Undefined citations | **0** |
| `hyperref` token warnings | 4 — unchanged from baseline |
| Float-specifier warnings | 1 → **2** (see §6.4) |

### Revision modes — pixel-verified

Both modes built and all 12 pages rasterised at 150 dpi:

| Page | Differing pixels | mode 1 ink | mode 0 ink |
|---|---:|---|---|
| 1 (intro clause) | 2,419 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 2 (§2.1 + Table 1) | 48,929 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 7 (§5.1) | 22,504 | **100% blue** | **RGB(0,0,0)**, 0 near-white |
| 3–6, 8–12 | **0** — pixel-identical | | |

Exactly the three pages I edited differ, and nothing else moved colour. `\revmode`
restored to `1`.

### `verify_numbers.py`

```
checks : 41 PASS / 5 FAIL / 1 UNVERIFIABLE
drift  : none
```

**No drift.** The 38 pre-existing checks are unchanged at **32 PASS / 5 FAIL / 1
UNVERIFIABLE** — the five known FAILs (peak power ×2, Jetson 25–35% band, FlashRAG energy
791.8 J, 4080 FlashRAG 1.9×) and the cold-start UNVERIFIABLE are all still exactly where
Task 1 left them, untouched. The tally moved to 41 PASS only because of the nine new
hardware-table anchors, all of which pass:

| Check | Claimed | Cell | Result |
|---|---:|---|---|
| `hwtable_cores_jetson` | 12 | `edge vs. server!F15` | PASS |
| `hwtable_cores_4090` | 24 | `!G15` | PASS |
| `hwtable_cores_a100` | 128 | `!H15` | PASS |
| `hwtable_mainmem_jetson` | 64 | `!F16` | PASS |
| `hwtable_mainmem_4090` | 128 | `!G16` | PASS |
| `hwtable_mainmem_a100` | 2048 | `!H16` | PASS |
| `hwtable_vram_jetson` | 64 | `!F18` | PASS |
| `hwtable_vram_4090` | 24 | `!G18` | PASS |
| `hwtable_vram_a100` | 80 | `!H18` | PASS |

`TablesAlgos/Jetson4090A100.tex` was added to `tex_sources`, so its literals now enter the
extraction (216 → 237 literals).

### PDF

`main.pdf` is **not committed** — it is gitignored (`.gitignore:4`) and untracked.
Timestamped copy saved as **`reports/task02_main_20260808-1229.pdf`**.

---

## 6. Things that contradict the instructions, or that you should decide

### 6.1 The brief says "most 'edge' uses are correct" — one is not, and it is adjacent

`background&motivation.tex:50` reads *"consistent across datacenter servers, **desktops,
and edge devices**"*. That sentence puts desktops **outside** the edge class, which is the
exact opposite of the §2.1 definition sitting four lines above it. Under the Step 5
instruction I only reported it rather than changing it, but it is the one line in the
paper that now openly contradicts the new definition, and it is in the same subsection
flow a shepherd will read. I would fix it next.

### 6.2 The table's *numbers* match the workbook; two *strings* are abbreviated

The brief states the table's values "match the `edge vs. server` tab exactly." All nine
numbers do. Two text cells are abbreviations rather than exact copies:

| Table | Workbook |
|---|---|
| `Arm-A78AE` | `Arm® Cortex®-A78AE` (F14) |
| `AMD 7742` | `AMD Rome 7742` (H14) |

These are contractions, not errors, so I left them and did not encode them as checks —
a string check would have manufactured a FAIL for a cosmetic abbreviation, which would
have violated both "no drift" and "do not fix defects outside this task." Noted in
`checks.yaml` so the omission is deliberate and visible.

### 6.3 Merging the memory rows required reordering, not just merging

To span one `64 (unified)` cell across Main Memory and GPU VRAM, those two rows must be
adjacent. The row order is now **CPU, CPU Cores, Main Memory, GPU VRAM, RAM Type, VRAM
Type** (previously Main Memory, RAM Type, GPU VRAM, VRAM Type). **Same six rows — none
added, none removed, no value altered.** It also groups capacities together and types
together, which reads better, and it let me merge the Jetson `LPDDR5` type cell too,
reinforcing that there is one memory.

### 6.4 The table float carries an empty placement specifier

`\begin{table}[]` was already in the file. It produces `LaTeX Warning: No positions in
optional float specifier`, taking the count from 1 to 2. Fixing it (`[t]`) is not among
the four permitted changes, so I left it. One character if you want it gone.

### 6.5 Table 1 floats above the heading that introduces it

Table 1 lands at the top of page 2, column 1 — *above* the "2.1. Deployment Scope"
heading. Same page, standard LaTeX float behaviour, and the caption is self-contained, so
it reads acceptably. If you want it below the prose, `[t]` → `[h]` or `[!b]` is the lever;
I did not touch it, per 6.4.

### 6.6 My four new `\Cref` uses add four instances of the known `Section §N` bug

The paper renders `\Cref{sec:...}` as "Section §N" — the word *and* the sign — which
Task 1 documented as a camera-ready blocker for Item 7. My additions take it from **9 to
13** instances: three "Section §2.1" (intro, §5.1 ×2) and one "Section §5.1" (§2.1's
pointer to the implementation subsection). This is not new breakage; it is the existing
bug applied consistently. **Item 7's global `\S` purge must cover these four.**

### 6.7 Table renumbering is automatic and expected

`tab:spec_comparison` is now **Table 1** (page 2) and the caching table `tab:cache_results`
became **Table 2** (page 9). Every `\Cref` updated itself; nothing hard-codes a table
number.

### 6.8 A power-envelope row would help, and I did not add it

As the brief anticipated: a TDP / power-envelope row is the single strongest addition this
table could carry — it would make criterion (iii) visible rather than asserted, since the
15 W Orin against a 450 W 4090 against a 400 W A100 is the whole argument in one line.
**No authorised source contains those figures**, so I am reporting rather than adding.
If you can supply them from a citable source, it is a three-cell change.

### 6.9 "Expect no drift — the same 32/5/1"

Strictly, the tally is now 41/5/1. The instruction's intent is satisfied: the 38 checks
that existed before this task hold **exactly** their previous statuses, and the drift
detector reports none. The nine added checks are all new PASSes.

---

## 7. Acceptance criteria

| | Criterion | Status |
|---|---|---|
| ☑ | `\subsection{Deployment Scope}` with `sec:BG:Scope`, before `Different Stages` | §2.1, page 2 |
| ☑ | Four constraints, both tiers, unified-memory objection answered | all four present; A100 fails (i), (iii), (iv) |
| ☑ | `Jetson4090A100.tex` input and rendered; memory unmisreadable; caption above and rewritten | Table 1, `64 (unified)` merged across both capacity rows |
| ☑ | §5.1 no longer calls the desktops "edge devices"; all three justified | "two local/personal-compute platforms and one embedded platform" |
| ☑ | One forward pointer in the introduction; paragraph otherwise untouched | one clause at `introduction.tex:162` |
| ☑ | New prose blue at `\revmode=1`, black at `\revmode=0` | 100% blue / RGB(0,0,0), 0 near-white pixels |
| ☑ | `make` clean: 0 undefined refs, 0 undefined citations | exit 0 |
| ☑ | `refs.bib` and `reference.bib` byte-identical | SHA-256 verified |
| ☑ | No drift; hardware-table checks added | 38 pre-existing unchanged; 9 added, all PASS |
| ☑ | `main.pdf` not committed; timestamped copy in `reports/` | `reports/task02_main_20260808-1229.pdf` |
| ☑ | Committed, not pushed | see `git log`; no `git push` was run |
| ☑ | Every numeral traced; nothing invented | §2 above — zero new numbers |
