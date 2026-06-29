# Install steps: run the wizard, then the self-test

The transcription engine ships a guided setup command, `/transcribe-setup`, that walks the install in order and stops on the first failure. This page wraps it and tells you what each step does, so you can follow along or do it by hand if you prefer. None of it needs a HuggingFace token.

If you have not installed the four prerequisites yet, do `prerequisites.md` first. This page assumes Python and a shell are working.

## The fast path: the wizard

Inside a Claude Code session with the transcription engine available, run:

```
/transcribe-setup
```

It runs six steps in order and reports the result of each, halting if one fails so you can fix it before moving on:

1. Python: confirms 3.10+ (`python --version`).
2. ffmpeg: confirms `ffmpeg -version` works. On Windows, if missing, it installs `Gyan.FFmpeg` via winget and reminds you to restart the shell.
3. PyTorch: installs the CUDA build if you have an NVIDIA GPU, the CPU build otherwise (this is the wheel choice from `prerequisites.md` step 3).
4. Dependencies: `pip install -r requirements.txt`.
5. Verify: runs `check-environment.py`, which must print `READY`.
6. Optional: adds the engine's `bin/` to PATH so you can run `transcribe` / `transcribe-video` from any terminal.

When step 5 prints `READY`, you are done. Read your result against `scorecard-rubric.md`.

## The manual path: the same steps by hand

If you are not in a Claude Code session, or you just want to do it yourself, the wizard is only these commands. Substitute the real engine path (see `engine-location.md`) for `<ENGINE>`.

### 1. Confirm Python

```
python --version
```

Need 3.10+. If not, fix per `prerequisites.md` step 1.

### 2. Confirm ffmpeg

```
ffmpeg -version
```

If "not found", install per `prerequisites.md` step 2, then RESTART your shell.

### 3. PyTorch, the right wheel

The single most common failure. Pick the line that matches your hardware:

- NVIDIA GPU:
  ```
  python -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126
  ```
- No NVIDIA GPU (CPU):
  ```
  python -m pip install torch torchaudio
  ```

### 4. The rest of the dependencies

```
python -m pip install -r "<ENGINE>/requirements.txt"
```

### 5. The readiness self-test (the gate)

```
python "<ENGINE>/scripts/check-environment.py"
```

This is the engine's own self-test. It prints one line per check, each tagged `[OK]`, `[WARN]`, or `[FAIL]`, then a final `READY` or `NOT READY` line, and exits 0 (ready) or non-zero (not ready). It treats a missing GPU as a WARN, not a FAIL, because CPU is a valid (slower) way to run.

What it checks: Python version, ffmpeg on PATH, every required Python module imports, and the GPU (name, VRAM, the compute type and batch size it will auto-pick). Read the output against `scorecard-rubric.md`.

If it says `NOT READY`, fix the `[FAIL]` lines (they each name the missing piece) and run it again. `[WARN]` lines are fine to leave: they note things like "no GPU, will run on CPU (slower)".

### 6. Optional: terminal commands from anywhere

To run the engine from any terminal (not just inside Claude Code), add `<ENGINE>/bin` to your PATH. Otherwise just use the engine inside a Claude Code session, where it auto-triggers on video paths and URLs.

## First real run

The very first transcription downloads about 3 GB of model weights (once, then cached). Do not be alarmed by the pause on run one. After that, runs are as fast as your hardware allows.

## Next

- `scorecard-rubric.md`: what your check-environment output means (tier + rough times).
- `engine-location.md`: the exact run command and where the engine lives.
