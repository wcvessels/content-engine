# Audience defaults

The default reader profile a deliverable is written for, when the run brief does not say otherwise. Loaded at **01-ingest** (to set the per-run reader) and **02-structure** (to set the significance bar). A lane's `lane-config.md` can sharpen this; the per-run brief in 01-ingest can override it for one document.

Shipped PRE-FILLED. `/setup` rewrites each `{{PLACEHOLDER}}`.

## Default reader

- **Who** ({{DEFAULT_READER}}): a teammate or new hire who was not in the recording and has no special background. Smart, busy, reading this to get something done.
- **Prior knowledge** ({{PRIOR_KNOWLEDGE}}): assume general computer literacy and nothing else. Do not assume they know the product, the team's shorthand, or any acronym. Define a term the first time it appears.
- **Format preferences** ({{FORMAT_PREFS}}): skimmable. Clear headings, short paragraphs, numbered steps for procedures, a screenshot next to the step it illustrates, callouts for the things that bite. They should be able to find one section without reading the whole document.

## What this controls downstream

- **Significance filter (02-structure):** keep an item only if cutting it would cost THIS reader a concept, step, fact, example, or pitfall. Banter, scheduling, and "let me share my screen" never survive.
- **Reading level (03-layout):** matches `voice.md` (around 8th grade). When in doubt, simpler.
- **Prerequisites framing:** because the reader has no special background, state prerequisites up front and phrase structural ones gently ("you'll get more from this if you already know X").

## Per-run override

The reader for ONE document is collected conversationally in 01-ingest (doc title, intended reader, render targets), never in `/setup`. Setup configures the durable default; 01-ingest can sharpen it for a specific deliverable (for example, "this one is for managers, not new hires").
