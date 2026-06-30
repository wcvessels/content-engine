# SOP document structure (the loadable 03 detail)

This is the reader-facing shape stage 03-layout lays the typed items into, as one `docmodel-1.0` (`../../../../_standards/doc-model-schema.md`). Citations are stripped to the sidecar at 04; nothing reader-facing carries a timestamp, ref, or speaker tag.

## Section order

The finished SOP, in order. An empty section carries its stated fallback line, never silence.

1. Purpose (stated-only; else "Not stated in source").
2. Scope (stated-only; else "Not stated in source").
3. Roles and owners (named only).
4. Before you start (Prerequisites; stated-only; else "None stated").
5. The procedure: numbered steps, each = action + owner (where named) + the screenshot from its `frame_index`; unstated-order steps internally flagged. Group multi-task procedures into level-2 sub-sections, one per task, in the stated order.
6. Decision points (stated sides only).
7. Risks and things to watch.
8. References and tools mentioned.
9. Open questions (READER-FACING: the honest gaps; the pointer that backs each gap lives in the sidecar).

## The per-step shape

Per procedure task: a one-line action list (ordered), the owner where named, a `note`/`warning` callout for a stated gotcha or decision, and one placed screenshot per task (the frame that actually shows that screen). Pick the frame by what it SHOWS, not by narration timestamp alone: in a fast walkthrough the on-screen view and the narration can drift, so confirm the frame before placing it (qa-bar item 11). Crop only to drop a webcam or participant tile that removes no needed content; otherwise keep the full frame (the shared rule in `../../../../_skills/render-doc/frame-crop.md`).

House rule: zero em dash characters.
