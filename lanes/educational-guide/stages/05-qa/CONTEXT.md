# Stage 05: QA & Deliver (educational-guide)

The ship gate. This stage is GENERIC: it runs the canonical `../../../../_standards/qa-bar.md` checklist (mirrored locally as `references/fidelity-checklist.md`) against the rendered deliverable + the provenance sidecar + the source. It reads the doc-model + sidecar, NOT the upstream build inputs.

## Inputs

- `../04-render/output/` (the rendered PDF + HTML + the `{slug}-provenance.md` sidecar).
- `../03-layout/output/{slug}-docmodel.json`.
- Load: `../../../../_standards/qa-bar.md` (the canonical 16-item gate) + `references/fidelity-checklist.md` (the lane-local copy of the audit, run line by line).
- Do NOT load: `../01-ingest/`, `../02-structure/`; the engine; the taxonomy + the doc-structure reference (QA reads the doc-model + sidecar, not the build inputs).

## Process

1. Fidelity audit: sample claims, confirm each traces to a real segment/frame via the sidecar (the full 16-item checklist). Item 4 (the source actually states the claim) is the strongest gate.
2. Visual QA: letterhead, TOC, image placement, collapsible nav (HTML), page breaks (PDF), crop quality (improved focus, clipped no needed context, no leftover webcam tile that was cleanly removable).
3. Reader check: zero leaked timestamps/refs/speaker tags, reading level matches, zero em dashes.
4. On any fail: fix at the RIGHT upstream stage and re-run (never patch the rendered file).
5. Collect passing files into `output/final/`. Write the QA report.
6. Present for approval.

## Checkpoints

The final approval (step 6): present the QA report + the final deliverables for sign-off before delivery.

## Audit

- Source fidelity: every sampled claim has a sidecar ref to a real segment/frame (checklist items 1-13).
- No leaked provenance: zero timestamps/refs in any reader file; sidecar present in `output/` but NOT shipped (items 14-15).
- All targets present and open cleanly.
- Brand + polish meet `../../../../_standards/qa-bar.md`: letterhead, design system, crop fidelity, NO em dashes (item 16 + polish conditions).

## Outputs

`output/qa-report.md`, `output/final/` (the approved PDF/HTML), `output/delivery-note.md` (what was produced, from which source video).
