# Dependency ordering: the learning-path rule (CANONICAL home)

How the educational lane turns a bag of typed items into an ordered, foundations-first learning path. This is the lane's ordering rule (specialization slot S3). The taxonomy of WHAT gets ordered lives in `concept-extraction.md`; this file is HOW it gets ordered.

## The goal

A learner should never hit a term, tool, or step that depends on something not yet taught. The path is correct when, reading top to bottom, every prerequisite has already appeared.

## The algorithm

1. **Build the prerequisite graph.** Nodes are items (mostly concepts and procedures). Add a directed edge A -> B ("A is a prerequisite of B") for each:
   - **Stated** prerequisite: the speaker said "before B you need A" (`inferred:false`).
   - **Structural** prerequisite: B uses a term, tool, or result that A defines or produces, and A was not already obviously known (`inferred:true`).
2. **Topo-sort** the graph so every prerequisite precedes its dependents. The sort MUST have no back-edges; a cycle means two items were mis-typed or one edge is wrong, fix it, do not break the cycle arbitrarily.
3. **Group into modules.** A module is one cluster that teaches one capability. Within a module, order items: concept -> examples -> procedures -> pitfalls.
4. **Order modules foundations-first**, following the topo-sorted dependency order across modules.
5. **Attach objectives.** 1 to 3 per module, each starting with an action verb (configure, create, troubleshoot...). Prefer stated objective signals; mark synthesized objectives `inferred:true`.

## The inference boundary (why structural ordering is allowed)

Reordering modules by an inferred dependency is an **ordering** decision, not a **content** claim. It changes the sequence the reader meets ideas in; it does NOT add a sentence the speaker never said. That is the asymmetry that separates this lane from the SOP lane (where step/owner/branch are factual assertions and inference is banned).

Rules that keep the boundary honest:

- Every inferred edge is recorded in the provenance sidecar as `inferred:true` with a one-line `inference_note` (e.g. "module 3 uses 'workspace', defined in module 1").
- An inferred prerequisite NEVER becomes reader-facing prose on its own. If the structural dependency is worth telling the reader, phrase it gently in the Prerequisites section ("you'll get more from this if you already know X"), and that sentence still traces to the segment where X was taught, not to thin air.
- If items genuinely have no dependency between them, keep the transcript order; do not invent an ordering to look clever.

## Audit hooks (stage 02 checks this produces)

- topo-sort has no back-edges (the "dependency order honest" check)
- every significant concept is in exactly one module (coverage)
- objectives are action verbs; synthesized ones and structural prerequisites are flagged `inferred:true`
- every item still points at a real segment after ordering (provenance survives the reshuffle)
