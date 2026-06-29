# Identity (ANCHOR)

The brand identity for deliverables. This is the single home for the name, tagline, brand sentence, and mission. Every lane's render stage and the letterhead pull from here. Nothing else re-declares these facts.

Shipped PRE-FILLED with the content-engine brand as the demo default. Run `/setup` (`setup/questionnaire.md`) to replace these with your own brand. The `{{PLACEHOLDER}}` name beside each field is what setup rewrites.

## Brand

- **Name** ({{COMPANY_NAME}}): content-engine
- **Tagline** ({{TAGLINE}}): Recordings in, documents out.
- **Brand sentence** ({{BRAND_SENTENCE}}): content-engine turns a recorded video into a polished, shareable document, with every claim traced back to what was actually said or shown.
- **Mission** ({{MISSION}}): Free the knowledge trapped in recordings nobody will rewatch. Make a faithful guide as easy to produce as a sloppy summary, so the document a teammate reads is one they can trust.

## How the name is written

- Lowercase, one word, hyphenated: `content-engine`. Never "Content Engine" or "ContentEngine".
- In the wordmark, the hyphen is the primary color (#2B3A8C); the rest is ink.
- Logo assets live in `brand/logo/`: `wordmark.svg` (light background) and `wordmark-dark.svg` (dark background) for headers and the title page, `mark.svg` for small placements, and `favicon-32.png` / `favicon-180.png` for the browser tab. The renderer inlines the mark + wordmark lockup and the favicon into every document (self-contained, no external files).

## Author attribution

- **Author** ({{AUTHOR}}): Will Vessels
- Used to fill the doc-model `meta.author` field at render (see `_standards/doc-model-schema.md`).

## Voice in one line

Plain English, low-technical, no jargon, no em dashes. The full rules live in `voice.md`.
