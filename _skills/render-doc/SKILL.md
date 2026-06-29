---
name: render-doc
description: Render a docmodel-1.0 document model to a self-contained interactive HTML file and a PDF on letterhead. The single shared renderer for every content-engine lane. Use at stage 04-render after 03-layout has produced a docmodel.json. Consumes one contract (docmodel-1.0), resolves screenshots from the run manifest, applies optional crops, and emits HTML + PDF from the same source.
---

# render-doc

The shared render engine. One doc-model in (`docmodel-1.0`, pinned in
`_standards/doc-model-schema.md`), the enabled targets out (PDF + HTML). It
never needs to know which lane produced the model: lane-specific logic
collapses into the doc-model shape upstream.

House rule: zero em dash characters.

## Files

| File | Role |
|---|---|
| `render.py` | `build_html` / `build_pdf` / `resolve_frame` / `render` + a documented `build_docx` stub |
| `print.css` | `@media print` rules (Letter, 1in margin, title-page sheet, static footer, NO page numbers) |
| `toc.js.tmpl` | OPTIONAL scroll-spy polish; the MVP ships a JS-free sticky-anchor TOC |
| `frame-crop.md` | the shared crop-decision rule (D6); both lanes' 03-layout reference it |

## How to invoke

From stage 04-render, after 03-layout wrote `{slug}-docmodel.json` and
01-ingest copied frames into `output/ingest/frames/` (so the manifest's
frames resolve in-bundle):

```bash
python _skills/render-doc/render.py \
    path/to/{slug}-docmodel.json \
    path/to/04-render/output \
    --manifest path/to/01-ingest/output/ingest/{name}_manifest.json \
    --slug {slug} \
    --targets html,pdf
```

Or from Python:

```python
from render import render
produced = render(docmodel_dict, out_dir, slug,
                  manifest_path="...ingest/.../manifest.json",
                  targets=("html", "pdf"))
# produced -> {"html": ".../slug.html", "pdf": ".../slug.pdf"}
```

## Targets

- **HTML (built first, the spine).** Single self-contained file: inline CSS,
  base64 screenshots, sticky `<nav>` TOC with in-page anchors, collapsible
  `<details open>` sections (so they also print expanded), restrained ~150ms
  transitions. A ~30-line inline-markdown escaper handles `**bold**`,
  `*italic*`, `` `code` ``, `[text](url)`. No markdown library.
- **PDF (derived from the same HTML).** `print.css` is injected inline, then
  headless Chrome (`chrome.exe`) or Edge (`msedge.exe`) `--print-to-pdf`
  produces the PDF. Title page on its own sheet, body, embedded screenshots, a
  static disclaimer footer. NO page numbers, NO print TOC (decision D4).
- **DOCX: documented, NOT built (decision D3).** `build_docx` raises
  `NotImplementedError` and documents the pandoc + `--reference-doc` path. See
  `../docx/SKILL.md`.

## Screenshots + crop

`resolve_frame(frame_index, manifest_path, crop=None)` resolves a frame:
builds `index -> file` from the manifest's `frames[]`, joins with
`artifacts.frames_dir` resolved RELATIVE TO THE MANIFEST FILE'S OWN DIRECTORY
(not cwd), applies the optional `crop` box with Pillow on a COPY (the original
frame is never modified), optionally downscales the long edge to ~1200px, then
base64-encodes and inlines as `data:image/jpeg;base64,...`. The crop rule lives
in `frame-crop.md`; 03 decides, 04 applies, 05 checks.

## Fallbacks (degrades, never hard-fails)

- **Missing frame:** if `frame_index` does not resolve, render a visible
  placeholder block and continue. Never hard-fail a render.
- **No Pillow:** raw bytes are inlined without crop/downscale (crop is skipped).
- **No browser for PDF:** `build_pdf` raises a clear `RuntimeError`; the HTML
  target is unaffected (it is the spine). Chrome is probed first, then Edge.
- **Unknown block `type` / `kind` / `variant`:** degrades to a plain block
  (the docmodel-1.0 graceful-fallback rule), never an exception.
- **Wrong schema literal:** `build_html` raises `ValueError` (refuses to guess
  a newer/older shape), mirroring the manifest version pin.

## Self-test

`_selftest/` holds a synthetic `docmodel.json` + a generated frame and the
rendered `sample.html` + `sample.pdf`, kept as proof the renderer is green
without needing a real manifest. Re-run:

```bash
python _skills/render-doc/_selftest/run_selftest.py
```
