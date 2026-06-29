# educational-guide: worked example (ANCHOR)

A worked example of ONE good guide module, the few-shot that stages 02 and 03 calibrate against. It shows the whole chain: raw talk -> typed items -> ordered module -> reader-facing prose -> the doc-model blocks. The numbers and content are illustrative (a generic "set up exports" walkthrough), not from any real recording.

## Step 1: what the raw transcript sounded like (segments)

> seg 40 (t=10:02): "...okay so before any of this you'll want a workspace already created, otherwise the export menu is empty."
> seg 41 (t=10:12): "An export is just a saved query you can re-run. Think of it as a recipe, not a one-time download."
> seg 42 (t=10:20): "Let me show you. You go to Settings, then Data, then click New export."
> seg 43 (t=10:34): "Name it something you'll recognize later. People skip this and end up with twelve 'export-final' files."
> seg 44 (t=10:47): "and uh, anyway, great weather today huh"

## Step 2: typed items (stage 02 output)

| Type | One-line statement | Source | Frame |
|---|---|---|---|
| Prerequisite (stated) | A workspace must exist before exports are available | seg 40 | -- |
| Concept | An export is a saved, re-runnable query (a recipe, not a one-time download) | seg 41 | -- |
| Procedure | Create an export: Settings -> Data -> New export | seg 42 | frame 7 |
| Pitfall | Name the export clearly, or you get many indistinguishable "final" files | seg 43 | -- |

seg 44 is chatter (weather) -> dropped by the significance filter.

## Step 3: ordering (stage 02)

The Concept ("what an export is") is a structural prerequisite of the Procedure ("how to make one"), so it sorts first even though both sit in the same module. The stated prerequisite (workspace exists) becomes a module-level prereq. One module results: **"Creating your first export."**

Provenance note: the concept-before-procedure ordering is `inferred:false` here (the speaker stated the concept first); had they demoed first and explained after, reordering to concept-first would be recorded `inferred:true` (an ordering decision, not a new claim).

## Step 4: the reader-facing module (stage 03 prose, in voice)

> ### Module 2: Creating your first export
> **In this module you'll learn to** create a reusable export and name it so you can find it later.
>
> **Before you start:** you need a workspace already created. If you do not have one, set that up first, the export menu is empty without it.
>
> An export is a saved query you can re-run whenever you need fresh data. Think of it as a recipe you keep, not a one-time download.
>
> **To create one:**
> 1. Open **Settings**, then **Data**.
> 2. Click **New export**.
>    [screenshot: the New export button, frame 7]
> 3. Give it a clear, recognizable name.
>
> **Watch out:** name it deliberately. Generic names like "export-final" pile up fast and become impossible to tell apart.
>
> *Recap: an export is a reusable saved query; create one under Settings -> Data and name it clearly.*

## Step 5: the doc-model blocks this becomes (stage 03 -> docmodel.json)

```json
{ "id": "module-2", "heading": "Creating your first export", "level": 1, "kind": "concept",
  "objective": "Create a reusable export and name it so you can find it later",
  "depends_on": ["module-1"],
  "blocks": [
    { "type": "callout", "variant": "prereq", "md": "You need a workspace already created. Without one, the export menu is empty." },
    { "type": "prose", "md": "An export is a saved query you can re-run whenever you need fresh data. Think of it as a recipe you keep, not a one-time download." },
    { "type": "list", "ordered": true, "items": ["Open **Settings**, then **Data**.", "Click **New export**.", "Give it a clear, recognizable name."] },
    { "type": "screenshot", "frame_index": 7, "caption": "The New export button under Settings -> Data.", "alt": "Settings Data panel with the New export button highlighted", "crop": null, "crop_reason": "full screen capture, no webcam tile to remove" },
    { "type": "callout", "variant": "warning", "md": "Name it deliberately. Generic names like \"export-final\" pile up fast and become impossible to tell apart." }
  ] }
```

## What makes this GOOD (the calibration takeaways)

- Every reader sentence traces to a real segment; the weather line was cut.
- The concept comes before the procedure (a learnable order), and that ordering is provenance-tracked.
- The screenshot sits at the exact step it illustrates, with a caption and alt text, crop decided by the shared rule.
- Zero timestamps, speaker names, or `frame NNNN` refs leak into the reader surface.
- An honest prereq callout instead of pretending setup was free.
