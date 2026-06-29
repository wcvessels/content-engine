# Concept extraction: the typed taxonomy (CANONICAL home)

This file is the single source of truth for WHAT the educational lane pulls out of a recording. The lane CLAUDE.md, the §4.6 specialization slot, and `../../../reference/rules.md` all NAME this taxonomy and point here; they do not restate the type list.

## The item types

Every kept item is exactly one of these:

| Type | What it is | Attaches to | Reader role |
|---|---|---|---|
| **Concept** | a thing the learner must understand | stands alone | explained in prose |
| **Procedure** | a how-to that was demonstrated | a concept (usually) | numbered steps |
| **Example** | a worked case that illustrates a concept | a concept | inline illustration |
| **Fact / constraint** | a stated rule, limit, number, or default | a concept/procedure | stated plainly, often a callout |
| **Pitfall** | a "watch out" tied to a concept or procedure | a concept/procedure | a "Watch out:" callout |
| **Objective signal** | an explicit "by the end you'll be able to..." | a module | seeds the module objective |

Unknown or ambiguous talk that does not fit a type is NOT forced into one; it either fails the significance filter (chatter) or is surfaced at the checkpoint for the human to type.

## What each item records

- `type` (one of the six above)
- a **one-line normalized statement** (plain English, the claim itself, no transcript verbatim)
- `source_segments`: the segment indices it came from (the provenance anchor; every item MUST have at least one)
- `frame_index`: the frame it maps to, or null
- `inferred`: almost always `false` at extraction time. Only an ordering/objective decision later (see `dependency-ordering.md`) sets `true`. Extraction never invents a fact.

## The significance filter (the keep test)

Promote a segment to an item ONLY if cutting it would cost the learner a concept, procedure, fact/constraint, example, or pitfall. Reliably DROP:

- greetings, sign-offs, "can you hear me", "let me share my screen"
- scheduling, logistics, "we'll cover that next week"
- tangents and war stories with no transferable lesson
- pure agreement / acknowledgement ("yep", "exactly", "makes sense")
- filler and self-correction that lands on the same claim

Borderline calls (a near-objective, a half-stated prerequisite) are KEPT and flagged for the stage-02 checkpoint, never silently cut.

## Prerequisite extraction (two signals)

- **Stated**: "before this you need X" -> recorded as a prerequisite, cited to the segment, `inferred:false`.
- **Structural**: module B uses a term module A defined earlier -> recorded as a prerequisite with `inferred:true`. This is the ONLY inference the lane permits, and it is an ORDERING decision, never a new sentence in the reader doc (full rationale: `dependency-ordering.md`).

## Objective signals

Prefer a stated "by the end you'll be able to..." as a module objective. If a module clearly teaches a capability but no objective was stated, a synthesized objective is allowed, phrased as an action verb and marked `inferred:true`. A synthesized objective restates what the module already teaches; it never promises something the recording did not cover.
