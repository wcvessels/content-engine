# _templates: blank stage skeletons

The canonical BLANK stage skeletons for a content-engine lane. `_lane-builder` copies these to stamp a new lane's `stages/`. Each lane is a SELF-CONTAINED ICM workspace with its OWN full `stages/01-ingest .. 05-qa` (D1): these templates are the pattern, each lane's stages are instances.

## How to use

1. Copy the five `NN-*/CONTEXT.md` files into a new lane's `stages/` (the `_lane-builder` README walks this).
2. Fill the `{{PLACEHOLDERS}}`: lane name, `{{LANE_*_ONE_LINER}}`, and the lane's `references/<taxonomy>.md` / `<doc-structure>.md` filenames.
3. Stages 01-ingest, 04-render, 05-qa are GENERIC: they point at the canonical `_standards/` + `_skills/` and need almost no per-lane edit beyond the lane name. The drift-prone logic (schema, render code, QA bar) lives in `_standards`/`_skills`, so these thin CONTEXT.md files carry no duplicated logic.
4. Stages 02-structure and 03-layout are the SPECIALIZATION POINTS: fill in the lane's extraction taxonomy and document shape via the lane's own `references/`.
5. Create each stage's `references/` (lane-authored) and an empty `output/` with a `.gitkeep`.

Each CONTEXT.md follows the ICM stage-context template: Inputs, Process, Checkpoints, Audit, Outputs. Keep them routing-and-process oriented; the canonical contracts they obey live in `_standards/`, not restated here.

House rule: zero em dash characters.
