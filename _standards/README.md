# The canonical shared layer: `_config` + `_standards`

content-engine is a document factory: you configure the brand, design, voice, audience, and render preferences ONCE, and every lane (each a full ICM workspace) reads that shared shelf instead of re-declaring anything. This README explains the two halves of that shelf.

## The clean split

| Layer | What lives here | Who sets it | Changes per install? |
|---|---|---|---|
| **`_config/`** | the DIALS: brand identity, letterhead, design system, voice, audience defaults, render preferences | a human, once, via `/setup` | YES (every install rebrands) |
| **`_standards/`** | the fixed CONTRACTS: doc-model schema, manifest contract + pinned schema, the QA ship gate | nobody per install; they are the engine's invariants | NO |

`_config/` is "what this factory's output looks and sounds like." `_standards/` is "the contracts the machinery obeys no matter whose factory it is."

A third shared home, `_skills/`, holds shared CODE (the renderer). Facts live in `_config`/`_standards`; code lives in `_skills`. Lanes reference all three outward (one-way pointers); no lane duplicates a fact or a renderer.

## Why centralize these

Single source of truth. The doc-model schema lives once, so all renderers and both lanes agree on the shape. The manifest schema is a verbatim, version-locked copy of the transcription engine's schema, pinned per version (1.0 and 1.1), so a version skew fails loud in one place. The QA bar lives once, so "what ships" means the same thing for every lane. Change one of these and there is exactly one file to edit; nothing else restates it, so nothing else drifts.

## What each `_standards/` file is

- **`doc-model-schema.md`** is the long pole: the `docmodel-1.0` contract that Stage 03-layout produces and every renderer consumes, with the provenance/sidecar rules folded in. Frozen for the submission.
- **`manifest-contract.md`** narrates which transcribe-video manifest fields the lanes rely on and points at the pinned JSON Schema for types (no prose field list).
- **`schema/manifest-1.0.schema.json`** and **`schema/manifest-1.1.schema.json`** are the canonical machine contract for manifest field types: verbatim engine copies, each locked to its version. `01-ingest` validates a manifest against the copy its `schema_version` names; the accepted set is {1.0, 1.1}.
- **`qa-bar.md`** is the 16-item fidelity + polish checklist that gates delivery (the differentiator: every claim traceable internally, the reader surface clean).

For the per-install dials, see `../_config/`. For routing, see `CONTEXT.md` here.
