# sop (L1 lane map)

A self-contained ICM workspace: a recorded process walkthrough in, a polished Standard Operating Procedure out (PDF + interactive HTML). The pipeline is the standard five stages; this lane specializes only at 02 and 03. A shipped public example (a Ramp manager onboarding SOP) lives in `../../samples/` (`ramp-manager-onboarding`).

## The pipeline

| Stage | Does | Specialized? |
|---|---|---|
| `stages/01-ingest/` | validate the manifest vs the pinned schema, resolve + copy frames, normalize to a self-contained bundle | no (generic) |
| `stages/02-structure/` | extract typed items (step/decision/owner/risk/reference/prerequisite/purpose/scope/open-question), filter, order by stated process order, ZERO content inference | **yes** |
| `stages/03-layout/` | turn the procedure into ONE doc-model; place screenshots by what they show; reader prose in voice | **yes** |
| `stages/04-render/` | one doc-model -> PDF + HTML via the shared renderer; apply brand; split provenance to a sidecar | no (generic) |
| `stages/05-qa/` | the 16-item fidelity audit + visual QA; ship gate | no (generic) |

## Lane-local files

- `CLAUDE.md` (this folder): L0 router + the canonical per-stage What-to-Load table.
- `lane-config.md`: lane dials (`doc_type=procedure`, default reader, significance thresholds).
- `reference/rules.md` + `reference/examples.md`: the zero-inference thesis with the S1-S5 delta vs educational, and a worked Procedure section.
- The loadable specialization detail: `stages/02-structure/references/sop-extraction.md` (taxonomy + ordering) and `stages/03-layout/references/sop-doc-structure.md` (section shape).

## Shared shelf (read OUTWARD, one-way; never re-declare a shared fact)

- `../../_config/` : the DIALS (identity, brand/letterhead, design-system, voice, audience-defaults, render-prefs). Set once via `/setup`.
- `../../_standards/` : the CONTRACTS (doc-model-schema, manifest-contract + pinned `schema/manifest-1.0.schema.json` & `manifest-1.1.schema.json`, qa-bar). Fixed, do not change per install.
- `../../_skills/` : shared CODE (render-doc: the doc-model -> PDF/HTML renderer + `frame-crop.md`) and the design skills.

## Need a transcript first?

If you have a video but no manifest, `../../00-install/` documents installing and running the separate engine (`transcribe-video "<video>"`), which writes the `{name}_manifest.json` + frames that `stages/01-ingest/` consumes. The committed `../../samples/` set lets you run the lane with zero install.
