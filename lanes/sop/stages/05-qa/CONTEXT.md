# Stage 05: QA (sop)

The ship gate. Run the canonical 16-item fidelity bar against the rendered SOP (PDF + HTML) plus the provenance sidecar plus the source manifest/transcript. Every item must PASS. A fail is fixed at the right upstream stage and the audit reruns: 05-qa never patches a symptom in the rendered file. This stage is GENERIC; the bar it runs is the shared one.

## Inputs

- `../04-render/output/` (the rendered PDF + HTML + the provenance sidecar).
- `../03-layout/output/{slug}-docmodel.json`.
- Load: `references/fidelity-checklist.md` (a POINTER to the canonical bar); `../../../../_standards/qa-bar.md` (the actual 16-item bar + polish conditions).
- Do NOT load: `../01-ingest/`, `../02-structure/` (QA reads the doc-model + sidecar, not the build inputs); the engine; the taxonomy + doc-structure.

## Process

1. Run the 16-item fidelity checklist in `../../../../_standards/qa-bar.md` against the rendered files + sidecar. For the SOP lane, items 6 (zero inferred content), 9 (owners named-only), and 10 (sequence honest) bite hardest.
2. Run the polish + render-fidelity conditions (targets, brand, images, content parity, navigation).
3. On any fail: identify the WRONG upstream stage, fix it THERE, re-render, re-run this checklist.
4. When all 16 plus the polish conditions pass: collect the passing files into `output/final/`, write `output/qa-report.md` and `output/delivery-note.md`, and present for approval.

## Checkpoints

The final ship checkpoint: present the qa-report and the rendered files for human approval before delivery.

## Audit

The 16-item bar IS the audit. The gate is binary: all 16 plus the polish conditions PASS, or it does not ship.

## Outputs

`output/final/` (the passing PDF + HTML), `output/qa-report.md`, `output/delivery-note.md`.
