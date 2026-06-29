# qa-bar: the Stage 05 ship gate

The fidelity + polish pass conditions for 05-qa. Run AFTER render, against the rendered deliverable (PDF + HTML) plus the provenance sidecar (`{slug}-provenance.json`) plus the source manifest/transcript. Every item must PASS. A fail is fixed at the right upstream stage and the audit reruns: 05-qa never patches a symptom in the rendered file.

This 16-item audit plus the provenance sidecar is the DIFFERENTIATOR. It is funded BEFORE any second render target and before brand polish. If a choice must be made between a stretch feature and a working fidelity audit on the sample, the audit wins.

House rule: zero em dash characters anywhere in the repo, deliverables included.

---

## The 16-item fidelity checklist

| # | Check | Pass condition |
|---|---|---|
| 1 | Every block grounded | every reader block has a provenance entry in `blocks[]` naming real segments |
| 2 | No uncited claims | no rendered sentence asserts a step, concept, owner, sequence, decision, fact, or risk that lacks a backing entry |
| 3 | Provenance points at real locations | each entry's `source_segments` exist in the manifest (or line ranges fall within transcript bounds) |
| 4 | Provenance says the thing | re-read the source at each span; it must actually state the claim. A paraphrase that adds an action, owner, sequence, tool, reason, or branch the span lacks FAILS. This is the strongest anti-hallucination gate. |
| 5 | No invented content | gaps are surfaced honestly (educational: "not covered in the recording"; sop: an Open Questions entry), never silently filled |
| 6 | Inference flagged + bounded | every `inferred:true` entry is a reordering or an objective phrasing, never a new factual claim; the SOP lane has zero |
| 7 | Reversals captured | when the speaker changed their mind, the final version is the block; abandoned versions are absent from the reader doc |
| 8 | Chatter excluded | no greeting, scheduling, banter, or pure agreement became a block |
| 9 | Owners / objectives stated-only | (sop) every owner is named or "unassigned (clarify)"; (educational) non-synthesized objectives trace to a stated signal |
| 10 | Sequence honest | (sop) unstated-order steps are flagged; (educational) the topo-sort has no back-edges |
| 11 | Screenshots grounded | every screenshot has a `screenshots[]` entry; its `frame_index` exists in the manifest; it sits in the correct section |
| 12 | Structure complete | every output-structure section is present and in order; an empty section carries its stated-fallback line |
| 13 | Exclusions respected | no excluded segment appears in any block or entry; `source.exclusions` records what was excluded |
| 14 | Reader surface is clean | the rendered PDF and HTML contain ZERO `[HH:MM:SS]` / timestamps / speaker tags / `frame NNNN` / `[ref]` / provenance of any kind |
| 15 | Sidecar not shipped | the sidecar lives in `output/` and is NOT embedded in or attached to any deliverable |
| 16 | No em dashes / plain English | zero em dash characters; imperative, low-technical prose at the configured reading level throughout |

Items 14 and 15 are the load-bearing checks that keep the audience document clean and the grounding internal. Item 4 is the strongest anti-hallucination gate. If the source genuinely lacks information, surface the gap (item 5) and pass honestly rather than inventing.

---

## Polish + render-fidelity conditions (folded in from the 04-render audit)

These are confirmed at 05 alongside the fidelity items above:

- **Targets produced.** Every enabled target exists (PDF + HTML for this submission) and opens cleanly.
- **Brand applied.** Letterhead, logo, and the static disclaimer footer on the PDF; design-system colors and fonts on both PDF and HTML.
- **Images embedded.** No broken image links; every screenshot renders.
- **One source, two targets.** PDF and HTML both derive from the SAME doc-model: content parity, no divergence.
- **Crop did not clip context (D6).** Where a `crop` was applied, it improved focus and clipped NO needed on-screen content; no webcam or participant tile remains in a frame where it was cleanly removable; a frame whose webcam tile could not be removed without cutting content was correctly left full (`crop: null`).
- **Navigation works.** The HTML sticky nav TOC links resolve to in-page anchors; collapsible sections are present and printable (`<details open>`); PDF page breaks fall sensibly (title page breaks after the cover).

---

## How a fail is handled

1. Identify the WRONG stage (a clipped crop is a 03 decision or a 04 application bug; an uncited claim is a 02 extraction or a 03 prose bug; a leaked timestamp is a 03 prose or a 04 split bug).
2. Fix it THERE, not in the rendered file.
3. Re-render and re-run this checklist.
4. Only when all 16 items plus the polish conditions pass: collect the passing files into `output/final/`, write `output/qa-report.md` and `output/delivery-note.md`, and present for approval.
