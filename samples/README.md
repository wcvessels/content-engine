# samples: the shipped worked examples

This folder ships complete worked examples so anyone (a judge, a new user) can see content-engine's output and re-render with ZERO install and zero GPU. You do not need the transcription engine to inspect what is here; open the rendered guide, or point a lane at the committed manifest and render.

Five samples ship here. Four are educational guides rendered from PUBLIC Jake Van Clief YouTube videos (from his Clief Notes set), attributed to Jake Van Clief. The fifth is a Standard Operating Procedure from the second lane (`../lanes/sop/`), rendered from a PUBLIC Ramp training video, attributed to Ramp. We deliberately ship nothing derived from PRIVATE recordings: a rendered SOP built from an internal clip stays on the tester's machine and is never committed here.

## The featured sample: Getting Started with Claude Code

An educational guide rendered from **"Stop Copy-Pasting Into Claude. Install Claude Code and Actually Use It."** (about 24 minutes). It walks a newcomer through the three ways to use Claude (Desktop, the VS Code extension, the terminal) and the full install and first-use path. Open it first:

- `rendered/getting-started-claude-code.html` (interactive HTML: sticky table of contents, collapsible sections)
- `rendered/getting-started-claude-code.pdf` (polished PDF on letterhead)

It is a step-heavy tutorial, so it shows off the educational lane's strength: six screenshots placed next to the exact step they illustrate, each cropped to drop the presenter webcam and the burned-in caption strip (the D6 crop rule, applied deterministically at render).

## Three more samples

The same lane, run on three more public videos of different shapes, to show it generalizes rather than being tuned for one clip:

- **The Ladder of Abstraction** (`rendered/ladder-of-abstraction.*`), from "The Ladder That Explains Every AI Failure" (about 14 minutes). A concept explainer: concepts and a worked example instead of install steps.
- **From Illustrator to Web Animations** (`rendered/illustrator-to-web-animations.*`), from "SVG to React: Turning Illustrator Designs into Web Animations with Claude Code" (about 12 minutes). A design-to-code tutorial.
- **The Folder System for AI** (`rendered/folder-architecture-walkthrough.*`), from "Stop Building AI Agents. Use This Folder System Instead." (about 23 minutes). A longer, twelve-section method walkthrough.

Four source shapes (a hands-on tutorial, a concept talk, a design-to-code build, and a method walkthrough) demonstrate the lane generalizes.

## The SOP sample: Ramp manager onboarding (a second lane)

The fifth sample is NOT an educational guide. It is a Standard Operating Procedure produced by the **sop lane** (`../lanes/sop/`), to show the factory runs a second document type, not just a second guide.

- `rendered/ramp-manager-onboarding.html` and `.pdf`, from **"Ramp manager training"** (about 6 minutes, public, by Ramp).
- It is structured as an SOP: Purpose, Scope, Roles, Before you start, a numbered Procedure grouped into tasks (accept invite, home task list, cards, receipts and codes, team invites, card requests, bank account, out-of-pocket and mileage reimbursements), Decision points, Risks, References, and Open questions.
- It shows the sop lane's defining rule, ZERO content inference: owners appear only where named, decision points list only the sides the recording stated, and the two genuinely company-dependent gaps (which fields are required, whether reimbursements are enabled) are surfaced as Open questions rather than guessed. The on-screen demo shows a specific "$75" receipt threshold, but because the narration says required fields "depend on how your company sets up their policies," the SOP does not assert $75 as a rule. That restraint is the lane.

The same shared shelf produced it: stages 01/04/05, the renderer, brand, voice, design system, the doc-model schema, and the 16-item fidelity bar are identical to the educational lane. Only stages 02 (taxonomy) and 03 (document shape) differ.

## View the rendered guides in your browser (no clone)

GitHub shows `.html` as source, so the interactive guides and the SOP are served via GitHub Pages:

- [Getting Started with Claude Code](https://wcvessels.github.io/content-engine/samples/rendered/getting-started-claude-code.html) (featured)
- [The Ladder of Abstraction](https://wcvessels.github.io/content-engine/samples/rendered/ladder-of-abstraction.html)
- [From Illustrator to Web Animations](https://wcvessels.github.io/content-engine/samples/rendered/illustrator-to-web-animations.html)
- [The Folder System for AI](https://wcvessels.github.io/content-engine/samples/rendered/folder-architecture-walkthrough.html)
- [Ramp Manager Onboarding (SOP)](https://wcvessels.github.io/content-engine/samples/rendered/ramp-manager-onboarding.html) (the sop lane, a second document type)

The PDFs render inline on GitHub: just click any `rendered/*.pdf`.

## What is here

Each sample is one slug. Per slug you get the same set (shown here for the featured slug; the other three follow the identical pattern):

```
samples/
├── <slug>_manifest.json    # the raw transcribe-video output (the lane's input), schema-valid against the pinned manifest schema (1.0 or 1.1)
├── <slug>_frames/          # the frames the guide embeds (named frame_NNNN_HHMMSS.jpg)
├── <slug>_transcript.txt   # the verbatim transcript (convenience)
└── rendered/
    ├── <slug>.html             # the shipped polished guide (interactive HTML)
    ├── <slug>.pdf              # the shipped polished guide (PDF)
    ├── <slug>-docmodel.json    # the docmodel-1.0 the renderer consumed (stage 03 output)
    └── <slug>-provenance.json  # the internal grounding sidecar: every block traces to real transcript segments

slugs: getting-started-claude-code (featured), ladder-of-abstraction,
       illustrator-to-web-animations, folder-architecture-walkthrough  (educational-guide lane)
       ramp-manager-onboarding  (sop lane)
```

**On the frames:** each manifest records the full dense curation the engine produced (982, 578, 480, and 933 frames for the four guides; 40 for the Ramp SOP). The committed `_frames/` folders hold only the frames each deliverable actually embeds (6, 4, 6, 6 for the guides; 8 for the SOP), which is what the blueprint's samples spec calls for. This keeps the repo light and, just as important, avoids republishing a raw screen-recording frame dump that can incidentally capture on-screen email addresses, keys, or file paths. The reader-facing HTML and PDF are self-contained (screenshots are base64-embedded) and carry ZERO timestamps, citations, or frame references; all grounding lives in the `-provenance.json` sidecars.

## How a sample was produced

1. `transcribe-video <public YouTube URL>` produced the manifest, frames, and transcript.
2. The educational-guide lane extracted typed items, ordered them into modules, placed and cropped screenshots, and emitted the docmodel + the provenance sidecar.
3. `_skills/render-doc/render.py` rendered the docmodel to HTML + PDF.

To re-render the featured guide from its committed manifest (no engine, no GPU):

```
python ../_skills/render-doc/render.py \
  rendered/getting-started-claude-code-docmodel.json rendered \
  --manifest getting-started-claude-code_manifest.json \
  --slug getting-started-claude-code --targets html,pdf
```

## Running a lane against a sample

Open `../lanes/educational-guide/stages/01-ingest/`, give it the path to a `*_manifest.json` here, and run the lane. Stage 01 validates the manifest against the pinned schema, copies the embedded frames into a self-contained bundle, and the lane produces a guide. No engine install, no GPU: the manifest is the heavy lifting already done.

House rule: zero em dash characters.
