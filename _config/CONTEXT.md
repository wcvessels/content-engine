# _config (routing)

The DIALS a human sets ONCE via `/setup` (`../setup/questionnaire.md`). Every lane reads these outward (Pattern 3, one-way); nothing re-declares a brand, voice, or design fact. These change per install; the fixed contracts live in `../_standards/`.

## Files here and which stage loads which

| File | What it holds | Loaded by |
|---|---|---|
| `identity.md` | name, tagline, brand sentence, mission, author (ANCHOR) | 04-render (brand fields) |
| `brand/letterhead.md` | title-page layout, header/footer, logo placement, static disclaimer | 04-render |
| `brand/logo/` | `wordmark.svg` (full), `mark.svg` (small/footer) | 04-render |
| `design-system.md` | palette, typography, type scale, per-target visual rules (theme-factory tokens) | 03-layout (TOC depth + heading hierarchy ONLY), 04-render (colors + fonts) |
| `voice.md` | plain English, low-technical, no jargon, no em dashes | 03-layout |
| `audience-defaults.md` | default reader profile, prior knowledge, format prefs | 01-ingest, 02-structure |
| `render-prefs.md` | default targets (PDF + HTML), page size, TOC depth, HTML effect ceiling, file naming | 03-layout (TOC depth), 04-render |

The clean split the stages rely on: **voice @ 03, brand @ 04.** Layout writes prose in the configured voice and sets hierarchy; render applies brand colors, fonts, and letterhead. `design-system.md` is the one file loaded at both stages, for two distinct reasons (hierarchy at 03, color/font at 04).

## See also

- `../setup/questionnaire.md` to fill every `{{PLACEHOLDER}}` in these files (run once).
- `../_standards/` for the fixed contracts (schema, manifest, QA bar) that do NOT change per install.
- `../_skills/render-doc/` for the shared render code that consumes these dials.
