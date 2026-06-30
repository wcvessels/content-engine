# SOP lane rules (ANCHOR): extract steps, owners, decisions, risks; zero inference

This file is the SOP lane's structuring ANCHOR: the zero-inference thesis and the prose contract behind the stages. The lane is WIRED (it has its own `stages/01-ingest .. 05-qa`), and a shipped public example, a Ramp manager onboarding SOP rendered from a public Ramp training video, lives in `../../../samples/` (`ramp-manager-onboarding`). It still proves the factory thesis: a new doc type is two stages of difference over identical 01/04/05 plumbing.

These rules are now wired into loadable homes: the taxonomy + ordering live in `../stages/02-structure/references/sop-extraction.md`, and the output structure in `../stages/03-layout/references/sop-doc-structure.md`. This anchor is the thinking behind those two files. Everything 01/04/05 (ingest, render, QA) is the SHARED template, unchanged from the educational lane.

## What this lane is

It turns a recorded process walkthrough (a screen-share of someone doing a task) into a step-by-step Standard Operating Procedure: numbered actions, who owns each, the decisions made along the way, and the risks to watch. The reader is an operator or new hire who needs to repeat the process correctly.

## The one rule that defines this lane: ZERO structural inference

This is the deepest difference from the educational lane and the reason the SOP lane exists as a separate specialization. An SOP makes FACTUAL ASSERTIONS: this step happens, this person owns it, this branch was chosen. A reader will ACT on those. So the lane infers nothing about content. If the source did not state it, the SOP does not claim it; it surfaces the gap instead.

Contrast with educational: a learning guide may infer ORDER (concept B uses a term concept A defined, so A comes first) because reordering is not a content claim. An SOP may not even do that on content. The asymmetry:

- A learning path can be reordered by an inferred dependency without asserting anything false.
- An SOP step, owner, or branch IS the assertion. Inferring one would put a false instruction in front of someone about to follow it.

So: educational has `inferred:true` items (structural prerequisites, synthesized objectives). The SOP lane has ZERO `inferred:true` content entries. The fidelity audit (`_standards/qa-bar.md` item 6) checks exactly this.

## Stage 02 extraction: the typed items

Pull these typed items from the transcript. Each records: type, a one-line normalized statement, source segment indices (the provenance anchor), and any `frame_index`.

| Type | What it is | The hard rule |
|---|---|---|
| Step | a single executable action ("click Export", "set the date range") | the FINAL stated version only (see reversals below) |
| Decision point | a branch the operator may hit ("if the total is over $X, route to approval") | only the SIDES the speaker stated; missing sides become Open questions, never invented |
| Owner | who performs a step | only where NAMED; otherwise "unassigned (clarify)". NEVER infer from who was speaking |
| Risk or gotcha | a stated warning, failure mode, or "watch out" | stated-only |
| Reference | a tool, doc, or link the recording pointed to | stated-only |
| Prerequisite | something needed before starting | stated-only, else "Not stated in source" |
| Purpose | why this procedure exists | stated-only, else "Not stated in source" |
| Scope bound | what the procedure does and does not cover | stated-only, else "Not stated in source" |
| Open question | a gap the reader genuinely needs filled | reader-facing on purpose; an honest gap is information |

Significance filter (the keep-or-cut test): keep a segment only if cutting it would lose a step, decision, owner, risk, reference, prerequisite, purpose, scope bound, or a real open question. Drop greetings, "let me share my screen", scheduling, tangents, and pure agreement.

## Reversal handling (a step that gets redone)

People change their minds mid-walkthrough: "actually, no, do it this way instead." The rule:

- The FINAL stated version is the step.
- The abandoned version is recorded INTERNALLY in the provenance sidecar only, never shown to the reader.

A reader following the SOP must see the one correct path, not the speaker's false starts. The audit (qa-bar item 7) checks that reversals were captured this way: final version present, abandoned versions absent from the reader doc.

## Decisions, not proposals

Only DECIDED actions become steps. If the speaker floated an idea but did not commit ("we could maybe also..."), it is not a step. For a decision point, only the branch sides actually stated appear; any side the speaker left open becomes an Open question, not a guessed branch.

## Procedure ordering (the ordering rule)

Order steps by the STATED process order: the sequence the speaker actually performed or described. Fall back, in order, to:

1. Stated process order (what the speaker did, in the order they did it).
2. Dependency order (step B clearly cannot happen before step A completes), where the dependency is itself stated or physically necessary.
3. Transcript order, with an `order not stated` flag on the affected steps.

Steps whose order was never stated carry an internal `order not stated` flag so the audit and the reader-facing doc can be honest about sequence (qa-bar item 10).

## Stage 03 output structure (reader-facing, citations stripped to the sidecar)

The finished SOP document, in order. Empty sections carry their stated fallback line, never silence.

1. Title.
2. Purpose (stated-only; else "Not stated in source").
3. Scope (stated-only; else "Not stated in source").
4. Roles and owners (named only).
5. Prerequisites (stated-only; else "None stated").
6. Procedure: numbered steps, each = action + owner + the screenshot from its `frame_index`; unstated-order steps internally flagged.
7. Decision points (stated sides only).
8. Risks and gotchas.
9. References and links.
10. Open questions (READER-FACING: the honest gaps; the pointer that backs each gap lives in the sidecar).

No citations, timestamps, or speaker tags anywhere in the reader doc. Footer and disclaimer come from `_config`.

## What is identical to the educational lane (the shared shelf)

Everything except the two stages above:

- Stages 01-ingest, 04-render, 05-qa: the shared template, unchanged.
- The deterministic-segment-then-typed-extract split.
- The significance-filter mechanism (only the keep-criteria differ).
- The `frame_index` / `timestamp_s` screenshot-placement machinery and the shared crop rule (`_skills/render-doc/frame-crop.md`).
- The provenance sidecar plus the 16-item fidelity audit (`_standards/qa-bar.md`).
- The "clean reader surface, grounding internal" rule.
- The brand, voice, design system, and renderer.

That is the factory thesis made concrete: a whole second deliverable type is exactly two reference files of difference.

House rule: zero em dash characters.
