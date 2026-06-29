# _lane-builder: how to add a new lane (scaffold by copy)

This is a documented METHOD, not an automated generator. A "lane" is one full ICM workspace that turns a video manifest into one kind of document (an educational guide, an SOP, release notes, a knowledge-base article). The factory idea: build more lanes, share what they have in common. This page is the recipe for stamping a new one.

The principle (D1): every lane is SELF-CONTAINED. It has its own complete `stages/01-ingest .. 05-qa`, each a real `CONTEXT.md`, not a pointer to some other lane. What lanes SHARE lives once in the shared shelf and lanes reference it outward: shared FACTS in `_config/` + `_standards/` (brand, voice, design, doc-model schema, manifest schema, QA bar), shared CODE in `_skills/` (the renderer). So a new lane copies a skeleton and fills two stages; it never re-declares a brand fact or re-implements the renderer.

## What you copy, what you point at, what you write

| Piece | Action | Why |
|---|---|---|
| The five blank stage skeletons in `_templates/` | COPY into the new lane's `stages/` | every lane owns its full stage set (D1); these are the canonical pattern |
| Stages 01-ingest, 04-render, 05-qa | keep THIN, fill only the lane name | generic: they obey `_standards/` + `_skills/`, carry no per-lane logic |
| Stages 02-structure, 03-layout | SPECIALIZE: write the lane's `references/` | this is where lanes genuinely differ (what you extract, how you lay it out) |
| `_config/`, `_standards/`, `_skills/` | POINT outward, never copy | shared facts and code have ONE home; copying them would invite drift |
| `lane-config.md`, `reference/rules.md`, `reference/examples.md` | WRITE for the lane | the lane's dials and worked example |

The whole trick: stages 01/04/05 are thin contracts that read the canonical `_standards`/`_skills`, so they barely change between lanes. Stages 02 and 03 are the only real authoring work. That is what makes a second lane cheap.

## The steps

Answer `questionnaire.md` first (it pins the four decisions a lane needs), then:

1. Make the lane folder: `lanes/<your-lane>/` with `stages/`, `reference/`, and `lane-config.md`.

2. Copy the skeletons. Copy all five `_templates/NN-*/CONTEXT.md` into `lanes/<your-lane>/stages/NN-*/CONTEXT.md`. Give each stage its own `output/` with a `.gitkeep`.

3. Fill the placeholders in the copied skeletons:
   - `{{LANE_NAME}}` everywhere (e.g. `release-notes`).
   - `{{LANE_02_ONE_LINER}}` and `{{LANE_03_ONE_LINER}}` (the S5 one-liners: a single sentence each for what 02 and 03 do in this lane).
   - `{{LANE_TAXONOMY_FILE}}` in stage 02 (the filename of your extraction taxonomy, e.g. `change-extraction.md`).
   - `{{LANE_DOC_STRUCTURE_FILE}}` in stage 03 (the filename of your document shape, e.g. `release-notes-doc-structure.md`).

4. Leave 01/04/05 thin. They already point at `_standards/` (schema, doc-model, qa-bar) and `_skills/render-doc` (the renderer). Do NOT copy logic into them. The only edit is the lane name. The moment the schema or renderer changes, there is exactly one home to edit, not one per lane.

5. Write the two specialization references (the real work):
   - `stages/02-structure/references/<your-taxonomy>.md`: the typed items this lane extracts from the transcript (its taxonomy) and its ordering rule. Compare educational's `concept-extraction.md` (concepts/procedures/examples/facts/pitfalls/objectives, dependency order) against the SOP delta (steps/owners/decisions/risks, procedure order, zero inference). Your lane sits somewhere in that space.
   - `stages/03-layout/references/<your-doc-structure>.md`: the reader-facing section order your document takes (educational: overview, objectives, prerequisites, modules, summary, references; SOP: purpose, scope, roles, prerequisites, procedure, decisions, risks, open questions). Define yours.

6. Write the lane dials and example:
   - `lane-config.md`: `doc_type=<free string>` (NOT a closed enum, so no shared contract needs editing), the default reader, and any significance thresholds.
   - `reference/rules.md`: how this lane structures (its taxonomy + ordering, in prose). This is the lane's contest anchor.
   - `reference/examples.md`: one worked example of a good output section, the few-shot that stages 02/03 calibrate against.

7. Write the lane's `CLAUDE.md` (L0 router with the per-stage What-to-Load table) and `CONTEXT.md` (L1 map). Copy the educational lane's as the pattern and swap the lane name and the two specialization references. The load table is otherwise identical because 01/04/05 are identical across lanes.

8. Add the lane to the root `CONTEXT.md` "pick a recipe" table so the router knows it exists.

## What stays shared (do not touch)

You never edit, copy, or re-declare any of these when adding a lane:

- `_standards/doc-model-schema.md` (the one contract all renderers read).
- `_standards/schema/manifest-1.0.schema.json` + `manifest-1.1.schema.json` (the pinned manifest field types, accepted set {1.0, 1.1}).
- `_standards/qa-bar.md` (the fidelity checklist).
- `_skills/render-doc/` (`render.py`, `print.css`, `frame-crop.md`).
- `_config/` (brand, voice, design-system, audience, render-prefs).

If your new doc type needed a NEW doc-model block type, that is a shared-shelf change (edit `doc-model-schema.md` once), not a lane change. Most lanes do not need one: the existing prose / screenshot / callout / list blocks cover almost everything, and `doc_type` is a free string.

## Why this is not an automated generator

A real generator (a script that reads the questionnaire and writes the files) is a nice-to-have, not the point. The point is the PATTERN: a thin self-contained workspace whose only real per-lane work is two stages, everything else referenced outward. Once you see that the SOP delta is just a different `02` taxonomy and `03` structure over the identical 01/04/05 plumbing (see `lanes/sop/`), you can stamp a lane by hand in well under an hour. See `questionnaire.md` for the four questions that pin a lane.

House rule: zero em dash characters in anything you author.
