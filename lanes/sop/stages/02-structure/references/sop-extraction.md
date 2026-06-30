# SOP extraction taxonomy + ordering (the loadable 02 detail)

This is what stage 02-structure loads to turn the segmented transcript into typed, significant, ordered items with internal provenance. The lane's thesis (zero content inference) lives in `../../../reference/rules.md`; this file is the operational detail.

## The one rule that defines this lane: ZERO structural inference

An SOP makes FACTUAL ASSERTIONS a reader will act on (this step happens, this person owns it, this branch was chosen). So the lane infers nothing about content. If the source did not state it, the SOP does not claim it; it surfaces the gap instead. Contrast educational, which may infer ORDER. An SOP may not even do that on content: every `inferred:true` content entry is forbidden here (qa-bar item 6 checks this).

## The typed items

Pull these from the transcript. Each records: type, a one-line normalized statement, source segment indices (the provenance anchor), and any `frame_index`.

| Type | What it is | The hard rule |
|---|---|---|
| Step | a single executable action ("click Export", "set the date range") | the FINAL stated version only (see reversals) |
| Decision point | a branch the operator may hit ("if over $X, route to approval") | only the SIDES the speaker stated; missing sides become Open questions, never invented |
| Owner | who performs a step | only where NAMED; otherwise "unassigned (clarify)". NEVER infer from who was speaking |
| Risk or gotcha | a stated warning, failure mode, or "watch out" | stated-only |
| Reference | a tool, doc, or link the recording pointed to | stated-only |
| Prerequisite | something needed before starting | stated-only, else "Not stated in source" |
| Purpose | why this procedure exists | stated-only, else "Not stated in source" |
| Scope bound | what the procedure does and does not cover | stated-only, else "Not stated in source" |
| Open question | a gap the reader genuinely needs filled | reader-facing on purpose; an honest gap is information |

## Significance filter

Keep a segment only if cutting it would lose one of the typed items above. Drop greetings, "let me share my screen", scheduling, tangents, and pure agreement.

## Reversal handling (a step that gets redone)

People change their minds mid-walkthrough ("actually, no, do it this way"). The rule: the FINAL stated version is the step; the abandoned version is recorded INTERNALLY in the provenance sidecar only, never shown to the reader (qa-bar item 7).

## Decisions, not proposals

Only DECIDED actions become steps. If the speaker floated an idea but did not commit ("we could maybe also..."), it is not a step. For a decision point, only the branch sides actually stated appear; any side left open becomes an Open question.

## Procedure ordering

Order steps by the STATED process order: the sequence the speaker actually performed or described. Fall back, in order, to:

1. Stated process order (what the speaker did, in the order they did it).
2. Dependency order (step B clearly cannot happen before step A completes), where the dependency is stated or physically necessary.
3. Transcript order, with an `order not stated` flag on the affected steps (qa-bar item 10).

House rule: zero em dash characters.
