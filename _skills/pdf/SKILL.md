---
name: pdf
description: PDF know-how for the content-engine render path. The PDF is the same HTML render-doc produces, run through headless Chrome or Edge --print-to-pdf with print.css. Use at stage 04-render. Covers the browser probe, the print CSS, and a pypdf letterhead-underlay fallback.
---

# pdf (pointer, thin)

The PDF target is NOT a separate render. It is the SAME self-contained HTML
`render-doc`'s `build_html` produces, with `print.css` injected inline, run
through headless Chrome (or Edge as the identical-engine fallback). One source,
content parity by construction.

House rule: zero em dash characters.

## The path

```
docmodel.json -> build_html() (print.css inlined) -> Chrome/Edge --print-to-pdf -> {slug}.pdf
```

`render.py` `build_pdf(html, out_pdf_path)`:

1. Probes for a browser: Chrome first (`chrome.exe`), then Edge (`msedge.exe`).
   Cross-platform candidate paths plus a `PATH` fallback.
2. Writes the HTML to a sibling `.src.html`.
3. Runs `--headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=out
   file:///abs/path.html` (falls back to legacy `--headless` if needed).
4. Verifies the output starts with `%PDF-`, else raises.

## Print rules (`../render-doc/print.css`)

- `@page { size: Letter; margin: 1in }`
- `.title-page { break-after: page }` (cover on its own sheet)
- `<details open>` prints expanded
- a STATIC disclaimer footer, NO page numbers, NO print-only TOC (decision D4)

## Fallbacks

- **No browser found:** `build_pdf` raises a clear `RuntimeError`. The HTML
  target is the spine and is unaffected.
- **pypdf letterhead underlay (optional):** if a RASTER letterhead is ever
  preferred over the CSS title page, the fallback is to render body PDF first,
  then `pypdf` a letterhead page-1 underlay. Not used in the default path (the
  CSS title page is cleaner and needs no extra dependency).

## Cut for this submission

WeasyPrint and LibreOffice PDF paths (GTK/Cairo time-sink on Windows). PDF/A,
accessibility tagging, font subsetting. Chrome is the path.
