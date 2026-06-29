# Fidelity checklist (the 16-item Stage 05 audit)

The lane-local working copy of the canonical ship gate. The canonical bar is `../../../../_standards/qa-bar.md`; this file is the runnable line-by-line list Stage 05 walks. Run it AFTER render, against the rendered PDF/HTML + the provenance sidecar + the source. Every item must pass; a fail is fixed at the right upstream stage and the audit reruns.

**This 16-item audit plus the provenance sidecar is the DIFFERENTIATOR and is funded BEFORE any second render target and before brand polish.**

| # | Check | Pass |
|---|---|---|
| 1 | Every block grounded | every reader block has a provenance entry naming real segments |
| 2 | No uncited claims | no rendered sentence asserts a step/concept/owner/sequence/decision/fact/risk lacking a backing entry |
| 3 | Provenance points at real locations | each entry's segments exist in the manifest (or line ranges within transcript bounds) |
| 4 | Provenance says the thing | re-read the source at each span; it must actually state the claim. A paraphrase that adds an action/owner/sequence/tool/reason/branch the span lacks FAILS. (strongest anti-hallucination gate) |
| 5 | No invented content | gaps surfaced honestly ("not covered in the recording"), never silently filled |
| 6 | Inference flagged + bounded | every `inferred:true` is a reordering or objective phrasing, never a new factual claim |
| 7 | Reversals captured | the final version is the block; abandoned versions absent |
| 8 | Chatter excluded | no greeting/scheduling/banter/pure-agreement became a block |
| 9 | Objectives stated-only or flagged | every non-synthesized objective traces to a stated objective signal; synthesized ones are `inferred:true` |
| 10 | Sequence honest | the topo-sort has no back-edges; no module depends on a later one |
| 11 | Screenshots grounded | every screenshot has a `screenshots[]` entry; `frame_index` exists; sits in the right section; crop in range |
| 12 | Structure complete | every output-structure section present + in order; empty sections carry the stated-fallback line ("No prior setup needed." / "No external references mentioned.") |
| 13 | Exclusions respected | no excluded segment in any block/entry; `source.exclusions` records it |
| 14 | **Reader surface is clean** | rendered PDF/HTML has zero `[HH:MM:SS]`/timestamps/speaker tags/`frame NNNN`/provenance |
| 15 | **Sidecar not shipped** | the sidecar is in `output/` but NOT embedded in or attached to any deliverable |
| 16 | No em dashes / plain English | zero em dash characters; imperative low-technical prose throughout |

## The educational-lane lens on a few items

- **Item 6 (inference bounded):** in this lane `inferred:true` appears ONLY on structural prerequisites and synthesized objectives, both ordering/phrasing decisions. If any `inferred:true` entry carries a new factual claim (a number, an owner, a step the source lacked), that is a FAIL, fix it at stage 02.
- **Item 9 (objectives):** the educational reading. Every module objective is either a stated "by the end you'll be able to..." signal or a synthesized restatement flagged `inferred:true`.
- **Item 10 (sequence honest):** the educational reading is the topo-sort check, no module teaches something its prerequisite has not yet covered.
- **Items 14 + 15** are load-bearing: they keep the audience document clean and the grounding internal. **Item 4** is the strongest anti-hallucination gate. If the source genuinely lacks information, surface the gap (item 5) and pass honestly.
