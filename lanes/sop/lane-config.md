# sop lane config (the DIALS this lane sets)

The per-lane settings stage 01/02 read. Brand, voice, design, and the render targets are NOT here: those live once on the shared shelf (`../../_config/`) and this lane reads them outward.

| Setting | Value | Used by |
|---|---|---|
| `doc_type` | `procedure` | 03-layout (meta.doc_type), 04-render |
| Default reader | An operator or new hire who needs to repeat the process correctly | 01-ingest, 02-structure |
| Inference posture | ZERO content inference (an SOP asserts facts; see `reference/rules.md`) | 02-structure |

## Significance filter (keep-or-cut)

Keep a transcript segment only if cutting it would lose a step, decision point, owner, risk, reference, prerequisite, purpose, scope bound, or a real open question. Drop greetings, "let me share my screen", scheduling, tangents, and pure agreement. The full taxonomy lives in `stages/02-structure/references/sop-extraction.md`.

House rule: zero em dash characters.
