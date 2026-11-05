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

Baseline: `facebook/bart-large-mnli` zero-shot, given only my label
definitions, scored on the same 38 held-out posts (`test_split.csv`, seed 42)
as the trained model.

| Measure | Baseline | Trained (seed 42) | Difference |
|---|---|---|---|
| Overall accuracy | 0.237 | 0.605 | +0.368 |
| Macro F1 | 0.176 | 0.595 | +0.419 |
| F1 — `analysis` | 0.000 | 0.533 | +0.533 |
| F1 — `hot_take` | 0.389 | 0.562 | +0.173 |
| F1 — `reaction` | 0.138 | 0.690 | +0.552 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

The baseline did worse than guessing. 0.237 accuracy is below the 0.33 of a
random pick and below the 0.42 of always answering `hot_take`. It never got
a single `analysis` post right: it spread its guesses over `hot_take` and
`reaction`, and called posts like the Neuer/Golden Ball comparison
`reaction`. My definitions alone aren't enough for a general model to find
the line between "backs it up" and "just says it". The 250 labelled
examples are what taught that, so fine-tuning added a real +0.42 macro F1.
But the trained model still sits well below my own 0.65 target, so beating
the baseline is a low bar here. It doesn't mean the model is good.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

8 epochs, lr 2e-5, batch 16, CPU. Test split is 38 posts per seed (9
`analysis`, 16 `hot_take`, 13 `reaction`).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 every seed | 0.605 | 0.500 | 0.553 | MISSED |
| 2. Per-label F1 | `analysis` ≥ 0.60; `hot_take`, `reaction` ≥ 0.55 | a 0.533 · h 0.562 · r 0.690 | a 0.500 · h 0.550 · r 0.417 | a 0.588 · h 0.541 · r 0.545 | MISSED |
| 3. Balance | no label > 50%, every label ≥ 45 | 43% max, 57 min | same data | same data | MET |
| 4. `analysis` → `hot_take` | < 1 in 4 true `analysis` | 4 / 9 | 5 / 9 | 4 / 9 | MISSED |
| 5. Confidence gap | top third ≥ 0.15 above bottom third | 0.750 vs 0.333 (+0.42) | 0.750 vs 0.417 (+0.33) | 0.750 vs 0.500 (+0.25) | MET |

Macro F1 across seeds: 0.595, 0.489, 0.558. Accuracy moved 0.105 across
seeds, more than 10 points, which the notebook flags as too small a dataset
for a stable measure.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42:

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 4 | 4 | 1 |
| **hot_take** | 2 | 9 | 5 |
| **reaction** | 0 | 3 | 10 |

Summed over all three seeds (114 test predictions):

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 12 | 13 | 2 |
| **hot_take** | 5 | 30 | 13 |
| **reaction** | 0 | 18 | 21 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

On seed 42 it's 5 `hot_take` posts called `reaction`, with 3 going the other
way. Across all three seeds, though, the pattern is that **everything leaks
into `hot_take`**. 13 real `analysis` posts were called `hot_take` and only
5 went the other way. 18 real `reaction` posts were called `hot_take`. On
the boundary I cared most about, the model leans hard toward `hot_take`:
nearly half of true `analysis` posts (13 of 27) get read as an unsupported
opinion. `hot_take` is also my biggest label (43%), so it works as the
model's default when it isn't sure. `analysis` → `reaction` almost never
happens (2) and `reaction` → `analysis` never does (0), so the model has
learned that `analysis` is long and argumentative. What it hasn't learned
is whether the argument is backed by evidence.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 on every seed | MISSED | 0.605 / 0.500 / 0.553. No seed reached it, and the best was 4.5 points short |
| 2 | Per-label F1 | `analysis` ≥ 0.60, others ≥ 0.55, every seed | MISSED | `analysis` never reached 0.60 (best 0.588). `reaction` fell to 0.417 on seed 7, and `hot_take` to 0.541 on seed 2024 |
| 3 | Balance | no label > 50%, every label ≥ 45 | MET | `hot_take` 43% is the largest, and `analysis` 57 the smallest. A property of `labels.csv`, so it holds on every seed |
| 4 | `analysis` → `hot_take` | < 1 in 4 of true `analysis` | MISSED | 4/9, 5/9, 4/9, roughly double the allowed rate on every seed |
| 5 | Confidence gap | top third ≥ 0.15 more accurate than bottom third | MET | Gaps of +0.42, +0.33, +0.25. All clear 0.15, though the gap shrinks as the least-sure third gets luckier |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

<!-- TODO: add the agreement-report evidence once data/staff_labels.csv
     arrives and agreement.py has run. The diagnoses below use the evidence
     available so far. -->

**Criterion 4 (`analysis` → `hot_take`): a boundary applied inconsistently.**
The errors run one way: 13 `analysis` → `hot_take` against 5 the other way
across seeds. A genuinely hard pair would blur in both directions. My own
labels show the inconsistency directly. When I labelled 20 posts cold, I
called a post that uses the ages of past winners as evidence `hot_take`. I
called "the kinda shot you take in real life and sail it 20 yards over"
`analysis`, though it has no checkable evidence at all, and that post sits
in the test split as a gold `analysis`. The other 230 labels were
pre-labelled under a stricter reading of the same rule. So the training data
holds two versions of the `analysis` boundary, and the model learned roughly
"long and argumentative" rather than "backed by evidence".

**Criteria 1 and 2 (accuracy, per-label F1): too little data for a stable
measure, on top of the boundary above.** With 38 test posts, one post moves
accuracy by 2.6 points, and accuracy moved 10.5 points between seeds. With 9
`analysis` posts per test split, one post moves its F1 by about 0.06, so
0.533 → 0.588 across seeds is a single post. `reaction` swinging from 0.690
to 0.417 is the same story: 13 test posts, and on seed 7 eight of them were
called `hot_take`. Unlike the `analysis` boundary, `hot_take` ↔ `reaction`
fails in both directions: 18 one way and 13 the other across seeds, and 3 vs
5 on seed 42, which the notebook calls "roughly symmetric". That makes it a
**genuinely hard pair** rather than a one-sided labelling habit. A reaction
that carries a verdict ("Couldn't be more deserved, H.") is both things at
once, which is my hard case 3 again.

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

**What I changed:** I relabelled the `analysis`/`hot_take` boundary under
one test, applied the same way everywhere: *is there a checkable fact, and
does it carry the argument?* That is my own written rule, and it matches the
staff taxonomy's rule 1. I re-checked all 20 cold labels and the 29 rows
marked `borderline`, and changed 16:

- 3 moved to `analysis` because a fact really carries the claim: the ages of
  past winners, the Özil precedent, Mao calling himself a dictator.
- 11 moved from `analysis` to `hot_take`: no checkable fact, or a number used
  as decoration on a conclusion already reached. One example is "3-4 key
  defenses per Benzema goal" (my hard case 2, now relabelled).
- 2 moved from `analysis` to `reaction`: "you can tell it means a lot to
  him" and "the kinda shot you'd sail 20 yards over".

The changed rows are noted `cold, relabelled in unit 6` or `pre-labelled by
Claude, corrected`. New counts: `analysis` 47, `hot_take` 116 (46%),
`reaction` 87. Criterion 3 still holds, but `analysis` now sits just above
its floor of 45. Nothing else changed: same posts, same settings, same seeds.
Because the split is stratified on label, the test posts per seed shift a
little, so before/after are not scored on identical test sets.

**Which diagnosis pointed at it:** Criterion 4. The confusion matrix showed
`analysis` → `hot_take` errors running one way (13 vs 5 across seeds), the
signature of a boundary applied inconsistently rather than one that is
inherently hard. My own cold labels contained clear rule-breaks in both
directions. On the staff set I made the same mistake: I labelled "Times are
down about 3% since the shoe rules changed, so obviously the shoes are the
whole story" as `analysis`, when the staff taxonomy gives almost that exact
post as its example of `hot_take`. I was counting a number as evidence even
when it did no work in the argument.

### Run Log — After

Same settings (8 epochs, lr 2e-5, batch 16, CPU). Test split is now 38
posts per seed: 7 `analysis`, 18 `hot_take`, 13 `reaction`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 every seed | 0.737 | 0.658 | 0.684 | MET (was MISSED) |
| 2. Per-label F1 | `analysis` ≥ 0.60; `hot_take`, `reaction` ≥ 0.55 | a 0.615 · h 0.750 · r 0.783 | a 0.000 · h 0.698 · r 0.769 | a 0.462 · h 0.700 · r 0.783 | MISSED (`analysis` only) |
| 3. Balance | no label > 50%, every label ≥ 45 | 46% max, 47 min | same data | same data | MET |
| 4. `analysis` → `hot_take` | < 1 in 4 true `analysis` | 3 / 7 | 7 / 7 | 4 / 7 | MISSED (worse) |
| 5. Confidence gap | top third ≥ 0.15 above bottom third | 0.833 vs 0.500 (+0.33) | 0.917 vs 0.250 (+0.67) | 0.750 vs 0.750 (+0.00) | MISSED (was MET) |

Macro F1: 0.716 / 0.489 / 0.648 (before: 0.595 / 0.489 / 0.558). Accuracy
spread across seeds: 0.079 (before: 0.105).

Summed confusion matrix, all three seeds after:

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 7 | 14 | 0 |
| **hot_take** | 5 | 44 | 5 |
| **reaction** | 0 | 11 | 28 |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

Overall yes, but not where I aimed it. Accuracy now clears 0.65 on every
seed, and `hot_take` and `reaction` F1 clear their bars on every seed.
`hot_take` ↔ `reaction` errors fell from 31 to 16 across seeds, and the
seed-to-seed spread narrowed. But the boundary I was trying to fix got
**worse**. On seed 7 the model never predicted `analysis` at all (F1 0.00,
all 7 called `hot_take`), and `analysis` → `hot_take` is now 14 of 21
across seeds, against 13 of 27 before.

I think this is why. Making the rule stricter moved 11 posts out of
`analysis` and into `hot_take`. That left `analysis` with only 47 examples
(about 33 in training) and made `hot_take` an even bigger default (46%).
Part of the accuracy gain is just that the test split now holds more
`hot_take` posts (18 of 38), and those are easy to get right by leaning that
way. Criterion 5 also fell: on seed 2024 the confident and unsure thirds
were equally accurate. The labels are cleaner, but the label I care about
is now too thin to learn. So the relabel fixed the consistency problem
without fixing the data problem behind it.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**Criterion 2 (`analysis` F1) and criterion 4 (`analysis` → `hot_take`).**
Both come down to `analysis` being too rare. 47 examples, 7 in each test
split, and one seed where the model gave up on the label entirely. The fix
I'd make next is more `analysis` data, not more relabelling: another 40-50
posts from tactical and match-analysis threads (r/soccer post-match threads,
or club subs like r/reddevils), labelled under the same strict rule. Class
weights in training would be a quicker second option, so that missing an
`analysis` post costs more than missing a `hot_take`. I stopped because
each three-seed run is about 30 minutes on CPU, and collecting and labelling
another batch didn't fit in the time I had.

**Criterion 5 (confidence gap).** It missed on one seed, where the gap was
exactly 0.00. With 12 posts per third, a gap of 0.15 is about two posts, so
this criterion is very sensitive to the split. I'd test it on a bigger test
set before trusting either the earlier MET or this MISSED.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `analysis` to mean "an argument that a checkable fact carries", but
the model learned something closer to "long and argumentative, otherwise
`hot_take`". `analysis` is never confused with `reaction` (0 both ways), yet
14 of 21 real `analysis` posts were called `hot_take`. Without enough
examples, the difference between "uses a fact" and "just argues" is the one
thing it can't see.



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
