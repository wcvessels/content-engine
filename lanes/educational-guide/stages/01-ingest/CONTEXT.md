# Stage 01: Ingest (educational-guide)

Validate the source, resolve frames, and normalize everything into a self-contained bundle the rest of the lane reads. This stage is GENERIC: it obeys the canonical contracts in `../../../../_standards/` and needs no per-lane logic beyond the lane name.

## Inputs

- The per-run brief (asked here): doc title/topic, intended reader, which render targets.
- One of: a `{basename}_manifest.json` (manifest provided) OR a video URI to transcribe.
- Load: `../../../../_standards/manifest-contract.md` + `../../../../_standards/schema/manifest-1.0.schema.json` + `../../../../_standards/schema/manifest-1.1.schema.json`; `../../../../00-install/references/engine-location.md` (only if a fresh transcription is needed); `../../../../_config/audience-defaults.md`.
- Do NOT load: the engine `scripts/` tree (invoke it, never read it); `_config/design-system.md` or `voice.md`; the render skills; stages 02-05.

## Process

1. Ask the per-run basics (title/topic, reader, targets). Record to `output/{slug}-run.md`.
2. Determine input mode: (a) manifest provided -> validate; (b) video provided -> run the engine per `engine-location.md` (`transcribe-video "<URI>"`), then confirm the 4-artifact set (`{name}_manifest.json`, `{name}_frames/`, `{name}_transcript.txt`, `{name}_frames.md`).
3. Validate against the pinned schema named by `schema_version`: it MUST be in {`1.0`, `1.1`}, and the manifest is checked against that version's pinned copy. Any other value fails loud ("produced by a newer or older engine than this lane supports").
4. Resolve frames RELATIVE TO THE MANIFEST FILE'S OWN DIRECTORY (`os.path.join(os.path.dirname(manifest_path), frames_dir)`), NOT cwd. Every `frames[].file` must exist there; every non-null `segments[].frame_index` must resolve. Missing = hard error.
5. Normalize to a self-contained bundle: `output/ingest/source.json`, `output/ingest/segments.json` (segments + a derived `frame_file`), `output/ingest/frames/` (COPIED to in-bundle paths), `output/ingest/provenance.md` (run_id, tool_version, generated_at, source.uri, per-segment timestamp index, the provenance seed). Downstream stages use the copied in-bundle paths only.

## Checkpoints

One, at the entry boundary (after step 5). Present: source title, duration, language, speaker count, segment count, frame count, transcription path (captions vs whisperx), any low-confidence flags. Ask: right source, transcript usable? Cheap to fix here, expensive later.

## Audit

| Check | Pass condition |
|---|---|
| Schema valid + version | `schema_version` in {1.0, 1.1}; validates against that version's pinned schema |
| Frame integrity | every `frames[].file` exists under the manifest-relative `frames_dir`; every non-null `frame_index` resolves |
| Non-empty content | `segments[]` non-empty; transcript text present |
| Provenance complete | run_id, tool_version, generated_at, source.uri captured into `provenance.md` |
| Run recorded | `output/{slug}-run.md` has title, reader, chosen targets |

## Outputs

`output/ingest/` (source.json, segments.json, frames/, provenance.md) + `output/{slug}-run.md`. Stages 02+ read ONLY from here.
