# SOP lane examples (ANCHOR) + the S1-S5 delta vs educational

Two things here: a worked example of one good SOP section (the few-shot a wired SOP lane's stages 02/03 would calibrate against), and a one-page prose description of exactly how this lane differs from the educational lane at each of the five specialization points. Together they prove that a second lane is a thin, legible specialization, not a fork.

The SOP lane is DOC-ONLY for this submission (see `rules.md`). It can be proven LOCALLY end to end by running the shared stages over a real process recording (a Ramp screen-capture, say), but that rendered SOP is private employer content and is NEVER committed to this repo. The shipped public samples are educational guides from public videos. This page is the public proof of the pattern.

## Worked example: one Procedure section, done right

Source (paraphrased transcript): a teammate shares their screen and says "OK so to submit an expense, first you hit New in the top right. Then, actually wait, no, go to the Expenses tab first, then New. Pick the category, upload the receipt. If it is over five hundred bucks it needs Dana's approval, otherwise it just auto-submits. I am not sure what happens if there is no receipt, we should check that."

What Stage 02 extracts (typed items, internal provenance shown for illustration; never reader-facing):

- Step: "Open the Expenses tab" `[ref: seg 12, t=00:01:40]`
- Step: "Click New (top right)" `[ref: seg 12, t=00:01:44]` (NOTE: the speaker first said New, then corrected to Expenses-tab-first; the abandoned order is recorded in the sidecar only)
- Step: "Pick the category" `[ref: seg 13, t=00:01:51, frame 4]`
- Step: "Upload the receipt" `[ref: seg 13, t=00:01:55, frame 5]`
- Decision point: "If over $500, route to Dana for approval; otherwise auto-submit" `[ref: seg 14, t=00:02:03]`
- Owner: Dana (approver, NAMED) `[ref: seg 14]`
- Open question: "What happens when there is no receipt?" `[ref: seg 15, t=00:02:10]` (the speaker flagged it unresolved)

What Stage 03 renders (reader-facing, clean, no citations):

> ### Procedure
>
> 1. Open the Expenses tab.
> 2. Click New (top right).
> 3. Pick the category. ![category screen](frame 4)
> 4. Upload the receipt. ![upload screen](frame 5)
>
> Decision point: if the expense is over $500, it routes to Dana for approval. Otherwise it auto-submits.
>
> (Later, in Open questions:) What happens if an expense has no receipt? Not covered in the recording; confirm before relying on this procedure.

Why this is correct:

- The reversal was handled: the corrected order (Expenses tab first) is the step; the abandoned "New first" is in the sidecar, invisible to the reader.
- The owner (Dana) appears only because she was named. No other owner was invented from who was talking.
- The decision shows only the two stated sides ($500 threshold); no third branch was guessed.
- The no-receipt gap became a reader-facing Open question, not a silently filled assumption. An honest gap is information the reader needs.
- Zero timestamps, refs, or speaker tags survive into the reader text.

## The S1-S5 delta vs the educational lane (one page)

The five specialization points are the ONLY places the SOP lane differs. Everything else (stages 01/04/05, the renderer, brand, voice, design, the schema, the fidelity audit) is the shared shelf, byte-for-byte identical.

| # | Slot | Educational guide | SOP (this lane) |
|---|---|---|---|
| S1 | Lane config (`lane-config.md`) | `doc_type=guide`; reader = "learner, low prior knowledge" | `doc_type=procedure`; reader = "operator or new hire" |
| S2 | 02 taxonomy (`02-structure/references/...`) | Concept / Procedure / Example / Fact-or-constraint / Pitfall / Objective-signal | Step / Decision-point / Owner / Risk-or-gotcha / Reference / Prerequisite / Purpose / Scope-bound / Open-question |
| S3 | 02 ordering rule | DEPENDENCY order: topo-sort the prerequisite graph into modules, foundations first; MAY infer structural order (flagged `inferred:true`), never new content | PROCEDURE order: stated sequence, fall back to dependency then transcript order with an `order not stated` flag; ZERO content inference |
| S4 | 03 doc shape (`03-layout/references/...`) | per module: objective -> concept -> example -> screenshot; pitfalls as callouts | per step: numbered action -> owner -> expected result -> decision/risk callout -> screenshot |
| S5 | The 02/03 one-liners | "Sequence concepts into a guided learning path." | "Order actions into an executable procedure." |

The single deepest difference is S3, the inference posture. The educational lane sequences and may infer order; the SOP lane asserts facts and infers nothing on content. That one choice ripples into the taxonomy (S2: SOP adds Owner, Decision-point, Open-question, all stated-only), the output structure (S4: SOP surfaces Open questions to the reader), and the audit emphasis (qa-bar items 4, 6, 9, 10 bite hardest on an SOP).

## How a reader of this repo can verify the thesis

1. Read the educational lane's `reference/rules.md` and this file's S1-S5 table side by side: the difference is two stages.
2. Note that neither lane re-declares brand, voice, the renderer, or the schema; both point at the shared shelf.
3. Conclude: adding a third lane (release notes, a KB article) is the same shape of work, which is what `_lane-builder/` documents.

## Proving it locally (private, not committed)

To prove the SOP lane truly runs (not just reads well), point the shared stages at a real process recording locally: stamp the lane from `_templates/` per `_lane-builder/README.md`, write the two reference files from `rules.md`, run 01->05. A Ramp expense-flow screen-capture works well as a private test. The rendered SOP stays on your machine; it is confidential and must never enter this public repo. The public proof is this prose plus the educational-guide samples.

House rule: zero em dash characters.
