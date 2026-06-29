# Voice

How every deliverable reads. Loaded at **03-layout** (where reader-facing prose is written), dropped at 04-render. The goal: a teammate with no background can follow the document on the first read and trust every line.

Shipped PRE-FILLED. `/setup` rewrites `{{READING_LEVEL}}` and `{{TONE_WORDS}}`. The jargon ban and the no-em-dash rule are FIXED and not setup-configurable.

## Settings

- **Reading level** ({{READING_LEVEL}}): around 8th grade. Short sentences. One idea per sentence.
- **Tone** ({{TONE_WORDS}}): clear, calm, helpful, direct. A knowledgeable colleague walking you through it, not a manual and not a hype reel.

## Fixed rules (never change per install)

1. **No em dash characters anywhere.** Use a comma, a colon, or parentheses. `->` is fine in a step. This is a hard repo rule and a QA gate (`_standards/qa-bar.md` item 16).
2. **No jargon, or define it on first use.** If a normal teammate would not know the word, replace it or explain it in plain words once.
3. **No timestamps, citations, speaker tags, or `frame NNNN` in reader text.** Grounding is internal only (the provenance sidecar). The reader surface stays clean.
4. **Plain English, active voice, imperative for steps.** "Click Save." not "The Save button should then be clicked by the user."

## Examples over descriptions

The rules are easier to follow as before/after pairs. Match the AFTER column.

| Avoid | Use |
|---|---|
| The user should navigate to the configuration pane and initialize the export workflow. | Open Settings, then click Export. |
| Leveraging this functionality enables you to operationalize the data. | This lets you send the data out as a file. |
| As demonstrated at the 4 minute mark, the speaker configures the threshold. | Set the threshold to 3. |
| It is important to note that one should be cognizant of the fact that... | Watch out: ... |
| Utilize the aforementioned methodology in order to facilitate the process. | Do it this way to save time. |
| The synchronization process is initiated automatically upon completion. | It syncs on its own when you finish. |

## Em-dash replacement (the one rule people forget)

| Avoid (em dash) | Use |
|---|---|
| Open Settings, the gear icon, and click Export. | Open Settings (the gear icon), then click Export. |
| There is one catch, the file must be under 10 MB. | There is one catch: the file must be under 10 MB. |
| Save first, then everything else follows. | Save first. Then everything else follows. |

## Callout phrasing

- `tip`: "Tip: ..." (a shortcut or a better way)
- `warning`: "Watch out: ..." (something that bites if ignored)
- `note`: "Note: ..." (useful context)
- `prereq`: "Before you start: ..." (something needed first)

## Honesty rule (ties to fidelity)

If the recording did not cover something, say so plainly: "This was not covered in the recording." Never invent a step, a number, or a reason to fill a gap. An honest gap is information the reader needs.
