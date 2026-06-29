# Stage 02: Structure ({{LANE_NAME}}) [SPECIALIZATION POINT]

{{LANE_02_ONE_LINER}}

Turn the deterministically-segmented source into typed, significant, ordered items with internal provenance. The SHAPE of this stage is fixed; the lane supplies the extraction taxonomy and ordering rule via `references/`.

## Inputs

- `../01-ingest/output/ingest/` (segments.json, source.json, frames/).
- Load: `references/{{LANE_TAXONOMY_FILE}}` (the canonical taxonomy + ordering home); `_config/audience-defaults.md`.
- Do NOT load: `_config/brand`, `design-system.md`, `render-prefs.md`; the render skills; stages 03/04/05.

## Process (skeleton, fixed)

1. Read segments (already segmented by the engine; structure comes from the source, never memory).
2. Extract typed items per the lane taxonomy in `references/{{LANE_TAXONOMY_FILE}}`. [SPECIALIZATION]
3. Significance filter: drop greetings, "let me share my screen", scheduling, tangents, pure agreement. Test: "if I cut this, does the reader miss something they need?"
4. Tag every kept item with internal provenance `[ref: seg N, t=HH:MM:SS, frame N]` (working artifact only, never reader-facing).
5. Order items into the document spine per the lane ordering rule. [SPECIALIZATION]
6. [Checkpoint] present typed items + ordered spine.
7. Audit; revise on fail. Save the spine + the partial provenance sidecar.

## Checkpoints

After step 5: typed items + ordered spine. Human decides items, types, order. Ask: anything missing, mis-typed, or out of order?

## Audit

- Typed coverage: every major topic yields at least one item.
- Significance held: no chatter survived.
- Provenance: every item points at a real segment/frame.
- Ordering rule honored. [SPECIALIZATION]

## Outputs

`output/{slug}-structure.md` (typed items + ordered sections, internal `[ref]` tags) + `output/{slug}-provenance.json` (item-level, seeds the sidecar).
