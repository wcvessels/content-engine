# Prerequisites: the four things the engine needs

The transcription engine is plain Python that runs locally. It needs four things on your machine before it can turn a video into a manifest. Get these in order. The third one (the PyTorch wheel) is where almost everyone trips, so read it carefully even if you know Python.

None of this needs a HuggingFace account or any API token. The engine is token-free: model weights download themselves on first run, sha256-verified, and cache after that.

## At a glance

| # | Prerequisite | Hard or soft | Why |
|---|---|---|---|
| 1 | Python 3.10+ (3.12 recommended) | Hard | the engine is Python |
| 2 | ffmpeg on PATH | Hard | pulls audio + frames out of the video |
| 3 | PyTorch (CUDA build if you have an NVIDIA GPU, else CPU build) | Hard (CPU is a valid, slower answer) | the transcription model runs on it |
| 4 | The Python dependencies | Hard | whisperx, yt-dlp, imagehash, Pillow, etc. |
| - | An NVIDIA GPU + CUDA | Soft | speed only; CPU works, just slower |
| - | ~3 GB free disk for model weights | Soft-ish | downloaded once on first run, then cached |

"Hard" means the engine will not run without it. "Soft" means it affects speed or convenience, not whether it works at all.

## 1. Python 3.10 or newer

Check what you have:

```
python --version
```

If it prints 3.10, 3.11, or 3.12 you are set. If it is older, or the command is not found:

- Windows: `winget install Python.Python.3.12`, or download from python.org. Tick "Add Python to PATH" in the installer.
- macOS: `brew install python@3.12` (Homebrew), or download from python.org.
- Linux: use your distro package (`sudo apt install python3.12 python3.12-venv` on Debian/Ubuntu, `sudo dnf install python3.12` on Fedora), or download from python.org.

A virtual environment is good hygiene but not required. If you use one, create and activate it before steps 3 and 4 so the packages land in it.

## 2. ffmpeg on PATH

ffmpeg is the tool that extracts the audio track and samples frames from your video. Check it:

```
ffmpeg -version
```

If that prints version info, you are done. If it says "not found":

- Windows: `winget install Gyan.FFmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg` (Debian/Ubuntu), `sudo dnf install ffmpeg` (Fedora), or your distro's package.

IMPORTANT, all platforms: after installing ffmpeg you must RESTART your shell (close and reopen the terminal). A new program on PATH does not show up in a terminal that was already open. This is the single most common "I installed it but it still says not found" cause.

## 3. PyTorch: the right wheel (the #1 failure)

PyTorch is the math engine the transcription model runs on. There are two builds, and installing the wrong one is the most common failure for this whole pipeline:

- If you have an NVIDIA GPU, you want the CUDA build. It uses the GPU and is roughly 5-10x faster.
- If you do not have an NVIDIA GPU (Mac, or a PC with only integrated/AMD graphics), you want the default CPU build. It is correct, just slower.

Do you have an NVIDIA GPU? On Windows/Linux, run `nvidia-smi`. If it prints a table, yes. If the command is not found, treat yourself as CPU-only. Macs are always CPU-only for this engine (Apple Silicon GPU acceleration is not wired in here).

Install the matching wheel:

- NVIDIA GPU (CUDA 12.6 build):
  ```
  python -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126
  ```
  The `--index-url` is the whole point: it pulls the GPU build instead of the plain CPU one from PyPI. Leave it off and you silently get the CPU build, then wonder why your GPU sits idle.

- No NVIDIA GPU (CPU build):
  ```
  python -m pip install torch torchaudio
  ```

CPU is a legitimate answer, not a failure. A 10-minute video still transcribes correctly on CPU, it just takes longer (see `scorecard-rubric.md` for rough times). Start with a short clip to get a feel for the speed.

## 4. The remaining Python dependencies

Everything else (whisperx, faster-whisper, yt-dlp, imagehash, Pillow, jsonschema, numpy, pandas) installs from the engine's requirements file:

```
python -m pip install -r requirements.txt
```

The exact path to `requirements.txt` is in `engine-location.md` (it lives with the engine). The install wizard in `install-steps.md` runs this for you.

## yt-dlp (already covered)

yt-dlp downloads videos from URLs (YouTube, Vimeo, etc.). It is included in step 4's dependencies, so there is nothing extra to do. You only strictly need it if you plan to feed the engine a URL rather than a local file.

## Disk and the first-run model download

The first time you transcribe anything, the engine downloads about 3 GB of WhisperX model weights plus a small (~32 MB) diarization model. This happens automatically, is verified by checksum, needs no token, and is cached, so it only happens once. Make sure you have a few GB free and a working internet connection for that first run.

## Next

Once these four are in place, go to `install-steps.md` to run the wizard and the readiness self-test.
