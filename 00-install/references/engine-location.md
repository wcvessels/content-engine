# Engine location: where it lives and how to run it (canonical)

This is the ONE place that says where the transcription engine is and how to run it. Every lane that needs a fresh transcription points here. If the engine moves or publishes, this file is the single edit.

## What the engine is

A separate, free, local tool called `transcribe-video` (part of the transcription-plugin). It is plain Python, not part of content-engine. content-engine points at it and does not bundle it, because the engine has its own home, pulls ~3 GB of model weights content-engine should not inherit, and may ship in more than one form (a GPU local build and a CPU-only web build). content-engine only cares that the engine produces a manifest whose `schema_version` is in its pinned set ({`"1.0"`, `"1.1"`} today).

## Engine: published

The transcription engine ships as a public, MIT-licensed Claude Code plugin: https://github.com/wcvessels/transcription-pipeline-plugin

Install it once from its marketplace, then it pulls its own ~3 GB of model weights on first run:

```
/plugin marketplace add https://github.com/wcvessels/transcription-pipeline-plugin
/plugin install transcription-pipeline
```

This gives you the `transcribe-video` skill, the `/transcribe-setup` wizard (Python + ffmpeg check, dependency install, self-test), and the `bin/` wrappers. content-engine never imports the engine; it only consumes the manifest the engine writes.

## How to run it

Once you are READY (see `scorecard-rubric.md`), point the engine at a video. It takes either a local file or a public URL.

```
transcribe-video "C:/path/to/your-video.mp4"
transcribe-video "https://youtube.com/watch?v=..."
```

If `transcribe-video` is not on your PATH, add the plugin's `bin/` directory to it. Or skip PATH entirely: inside a Claude Code session with the plugin installed, hand it a video path or URL and the `transcribe-video` skill auto-triggers.

## What you get back (the 4-artifact set)

The engine writes these next to your video (or in `--output-dir`). The one that matters to content-engine is the manifest:

| Artifact | What it is |
|---|---|
| `{name}_manifest.json` | the structured manifest, validates against the pinned schema (1.0 or 1.1). THIS is what a lane reads. |
| `{name}_frames/` | the curated screenshots, named `frame_NNNN_HHMMSS.jpg` (one per distinct on-screen scene) |
| `{name}_transcript.txt` | the verbatim transcript (speaker-grouped on the whisperx path) |
| `{name}_frames.md` | a flat index of the kept frames |

## Useful flags

The engine has sensible defaults; you rarely need flags. The few worth knowing:

| Flag | Use it when |
|---|---|
| `--output-dir DIR` | you want the artifacts somewhere other than next to the video |
| `--max-frames N` | a long session is producing too many screenshots; cap them |
| `--dedup-threshold N` | you want MORE screenshots (lower N, e.g. `2`) or fewer (higher N) |
| `--model medium` | a small-VRAM GPU hits out-of-memory on the default `large-v3` |
| `--diarize {auto,on,off}` | control speaker labelling (default `auto`) |

## Handing the result to a lane

Once the manifest exists, open the lane you want (`../../lanes/educational-guide/`) and start at its `stages/01-ingest/`. Give it the path to `{name}_manifest.json`. Stage 01 validates it against the pinned schema, copies the frames into a self-contained bundle, and the lane takes it from there.

## Performance reminder

- 10-min video to the curated set: ~1-2 min on GPU, ~5-10 min on CPU.
- First run downloads ~3 GB of models (once, cached after). Token-free, no account needed.
