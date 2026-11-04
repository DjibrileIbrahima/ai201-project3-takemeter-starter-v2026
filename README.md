# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads comments from r/soccer, the main general football subreddit,
where every big moment (a goal clip, an award, a controversy) gets a thread of
hundreds of replies. It sorts each comment into `analysis` (a point backed by
a specific, checkable observation), `hot_take` (a confident opinion with no
real support) or `reaction` (an in-the-moment emotional response). The goal is
to pull the handful of posts that actually argue something out of a thread
that is mostly noise.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** A post that makes a point and supports it with a specific,
checkable observation, explaining how that observation supports the point.

**Example 1:**
> “Since he has been in Milan, on paper we are playing 3-4-2-1, but if you
> look at games we are very often playing 4-3-3/4-4-2.”

**Example 2:**
> “I don’t think playing Bruno in a double pivot is a bad idea though. He was
> creating chances from deep ... he’s also excellent at ball progression.”

### `hot_take`

**Definition:** A confident judgment or claim that does not give concrete
support for its conclusion.

**Example 1:**
> “Man if this is red then every game I played in high school would be 1 vs 1.”

**Example 2:**
> “Bruno in double pivot is one of the stupidest ‘experiments’ I’ve seen yet.”

### `reaction`

**Definition:** A brief, immediate response to a specific event or post, mainly
expressing an emotion or first impression rather than making a broader argument.

**Example 1:**
> “I think sometimes people forget how good this guy actually is.”

**Example 2:**
> “It really felt like it was Mbappe vs Argentina.”

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`

**The decision rule I used every time:** If the post explains how a specific,
checkable observation supports its claim, label it `analysis`. Merely naming a
player, formation, or example is not enough. If it mainly asserts a confident
judgment without that connection, label it `hot_take`. If it is primarily an
immediate response to the event, label it `reaction`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Comments from five r/soccer threads, October
2026: Yamal's goal against Real Betis (fan angle), China rejecting Mbappé and
Real Madrid's apologies, Harry Kane winning the 2026 Ballon d'Or, Ronaldo's
2008 season winning the fan-voted "BOAT" award, and Bellingham's skill in the
build-up to a Real Madrid goal. I saved each thread's JSON from the browser
and `collect.py` pulled out every comment of 4+ words (dropping deleted posts
and AutoModerator), giving 1,857 posts in `raw_posts.csv`. Because the median
post is 13 words and `analysis` lives in the long tail, I built the labelling
pool from every post of 35+ words plus a random sample of shorter ones, then
added the longest argumentative posts from the Ronaldo and Bellingham threads
when `analysis` came up short of criterion 3.

**How I labelled them:** I labelled the first 20 usable posts cold (note
`cold`). The remaining 230 were pre-labelled by Claude from my definitions and
decision rule (note `pre-labelled by Claude`; 29 close calls are marked
`borderline`). Posts that were off-topic politics with no football angle, or
fit no label, were marked `skip` in `to_label.csv` and left out of
`labels.csv`. See the disclosure under **How I Used AI**.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `hot_take` | 108 | 43% |
| `reaction` | 85 | 34% |
| `analysis` | 57 | 23% |
| **Total** | 250 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Yes but its getting increasingly more difficult as he gets
> older. In modern time the oldest player was 36 and it was Messi. The second
> oldest was Benzema at 34. Kane is 33 so there are realistically 1 or 2 more
> seasons ... where he could win it."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* I labelled it `hot_take` cold, reading it as a
> prediction about Kane. Under my own decision rule it is arguably `analysis`:
> the winners' ages are checkable and the post uses them to support the
> claim. This is the clearest case where I applied my rule loosely, and it is
> exactly the boundary criterion 4 measures.

**2.**
> *The post:* "I will always die on the hill that Courtois should have won
> over Benzema. For every Benzema goal there were 3-4 key defenses by
> Courtois throughout that season."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `analysis` (pre-labelled, marked borderline). The "3-4
> key defenses per goal" is a specific, countable comparison tied directly
> to the claim, even though it is probably exaggerated. My rule asks whether
> the evidence is checkable and linked, not whether it is right.

**3.**
> *The post:* "I love Lamine and I would've loved for him to win it, but Kane
> absolutely deserved it. ... the slander on his name for staying loyal to
> Tottenham and now getting recognize as one of the best as he has always
> been."
>
> *Could have been:* `reaction` or `hot_take`
>
> *I chose, because:* `reaction` (cold). It is a judgment ("Kane absolutely
> deserved it"), but the post is mostly an emotional response to the result
> being announced, not an argument for the judgment. Posts like this, a
> verdict wrapped in feelings, are where `reaction` and `hot_take` blur.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, trained on CPU (no GPU on this
laptop).

**Settings:** 8 epochs, learning rate 2e-5, batch size 16, max length 128,
seed 42.

**Anything I changed from the defaults, and why:** Epochs went from 3 to 8.
With the default 3 epochs, 174 training posts gave only 33 gradient steps.
Training loss stayed at 0.92, close to the 1.10 of pure guessing among three
labels, and the model never predicted `analysis` at all: test accuracy
0.526, macro F1 0.384, `analysis` F1 0.000. That is underfitting, not a hard
boundary. At 8 epochs: accuracy 0.605, macro F1 0.595, and F1 of 0.533
(`analysis`), 0.562 (`hot_take`) and 0.690 (`reaction`). The most confident
third of predictions was right 75% of the time, against 33% for the least
confident third. One run takes about 10 minutes on CPU. Nothing else
changed.

**Split sizes:** train 174 / val 38 / test 38. In the test split: 9
`analysis`, 16 `hot_take`, 13 `reaction`. `analysis` is just above the
roughly 8-post line, so a single post moves its F1 a lot, and I expect it to
be the jumpiest number across seeds next unit.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* A script to pull every comment from a Reddit thread
  into a CSV for labelling.
- *What came back:* `collect.py`, using Reddit's public `.json` endpoint. On
  the first run Reddit answered with 403 Blocked.
- *What I changed:* Instead of trying to get around the block, I saved each
  thread's `.json` page from my own browser, and the script was changed to
  read saved files. It also filters out deleted posts, AutoModerator and
  comments under 4 words. One goal-clip thread was mostly reactions, so I
  added more argumentative threads.

**Moment 2**

- *What I asked for:* Pre-labels for the posts after my 20 cold ones, using
  my definitions.
- *What came back:* Before labelling, Claude pointed out that several of my
  cold labels didn't follow my own written decision rule. I had called a post
  with checkable age stats `hot_take`, and posts like "you can tell it means
  a lot to him" `analysis`. It asked whether to follow the rule as written or
  my cold habits.
- *What I changed:* I had it follow the written rule strictly and kept my
  cold labels unchanged as an honest record. The first pass left `analysis`
  at 40, under criterion 3's floor of 45, so I collected two more threads,
  and the strongest argumentative posts from them brought it to 57.

**Pre-labelling disclosure:** 20 of the 250 posts were labelled cold by me
(`note = cold`). The other 230 were pre-labelled by Claude (Opus 5.5) from the
definitions and decision rule above, each marked `pre-labelled by Claude` in
the `note` column, with 29 close calls marked `borderline`. Because of time, I
did not read and correct every pre-label before this training run. Where I
change one later, its note becomes `pre-labelled by Claude, corrected`.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline |
|---|---|
| Overall accuracy | 1.000 |
| Macro F1 | 1.000 |
| F1 — `your_label_here` | 1.000 |

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
