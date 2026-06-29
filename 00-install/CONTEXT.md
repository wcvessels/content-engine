# 00-install (routing): are you ready to make a transcript?

content-engine turns a video into polished docs. It does NOT transcribe the video itself: a separate, free tool (the transcription engine, `transcribe-video`) does that and writes the `{name}_manifest.json` + frames that a lane reads. This folder is the self-serve onboarding for that engine. It is DOCUMENTATION ONLY: it tells you what to install and how to check you are ready. It does not run anything for you.

## You may not need this at all

If you only want to see content-engine work, use the committed samples in `../samples/`. A lane runs against them with ZERO install and zero GPU. Come here only when you want to feed your OWN video in.

## Pick your path

| Your situation | Go to |
|---|---|
| "What do I need on my machine first?" | `references/prerequisites.md` (per-OS; the PyTorch wheel is the #1 trip-up) |
| "How do I actually install it?" | `references/install-steps.md` (wraps the engine's `/transcribe-setup` wizard) |
| "I ran the check, what does the output mean?" | `references/scorecard-rubric.md` (translates `[OK]/[WARN]/[FAIL]` into GREEN / YELLOW / RED + rough times) |
| "Where does the engine live and how do I run it?" | `references/engine-location.md` (CANONICAL run command + the marketplace install) |
| "Show me what a finished readiness check looks like" | `output/readiness-scorecard.example.md` (illustrative, not a live run) |

## The shape of it

1. Install the four prerequisites (`prerequisites.md`).
2. Run the wizard + self-test (`install-steps.md`).
3. Read your result against the rubric (`scorecard-rubric.md`): GREEN-GPU is fast, YELLOW-CPU is correct but slow, RED means fix the listed items first.
4. Run the engine on your video (`engine-location.md`): `transcribe-video "<your-video>"`.
5. Point a lane's `stages/01-ingest/` at the `{name}_manifest.json` it produced.

## Note: the engine is a published plugin

The transcription engine is a separate, published Claude Code plugin (`engine-location.md` has the one-line marketplace install). content-engine consumes the manifest it writes and is fully usable right now via the committed samples, with zero install.
