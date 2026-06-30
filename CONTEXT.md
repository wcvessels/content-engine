# content-engine (L1 root map: pick a recipe)

Task -> which lane. Each lane is a full ICM workspace that reads the shared shelf (`_config` + `_standards` + `_skills`) and specializes only in extraction (stage 02) and layout (stage 03).

## Pick a recipe

| Your source + goal | Lane | Status |
|---|---|---|
| A recorded walkthrough -> a polished educational guide (learning path, screenshots, objectives) | `lanes/educational-guide/` | wired, primary |
| A recorded process -> a step-by-step SOP (actions, owners, decisions, risks) | `lanes/sop/` | wired; shipped sample `ramp-manager-onboarding` (from a public Ramp video) |
| A new doc type (KB article, release notes, ...) | `_lane-builder/` then a new lane | documented scaffold-by-copy method |

## First time here?

1. Read `brief.md` (what this solves) and `README.md` (quickstart + install pointer).
2. If the brand is not yet yours, run `/setup` (`setup/questionnaire.md`) to fill `_config/`. The demo ships pre-branded as content-engine.
3. To make a deliverable, open the lane and start at its `stages/01-ingest/`.

## Need a transcript first?

If you have a video but no manifest, `00-install/` documents how to install and run the separate transcription engine (`transcribe-video "<video>"`), which produces the `{name}_manifest.json` + frames that lane 01-ingest consumes. The committed `samples/` set (four rendered guides, featured: getting-started-claude-code, plus a Ramp SOP from the sop lane) lets you inspect the output and run the lane with zero install.

## The shared shelf (the factory's shared parts)

If changing it would affect every deliverable's look or wording, it is SHARED (`_config`/`_standards`/`_skills`). If it changes only what you pull out of the video or how you lay it out, it is LANE-SPECIFIC (the lane's `reference/` + stages 02/03). See `_standards/README.md`.
