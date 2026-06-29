# Scorecard rubric: reading the readiness check

The engine's `check-environment.py` prints a plain, line-by-line self-test. This page translates that raw output into one of three readiness tiers (GREEN / YELLOW / RED) plus a rough sense of how long a transcription will take. It is honest about CPU being correct but slow.

This rubric is authored against the engine's actual output format. content-engine does NOT run the check or duplicate its logic; it just tells you how to read the result the engine prints.

## What the raw output looks like

`check-environment.py` prints one line per check, each tagged with a status in square brackets, then a blank line, then a final verdict, then exits with code 0 (ready) or non-zero (not ready). The three line tags are:

- `[OK  ]` the check passed.
- `[WARN]` a non-critical issue. The engine still runs. This is what a missing GPU produces (CPU is valid, just slower).
- `[FAIL]` a critical dependency is missing. The engine will NOT run until you fix it.

A real run on a GPU machine looks like this (illustrative, your details vary):

```
[OK  ] Python 3.12 (>= 3.10) - 3.12.4
[OK  ] ffmpeg on PATH - C:\ffmpeg\bin\ffmpeg.exe
[OK  ] import torch
[OK  ] import whisperx
[OK  ] import faster_whisper
[OK  ] import yt_dlp
[OK  ] import imagehash
[OK  ] import PIL
[OK  ] import jsonschema
[OK  ] import numpy
[OK  ] import pandas
[OK  ] CUDA GPU: NVIDIA GeForce RTX 3090 - compute_type=float16, batch_size=16, 24 GB VRAM

READY
```

On a CPU-only machine the GPU line instead reads:

```
[WARN] CUDA GPU - none detected - will run on CPU (much slower)
```

and the final line is still `READY` (CPU is a valid answer). If a hard dependency is missing you get a `[FAIL]` line and a final `NOT READY - fix the FAIL items above`.

## How to read it: three tiers

Read the GPU line and scan for any `[FAIL]`. That is all you need.

| Tier | What the output shows | What it means | Rough time, 10-min video |
|---|---|---|---|
| GREEN-GPU | a `[OK  ] CUDA GPU: ...` line, no `[FAIL]` anywhere, final `READY` | You have a working NVIDIA GPU. Fast. | ~1-2 min (strong card) to ~4 min (smaller card) |
| YELLOW-CPU | a `[WARN] CUDA GPU - none detected ...` line, no `[FAIL]`, final `READY` | No NVIDIA GPU. The engine runs correctly on CPU, just slower. | ~5-10 min, longer on older CPUs |
| RED | any `[FAIL]` line, final `NOT READY` | A hard dependency is missing. Not ready yet. | n/a until fixed |

If you are RED, the `[FAIL]` lines name exactly what is missing (Python too old, ffmpeg not found, a module that will not import). Fix each one (`prerequisites.md` has the remediation per item), then run the check again.

## Finer GPU detail (optional)

The GPU line carries more than pass/fail: it prints the card name, the VRAM, and the `compute_type` and `batch_size` the engine auto-picks for that card. You do not have to act on any of it (the engine chooses for you), but if you want a sharper time estimate, read the VRAM number off that line:

| VRAM on the GPU line | Practical read | Rough time, 10-min video |
|---|---|---|
| >= 10 GB | strong, comfortable headroom | ~1-2 min |
| 6 to 10 GB | works well | ~2-4 min |
| < 6 GB | usable; the engine auto-shrinks the batch size. If you hit an out-of-memory error, add `--model medium` | ~3-6 min |

These VRAM rows are a refinement of the GREEN-GPU tier, not separate tiers. The engine reads VRAM itself and sets `batch_size` accordingly, so even a tight card just works; the table only helps you predict the wait.

If a future engine build does not print a parseable VRAM number on the GPU line, ignore this finer table and use the three coarse tiers above (GREEN-GPU / YELLOW-CPU / RED), which only need the WARN-vs-FAIL signal that is always present.

## The first-run note

Whatever your tier, the FIRST transcription downloads about 3 GB of model weights (once, then cached). That download is separate from the per-video time above. Budget a few extra minutes and a working internet connection for run one only.

## What to do next

- GREEN-GPU or YELLOW-CPU: you are ready. Go to `engine-location.md` and run `transcribe-video "<your-video>"`.
- RED: fix the `[FAIL]` items (`prerequisites.md`), re-run `check-environment.py`, then proceed.

See `output/readiness-scorecard.example.md` for a filled-in example of how a result reads end to end.
