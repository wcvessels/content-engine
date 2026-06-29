# manifest contract

How content-engine consumes a transcribe-video manifest. This file narrates which manifest fields the lanes rely on and WHY. It does NOT transcribe a field list in prose: the canonical machine contract for field TYPES is the pinned JSON Schema set `schema/manifest-1.0.schema.json` + `schema/manifest-1.1.schema.json` (verbatim, version-locked copies of the engine schema; a manifest is checked against the one its `schema_version` names). When in doubt about a field's type or whether it is required, read the JSON Schema, not this file.

---

## The load-bearing seam

content-engine and the transcription engine are decoupled by ONE file: `{basename}_manifest.json`, validated against the pinned schema. Lane `01-ingest` validates it, checks `schema_version` against the pinned set {`1.0`, `1.1`} and validates against the matching schema (any other value fails loud), resolves and copies frames, and normalizes everything into a self-contained `output/ingest/` bundle. Nothing downstream re-parses raw manifest JSON.

Two arrival modes are treated identically: (1) a user runs the engine themselves and points lane 01 at the output; (2) the committed `samples/` manifest a judge runs with zero install. Lane 01 cannot tell them apart.

---

## Which fields the lanes rely on, and why

The schema is the type authority. This section explains intent only.

- **`schema_version`** is the version pin. content-engine COPIES the engine schema rather than importing it by path, and pins a SET of accepted versions ({`1.0`, `1.1`} today). A manifest validates against the pinned copy whose `const` matches its `schema_version`; a version outside the set fails loud with a clear message until content-engine adds it. The seam is versioned on purpose.

- **`source`** gives the run its identity for provenance: the title and URI feed `meta.source` in the doc-model and the `delivery-note.md`. Duration/dimensions inform sanity checks at ingest.

- **`run`** carries `run_id`, `tool_version`, and `generated_at`. These are captured into `output/ingest/provenance.md` so every deliverable traces back to a specific engine run.

- **`transcription`** tells the lane which path produced the text (`captions` vs `whisperx`), the `language`, and the `speaker_count`. The ingest checkpoint surfaces these so a human can confirm the transcript is usable before structuring begins.

- **`frames`** is the screenshot catalog. The doc-model's `screenshot.frame_index` joins to `frames[].index`; `frames[].file` is the filename under `artifacts.frames_dir`; `frames[].sharpness` breaks ties when 03-layout picks the best frame for a section; `frames[].timestamp_s` maps a frame to the segment span it falls in.

- **`segments`** is the spine. `segments[].frame_index` is the JOIN that places the right screenshot next to the right spoken content and grounds provenance. `segments[].text`, `start_s`, `end_s`, and `speaker` are the raw material stage 02 extracts typed items from. `segments[].index` is the provenance anchor recorded in the sidecar.

- **`artifacts`** locates the sibling files. `frames_dir` is resolved RELATIVE TO THE MANIFEST FILE'S OWN DIRECTORY (not cwd); every `frames[].file` must exist under that resolved directory, and every non-null `segments[].frame_index` must resolve. Missing = hard error at ingest.

- **`curation`** and **`alignment`** are informational for content-engine: they record how the engine selected and aligned frames. The lanes do not branch on them, but `01-ingest` may surface frame counts and the alignment mode at the checkpoint.

---

## Frame resolution rule (repeated because it is the #1 break)

`frames_dir` resolves relative to the manifest file's own directory:

```
os.path.join(os.path.dirname(manifest_path), frames_dir)
```

NOT the current working directory. Stage 01 copies frames into `output/ingest/frames/` so downstream stages and `render.py` use in-bundle absolute paths and never re-resolve this relative field.

---

## Version bump procedure

A new engine schema version is ADDED as another pinned copy, beside the frozen ones. That is how `1.1` arrived: `schema/manifest-1.1.schema.json` (the `1.0` schema minus `contactsheet_jpg`) sits next to the byte-frozen `manifest-1.0.schema.json`, and `01-ingest` validates each manifest against the copy its `schema_version` names. Freezing the old copy means existing samples never re-validate against changed rules. Nothing else restates field types, so nothing else drifts. A version that is not yet pinned still fails loud until its copy is added.
