# Stage 04: Render (sop)

One doc-model in, the enabled targets out (PDF + HTML). This stage is GENERIC: it reads only the doc-model + `_config` + the shared renderer and never needs to know which lane produced the model. It is identical in intent to the educational lane's 04-render.

## Inputs

- `../03-layout/output/{slug}-docmodel.json` (the one intermediate).
- `../01-ingest/output/ingest/frames/` (the copied in-bundle frames).
- Load: `../../../../_config/brand` + `../../../../_config/design-system.md` (colors/fonts) + `../../../../_config/render-prefs.md`; `../../../../_skills/render-doc/` (+ pdf / frontend-design / theme-factory pointers).
- Do NOT load: `_config/voice.md` (applied at 03); the 02 taxonomy + 02 output; the engine; the doc-structure reference; the `docx` skill (DOCX not built).

## Process

1. Read the doc-model + targets from `render-prefs.md` (default PDF + HTML).
2. Split provenance: write every block's `[ref]` to `output/{slug}-provenance.json`; produce a clean doc-model with refs removed.
3. Fill brand fields from `../../../../_config/brand` + `../../../../_config/identity.md`.
4. HTML (build first, the spine): single self-contained file via `render-doc/render.py` (`build_html`), inline CSS, base64 screenshots (crop applied with Pillow per the block's `crop`, original frame untouched), sticky `<nav>` TOC, collapsible `<details open>`.
5. PDF (derived from the HTML): the same HTML + print CSS -> headless Chrome `--print-to-pdf` (Edge is the identical-engine fallback). Static disclaimer footer with the source attribution.
6. DOCX: NOT built this submission (the shared `render.py` carries a documented stub).
7. Audit per produced file; fix at the right upstream stage and re-render on fail.

## Checkpoints

None at the entry boundary (the doc-model was approved at 03). The render audit below gates the handoff to 05.

## Audit

- Targets produced: every enabled target exists.
- Clean of provenance: no timestamp / `[ref]` in any rendered file.
- Brand applied: letterhead/logo/footer on the PDF; design-system colors/fonts on both.
- Images embedded: no broken links; crops applied as specified; original frames untouched.
- One source: both targets from the same doc-model (content parity).

## Outputs

`output/{slug}.pdf`, `output/{slug}.html`, `output/{slug}-provenance.json` (internal, NOT shipped to the reader).
