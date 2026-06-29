---
name: docx
description: DOCX is a DOCUMENTED path for content-engine, NOT built for this submission (decision D3). This file records the pandoc + reference-doc recipe so DOCX can be promoted later. Do not author reference.docx. PDF + HTML are the shipped targets.
---

# docx (pointer, DOCUMENTED ONLY, NOT BUILT)

DOCX is parked (decision D3). PDF + interactive HTML are the shipped targets.
This file documents the real path so DOCX is a known, promotable follow-up, not
a mystery. `render.py`'s `build_docx` is a stub that raises
`NotImplementedError` pointing here.

House rule: zero em dash characters.

## The intended path (pandoc + reference-doc)

```
docmodel.json
  -> build_html(docmodel, manifest_path)   # docx-flavored HTML fragment,
                                            # base64 data-URI images inline
  -> pandoc fragment.html -o out.docx --reference-doc=brand/reference.docx
```

- pandoc 3.x embeds the data-URI images as `word/media/*.png`.
- `--reference-doc` carries STYLES only: heading styles, body, header/footer.
  pandoc maps the doc-model heading hierarchy (`level` 1/2) to Word heading
  styles.

## Why it is NOT built for this submission

1. Authoring a good `reference.docx` (heading styles + header/footer +
   page-number field) is its own mini-project.
2. `--reference-doc` carries styles only and CANNOT inject a letterhead COVER
   PAGE (pandoc has no cover concept). DOCX would ship without the cover-page
   promise the PDF keeps.
3. It triples the content-parity QA surface (a third target to keep in sync
   with the doc-model on a one-day clock).

PDF + HTML satisfy decision 3's spirit (one polished print target + one
interactive target, both from the same doc-model).

## If promoted later (stretch)

Ship styled-headings + embedded-images + a header/footer `reference.docx`,
WITHOUT a DOCX cover-page promise. Update this file from documented to built and
implement `render.py` `build_docx` against the path above. Do NOT attempt a
DOCX cover page.
