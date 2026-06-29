# Render preferences

The default render settings for every deliverable. Loaded at **04-render** (targets, page size, naming) and **03-layout** (TOC depth). The per-run brief in 01-ingest can override targets for one document; everything else is a durable default.

Shipped PRE-FILLED. `/setup` rewrites each `{{PLACEHOLDER}}`.

## Settings

| Setting | Placeholder | Default | Notes |
|---|---|---|---|
| Default targets | {{DEFAULT_TARGETS}} | `PDF, HTML` | Both on by default. DOCX is documented-only this build (`_skills/docx/SKILL.md`), not produced. |
| Page size | {{PAGE_SIZE}} | `Letter` | `@page { size: Letter; margin: 1in }`. Set to `A4` for non-US deliverables. |
| TOC depth | {{TOC_DEPTH}} | `2` | Include heading levels 1 and 2 in the sticky nav. Level-2 nests under its level-1. |
| HTML effect ceiling | {{HTML_EFFECT_CEILING}} | `restrained` | Allowed: ~150ms hover/expand transitions, sticky nav, `<details>` collapse. Banned: parallax, animated gradients, autoplay, decorative motion. |
| File naming | {{FILE_NAMING}} | `{slug}.{ext}` | `{slug}` is the kebab-case document title from the run brief (for example `configuring-expense-exports.pdf`). One slug, both targets. |

## Target behavior

- **HTML** is the spine: a single self-contained file (inline CSS, base64 screenshots, no network).
- **PDF** is derived from the same HTML plus print CSS via headless Chrome (Edge fallback). Same content, both targets, one doc-model.
- **Footer:** static disclaimer line only (no page numbers, no print TOC). See `brand/letterhead.md`.

## What is NOT here

- Brand colors and fonts live in `design-system.md`.
- Letterhead layout and the disclaimer text live in `brand/letterhead.md`.
- The per-document title, reader, and chosen targets are collected in 01-ingest, not in `/setup`.
