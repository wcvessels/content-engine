# educational-guide (L0 lane router)

You are in the **educational-guide** lane: a self-contained ICM workspace that turns a recorded walkthrough into a polished learning guide (a guided learning path, screenshots placed at the concept they illustrate, objectives per module). This is the PRIMARY lane of content-engine.

## Where am I? (routing)

- **Start a deliverable:** open `stages/01-ingest/CONTEXT.md` and walk 01 -> 02 -> 03 -> 04 -> 05.
- **Lane map + shared pointers:** `CONTEXT.md` (this folder).
- **Lane dials:** `lane-config.md` (`doc_type=guide`, default reader, significance thresholds).
- **How this lane structures:** `reference/rules.md` (typed concepts, prereqs, dependency order) + `reference/examples.md` (a worked module).
- **The shared shelf (read OUTWARD, never re-declare):** `../../_config/` (brand, voice, design, audience, render prefs), `../../_standards/` (doc-model schema, manifest contract, qa-bar), `../../_skills/` (the renderer + design skills).

This lane SPECIALIZES only at stages **02 (extract)** and **03 (layout)**. Stages 01 / 04 / 05 are generic: they obey the canonical `_standards/` contracts and invoke the shared `_skills/render-doc` code, carrying no lane-specific logic.

## What-to-Load / What-NOT-to-Load (THE canonical load-rule table)

Five-layer routing + 60/30/10: most stages load deterministic `_config`/references; AI judgment is the thin layer at 02/03 only. `[SPEC]` notes are the only per-lane differences. Paths are relative to a stage folder (`stages/NN-name/`).

| Stage / Task | Load These | Do NOT Load |
|---|---|---|
| **01-ingest** | `stages/01-ingest/CONTEXT.md`; `../../../00-install/references/engine-location.md`; `../../../_standards/manifest-contract.md` + `../../../_standards/schema/manifest-1.0.schema.json` + `../../../_standards/schema/manifest-1.1.schema.json`; `../../../_config/audience-defaults.md` | the engine `scripts/` tree (invoke, never read); `_config/design-system.md`, `voice.md`; render skills; stages 02-05 |
| **02-structure** | `stages/02-structure/CONTEXT.md`; `references/concept-extraction.md` + `references/dependency-ordering.md` **[SPEC]**; `../01-ingest/output/ingest/`; `../../../_config/audience-defaults.md` | `_config/brand`, `design-system.md`, `render-prefs.md`; all render skills; stages 03/04/05 |
| **03-layout** | `stages/03-layout/CONTEXT.md`; `references/educational-doc-structure.md` **[SPEC]**; `../02-structure/output/`; `../01-ingest/output/ingest/frames/`; `../../../_config/voice.md`; `../../../_config/design-system.md` (TOC depth + heading hierarchy ONLY); `../../../_standards/doc-model-schema.md`; `../../../_skills/render-doc/frame-crop.md` | `_config/brand` (brand is filled at render, not layout); render skills + the engine; `../01-ingest/references/`; stages 04/05 |
| **04-render** | `stages/04-render/CONTEXT.md`; `../03-layout/output/{slug}-docmodel.json`; `../01-ingest/output/ingest/frames/`; `../../../_config/brand` + `design-system.md` (colors/fonts) + `render-prefs.md`; `../../../_skills/render-doc` + pdf/frontend-design/theme-factory | `_config/voice.md` (applied at 03); the 02 taxonomy + 02 output; the engine; the doc-structure reference; `docx` skill (DOCX not built) |
| **05-qa** | `stages/05-qa/CONTEXT.md` + `references/fidelity-checklist.md`; `../04-render/output/` (incl. sidecar); `../03-layout/output/{slug}-docmodel.json`; `../../../_standards/qa-bar.md` | `../01-ingest/`, `../02-structure/`; the engine; the taxonomy + doc-structure (QA reads the doc-model + sidecar, not the build inputs) |

Rationale: voice loaded only at 03, dropped at 04; design-system loaded at 03 for hierarchy/TOC and at 04 for colors/fonts (two distinct reasons); brand loaded only at 04 (not 03, so the doc-model stays reusable); the engine is invoked at 01, never read; QA reads the doc-model + provenance, never the upstream build inputs.
