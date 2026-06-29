# Readiness scorecard (EXAMPLE, not a live run)

ILLUSTRATIVE ONLY. This is a hand-written example of how a readiness result reads, so you know what to expect before you run anything. It was NOT produced by running `check-environment.py` on this machine. To get your real result, follow `references/install-steps.md` and run the self-test yourself.

Two examples below: a GPU machine (GREEN) and a CPU-only machine (YELLOW). A RED example is at the end.

---

## Example A: GPU machine (GREEN-GPU)

Raw `check-environment.py` output:

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

Read against the rubric:

| | |
|---|---|
| Tier | GREEN-GPU |
| Why | a working CUDA GPU, no `[FAIL]` lines, final `READY` |
| VRAM detail | 24 GB (>= 10 GB row): strong, comfortable headroom |
| Rough time, 10-min video | ~1-2 min |
| Verdict | Ready. Run `transcribe-video "<your-video>"`. |

Note: the first transcription downloads ~3 GB of models once, then caches. That is separate from the ~1-2 min above.

---

## Example B: CPU-only machine (YELLOW-CPU)

Raw `check-environment.py` output:

```
[OK  ] Python 3.11 (>= 3.10) - 3.11.9
[OK  ] ffmpeg on PATH - /usr/bin/ffmpeg
[OK  ] import torch
[OK  ] import whisperx
[OK  ] import faster_whisper
[OK  ] import yt_dlp
[OK  ] import imagehash
[OK  ] import PIL
[OK  ] import jsonschema
[OK  ] import numpy
[OK  ] import pandas
[WARN] CUDA GPU - none detected - will run on CPU (much slower)

READY
```

Read against the rubric:

| | |
|---|---|
| Tier | YELLOW-CPU |
| Why | no NVIDIA GPU (a `[WARN]`, not a `[FAIL]`), everything else OK, final `READY` |
| Rough time, 10-min video | ~5-10 min, longer on older CPUs |
| Verdict | Ready, just slower. Start with a short clip to gauge the speed, then scale up. |

CPU is correct, not broken. The transcript and screenshots come out the same; the wait is longer.

---

## Example C: not ready yet (RED)

Raw `check-environment.py` output (ffmpeg missing):

```
[OK  ] Python 3.12 (>= 3.10) - 3.12.4
[FAIL] ffmpeg on PATH - not found - install ffmpeg, then restart the shell
[OK  ] import torch
[FAIL] import whisperx - No module named 'whisperx'
...
[WARN] CUDA GPU - none detected - will run on CPU (much slower)

NOT READY - fix the FAIL items above
```

Read against the rubric:

| | |
|---|---|
| Tier | RED |
| Why | two `[FAIL]` lines, final `NOT READY` |
| Fix | install ffmpeg and RESTART the shell (`prerequisites.md` step 2); install the dependencies (`prerequisites.md` step 4) |
| Then | run `check-environment.py` again; you want a final `READY` |

The GPU `[WARN]` here is NOT the problem; the two `[FAIL]` lines are. A RED result always names exactly what to fix.
