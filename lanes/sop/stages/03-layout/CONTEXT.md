# Stage 03: Layout (sop) [SPECIALIZATION POINT]

Lay the procedure out as one reader-ready doc-model.

Turn the ordered procedure into ONE doc-model that all targets consume. The doc-model schema and the frame-placement/crop mechanic are fixed; this lane supplies the section/document shape via `references/`.

## Inputs

- `../02-structure/output/` (the procedure + item-level provenance).
- `../01-ingest/output/ingest/frames/` (the copied in-bundle frames).
- Load: `references/sop-doc-structure.md` (the lane document shape) **[SPEC]**; `../../../../_config/voice.md`; `../../../../_config/design-system.md` (TOC depth + heading hierarchy ONLY; brand colors/fonts are applied at 04); `../../../../_standards/doc-model-schema.md`; `../../../../_skills/render-doc/frame-crop.md`.
- Do NOT load: `_config/brand` (brand is filled at render, so the doc-model stays reusable); the render skills + the engine; `../01-ingest/references/`; stages 04/05.

## Process (skeleton, fixed)

1. Read the procedure + the lane doc-structure (`references/sop-doc-structure.md`).
2. Write the title-page meta block (`meta.doc_type=procedure`; `meta.author` filled by Stage 04 from `_config`; do NOT hardcode brand here).
3. Write reader-facing prose per section in the configured voice. Plain English, NO `[HH:MM:SS]` in visible text. [SPECIALIZATION] section shape: Purpose, Scope, Roles, Before you start, the Procedure (numbered steps grouped into level-2 tasks), Decision points, Risks, References, Open questions.
4. Place screenshots: pick the frame that ACTUALLY SHOWS the step's screen (confirm the frame; narration and on-screen view can drift in a fast walkthrough), emit a `screenshot` block. **CROP (D6):** apply `../../../../_skills/render-doc/frame-crop.md`; remove a webcam/participant tile ONLY if it cuts no relevant content; otherwise null; when unsure keep the full frame.
5. Keep the internal `[ref]` tag on each block (Stage 04 strips it to the sidecar).
6. [Checkpoint] present the assembled doc-model outline (sections + figure placements + crop decisions).
7. Audit; revise. Save the doc-model + extend the provenance sidecar to block/screenshot level.

## Checkpoints

After step 5/6: the doc-model outline. Human steers structure, step density, image choices, and which gaps surface as Open questions. Ask: right sections, right images, honest about what was not stated?

## Audit

- Schema valid against `docmodel-1.0` (`../../../../_standards/doc-model-schema.md`).
- Clean prose: zero `[HH:MM:SS]` / `[ref]` in any reader field.
- Figure validity: every `frame_index` resolves; the placed frame matches the step it sits under; every `crop` is in range.
- Voice compliance: reading level + NO em dashes.
- SOP structure honored (Purpose..Open questions); empty sections carry their fallback line. [SPECIALIZATION]
- Block-level provenance complete; zero inferred content entries.

## Outputs

`output/{slug}-docmodel.json` (the one intermediate) + `output/{slug}-provenance.json` (extended to block/screenshot level) + `output/{slug}-preview.md` (readable preview for the checkpoint).
