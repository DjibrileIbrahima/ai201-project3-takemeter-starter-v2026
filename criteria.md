# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

**Overall accuracy of at least 0.65 on the held-out test split, on every one
of the three seeds.**

**Why this target:**

Three labels means a guesser gets about 0.33, so 0.65 is roughly double chance.
With a test split of only about 30 posts, a single post moves accuracy by about
3 points, so I set this below what I'd hope for on an average seed so that one
unlucky split doesn't decide it.


---

## 2.

<!-- Your criterion. -->

**`hot_take` and `reaction` each have an F1 of at least 0.55, and `analysis`
an F1 of at least 0.60, on every seed.**

**Why this target:**

`analysis` posts have the most distinctive wording (formations, stats, "because"),
so I expect it to be the easiest to learn. `hot_take` and `reaction` are
both short, opinionated posts, and with roughly 10 of each in the test split
their F1 will jump between seeds, so their bar is looser.


---

## 3.

<!-- Your criterion. -->

**No label makes up more than 50% of `labels.csv`, and no label has fewer
than 45 examples.**

**Why this target:**

Match threads are full of short `reaction` posts, so this
is the label most likely to swamp the others. Below about 45 examples a label
lands only 6 or 7 posts in the test split, which is too few to give a stable F1.


---

## 4.

<!-- Your criterion. -->

**Fewer than 1 in 4 true `analysis` posts in the test split are predicted
as `hot_take`, on every seed.**

**Why this target:**

`analysis` vs `hot_take` is my hardest boundary: both make a claim, and the
only difference is whether the post explains how its evidence supports it. A
post that just names a player or formation looks like analysis but isn't. If
the model misses this boundary, it hasn't learned my main distinction.


---

## 5.

<!-- Your criterion. -->

**The model's most confident third of test predictions is at least 0.15
more accurate than its least confident third, on every seed.**

**Why this target:**

I expect the obvious cases (a one-line "What a goal!" or a detailed tactical
breakdown) to be easy and the borderline `analysis`/`hot_take` posts to be
hard. If confidence doesn't separate those, the model's confidence scores
can't be used to flag posts for a human to check.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
