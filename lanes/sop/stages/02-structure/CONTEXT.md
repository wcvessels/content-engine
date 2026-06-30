# Stage 02: Structure (sop) [SPECIALIZATION POINT]

Order actions into an executable procedure.

Turn the deterministically-segmented source into typed, significant, ordered items with internal provenance. The SHAPE of this stage is fixed; this lane supplies the extraction taxonomy and the ordering rule via `references/`.

## Inputs

- `../01-ingest/output/ingest/` (segments.json, source.json, frames/).
- Load: `references/sop-extraction.md` (the taxonomy + ordering + zero-inference rule) **[SPEC]**; `../../reference/rules.md` (the lane thesis); `../../../../_config/audience-defaults.md`; `../../lane-config.md` (significance thresholds).
- Do NOT load: `_config/brand`, `design-system.md`, `render-prefs.md`; the render skills; stages 03/04/05.

## Process (skeleton, fixed)

1. Read segments (already segmented by the engine; structure comes from the source, never memory).
2. Extract typed items per `references/sop-extraction.md` (step / decision-point / owner / risk / reference / prerequisite / purpose / scope-bound / open-question). [SPECIALIZATION]
3. Significance filter: drop greetings, screen-share preamble, scheduling, tangents, pure agreement. Test: "if I cut this, does the operator lose a step, decision, owner, risk, or a real gap?"
4. Tag every kept item with internal provenance `[ref: seg N, t=HH:MM:SS, frame N]` (working artifact only, never reader-facing).
5. Order steps by STATED process order; fall back to stated/physical dependency, then transcript order with an `order not stated` flag. ZERO content inference: owners named-only, decision sides stated-only, reversals keep the final version (abandoned version to the sidecar only). [SPECIALIZATION]
6. [Checkpoint] present typed items + the ordered procedure.
7. Audit; revise on fail. Save the structure + the partial provenance sidecar.

## Checkpoints

After step 5: typed items + the ordered procedure. Human decides items, types, order, and which gaps are real Open questions. Ask: anything missing, mis-typed, an invented owner/branch, or an out-of-order step?

## Audit

- Typed coverage: every stated step/decision/owner/risk yields an item; chatter dropped.
- Provenance: every item points at a real segment/frame.
- ZERO inference: no `inferred:true` content entry exists. [SPECIALIZATION]
- Owners named-only; decision points carry only stated sides; unstated-order steps flagged.
- Reversals: final version kept, abandoned version absent from the reader-facing set.

## Outputs

`output/{slug}-structure.md` (typed items + ordered procedure, internal `[ref]` tags) + `output/{slug}-provenance.json` (item-level, seeds the sidecar).
