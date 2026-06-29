# Stage 02: Structure (educational-guide) [SPECIALIZATION POINT]

Sequence concepts into a guided learning path.

Turn the deterministically-segmented source into typed, significant, ordered items with internal provenance. The SHAPE of this stage is fixed; this lane supplies the extraction taxonomy and the ordering rule via `references/`.

## Inputs

- `../01-ingest/output/ingest/` (segments.json, source.json, frames/).
- Load: `references/concept-extraction.md` (the canonical taxonomy home) + `references/dependency-ordering.md` (the topo-sort/learning-path rule); `../../../../_config/audience-defaults.md`.
- Do NOT load: `_config/brand`, `design-system.md`, `render-prefs.md`; the render skills; stages 03/04/05.

## Process (skeleton, fixed)

1. Read segments (already segmented by the engine; structure comes from the source, never memory).
2. Extract typed items per `references/concept-extraction.md` (concept / procedure / example / fact-constraint / pitfall / objective-signal). [SPECIALIZATION]
3. Significance filter: drop greetings, "let me share my screen", scheduling, tangents, pure agreement. Test: "if I cut this, does the learner miss a concept/procedure/fact/example/pitfall?" (thresholds in `../../lane-config.md`).
4. Tag every kept item with internal provenance `[ref: seg N, t=HH:MM:SS, frame N]` (working artifact only, never reader-facing).
5. Order items into a learning path per `references/dependency-ordering.md`: build the prerequisite graph, topo-sort (no back-edges), group into foundations-first modules, attach 1-3 action-verb objectives per module. Mark any structural prerequisite or synthesized objective `inferred:true` in the sidecar. [SPECIALIZATION]
6. [Checkpoint] present typed items + the ordered module spine.
7. Audit; revise on fail. Save the spine + the partial provenance sidecar.

## Checkpoints

After step 5: typed items + the ordered learning path. Human decides items, types, module grouping, order. Ask: anything missing, mis-typed, out of order, or a wrong inferred prerequisite?

## Audit

- Typed coverage: every major topic yields at least one item; every significant concept lands in exactly one module.
- Significance held: no chatter survived.
- Provenance: every item points at a real segment/frame.
- Dependency order honest: the topo-sort has no back-edges. [SPECIALIZATION]
- Objectives are action verbs; synthesized ones flagged `inferred:true`; structural prerequisites flagged `inferred:true`.

## Outputs

`output/{slug}-structure.md` (typed items + ordered modules, internal `[ref]` tags) + `output/{slug}-provenance.json` (item-level, seeds the sidecar).
