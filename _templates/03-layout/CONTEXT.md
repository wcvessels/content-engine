# Stage 03: Layout ({{LANE_NAME}}) [SPECIALIZATION POINT]

{{LANE_03_ONE_LINER}}

Turn the ordered spine into ONE doc-model that all targets consume. The doc-model schema and the frame-placement mechanic are fixed; the lane supplies the section/document shape via `references/`.

## Inputs

- `../02-structure/output/` (the spine + item-level provenance).
- `../01-ingest/output/ingest/frames/` (the copied in-bundle frames).
- Load: `references/{{LANE_DOC_STRUCTURE_FILE}}` (the lane document shape); `_config/voice.md`; `_config/design-system.md` (TOC depth + heading hierarchy ONLY; brand colors/fonts are applied at 04); `_standards/doc-model-schema.md`; `_skills/render-doc/frame-crop.md` (the shared crop rule).
- Do NOT load: `_config/brand` (brand is filled at render, not layout, so the doc-model stays reusable); the render skills + the engine; `../01-ingest/references/`; stages 04/05.

## Process (skeleton, fixed)

1. Read the spine + the lane doc-structure.
2. Write the title-page meta block (brand fields filled by Stage 04; do NOT hardcode brand here).
3. Write reader-facing prose per section in the configured voice. Plain English, NO `[HH:MM:SS]` in visible text. [SPECIALIZATION] per-section shape.
4. Place screenshots: pick the best `frame_index` per section (sharpest via `frames[].sharpness` unless distinct screens), emit a `screenshot` block. Set `crop` + `crop_reason` per the shared rule in `_skills/render-doc/frame-crop.md` (remove a webcam/participant tile only if it does not cut relevant content; else null; when unsure keep the full frame).
5. Keep the internal `[ref]` tag on each block (Stage 04 strips it to the sidecar).
6. [Checkpoint] present the assembled doc-model outline (sections + figure placements + crop decisions).
7. Audit; revise. Save the doc-model + extend the provenance sidecar to block/screenshot level.

## Checkpoints

After step 5/6: the doc-model outline. Human steers structure, density, image choices, and crops. Ask: right sections, images, order, density?

## Audit

- Schema valid against `docmodel-1.0`.
- Clean prose: zero `[HH:MM:SS]` / `[ref]` in any reader field.
- Figure validity: every `frame_index` resolves; every `crop` is in range (else treated as null).
- Voice compliance: reading level + NO em dashes.
- Section template honored. [SPECIALIZATION]
- Block-level provenance complete.

## Outputs

`output/{slug}-docmodel.json` (the one intermediate) + `output/{slug}-provenance.json` (extended to block/screenshot level) + `output/{slug}-preview.md` (readable preview for the checkpoint).
