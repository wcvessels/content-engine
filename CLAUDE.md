# content-engine (L0 root router)

content-engine is a document factory (the brief's ask: "it has to be a factory"): it turns a recorded video into polished, shareable documents (educational guides, SOPs, knowledge-base articles, release notes). Configure the brand/design/voice ONCE in the shared shelf, then each "lane" is a production line for one document type, specializing only in what it pulls out of the video and how it lays it out. Every claim in a deliverable traces back to the transcript internally; the reader never sees a citation.

House rule: zero em dash characters anywhere in this repo. Use commas, colons, or parens. `->` is fine. Plain English, low-technical audience. CONTEXT.md files are routing-only and under 80 lines.

## Where am I? (the map)

| You want to | Go to |
|---|---|
| Understand what this is / how to run it | `brief.md`, `README.md` |
| Make a deliverable from a video | a lane: `lanes/educational-guide/` (primary) |
| See how a second doc type specializes | `lanes/sop/` (documentation-only delta) |
| Set the brand / design / voice / render prefs | `_config/` (run `/setup` to fill it) |
| Read the fixed contracts (schema, QA bar) | `_standards/` |
| Use the shared render code | `_skills/render-doc/` |
| Stamp a new lane | `_lane-builder/` (documented scaffold-by-copy method) |
| Install the transcription engine | `00-install/` (documentation only) |

## The shared shelf (read outward, never re-declare)

- `_config/` = the DIALS a human sets at setup (brand, letterhead, design-system, voice, audience, render prefs).
- `_standards/` = the fixed CONTRACTS (doc-model schema, manifest contract + pinned schema, QA bar).
- `_skills/` = the shared CODE (the renderer: doc-model -> PDF + HTML).
- `_templates/` = the blank stage skeletons `_lane-builder` copies to stamp a new lane.

## How a lane is built

Each lane is a SELF-CONTAINED ICM workspace with its own full `stages/01-ingest .. 05-qa`, each a real `CONTEXT.md` (Inputs/Process/Checkpoints/Audit/Outputs). Stages 01/04/05 are generic (they point at `_standards`/`_skills`); stages 02-structure and 03-layout are the per-lane specialization points. A lane reads the shared shelf outward and never duplicates a brand/voice/design fact or the render code.

For task -> which-lane routing, see `CONTEXT.md`.
