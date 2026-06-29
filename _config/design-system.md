# Design system

The palette, typography, and per-target visual rules for every deliverable. Written as theme-factory-style tokens so the renderer can drop them straight into a CSS variable block. Loaded at **03-layout** for TOC depth + heading hierarchy only, and at **04-render** for colors + fonts.

Shipped PRE-FILLED with the content-engine brand. `/setup` rewrites each `{{PLACEHOLDER}}`. The values below ARE the defaults; the placeholder name beside each is what setup swaps.

## Palette (hex)

| Token | Placeholder | Hex | Role |
|---|---|---|---|
| `--primary` | {{PRIMARY}} | `#2B3A8C` | press indigo: headings, links, the title-page bar, the hyphen in the wordmark |
| `--secondary` | {{SECONDARY}} | `#5B647F` | muted slate: subtitles, captions, metadata, secondary UI |
| `--accent` | {{ACCENT}} | `#E8A33D` | warm amber: the resolved-page mark, callout rules, the one highlight color (use sparingly) |
| `--bg` | {{BG}} | `#FFFFFF` | paper white: page and document background |
| `--bg-soft` | (derived) | `#F4F5F8` | soft panel: callout fills, code blocks, the TOC rail |
| `--text` | {{TEXT}} | `#14171F` | ink: body text |
| `--border` | (derived) | `#E2E4EC` | hairlines, table rules, section dividers |

Callout variant tints (used by the doc-model `callout` block; all pass WCAG AA on `--text`):

| Variant | Bar | Fill |
|---|---|---|
| `tip` | `#2B3A8C` | `#EDEFF9` |
| `warning` | `#E8A33D` | `#FBF1DE` |
| `note` | `#5B647F` | `#F1F2F5` |
| `prereq` | `#3B8C6E` | `#E8F3EE` |

Callout label text must meet WCAG AA, so amber and green bars use AA-darkened label colors (the bar stays vivid): `warning` label `#8A5800`, `prereq` label `#2B6B54`. `tip` and `note` labels use the bar color directly (both pass AA).

## Typography

| Token | Placeholder | Stack | Use |
|---|---|---|---|
| `--font-heading` | {{HEADING_FONT}} | `'Helvetica Neue', Helvetica, Arial, sans-serif` | H1-H3, the wordmark, the title page |
| `--font-body` | {{BODY_FONT}} | `'Helvetica Neue', Helvetica, Arial, sans-serif` | body, lists, captions |
| `--font-mono` | (fixed) | `ui-monospace, Menlo, Consolas, 'Liberation Mono', monospace` | inline `code`, CLI, labels |

Webfont policy: system-safe by design. The renderer does NOT fetch webfonts (self-contained file rule), so the brand uses Helvetica Neue with an Arial then system-sans fallback that renders identically offline on every OS. No CDN, no `@import`, no `@font-face`, no network. (A distinctive heading face could be added later by base64-embedding one subsetted woff2; tracked, not done.)

## Type scale ({{SIZE_SCALE}}, 1.25 major-third on a 16px base)

| Step | Size | Line height | Used for |
|---|---|---|---|
| `h1` | 33px | 1.15 | document title |
| `h2` | 26px | 1.2 | section heading (level 1) |
| `h3` | 21px | 1.3 | sub-heading (level 2) |
| `body` | 16px | 1.6 | prose |
| `small` | 13px | 1.4 | captions, footer, metadata |

## Per-target visual rules

**HTML (interactive, restrained):**
- Max content width ~`760px`, centered, generous whitespace.
- Sticky `<nav>` TOC rail on `--bg-soft`, plain in-page anchor links, current section in `--primary`.
- Collapsible sections via native `<details open>` (prints expanded).
- Transitions: ~150ms ease on hover/expand only. No parallax, no animated gradients, no autoplay, no decorative motion.
- Screenshots: full width within content, `8px` radius, `1px` `--border`, short caption in `--secondary`.

**PDF (on letterhead):**
- `@page { size: Letter; margin: 1in }`.
- Title page: wordmark top-left, `--primary` rule under the title, subtitle in `--secondary`, brand fields from `identity.md`, `break-after: page`.
- Body matches HTML structure; `<details>` render expanded.
- Footer: static disclaimer line only (`--secondary`, `small`). No page numbers, no print TOC (the HTML nav covers navigation).

**Shared discipline:** one design system, both targets. No per-target custom theming. Color carries meaning (primary = structure/links, accent = the single highlight, variant tints = callout type); never decorate for its own sake.

## CSS variable block (the brand vocabulary)

The renderer's LIVE token block is `_DEFAULT_CSS` in `_skills/render-doc/render.py` (it uses `--ce-*` names and inlines the brand into every output, including a bar/fill/label set per callout). The block below is the readable design-vocabulary mirror; keep the two in sync. A loader that reads this file at render and passes it via `build_html(css=...)` is a tracked follow-up.

```css
:root {
  --primary:#2B3A8C; --secondary:#5B647F; --accent:#E8A33D;
  --bg:#FFFFFF; --bg-soft:#F4F5F8; --text:#14171F; --border:#E2E4EC;
  --font-heading:'Helvetica Neue',Helvetica,Arial,sans-serif;
  --font-body:'Helvetica Neue',Helvetica,Arial,sans-serif;
  --font-mono:ui-monospace,Menlo,Consolas,'Liberation Mono',monospace;
}
```
